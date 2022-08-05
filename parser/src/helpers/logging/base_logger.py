import enum
import logging
import sys
from typing import List
from .formatters import *
from .levels import SubCrawlLoggerLevels
from threading import Lock
from logging.handlers import TimedRotatingFileHandler
from src.helpers.singleton.singleton_meta_class import MetaClassSingleton

class SubParserSingletonLogger(logging.Logger, metaclass=MetaClassSingleton):
    """
    Custom logger implementation for SubParse using the logging package

    Methods
    -------
        - instance(self): SubParserLogger
                The instance of the SubParserLogger

        - get_console_handler(self): 
                Console handler for logging
        
        - get_file_handler(self):
                File handler for logging

        - get_logger(self): Logger
                Logger object from the logging package

        - change_log_level(cls, log_level):
                Override the current instances logging level. 

    """
    
    def __init__(self, file_name: str, log_name: str, log_level: SubCrawlLoggerLevels, file_formatter = None, console_formatter = None):
        super(SubParserSingletonLogger, self).__init__(log_name, log_level.value)

        self.file_name = file_name
        self.log_level = log_level
        self.logger_name = log_name
        self._lock: Lock = Lock()
        self.file_formatter = CustomFileFormatter() if file_formatter == None else file_formatter
        self.console_formatter = CustomConsoleFormatter() if console_formatter == None else console_formatter
    
    def init(self):
        with self._lock:
            self.setLevel(self.log_level.value)
            self.addHandler(self.get_console_handler())
            self.addHandler(self.get_file_handler())
            self.propagate = False

    def change_log_level(self, level: SubCrawlLoggerLevels):
        self.setLevel(level.value)

    def debug(self, msg):
        with self._lock:
            # self.debug(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.DEBUG.value, msg)
    
    def info(self, msg):
        with self._lock:
            # self.info(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.INFO.value, msg)

    def warning(self, msg):
        with self._lock:
            # self.warning(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.WARN.value, msg)

    def warn(self, msg):
        with self._lock:
            # self.warn(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.WARN.value, msg)

    def error(self, msg):
        with self._lock:
            # self.error(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.ERROR.value, msg)

    def critical(self, msg):
        with self._lock:
            # self.critical(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.CRITICAL.value, msg)
    
    def exception(self, msg):
        with self._lock:
            # self.exception(self._msg_builder(msg))
            super().log(SubCrawlLoggerLevels.CRITICAL.value, msg)

    def get_console_handler(self):
        """
        Sets up the console handler for the logger.

        Returns
        -------
        StreamHandler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.console_formatter)
        return console_handler

    def get_file_handler(self):
        """
        Sets up the file handler for the logger.

        Returns
        -------
        TimedRotatingFileHandler
        """
        file_handler = TimedRotatingFileHandler(self.file_name, when='midnight')
        file_handler.setFormatter(self.file_formatter)
        return file_handler
