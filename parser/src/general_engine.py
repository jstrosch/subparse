import hashlib
import magic
import mimetypes
import os
from src.database.base.client import Client
from src import ExtensionHelper, SubParserLogger, ThreadCommand

class GeneralEngine(ThreadCommand):
    def __init__(self, client: Client) -> None:
        self.logger = SubParserLogger("GENERAL-ENGINE")
        self.client = client

    def execute(self, collected_data: dict = None, file: str = None) -> dict:
        try:
            _md5 = hashlib.md5(open(file, "rb").read()).hexdigest()
            _has_doc = self.client.query(_md5)

            self.logger.debug("FILE: " + str(_md5))

            if _has_doc[0] == False:
                self.logger.debug(str(_md5) + " :: NOT IN ELASTIC")

                _file_magic = magic.from_file(file)
                _file_magic_mime = magic.from_file(file, mime=True)
                try:
                    _extension = os.path.splitext(file)[-1]
                    _derived_extension = 'Unknown'
                    if len(_extension) == 0:
                        _extension = 'Unknown'
                        
                    detected = magic.from_file(file, mime=True)
                    _derived_extension = mimetypes.guess_extension(detected)

                    if _derived_extension == None:
                        _extension_guess = ExtensionHelper().get_extension_from_mime(detected)
                        if _extension_guess != None:
                            _derived_extension = _extension_guess
                        else:
                            self.logger.error("Extension not found: " + detected + " : " + file)
                    

                except Exception as no_ex:
                    self.logger.error("No Extension for file %s" % str(_md5))

                collected_data = {
                    "es_has_value": False,
                    "md5" : _md5,
                    "file_size" : os.path.getsize(file),
                    "file_name" : os.path.basename(file),
                    "derived_extension" : _derived_extension,
                    "file_extension" : _extension,
                    "used_enrichers": [],
                    "old_enrichers": [],
                    "enricher_data": {},
                    "used_parsers": [],
                    "old_parsers": [],
                    "parser_data": {},
                    "parser_type": None,
                    "file_magic": _file_magic,
                    "file_magic_mime" : _file_magic_mime,
                    "path": file,
                    "needs_updated": True
                }

            else: 
                self.logger.debug(str(_md5) + " :: IN ELASTIC")
                collected_data = {
                    "es_has_value": True, 
                    "md5" : _has_doc[1]['md5'],
                    "old_enrichers" : _has_doc[1]['used_enrichers'],
                    "old_parsers" : _has_doc[1]['used_parsers'],
                    "used_parsers": [],
                    "used_enrichers" : [],
                    "parser_type" : _has_doc[1]['parser_type'],
                    "file_magic" : _has_doc[1]['file_magic'],
                    "file_magic_mime" :  _has_doc[1]['file_magic_mime'],
                    "parser_data": {},
                    "enricher_data": {},
                    "path": file,
                    "needs_updated": False
                }

            return collected_data
        except Exception as e:
            raise Exception("[GENERAL-ENGINE] ERROR PARSING :: %s :: %s" % (str(e), str(_md5)))

