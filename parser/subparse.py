#!/usr/bin/env python3.8

# region Imports
from copy import copy
import argparse
import os
import time
from typing import List
from watchdog.observers import Observer
from src.helpers.guarddog.guard_dog import GuardDogHandler
from src import Configuration, CLI_Params,\
                Zip, SubCrawlLoggerLevels, SubParserLogger, SubParserSingletonLogger,\
                ParserEngine, EnricherEngine, GeneralEngine, ThreadingObject, ThreadInvoker,\
                Repository


from src.main.main import Main
                
# endregion

# region Main
# the only thing that this should do is check the file and load it into the queue for processing
# also should not be building out the workers that are going to be used!
def main(_main: Main, _sample_files: List[str]):
    
    _main.logger.debug("CLI Params: " + str(_main.cli_params))
    
    try:
        # region Sample Checking
        if os.path.isdir(_main.cli_params.samples_dir) and _main.cli_params.watchdog == False:
            _main.logger.debug("Sample Dir Path: " + _main.cli_params.samples_dir)
        elif _main.cli_params.watchdog == True:
            _main.logger.info("Service Mode: " + _main.cli_params.samples_dir)
        else:
            raise Exception("Samples path needs to be a folder")
        # endregion

        _thread_invoker = ThreadInvoker()
        _thread_invoker.set_general_engine(copy(_main.general_engine))
        _thread_invoker.set_parser_engine(copy(_main.parsers_engine))
        _thread_invoker.set_enricher_engine(copy(_main.enrichers_engine))

        for sample in _sample_files:
            if _main.lock.acquire():
                _main.samples_processing += 1
                _main.logger.info("PROCESSING [" + str(_main.samples_processing) + "/" + str(_main.sample_count) + "]: " + os.path.basename(sample))
                _thread_invoker.set_file(sample)
                _main.queue.put(copy(_thread_invoker))
                _main.lock.release()
        _main.queue.join()
        # endregion        
    except KeyboardInterrupt as ke:
        for i in _main.queue:
            i.stop()
        raise ke
    except Exception as e:
        _main.logger.critical("MASSIVE ERROR :: " + str(e))


# region Callback for watchdog
# should be moved to the main object
def watchdog_callback(sample_path: str, _main: Main):
    _main.logger.debug("Trying to use path: " + sample_path)
    _main.sample_count += 1
    main(_main, [sample_path])
# endregion

 #region Import Enrichers
def get_current_enrichers():
    _enrichers = []    
    for file in os.listdir(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "src", "enrichers"
        )):
        if ".py" in file and "__init__" not in file:
            _file = file.split(".py")[0]
            _c1 = _file.split('enricher')[0]
            _enricher_file = "%s%s" % (_c1.upper(), "Enricher")
            if _enricher_file not in _enrichers:
                _enrichers.append(_enricher_file)

    return _enrichers
#endregion

