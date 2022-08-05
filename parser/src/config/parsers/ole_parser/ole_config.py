import os
import configparser
from src.helpers.singleton.singleton_meta_class import MetaClassSingleton

class OLEParserConfiguration(metaclass=MetaClassSingleton):
    def __init__(self) -> None:
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "ole_configuration.cfg"
        )
        conf.read(_path)

        self.ole_parser_output = conf.get("OLE_PARSER", "output_dir")