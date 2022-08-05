import json
from kafka import KafkaProducer
from kafka.producer.future import FutureRecordMetadata
from src.helpers.logging import SubParserLogger
from src.config.configuration import Configuration
from src.service.message import ServiceMessage 

class RemoteConsumerOperations(object):
    def __init__(self) -> None:
        self.producer = KafkaProducer(bootstrap_servers=Configuration().kafka_master_server, 
                                        value_serializer=self._serializer)
        self.log = SubParserLogger("PRODUCER-PROCESS", "SERVICE")

    def _serializer(self, message: ServiceMessage):
        return json.dumps(message.__dict__).encode('utf-8')

    def submit_message(self, msg) -> FutureRecordMetadata:
        self.log.debug("Trying to submit message to kafka")
        self.log.debug("Msg: " + str(msg))
        try:
            self.producer.send(topic=msg.topic, value=msg).add_callback(self.on_send_success).add_errback(self.on_send_error)
            return True
        except Exception as e:
            self.on_send_error("There was an error running submitting to kafka: " + str(e))
            raise Exception("There was an error running submitting to kafka: " + str(e))

    # region Submit Message On Send Success
    def on_send_success(self, record_metadata):
        """
        On successful send, the topic, partition, and serialized_key_size are all logged,
            better to have to much then not enough information with messaging systems.

        Parameter
        ---------
            - record_metadata:
                Kafka metadata from the successful submittion 
        """
        try:
            self.log.info(
                "Successfully Added To Kafka : (Topic) : " + 
                str(record_metadata.topic) + 
                " (Offset) : " + str(record_metadata.offset) +
                " (Partition) : " + 
                str(record_metadata.partition) + 
                " (Seri_Key) : " +
                str(record_metadata.serialized_key_size))
        except Exception as e:
            self.log.error(str(e))
    # endregion

    # region Submit Message On Send Error
    def on_send_error(self, excp):
        """
        If there is an error sending a message to Kafka, the error is logged. 
        """
        self.log.error(str(excp))
    # endregion