# region __Name__
if __name__ == "__main__":
    _config = Configuration()
    _start = time.time()
    _main = Main()

    SubParserSingletonLogger(_config.log_file, _config.logger_name, SubCrawlLoggerLevels[_config.log_level])
    SubParserSingletonLogger().init()
    mlogger = SubParserLogger()
    
    try:    
        #region Parser Arguments
        parser = argparse.ArgumentParser(description="")

        parser.add_argument(
            "-d",
            "--directory",
            action="store",
            dest="samples_dir",
            default="",
            help="Directory to find samples to parse",
        )

        parser.add_argument(
            "-r",
            "--reset",
            action="store_true",
            dest="elastic_reset",
            help="Deletes all data in the configured Elasticsearch cluster",
        )

        parser.add_argument(
            "-e",
            "--enrichers",
            action="store",
            dest="enricher_modules",
            help="Enricher modules for additional file data. Current enrichers: %s" % (', '.join(get_current_enrichers()))
        )

        parser.add_argument(
            "-ue",
            "--update-enrichers",
            action="store_true",
            dest="update_enrichers",
            help="Force Enrichers that have been used on the samples to be re-executed",
            default=False
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store",
            dest="verbose",
            help="Verbose Output/Logging. Available levels: CRITICAL, ERROR, WARN, INFO, DEBUG, NOTSET",
            default=str(_config.log_level).upper()
        )

        parser.add_argument(
            "-s",
            "--service-mode",
            action="store_true",
            dest="service_mode",
            help="Enter Service Mode",
            default=False
        )
        #endregion 

        _cli_options = parser.parse_args()

        if str(_cli_options.verbose).upper() != _config.log_level:
            try:
                SubParserSingletonLogger().change_log_level(SubCrawlLoggerLevels[str(_cli_options.verbose).upper()])
            except Exception as ovl:
                mlogger.exception(ovl)
                raise Exception("ERROR :: CHANGING LOGGING VALUE FAILED (CHECK AVAILABLE LEVELS WITH -h)")

        _main.logger = mlogger
        _main.cli_params = CLI_Params(
                            reset=_cli_options.elastic_reset,
                            enrichers=_cli_options.enricher_modules,
                            samples_dir=_cli_options.samples_dir,
                            verbose=_cli_options.verbose,
                            watchdog=True if _cli_options.service_mode else False, # this needs to be changed (use property)
                            update_enrichers=_cli_options.update_enrichers,
                            isService=_cli_options.service_mode
                        ) 

        #region Setting Up Elastic DB Object
        try:
            Repository.dbType = _config.databaseType
            _main.repository = Repository.get_connection()
            _main.repository.connect()
        except Exception as e:
            raise e
        #endregion

        # region checking for reset flag
        if _main.cli_params.reset:
            try:
                if _main.repository.reset():
                    exit()
                else:
                    raise Exception("Elastic was not successfully reset")
            except Exception as e:
                raise e
        # endregion

        #region Loading Engines
        # Needs to be moved out of this 'main' should be a 'prepare'
        _main.general_engine = GeneralEngine(_main.repository)
        _main.parsers_engine = ParserEngine()
        _main.enrichers_engine = EnricherEngine(_main.cli_params.enrichers, _main.cli_params.update_enrichers, Configuration())

        _main.parsers_engine.load_imports()        
        _main.enrichers_engine.load_imports()
        _main.enrichers_engine.check_setup_needs()
        #endregion

        if _main.cli_params.isService == False:
            _sample_files = []
            for path, subdirs, files in os.walk(_main.cli_params.samples_dir):
                for name in files:
                    if(name not in Configuration().file_exclusions):
                        _sample_files.append(os.path.join(path, name))

            _main.sample_count = len(_sample_files)

        #region Setting Up Threading Queue Start
        for x in range(Configuration().worker_count):
            worker = ThreadingObject(_main.queue, _main.logger, _main.lock, _main.repository, (_main.sample_count if not _main.isService else None), _main.isService)
            worker.setDaemon(True)
            worker.start()
        #endregion Setting Up Threading Queue End

        #region Specifying specific `modes`
        if _main.isService:
            _main.logger.debug("Is Service") 
            _main.guard_dog = GuardDogHandler(watchdog_callback, _main)
            _main.observer = Observer() 
            _main.logger.debug(_main.cli_params)
            _main.observer.schedule(_main.guard_dog, _main.cli_params.samples_dir, recursive=True)
            _main.observer.start()
            try:
                while True:
                    time.sleep(1)
            except Exception as e:
                raise e
            finally:
                _main.observer.stop()
                _main.observer.join()
        else:
            _main.logger.debug("Start in normal mode")
            main(_main, _sample_files)
        #endregion

        try:
            #region Zip Creation
            mlogger.info("Attempting Zip Creation")
            if(_config.create_zip):
                _zip = Zip(_main.cli_params.samples_dir, _config.zip_path, _config.zip_pass, _config.delete_orig, _main.logger)
                _zip.zip()
            else:
                _main.logger.info("Skipping zip creation :: User Requested No Zip")
            #endregion 
        except Exception as e:
            mlogger.debug("[ZIP] ERROR ATTEMPTING ZIP CREATION")
            
    except KeyboardInterrupt as ke:
        mlogger.error("User Terminated Process")
    except Exception as e:
        mlogger.error(str(e))
    finally:
        try:
            mlogger.info("[ELASTIC] Closing Elastic Connection")
        except Exception as e:
            mlogger.debug("[ELASTIC] ERROR CLOSING CONNECTION")

        mlogger.info("Finished Processing")
        mlogger.info("--- %s seconds ---" % (time.time() - _start))
# endregion
