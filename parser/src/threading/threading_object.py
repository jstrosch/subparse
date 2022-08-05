from queue import Queue, Empty
from threading import Thread, Lock, Event
from src.database.base.client import Client
from src.helpers.logging import SubParserLogger
import traceback

class ThreadingObject(Thread):
    def __init__(self, queue: Queue, logger: SubParserLogger, lock: Lock, client: Client, total_sample_count: int = None, isService: bool = False):
        Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.lock = lock
        self.client = client
        self.total_count = total_sample_count
        self.isService = isService
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        while True:
            try:
                _exec = self.queue.get() # ThreadInvoker = _exec
                _data = _exec.execute()
                if self.lock.acquire():
                    if self.total_count != None or self.isService:
                        self.client.threading_callback(_data, self.total_count, self.isService)
                self.lock.release()
                
            except Empty:
                break
            except KeyError as ke:
                print(traceback.print_exc())
                self.logger.error("[THREADING-OBJECT] KEY ERROR :: " + str(type(ke)) + " :: " + str(ke))
            except Exception as e:
                self.logger.error("[THREADING-OBJECT] ERROR :: " + str(type(e)) + " :: " + str(e))
            finally:
                self.queue.task_done()