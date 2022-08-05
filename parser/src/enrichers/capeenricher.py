import json
import time
import hashlib
from src.database.base.client import Client
from src.helpers import SubParserLogger, ServiceCommand
from src.service.message.service_message import ServiceMessage
from src.service.manager_producer_service import ProducerProcessorManager
from src.sandboxes.cape_sandbox import CapeSandBox
from src.config.configuration import Configuration

class CAPEEnricher(ServiceCommand):
    """
    Cape Sandbox Enricher Command - Collects data from the cape sandbox.

    Methods
    -------
        - information(self): dict
                returns a dictionary that has information about the enricher
        
        - service_initialized(self, message: ServiceMessage) -> bool:
                returns a boolean if the callback from the service was able to submit the sample to the CAPE V2 Instance

        - service_processing(self, message: ServiceMessage) -> bool:
                returns a boolean if the callback from the service was able to submit the processing message

        - service_reporting(self, message: ServiceMessage, elastic: Elastic) -> bool:
                returns a boolean if the callback from the service was able to submit the reporting message
                    and update the elastic instance(s) database
        
        - service_error(self, message: ServiceMessage, elastic: Elastic) -> bool:
                returns nothing at the moment, have not gotten to the error messages from CAPE V2, 
                    since as of yet, no sample has been submitted has generated an error on that end

        - _submit_message(self, type: str, org_submitted_time: int):
                makes the call to Kafka submitting the message to the messaging service

        - execute(self) -> dict:
                returns a dictionary that has the inital data to be placed into Elastic noting that it is processing.
                    This also make a call to Kafka to start the messaging process(es) that will be used during the 
                    processing of the sample with CAPE.
    
    """

    def __init__(self, md5: str, path: str):
        """
        Constructor for cape enricher

        Parameters
        ----------
            - md5: str
                    MD5 hash of the sample
            
            - logger: SubParserLogger
                    SubParserLogger Object for output to console and file

            - path: str
                    Full path to the location of the sample

       
        """
        ServiceCommand.__init__(self)
        self.full_path = path
        self.logger = SubParserLogger("CAPE-ENRICHER")
        self._config = Configuration()
        self.module_type = str(self.__module__) + "." + str(self.__class__.__name__)
        self.message_producer = ProducerProcessorManager()
        self.cape_sandbox = CapeSandBox(self._config, self.logger)
        self.tasks = None
        
        if self.full_path != None:
            self.md5 = str(hashlib.md5(open(self.full_path,'rb').read()).hexdigest())
        else:
            self.md5 = None

    def information(self) -> dict:
        """
        Compatiblity information for enricher

        Returns
        -------
        Dictionary
        """
        return {"name": "CAPEEnricher"}

    def service_initialize(self, message: ServiceMessage) -> bool:
        """
        The first message to be used when submitting a sample to CAPE V2

        Parameters
        ----------
            - message: ServiceMessage
                This message contains the information needed to submit the sample to the CAPE V2 instance. 
        """
        try:
            try:
                if self.cape_sandbox.sandbox_status() == True:
                    # check to see if the sample has been submitted 
                    self.tasks = self.service_getTasks()
                    _md5 = hashlib.md5(open(message.sample,'rb').read()).hexdigest()
                    _exits = False

                    if self.tasks != None:
                        for _t in self.tasks['data']:
                            self.logger.info("In tasks: " + str(_t['sample']['md5']))
                            if _t['sample']['md5'] == _md5:
                                _exits = True
                                break
                    if _exits:
                        self.logger.info("Sample Exists")
                        _submitted = True
                    else:
                        self.logger.info("Sample Not there")
                        _submitted = self.cape_sandbox.submit_job(message)
                    
                    if _submitted: 
                            self._submit_message("processing", message.first_seen)
                    else:
                        self._submit_message("error", message.first_seen)

                else:
                    raise Exception("[CAPE-Enricher] (Init Message) CAPE SYSTEM CAN NOT BE REACHED :: STATUS :: " + str(self.cape_sandbox.sandbox_status()))

                
            except Exception as e:
                self.logger.error(str(e))
                return False
        except Exception as e:
            self.logger.error(str(e))
            return False

    def service_processing(self, message: ServiceMessage) -> bool:
        """
        The second message to be used, this checks on the progress of the sample and if it has been completed or not
            if it has been, a reporting message is emited, else it replays the processing message.

        Parameters
        ----------
            - message: ServiceMessage
                This message contains the information needed to check on the sample in the CAPE V2 instance.
        """
        self.logger.info("[CAPE-Enricher] (Processing Message) Sample is processinig...")
        self.logger.info("[CAPE-Enricher] (Processing Message) Sample status needs to be checked...")
        if(message.job_id == None):
            try:
                _sample = self.cape_sandbox.sample_exists(message.md5)
                message.job_id = _sample.data[0]['id']  
                self.logger.info("[CAPE-Enricher] (Processing Message) Job ID: " + str(message.job_id))
                _status = self.cape_sandbox.job_status(message.job_id)
                self.logger.info("[CAPE-Enricher] (Processing Message) Job Status")
                self.logger.info(_status)

                _json = json.loads(_status)

                if _json['data'] == "running":
                    self._submit_message("processing", message.first_seen)
                elif _json['data'] == "pending":
                    self._submit_message("processing", message.first_seen)
                elif _json['data'] == "reported":
                    self._submit_message("reporting", message.first_seen)
                else:
                    self.logger.info("[CAPE-Enricher] (Processing Message) Job Status :: " + str(_status))

            except Exception as e:
                self.logger.error("[CAPE-Enricher] (Processing Message) Error getting job status: "  + str(e))

        return True
    
    def service_reporting(self, message: ServiceMessage, client: Client) -> bool:
        """
        The last message to be used, this will collect the report from CAPE V2 and add the data to the corresponding 
            samples data in the Elastic instance.

        Parameters
        ----------
            - message: ServiceMessage
                This message contains the information needed to check on the sample in the CAPE V2 instance.

            - elastic: Elastic
                Allows access to the Elastic Instance that contains the rest of the sample(s) data.
        """
        self.logger.info("[CAPE-Enricher] (Reporting Message) Reporting From Kafka")
        if self.cape_sandbox.sandbox_status() == True:
            _exits = False
            _task_data = None
            self.tasks = self.service_getTasks()
            if self.tasks != None:
                for _t in self.tasks['data']:
                    self.logger.info("In tasks: " + str(_t['sample']['md5']))
                    if _t['sample']['md5'] == message.md5:
                        _exits = True
                        _task_data = _t
                        break
            if _exits:
                self.logger.info("Sample Exists")
                self.logger.info("Job Report: " + str(_task_data['id']))
                try:
                    _job_report = self.cape_sandbox.get_job_report(_task_data['id']) 
                    self.logger.info("Report Type: " + str(type(_job_report)))
                    if _job_report != None:
                        try:
                            _report_data = {
                                            'payloads' : None,
                                            'info' : None
                                        }
                            self.logger.info("Report data type: " + str(type(_job_report)))

                            try:
                                _payloads = _job_report['CAPE']['payloads']
                                for _payload in _payloads:
                                    del _payload['strings']

                                _report_data['payloads'] = _payloads
                            except Exception as e:
                                self.logger.exception(str(e))

                            try:
                                _report_data['target'] = _job_report['target']
                                del _report_data['target']['file']['strings']
                            except Exception as e:
                                self.logger.exception(str(e))

                            try:
                                _report_data['info'] = _job_report['info']
                            except Exception as e:
                                self.logger.exception(str(e))

                            try:
                                _report_data['dropped'] = _job_report['dropped']
                            except Exception as e:
                                self.logger.exception(str(e))
                                
                            client.update_sandbox_data(_report_data, message)
                        except Exception as e:
                            self.logger.error("Error with submitting to client: "  + str(e))
                            return False
                except Exception as e:
                    self.logger.exception("ERROR GETTING REPORT :: " + str(e))
            else:
                self.logger.info("Sample Not there")
                self.logger.info("[CAPE-Enricher] (Reporting Message) Trying to submit job to cape :: REPORT NOT THERE")

        return True
        
    def service_error(self, message: ServiceMessage, client: Client) -> bool:
        """
        Currently not being used, as of yet, the samples that have been used have not caused CAPE V2 to emit a 
            error status
        """
        pass

    # could be moved to the parent object?
    def _submit_message(self, type: str = None, org_submitted_time: int = None, msg: ServiceMessage = None):
        """
        Wrapper for submitting a new ServiceMessage to the background services that work with Kafka.
        """
        if msg == None:
            msg = ServiceMessage(
                            first_seen=org_submitted_time, last_seen=int(time.time()),
                            topic=self._config.cape_topic, md5=self.md5, sample=self.full_path, type=type,
                            module= self.module_type, module_name=self.__class__.__name__
                        )
        self.message_producer.commands.submit_message(msg)
        self.logger.info("[CAPE-Enricher] (Submitting Message) :: " + str(msg))
        

    def service_getTasks(self):
       return self.cape_sandbox.get_task()
        

    def execute(self) -> dict:
        """
        Execute the CapeEnricher from subparse, to then pass the rest of the processing off to the 
            background services and the CAPE V2 Sandbox.
        """
        # Since this is now a service command the execute section is for submitting
        #   a message to the producer service ONLY!
        _message = ServiceMessage(
            first_seen=int(time.time()), last_seen=int(time.time()),
            topic=self._config.cape_topic, md5=self.md5, sample=self.full_path, type="initialized",
            module= self.module_type, module_name=self.__class__.__name__
            )
        
        self._submit_message(msg=_message)
        
        return {"enricher": "CAPEEnricher", "data": {"status" : "processing"}}