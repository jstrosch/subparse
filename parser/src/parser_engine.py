import os
from pydoc import locate
from src.helpers.logging import SubParserLogger
from src import Invoker, SubParserLogger, ThreadCommand

class ParserEngine(ThreadCommand):
    def __init__(self) -> None:
        self.logger = SubParserLogger("PARSER-ENGINE")
        self.parser_modules = {}

    def load_imports(self) -> dict:
        self.logger.info("Loading Imports...")
        for parser in os.listdir(os.path.join('.', 'src', "parsers")):
            if not parser.startswith('__'):
                _file_name = str(parser).replace('.py','')
                dynamic_class = locate("src.parsers.%s.%s" % (_file_name, _file_name))
                if dynamic_class == None:
                    self.logger.error("Error Finding Parser " + _file_name + ". Check file & class name.")
                else:
                    self.parser_modules[_file_name] = {"class" : dynamic_class, "information" : dynamic_class().information()}

    # def process_sample(self, sample: dict):
    def execute(self, collected_data: dict = None) -> dict:
        try:
            _md5 = collected_data['md5']
            _file_magic_mime = collected_data['file_magic_mime']

            self.logger.debug(str(_md5) + " :: PARSING")
            
            for parser, data in self.parser_modules.items():
                _found = False
                for _type in data['information']['file_magic']['other_types']:
                    if _type in _file_magic_mime:
                        collected_data["parser_type"] = data['information']['file_magic']['short_type']
                        _found = True
                        break
                if _found:
                    break

            # if _found == False:
                # print("Mime Type: %s" % _file_magic_mime)
        
            if len(self.parser_modules) != 0:
                for  _parser, _parser_data in self.parser_modules.items():
                    try:
                        self.logger.submodule = _parser
                        if _parser_data['information']['file_magic']['short_type'] == collected_data["parser_type"] and _parser not in collected_data["old_parsers"]:
                            
                            self.logger.debug(str(_md5) + " :: STARTING")
                            _invoker = Invoker()
                            _invoker.set_on_start(_parser_data['class'](md5=_md5, path=collected_data['path']))
                            _result = _invoker.execute()

                            if _result['data'] != {}:
                                collected_data["parser_data"][_result['parser']] = _result['data']
                                collected_data['used_parsers'].append(_parser_data['information']['name'])
                                self.logger.debug(str(_md5) + " :: FINISHED")
                            else:
                                self.logger.error("Error With Parsing File :: PARSER ERROR (" + _parser + ") MD5: " + _md5)
                        elif  _parser in collected_data["old_parsers"]:
                                self.logger.debug(str(_md5) + " :: ALREADY USED")
                        else:
                            self.logger.debug("NOT COMPATIBLE : " + str(_md5))
                    except Exception as e:
                        self.logger.critical(str(e))
                        self.logger.critical("Error With Parsing File :: PARSER FATAL EXCEPTION")
                    finally:
                        self.logger.submodule = None

            return collected_data
        except Exception as e:
            raise Exception("[PARSER-ENGINE] ERROR PARSING :: %s :: %s" % (str(e), _md5))

