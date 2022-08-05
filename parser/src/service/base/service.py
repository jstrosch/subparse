from src.helpers.logging import SubParserSingletonLogger
from service import Service
from daemon import DaemonContext
import setproctitle
import os
import signal
import threading
import time

class BaseService(Service):
    """
    Base Service - this is the parent class for setting up the system deamons for the 
        consumer/producer background services

    Methods
    -------
        - kill(self, block=False):
            kills the associated service
        
        - start(self, block=False):
            start an instance of the service
    """
    def __init__(self, name, pid_dir='/tmp/baseservice', signals=None, subparselogname: str = ""):
        super(BaseService, self).__init__(name, pid_dir, signals)
        self.splogname = subparselogname
        # This overrides the logger that the Service Pacakge wants implemented
        #   since our logger is also build off of the logging package like 
        #   they require it is an easy exchange
        self.logger = SubParserSingletonLogger()

    def kill(self, block=False):
        return super().kill(block)

    def start(self, block=False):
        return super().start(block)

    def runner(self):
        try:
            # We acquire the PID as late as possible, since its
            # existence is used to verify whether the service
            # is running.
            self.pid_file.acquire()
            self._debug('PID file has been acquired')
            self._debug('Calling `run`')
            self.run()
            self._debug('`run` returned without exception')
        except Exception as e:
            self.logger.exception(e)
        except SystemExit:
            self._debug('`run` called `sys.exit`')
        try:
            self.pid_file.release()
            self._debug('PID file has been released')
        except Exception as e:
            self.logger.exception(e)
            os._exit(os.EX_OK)  # FIXME: This seems redundant

        try:
            setproctitle.setproctitle(self.name)
            self._debug('Process title has been set')
            files_preserve = (self.files_preserve +
                              self._get_logger_file_handles())
            signal_map = {s: self.on_signal for s in self._signal_events}
            signal_map.update({
                    signal.SIGTTIN: None,
                    signal.SIGTTOU: None,
                    signal.SIGTSTP: None,
            })
            with DaemonContext(
                    detach_process=False,
                    signal_map=signal_map,
                    files_preserve=files_preserve):
                self._debug('Daemon context has been established')

                # Python's signal handling mechanism only forwards signals to
                # the main thread and only when that thread is doing something
                # (e.g. not when it's waiting for a lock, etc.). If we use the
                # main thread for the ``run`` method this means that we cannot
                # use the synchronization devices from ``threading`` for
                # communicating the reception of SIGTERM to ``run``. Hence we
                # use  a separate thread for ``run`` and make sure that the
                # main loop receives signals. See
                # https://bugs.python.org/issue1167930
                thread = threading.Thread(target=self.runner)
                thread.start()
                while thread.is_alive():
                    time.sleep(1)
        except Exception as e:
            self.logger.exception(Exception("Issue with daemon creation"))
            self.logger.exception(e)