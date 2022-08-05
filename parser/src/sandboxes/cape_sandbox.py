import os
import urllib3
from urllib3 import exceptions
import json
from src.service.message.service_message import ServiceMessage
from src.sandboxes.helpers.cape.cape_sandbox_neterror import CapeSandboxNetError
from src.sandboxes.helpers.cape.cape_sandbox_md5_search import CapeSandboxMD5Search
from src.helpers.logging import SubParserLogger
from src.config.configuration import Configuration
from .base import SandBox

class CapeSandBox(SandBox):
    """
    Cape Sand Box

    Methods
    -------
        - _wrapped_caller(self, info: str, url: str) -> str:
                returns the responce from its called url, used as a helper function within this object

        - submit_report_to_elastic(self, report: dict, message: ServiceMessage) -> bool:
                returns a boolean depending on if the report could be submitted to Elastic 

        - sample_exists(self, md5: str) -> CapeSandboxMD5Search:
                returns a CapeSandBoxMD5Search Object with information about the samples existence in CAPE V2 

        - submit_job(self, message: ServiceMessage) -> bool:
                returns a boolean depending on if the sample was able to be submitted to CAPE V2

        - job_status(self, job_id: str) -> dict:
                returns a dictionary which is the samples status results from CAPE V2

        - sandbox_status(self) -> bool:
                returns a boolean depending on if the connection to CAPE V2 was able to be made
    
    """
    def __init__(self, cape_config: Configuration = None, logger: SubParserLogger = None) -> None:
        """
        Constructor for CapeSandBox

        Parameters
        ----------

            - cape_config: Configuration
                    Main Configuration Object

            - logger: SubParseLogger
                    SubParseLogger Object
        """
        SandBox.__init__(self)
        self.logger = logger
        self.cape_config = cape_config
        self.header = {"Authorization" : "Token " + self.cape_config.cape_token} if self.cape_config.cape_token != None else {}


    # region Wrapped Caller for cape url queries
    def _wrapped_caller(self, info: str, url: str) -> str:
        """
            A helper function for making calls to the CAPE V2 instance, setting up the header(s) that are needed
        """
        try:
            try:
                http = urllib3.PoolManager(num_pools=2, retries=5)
                self.logger.info("[CAPE-SANDBOX] (" + info + ") Trying to make call :: " + url)
                resp = http.request("GET", url, headers=self.header, timeout=5)
                self.logger.info("[CAPE-SANDBOX] (" + info + ") Job status code :: " + str(resp.status))

                if int(resp.status) == 401:
                    _json = json.loads(resp.data.decode('utf-8')) 
                    _error = CapeSandboxNetError(**_json)
                    raise Exception("[CAPE-SANDBOX] (" + info + ") ERROR CONNECTING TO CAPE SANDBOX :: " + str(_error.detail).upper())
                elif int(resp.status) == 200:
                    if len(resp.data) > 1000:
                        self.logger.info("[CAPE-SANDBOX] (" + info + ") Call returned :: A LOT OF DATA > 1000")
                    else:
                        self.logger.info("[CAPE-SANDBOX] (" + info + ") Call returned :: " + str(resp.data.decode('utf-8')))
                    return resp.data.decode('utf-8')

            except Exception as e:
                raise Exception("[CAPE-SANDBOX] (" + info + ") ERROR GETTING JOB STATUS FROM CAPE :: " + str(e).upper())

        except Exception as jse:
            self.logger.error(str(jse))

        return None
    # endregion

    # region Get Job Report
    def get_job_report(self, job_id: int) -> dict:
        try:
            url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/tasks/get/report/" + str(job_id) + "/"
            _report = self._wrapped_caller("JOB REPORT", url)
            self.logger.info("[CAPE-SANDBOX] Report for job id " + str(job_id) + " :: Pulled Successfully")
            return json.loads(_report)

        except Exception as jse:
            self.logger.error("[CAPE-SANDBOX] Error getting Report: " + str(jse))

        return None
    # endregion

    def submit_report_to_elastic(self, report: dict, message: ServiceMessage) -> bool:
        """
        Submit a report from CAPE V2 to Elastic 

        Parameters 
        ----------
            - report: dict
                    report from CAPE V2 that needs to be submitted to Elastic 

            - message: ServiceMessage
                    Service Message to help with placing the report into Elastic, includes information for the sample
                        to place the information in the right place. This message comes from the Kafka Service.
        """
        self.logger.info("[CAPE-SANDBOX] (Submitting Report) Submitting report to elastic needs done")
        self.logger.info("[CAPE-SANDBOX] (Submitting Report) ID :: " + message.md5)
        self.logger.info("[CAPE-SANDBOX] (Submitting Report) DataType :: " + message.type)
        try:
            self.logger.info("[CAPE-SANDBOX] Elastic missing hash cannot update data")
        except Exception as e:
            self.logger.error("[CAPE-SANDBOX] Elastic :: submitting job :: " + str(e))

    # region Check if samples exists in Cape Sandbox
    def sample_exists(self, md5: str) -> CapeSandboxMD5Search:
        """
        Checks to see if the sample exists in CAPE V2 

        Parameters
        ----------
            - md5: str
                The MD5 hash of the sample that is to be submitted
        """
        # curl http://192.168.86.51:8080/apiv2/tasks/search/md5/549deb302ad75077461314056114a477/
        try:
            url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/tasks/search/md5/" + str(md5) + "/"
            _sample = self._wrapped_caller("SAMPLE EXISTS", url)
            if _sample == None:
                self.logger.info("[CAPE-SANDBOX] (Sample Exists Check) Sample Does Not Exists :: " + str(md5))
                return None
            else:
                self.logger.info("[CAPE-SANDBOX] (Sample Exists Check) Sample Might Exist :: " + str(_sample))
                try:
                    _json = json.loads(str(_sample))
                    if _json['data'] != []:
                        _search = CapeSandboxMD5Search(**_json)
                        self.logger.info("[CAPE-SANDBOX] (Sample Exists Check) Sample Exists :: search object completed_on :: " + str(_search.data[0]["completed_on"]))
                        return _search
                    else:
                        self.logger.info("[CAPE-SANDBOX] (Sample Exists Check) Sample Exists :: False")
                        return None
                except Exception as e:
                    raise Exception("[CAPE-SANDBOX] (Sample Exists Check) ERROR CONVERTING OBJECT :: " + str(e))

        except Exception as jse:
            self.logger.error(str(jse))

        return None
    # endregion

    # region Submit Sample to Cape
    def submit_job(self, message: ServiceMessage) -> bool:
        """
        Submit a sample to CAPE V2 
        
        Parameters
        ----------
            - message: ServiceMessage
                    This message contains the path of the sample that needs to be submitted to CAPE V2, this message 
                        originates from the Kafka Service
        """
        try:
            _filename = os.path.basename(message.sample)
            self.logger.info("[CAPE-SANDBOX] (Submitting Job) Sample file to submit: " + message.sample)
            with open(message.sample, "rb") as sample:
                # multipart_file = {"file": ("temp_file_name", sample)}
                file_data = sample.read()
                
            http = urllib3.PoolManager(num_pools=2,retries=5)
            url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/tasks/create/file/"
            self.logger.info("[CAPE-SANDBOX] (Submitting Job) Calling to Cape Sanbox :: " + str(url))
            resp = http.request('POST', url, headers=self.header, timeout=5, 
                fields={
                    "file": (_filename, file_data),
                    "timeout" : self.cape_config.cape_timeout,
                    "enforce_timeout" : self.cape_config.cape_enforce_timeout,
                    "priority" : self.cape_config.cape_priority
                    }
                )
                
            self.logger.info("[CAPE-SANDBOX] (Submitting Job) Submit resp: " + str(resp.data))
            return True

        except Exception as sube:
            self.logger.error("[CAPE-SANDBOX] (Submitting Job) ERROR :: " + str(sube))
            return False
    # endregion

    # region Get Job Status
    def job_status(self, job_id: str) -> dict:
        """
        Check on the status of a job (sample) that has been submitted to CAPE V2 

        Parameters
        ----------
            - job_id: str
                Gets the status of the job that has been submitted too CAPE V2 and returns the dictionary that is 
                    produced by CAPE V2
        """
        try:
            url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/tasks/status/" + str(job_id) + "/"

            _status = self._wrapped_caller("JOB STATUS", url)
            self.logger.info("[CAPE-SANDBOX] (Job Status) Trying to get job status :: " + str(job_id))
            return _status
        except Exception as jse:
            self.logger.error(str(jse))

        return None
    # endregion

    # region Get CapeSand Box Status 
    def sandbox_status(self) -> bool:
        """
        Checks the availability of the CAPE V2 instance to make sure that its reachable.
        """
        try:

            try: 
                url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/cuckoo/status/"
                _status = self._wrapped_caller("SANDBOX STATUS", url)

                if _status == None:
                    return False
                else:
                    return True
            except exceptions.NewConnectionError as htce:
                raise Exception("[CAPE-SANDBOX] (Sandbox Status) ERROR CONNECTING TO CAPE SANDBOX :: CHECK SANDBOX NETWORK SETTINGS :: " + str(htce).upper())
                
        except Exception as e:
            self.logger.error(str(e))

        return False
    # endregion

    #region Task List
    def get_task(self) -> list:
        try:
            url = "http://" + self.cape_config.cape_host + ":" + self.cape_config.cape_port + "/apiv2/tasks/list/"
            _report = self._wrapped_caller("JOB REPORT", url)
            self.logger.info("[CAPE-SANDBOX] Task List ")
            return json.loads(_report)

        except Exception as jse:
            self.logger.error("[CAPE-SANDBOX] Error getting Report: " + str(jse))

        return None

    #endregion