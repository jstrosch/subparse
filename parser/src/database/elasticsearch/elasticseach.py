from threading import Thread, Lock
import traceback
from src.helpers.logging.logger import SubParserLogger
from .elasticsearch_config import ElasticsearchConfig
from ..base import Client
from elasticsearch.helpers import bulk
from datetime import datetime
from src.helpers.input import InputPrinter
from src.helpers.singleton import MetaClassSingleton
from elasticsearch import Elasticsearch, ConnectionError
from six import with_metaclass

class ElasticsearchRepository(Client, ElasticsearchConfig):

    def __init__(self) -> None:
        super().__init__()
        self.client = None
        self.logger = SubParserLogger("ELASTIC-CLIENT")
        self.waiting_upload_data = {}
        self.count = 0

    def print_config(self):
        print(super().__str__())

    def create(self) -> bool:
        raise NotImplementedError

    def create_table(self):
        try:
            _setting = {
                "settings" : {
                    "index.mapping.total_fields.limit": 15000,
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
            self.client.indices.create(index=self.collection(), ignore=400, body=_setting)
            
            self.logger.info("Created Empty Table")
            self.logger.info("Elastic was successfully reset")
            return True
        except Exception as e:
            raise Exception("ERROR CREATING COLLECTION")

    def check_table(self) -> bool:
        """
        This checks to see if the collection that is being passed in the elastic configuration exists. ('Private Method')
            
        Returns
        -------
        False: doesn't exist
        True: exists
        """
        return self.client.indices.exists(index=self.collection())

    def read(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
    
    def delete(self):
        raise NotImplementedError

    def threading_callback(self, data: dict, total_count: int = None, isService: bool = False):
        lock = Lock()
        if lock.acquire():
            _md5 = data['md5']
            self.waiting_upload_data[_md5] = data       
            self.count += 1
            
            if isService:
                if(self.bulk_add(self.waiting_upload_data)):
                        self.waiting_upload_data = {}
            else:
                if(len(self.waiting_upload_data) == self.batch_size() or 
                        self.count == total_count):
                    if(self.bulk_add(self.waiting_upload_data)):
                        self.waiting_upload_data = {}

            lock.release()
        return

        # region Update Sandbox Data
    def update_sandbox_data(self, report: dict, message: object, isEnricher: bool = True):
        try:
            self.logger.info("Trying to update sandbox data : " + message.md5)
            self.logger.info("Place to put it : enricher_data." + message.module_name)

            self.logger.info("Elastic Collection." + self.collection())
            self.logger.info("MD5: " + message.md5)
            self.client.update(index=self.collection(), error_trace=True, id=message.md5, body={'doc' : { 
                            "enricher_data" : {message.module_name : {"status": "reported", "report" : report}}, 
                            "updated_on" : datetime.now()
                            }})
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.print_exc())

    # endregion

    def bulk_add(self, data: dict = None) -> bool:
        """
        Allows for submitting bulk samples to the Elasticsearch instance/cluster.

        Parameters
        ----------
            - data: dict
                    Dictionary that contains the data that needs to be parsed and submitted to Elastic via bulk upload

        Returns
        -------
        False: failed to insert bulk data
        True: successful inserted bulk data
        """
        self.logger.debug("Pushing batch sample data")
        _bulk_data = []
        try:
            for _md5, _data in data.items():
                if(_data['es_has_value'] is True):

                    # region preparing enricher changes
                    if _data['used_enrichers'] != []:
                        if _data['used_enrichers'] != _data['old_enrichers']:
                            _enrichers = _data['used_enrichers'] + _data['old_enrichers']
                            _enricher_data = {}
                            for _used_enricher in _data['used_enrichers']:
                                _enricher_data[_used_enricher] = _data['enricher_data'][_used_enricher]

                            _bulk_data.append({
                                "_index" : self.collection(), 
                                "_id" : _md5,
                                "_op_type" : "update", 
                                "doc" : { 
                                    "used_enrichers" : _enrichers, 
                                    "enricher_data" : _enricher_data, 
                                    "updated_on" : datetime.now()
                                    }
                                })
                    # endregion

                    # region preparing parser changes
                    if _data['used_parsers'] != []:
                        if _data['used_parsers'] != _data['old_parsers']:
                            _parsers = _data['used_parsers'] + _data['old_parsers']
                            _parser_data = {}
                            for _used_parser in _data['used_parsers']:
                                _parser_data[_used_parser] = _data['parser_data'][_used_parser]

                            _bulk_data.append({
                                "_index" : self.collection(), 
                                "_id" : _md5, 
                                "_op_type" : "update", 
                                "doc" : {
                                    "used_parsers" : _parsers, 
                                    "parser_data" : _parser_data, 
                                    "updated_on" : datetime.now()
                                    }
                                })
                    # endregion
                
                else:
                    # region preparing first seen sample
                    _data['_index'] = self.collection()
                    _data['_id'] = _md5
                    # defaults to index but for clarity adding it to the dictionary
                    _data['_op_type'] = "index"

                    _data['added_on'] = datetime.now()
                    _data['updated_on'] = datetime.now()
                    
                    _data.pop('es_has_value', None)
                    _data.pop('old_parsers', None)
                    _data.pop('old_enrichers', None)

                    _bulk_data.append(_data)
                    # endregion

            bulk(self.client, _bulk_data, chunk_size=1000, request_timeout=200)
            return True
        except Exception as e:
            self.logger.error(str(e))
            return False

    def bulk_delete(self):
        raise NotImplementedError
    
    def reset(self) -> bool:
        try:
            _force = InputPrinter().input("Are you sure you want to reset Elastic? (y/N)")
            if _force:

                try:
                    if self.check_table() == False:
                        self.create_table()
                    else:
                        self.logger.info("Resetting Elastic")
                        self.client.indices.delete(index=self.collection(), ignore=[404, 404])
                        self.logger.info("Deleted Old Data")
                        self.create_table()

                    return True
                except KeyboardInterrupt as ke:
                    raise ke
                except Exception as e:
                    raise e
            else:
                return False
        except Exception as e:
            raise e

    def connect(self):
        try:
            self.client = Elasticsearch(
                    hosts=self.host(),
                    timeout=self.timeout(), 
                    max_retries=self.max_retries(), 
                    retry_on_timeout=self.retry_on_timeout()
                )
            self.client.ping()
            if self.check_table() == False:
                self.create_table()
        except Exception as e:
            print(str(e))
            raise e

        return self

    def close(self):
        self.client.close()


    def query(self, md5: str):
        """
        Checks to see if the md5 of the malware is already present in Elasticsearch

        Returns
        -------
        False: doesn't exist
        True: exists
        """
        try:
            _doc = dict(self.client.search(index=self.collection(), body={"query": {"match": {"_id": md5}}}))
            if (_doc["hits"]["total"]["value"]== 0):
                return (False,None)
            else:
                return (True, {
                    "md5" : _doc["hits"]["hits"][0]["_source"]["md5"],
                    "used_parsers" : _doc["hits"]["hits"][0]["_source"]["used_parsers"],
                    "parser_type" : _doc["hits"]["hits"][0]["_source"]["parser_type"],
                    "used_enrichers" : _doc["hits"]["hits"][0]["_source"]["used_enrichers"],
                    "file_magic" : _doc["hits"]["hits"][0]["_source"]["file_magic"], 
                    "file_magic_mime" : _doc["hits"]["hits"][0]["_source"]["file_magic_mime"]
                })
        except Exception as e:
            raise e