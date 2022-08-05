from threading import Lock
from typing import List
from src.helpers import ThreadCommand

class ThreadInvoker:
    """
    The Invoker is associated with one or several thread commands. 

    Methods
    -------
        - set_on_start(self, command: Command): None
                Set pre-execution Command
            
        - set_on_finish(self, command: Command): None
                Set post-execution Command

        - execute(self): None:
                Set main execution Command
    """

    _general_engine = None
    _parser_engine = None
    _enricher_engine = None
    _file = None

    def set_general_engine(self, engine: ThreadCommand):
        self._general_engine = engine

    def set_enricher_engine(self, engine: ThreadCommand):
        self._enricher_engine = engine

    def set_parser_engine(self, engine: ThreadCommand):
        self._parser_engine = engine
    
    def set_file(self, file):
        self._file = file

    def execute(self) -> dict:
        lock = Lock()
        if lock.acquire():
            _sample_data = {}
            _sample_data = self._general_engine.execute(_sample_data, self._file)
            _sample_data = self._parser_engine.execute(_sample_data)
            _sample_data = self._enricher_engine.execute(_sample_data)
        return _sample_data
        