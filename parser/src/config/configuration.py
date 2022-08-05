import ast
import configparser
import os
from .sandboxes import CapeConfiguration
from .messaging import KafkaConfiguration
from .parsers import OLEParserConfiguration
from src.helpers.singleton import MetaClassSingleton
from src.database.enums.dbtype import parser_config_field

class Configuration(CapeConfiguration, KafkaConfiguration, OLEParserConfiguration, metaclass=MetaClassSingleton):
    """
    This is the main configuration for the Python SubParse program

    Attributes
    ----------
        - config: RawConfigParser
                Raw configuration parser from the configparser library 

        - cape_config: CapeConfiguration
                Cape Sandbox Configuration, all constructor requirements are pulled from the config attribute

        - samples_config: SamplesConfiguration
                Infected Samples Configuration, all constructor requirements are pulled from the config attribute

        - log_file: str
                Log file name to be used for Logger Object output

        - logger_name: str
                Logger name to be used for the Logger Object formatting

        - log_level: str
                Default log level to use for output and file creation
            
        - zip_pass: str
                Password to use for creation of zip file
        
        - delete_orig: bool
                True/False on if to delete the original samples given to the program AFTER zip file creation

        - zip_path: str
                Path to save the zip file 

        - create_zip: bool
                True/False on if a zip file is to be created

        - file_exclusions: list
                Hold a list of file names that should be excluded when creating the list of samples to parse
        
    Methods
    -------
        - save(self): -> null
            Saves the current configuration of the system

    """
    def __init__(self) -> None:
        # region init for the configration
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "configuration.cfg"
        )
        conf.read(_path)

        self.config = conf
        # endregion

        CapeConfiguration.__init__(self)
        KafkaConfiguration.__init__(self)
        # ElasticConfiguration.__init__(self)
        OLEParserConfiguration.__init__(self)

        #region Worker Count
        self.worker_count = int(self.config.get("THREADING", "worker_count"))
        #endregion 

        # region Logging
        self.log_file = self.config.get("LOGGER", "log_file")
        self.logger_name = self.config.get("LOGGER", "logger_name")
        self.log_level = self.config.get("LOGGER", "log_level")
        # endregion 

        #region Zip File
        self.zip_pass = self.config.get("ZIP", "password")
        self.delete_orig = self.config.getboolean("ZIP", "delete_orig")
        self.zip_path = self.config.get("ZIP", "zip_path")
        self.create_zip = self.config.getboolean("ZIP", "create_zip")
        #endregion

        #region Exclusion(s)
        self.file_exclusions = ast.literal_eval(self.config.get('PARSE_EXCLUDE', 'file_exclude_list'))
        #endregion      

        # region On Start Options
        self.start_up_options = dict({"CAPEEnricher" : self.cape_onstart}) 
        # endregion

        # region Get Database Type
        self.databaseType = parser_config_field(self.config.get("DATABASE", "database"))
        # endregion