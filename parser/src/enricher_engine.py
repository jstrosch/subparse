import traceback
from time import sleep
from pydoc import locate
from src import ThreadCommand
from src.config import Configuration
from src import Invoker, SubParserLogger
from src.service.manager_consumer_service import ConsumerProcessorService

class EnricherEngine(ThreadCommand):
    def __init__(self, enrichers: list, update_enrichers: bool, config: Configuration) -> None:
        self.logger = SubParserLogger("ENRICHER-ENGINE")
        self.config = config
        self.enrichers = enrichers
        self.enricher_modules = []
        self.update_enrichers = update_enrichers

    #region Import Enrichers
    def load_imports(self):
        self.logger.info("Loading Imports...")
        
        for _enricher in self.enrichers:
            dynamic_class = locate(
                "src.enrichers.%s.%s" % (_enricher.lower(), _enricher)
            )
            if dynamic_class == None:
                self.logger.error("Error Finding Enricher: " + _enricher + ". Check file & class name.")
            else:
                self.enricher_modules.append({"original_name" : _enricher, "class" : dynamic_class})
        self.logger.debug("All Enrichers Have Been Imported")
        self.logger.debug(self.enricher_modules)
    #endregion

    #region Check Enricher Needs
    def check_setup_needs(self):
        try:
            self.logger.debug("Checking services....")
            for _enricher in self.enricher_modules:
                if(_enricher["original_name"] in self.config.start_up_options.keys()):
                    if "start_background_services" in self.config.start_up_options[_enricher["original_name"]].keys():
                        _consumer = ConsumerProcessorService()
                        self.logger.info("Consumer is running :: " + str(_consumer.is_running()))

                        if _consumer.is_running() == False:
                            self.logger.info("Starting Consumer Daemon...")
                            _consumer.start()
                            while _consumer.is_running() == False:
                                self.logger.info("Waiting for daemon to start...")
                                sleep(1)

                            self.logger.info("Started Daemon : PID :: " + str(_consumer.get_pid()))
                        else:
                            self.logger.info("Consumer Daemon Already Running")
                            self.logger.info("Running Daemon At : PID :: " + str(_consumer.get_pid()))

                        break
        except Exception as e:
            self.logger.critical("Error with Service:: " + str(traceback.print_exc()))
            raise e
    #endregion

    #region Execute Enricher(s)
    def execute(self, collected_data: dict = None) -> dict:
        try:
            if self.enricher_modules != [] or self.update_enrichers:
                _use_enrichers = self.enricher_modules
                _md5 = collected_data['md5']

                _keys = []
                for _key in _use_enrichers:
                    if _key['original_name'] not in _keys:
                        _keys.append(_key['original_name'])

                # If force update enrichers is true then collect the class that is needed for re-execution
                if self.update_enrichers:
                    for _update_enricher in collected_data['old_enrichers']:
                        dynamic_class = locate(
                            "src.enrichers.%s.%s" % (str(_update_enricher).lower(), _update_enricher)
                        )
                        if dynamic_class == None:
                            self.logger.error("Error Finding Enricher To Re-Execute: " + _update_enricher + ". Check file & class name.")
                        else:
                            _upd_dict = {"original_name" : _update_enricher, "class" : dynamic_class}
                            if _update_enricher not in _keys:
                                _use_enrichers.append(_upd_dict)

                # Execute enrichers on sample
                for _enricher in _use_enrichers:
                    _enricher_name = str(_enricher['original_name']).upper()
                    _enricher_class = _enricher['class']
                    self.logger.submodule = _enricher_name

                    self.logger.debug(str(_md5) + " :: STARTING" + (" UPDATE" if self.update_enrichers else ""))
                    try:
                        
                        # will execute if the sample is not in the old enrichers OR if update enrichers is true
                        if (self.update_enrichers == False and _enricher_class(None, None).information()['name'] not in collected_data['old_enrichers']) or self.update_enrichers:
                            _invoker = Invoker()
                            _invoker.set_on_start(_enricher_class(md5=_md5, path=collected_data['path']))
                            _result = _invoker.execute()

                            collected_data["used_enrichers"].append(_enricher['original_name'])
                            collected_data["enricher_data"][_result["enricher"]] = _result["data"]
                            self.logger.debug(str(_md5) + " :: FINISHED")
                        else:
                            self.logger.debug(str(_md5) + " :: ALREADY USED")
                    except Exception as e:
                        self.logger.critical(str(e))
                        self.logger.critical("Error With Enricher File :: ENRICHER FATAL EXCEPTION :: " + str(_md5))
                        self.logger.critical(str(traceback.print_exc()))
                    finally:
                        self.logger.submodule = None

                # cleaning parser data if update_enrichers was true
                if self.update_enrichers:
                    collected_data["old_enrichers"] = []

            return collected_data
        except Exception as e:
            raise Exception("[ENRICHER-ENGINE] ERROR PARSING :: %s :: %s" % (str(e), str(_md5)))
    #endregion

