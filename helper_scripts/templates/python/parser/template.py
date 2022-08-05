import os
from typing import Any
from src.helpers.logging import SubParserLogger
from src.helpers import Command

class TEMPLATEParser(Command):
    """
    Template Parser: Template

    Attributes
    ----------
        - name: str
                MD5 of the sample

        - path: str
                Path to the samples location

        - logger: SubParserLogger
                SubParserLogger Object for output to console and file 

    Methods
    -------
        - execute(self): dict
                Collects PE Information and is executed by the command invoker

        - information(self): dict
                Parser information for compatible file types
    """
    def __init__(self, md5: str = None, path: os.path = None) -> None:
        """
        Constructor for pe parser

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
        self.name = md5
        self.path = path
        self.logger = SubParserLogger()
        self._data = {}
        
        
    def information(self):
        """
        Compatiblity information for parser

        Returns
        -------
        Dictionary
        """
        return {
                "name": "TEMPLATEParser",
                "file_magic": {
                    "short_type": "pe",
                    "other_types": [
                        "pe32",
                        "ms-dos",
                        "application/x-dosexec"
                    ]
                }
            }

    # region Execute ( For Command Object )
    def execute(self) -> Any:
        """
        Template Example

        Returns
        -------
        Dictionary
        """

        # Do stuff here and then return the self._data dictionary
        
        return {"parser" : "TEMPLATEParser", "data" : self._data}
    # endregion
