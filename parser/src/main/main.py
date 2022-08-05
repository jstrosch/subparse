from threading import Lock
from queue import Queue
from src.database.base.client import Client
from src.helpers.singleton import MetaClassSingleton

class Main(metaclass=MetaClassSingleton):

    def __init__(self) -> None:

        self.__logger = None
        self.__repository = None
        self.__cli_params = None
        self.__guard_dog = None
        self.__observer = None

        self.__parser_engine = None
        self.__enricher_engine = None
        self.__general_engine = None

        self.__sample_count = 0
        self.__samples_processing = 0

        self.lock = Lock()
        self.queue = Queue(maxsize=0)

    #region Properties
    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger):
        self.__logger = logger

    @property
    def repository(self) -> Client:
        return self.__repository

    @repository.setter
    def repository(self, repository: Client):
        self.__repository = repository

    @property
    def cli_params(self):
        return self.__cli_params

    @cli_params.setter
    def cli_params(self, cli_params):
        self.__cli_params = cli_params

    @property
    def isService(self):
        return self.cli_params.isService 


    @property
    def guardDog(self):
        return self.__guard_dog

    @guardDog.setter
    def guardDog(self, handler):
        self.__guard_dog = handler

    @property
    def observer(self):
        return self.__observer

    @observer.setter
    def observer(self, observer):
        self.__observer = observer

    @property
    def parser_engine(self):
        return self.__parser_engine

    @parser_engine.setter
    def parser_engine(self, engine):
        self.__parser_engine = engine

    @property
    def enricher_engine(self):
        return self.__enricher_engine

    @enricher_engine.setter
    def enricher_engine(self, engine):
        self.__enricher_engine = engine

    @property
    def general_engine(self):
        return self.__general_engine

    @general_engine.setter
    def general_engine(self, engine):
        self.__general_engine = engine
    
    @property
    def sample_count(self):
        return self.__sample_count

    @sample_count.setter
    def sample_count(self, count):
        self.__sample_count = count

    @property
    def samples_processing(self):
        return self.__samples_processing

    @samples_processing.setter
    def samples_processing(self, count):
        self.__samples_processing = count
    #endregion
