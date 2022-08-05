import configparser
import os
from src.helpers.singleton.singleton_meta_class import MetaClassSingleton

class CapeConfiguration(metaclass=MetaClassSingleton):

    """
    Cape Sandbox Configuration

    Attributes
    ----------
        - host: str
                IP/URL to be used for the cape sandbox 
        
        - port: str
                Port number to be used when communicating with cape sandbox

        - topic: str
                Kafka topic to be used by the producer/consumer

        - auth_token: str
                Auth token generated for api usage


    Overloaded
    ----------

        - __str__: 
            Returns the cape configuration settings in a formatted string
    """
    def __init__(self) -> None:
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "cape_configuration.cfg"
        )
        conf.read(_path)

        self.cape_host = conf.get("CAPE", "host")
        self.cape_port = conf.get("CAPE", "port")
        self.cape_topic = conf.get("CAPE", "topic")
        self.cape_token = conf.get("CAPE", "auth_token")
        self.cape_timeout = conf.get("CAPE", "timeout")
        self.cape_priority =  conf.get("CAPE", "priority")
        self.cape_memory =  conf.get("CAPE", "memory")
        self.cape_enforce_timeout =  conf.get("CAPE", "enforce_timeout")

        self.cape_onstart = dict(conf.items("ONSTART"))

    def __str__(self) -> str:
        return f"Host: {self.cape_host}, Port: {self.cape_port}, Topic: {self.cape_topic}, Token: {'Present' if self.cape_token != None else 'Missing' }"