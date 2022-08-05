#!/usr/bin/env python
from src.helpers.logging import SubCrawlLoggerLevels, SubParserSingletonLogger
from src.config.configuration import Configuration
from src.helpers.logging.logger import SubParserLogger
from src.service.manager_consumer_service import ConsumerProcessorService
from time import sleep
import sys

if __name__ == '__main__':
    _config = Configuration()
    SubParserSingletonLogger(
        _config.log_file,
        _config.logger_name,
        SubCrawlLoggerLevels[_config.log_level],
    )
    SubParserSingletonLogger().init()
    service = ConsumerProcessorService()
    mlogger = SubParserLogger("CONSUMER-PROCESS", "Controller")

    try:
        if len(sys.argv) == 2:
            cmd = sys.argv[1].lower()
            if cmd not in ['start', 'stop', 'status']:
                raise Exception("UNKNOWN COMMAND")
            else:
                if cmd == 'start':
                    mlogger.info("Starting Daemon")
                    service.start()
                    while service.is_running() == False:
                        mlogger.info("Waiting for service to start...")
                        sleep(1)
                    mlogger.info("Daemon Started : PID :: " + str(service.get_pid()))
                elif cmd == 'stop':
                    mlogger.info("Starting Daemon")
                    service.kill()
                elif cmd == 'status':
                    mlogger.info("\nStatus: " + ("Running" if service.is_running() == True else "Not Running"))
        else:
            raise Exception("ARGUMENTS MISMATCH")
    except Exception as e:
        mlogger.exception(Exception("usage: %s start|stop|status" % sys.argv[0]))
        sys.exit(2)

