import configparser
import json
import os
from src.helpers.singleton.singleton_meta_class import MetaClassSingleton

class KafkaConfiguration(metaclass=MetaClassSingleton):
    """
    Kafka Configuration

    Attributes
    ----------
        - host: str
                IP/URL to be used for the cape sandbox 
        
        - port: str
                Port number to be used when communicating with cape sandbox

        - auth_token: str
                Auth token generated for api usage


    Overloaded
    ----------

        - __str__: 
            Returns the cape configuration settings in a formatted string
    """
    # def __init__(
    #     self, host: str = None, port: str = None) -> None:
    #     super().__init__()
    def __init__(self) -> None:
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "kafka_configuration.cfg"
        )
        conf.read(_path)

        self.kafka_host = conf.get("KAFKA", "host")
        self.kafka_port = conf.get("KAFKA", "port")
        self.kafka_service_security = conf.getboolean("KAFKA", "use_security")
        self.kafka_master_server = json.loads(conf.get("KAFKA_SERVERS", "master"))

        # security for services
        # consumer
        self.kafka_consumer_service_sasl_mech = conf.get("KAFA_CONSUMER_SERVICE_SECURITY", "sasl_mechanism")
        self.kafka_consumer_service_usr = conf.get("KAFA_CONSUMER_SERVICE_SECURITY", "username")
        self.kafka_consumer_service_pwd = conf.get("KAFA_CONSUMER_SERVICE_SECURITY", "password")
        self.kafka_consumer_service_proto = conf.get("KAFA_CONSUMER_SERVICE_SECURITY", "security_protocol")
        
        # producer
        self.kafka_producer_service_sasl_mech = conf.get("KAFA_PRODUCER_SERVICE_SECURITY", "sasl_mechanism")
        self.kafka_producer_service_usr = conf.get("KAFA_PRODUCER_SERVICE_SECURITY", "username")
        self.kafka_producer_service_pwd = conf.get("KAFA_PRODUCER_SERVICE_SECURITY", "password")
        self.kafka_producer_service_proto = conf.get("KAFA_PRODUCER_SERVICE_SECURITY", "security_protocol")

        # for background Remote Manager / Process
        self.kafka_process_host = str(conf.get("KAFKA_PROCESS", "host"))
        self.kafka_process_port = int(conf.get("KAFKA_PROCESS", "port"))

    def __str__(self) -> str:
        return f"Kafka Host: {self.host}, Kafka Port: {self.port}"
