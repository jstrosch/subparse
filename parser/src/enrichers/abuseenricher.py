import requests
from src.helpers import Command
from src.helpers.logging import SubParserLogger

class ABUSEEnricher(Command):
    """
    Abuse Enricher Command - Collects data from the abuse.ch api

    Attributes
    ----------
        - url: str
                Abuse API URL

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
        self.url = "https://mb-api.abuse.ch/api/v1/"
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
        return {"name": "ABUSEEnricher"}
        

    def execute(self) -> dict:
        """
        Requests information about the malwares hash and returns the json request back to the invoker

        Returns
        -------
        Dictionary
        """
        try:
            self._get_abuse_data()
        except Exception as e:
            self.logger.exception(str(e))
            self.data = None
        return {"enricher": "ABUSEEnricher", "data": self.data} 

    def _get_abuse_data(self) -> None:
        """
        Calling Malware Bazaar
        """

        r = requests.post(self.url, data={"query": "get_info", "hash": self.md5})

        if "data" in r.text:
            jobj = r.json()
            data = jobj["data"]
            self.data["AbuseCHData"] = data[0]
            self.data["AbuseCHSignature"] = str(data[0]["signature"]).lower()
            self.logger.debug("[ABUSEENRICHER] - Found Sample On Malware Bazaar")

        return {"enricher": "ABUSEEnricher", "data": self.data}
