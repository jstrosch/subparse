from src.database.base.client import Client
from src.helpers.singleton import MetaClassSingleton
from .enums import DBTYPE
from .elasticsearch import ElasticsearchRepository

class Repository(metaclass=MetaClassSingleton):
    __client = None
    __dbType = None

    @property
    def dbType(self):
        return Repository.__dbType

    @dbType.setter
    def dbType(self, dbtype: DBTYPE = DBTYPE.ELASTICSEARCH):
        Repository.__dbType = dbtype

    @staticmethod
    def get_connection() -> Client:
        # return "testing connection"
        if Repository.__client == None:
            _client = None
            if Repository.dbType == DBTYPE.ELASTICSEARCH:
                Repository.__client = ElasticsearchRepository()
            else:
                print("Error")
        
        return Repository.__client
        