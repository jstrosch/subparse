from email import header
from urllib import response
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from src.helpers import Command
from src.helpers.logging import SubParserLogger

class TEMPLATEEnricher(Command):
    """
    TEMPLATE Enricher Command - AN EXAMPLE

    Attributes
    ----------
        - md5: str
                Samples MD5 hash

        - data: dict
                Collected data from the Abuse API call

        - logger: SubParserLogger
                SubParserLogger Object for output to console and file 
    
    Methods
    -------
        - execute(self): dict
                Used by the Commands Invoker to execute the underlying Abuse Enrichers collection process

        - information(self): dict
                Enricher information for compatible file types

    """
    def __init__(self, md5: str, path: str):
        """
        Constructor for abstract enricher

        Parameters
        ----------
            - md5: str
                    MD5 hash of the sample
            
            - logger: SubParserLogger
                    SubParserLogger Object for output to console and file

            - path: str
                    Full path to the location of the sample
        """
        super().__init__()
        self.md5 = md5
        self.data = {}
        self.logger = SubParserLogger("ABUSE-ENRICHER")

    def information(self):
        """
        Compatiblity information for enricher

        Returns
        -------
        Dictionary
        """
        return {"name": "TEMPLATEEnricher"}
        

    def execute(self) -> dict:
        """
        Requests information about the malwares hash and returns the json request back to the invoker

        Returns
        -------
        Dictionary
        """
        try:
            # DO Stuff Here
            pass
        except Exception as e:
            self.logger.exception(str(e))
            self.data = None
        return {"enricher": "TEMPLATEEnricher", "data": self.data} 


