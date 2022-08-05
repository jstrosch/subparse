from .base_logger import SubParserSingletonLogger

class SubParserLogger(object):
    def __init__(self, module: str = None, submodule: str = None):
        self.module = module if module != None else (SubParserSingletonLogger().logger_name if SubParserSingletonLogger().logger_name != None else "UNKNOWN-MODULE")
        self.submodule = submodule
        

    def _get_message(self, msg):
        _msg = ''
        if self.module != None and self.submodule != None:
            _msg = "[" + self.module + "][" + self.submodule + "] " + msg
        elif self.module != None:
            _msg = "[" + self.module + "] " + msg
        elif self.submodule != None:
            _msg = "[" + self.submodule + "] " + msg
        else:
            _msg = msg
        
        return _msg

    def debug(self, msg):
        SubParserSingletonLogger().debug(self._get_message(str(msg)))
    
    def info(self, msg):
        SubParserSingletonLogger().info(self._get_message(str(msg)))

    def warning(self, msg):
        SubParserSingletonLogger().warning(self._get_message(str(msg)))

    def warn(self, msg):
        SubParserSingletonLogger().warn(self._get_message(str(msg)))

    def error(self, msg):
        SubParserSingletonLogger().error(self._get_message(str(msg)))

    def critical(self, msg):
        SubParserSingletonLogger().critical(self._get_message(str(msg)))
    
    def exception(self, msg):
        SubParserSingletonLogger().exception(self._get_message(str(msg)))
