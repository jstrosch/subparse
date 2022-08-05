from src.database.base.db_configuration import DBConfiguration
import configparser
import os

class ElasticsearchConfig(DBConfiguration):

    def __init__(self) -> None:
        self.conf = configparser.RawConfigParser()
        self.conf.read(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "elastic_configuration.cfg"
        ))

    def collection(self) -> str:
        return self.conf.get("ELASTICSEARCH-GENERAL", "collection")
    
    def batch_size(self) -> int:
        return int(self.conf.get("ELASTICSEARCH-GENERAL", "batch_size"))

    def timeout(self) -> int:
        return int(self.conf.get("ELASTICSEARCH-GENERAL", "timeout"))

    def retry_on_timeout(self) -> bool:
        return bool(self.conf.get("ELASTICSEARCH-GENERAL", "retry_on_timeout"))

    def max_retries(self) -> int:
        return int(self.conf.get("ELASTICSEARCH-GENERAL", "max_retries"))
    
    def host(self):
        _host = {"host": self.conf.get("CLUSTER", "host"), "port": int(self.conf.get("CLUSTER", "port")), 'scheme': self.conf.get("CLUSTER", "scheme")}
        return [_host]

    def __str__(self) -> str:
        return f"Hosts: {self.host()}, Collection: {self.collection()}, Batch Size: {self.batch_size()}"