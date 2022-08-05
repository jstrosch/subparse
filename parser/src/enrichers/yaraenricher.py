import os
import yara
from src.helpers import Command
from src.helpers.logging import SubParserLogger

# Using Rules from 
# https://yara-rules.github.io/blog/

class YARAEnricher(Command):
    """
    Yara Enricher Command - Collects data for yara information

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
        self.path = path
        self.data = {}
        self.logger = SubParserLogger("YARA-ENRICHER")

    def information(self):
        """
        Compatiblity information for enricher

        Returns
        -------
        Dictionary
        """
        return {"name": "YARAEnricher"}
        

    def execute(self) -> dict:
        """
        Requests information about the yara rules

        Returns
        -------
        Dictionary
        """
        try:
            local_rules = yara.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "yara_rules", 'all_rules'))
            file_data = None
            
            self.data['yara_file'] = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "yara_rules", 'all_rules'))
            self.data['matched'] = []

            try:
                with open(self.path, "rb") as file_open:
                    file_data = file_open.read()
            except Exception as e:
                raise Exception("ERROR OPENING SAMPLE")

            try:
                match = local_rules.match(data=file_data)

                if len(match) != 0:
                    for rule in match:
                        rule_data = {
                            'rule': None,
                            'meta_data': {
                                'author' : None,
                                'original_author' : None,
                                'date' : None,
                                'description' : None,
                                'reference' : None,
                                'method' : None,
                                'version' : None,
                                'filetype' : None,
                                'source' : None
                            },
                            'tags': None
                        }

                        rule_data['rule'] = "%s" % rule
                        rule_data['tags'] = rule.tags
                        self.data['matched'].append(rule_data)
                        
                        if rule.meta != {}:
                            _meta_keys = rule.meta.keys()
                            for key in ['author', 'original_author', 'description', 'reference', 'method', 'version', 'filetype', 'source']:
                                if key in _meta_keys:
                                    rule_data['meta_data'][key] = "%s" % rule.meta[key]
            except Exception as e:
                raise Exception("ERROR WITH YARA DATA :: %s :: %s" % (self.md5, str(e)))
            
        except Exception as e:
            self.logger.exception(str(e))
            self.data = None

        return {"enricher": "YARAEnricher", "data": self.data} 
