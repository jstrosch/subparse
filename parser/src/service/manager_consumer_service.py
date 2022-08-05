import json
import traceback
from time import sleep
from queue import Queue
from pydoc import locate
from threading import Thread
from kafka import KafkaConsumer
from .message import ServiceMessage
from src.config import Configuration
from .base.service import BaseService
from src.database.base.client import Client
from src.database.repository import Repository
from .base.remote_manager import RemoteManager
from src.helpers.logging import  SubParserLogger
from .commands.remote_commands import RemoteConsumerOperations

_messages = Queue()
_workers = []

class ConsumerServiceThread(Thread):
    def __init__(self, client: Client):
        Thread.__init__(self)
        self.log = SubParserLogger("CONSUMER-PROCESS", "Message-Thread")
        self.client = client

    def run(self):
        self.log.info("Processing Thread")
        while True:
            message = _messages.get()
            self.log.info("Process Message::: " + str(message))
            """
            Executes the underlying messages needs, there are four possible messages that can be handled by the service.

            Message Types:
            --------------
                - initialized
                - processing
                - reporting
                - error

            Parameters
            ----------
                - message: ConsumerRecord
                    This is the message that has been passed to Kafak (the message that we need is the ServiceMessage, 
                        which is the value of the ConsumerRecord)
            """
            try:
                self.log.info("Message record: " + str(message))

                _msg = ServiceMessage(**message.value)
                self.log.info("Type of messaage: " + str(_msg.type))
                self.log.info("Module: " + str(_msg.module_name))
                
                _obj = locate(_msg.module)
                _t = _obj(_msg.md5, _msg.sample)

                if(_msg.type == "initialized"):
                    self.log.info("Initializing...")
                    _success =  _t.service_initialize(_msg)
                    self.log.info("Finished Initializing Message : " + ("Successful" if _success == True else "Failed"))
                    return _success

                elif(_msg.type == "processing"):
                    self.log.info("Processing...")
                    _success =  _t.service_processing(_msg)
                    self.log.info("Finished Processing Message : " + ("Successful" if _success == True else "Failed"))
                    return _success

                elif(_msg.type == "reporting"):
                    self.log.info("Reporting...")
                    _success =  _t.service_reporting(_msg, self.client)
                    self.log.info("Finished Reporting Message : " + ("Successful" if _success == True else "Failed"))
                    return _success
                elif(_msg.type == "error"):
                    self.log.info("Error...")
                    _success =  _t.service_error(_msg, self.client)
                    self.log.info("ERROR Message : " + ("Successful" if _success == True else "Failed"))
                    return _success
                elif(_msg.type == "tasks"):
                    try:
                        self.log.info("Task List...")
                        _success =  _t.service_getTasks()
                        self.log.info(str(_success))
                    except Exception as e:
                        self.log.exception(str(e))
                else:
                    raise Exception("ERROR WITH MSG TYPE :: " + str(_msg.type))
                
            except Exception as e:
                self.log.error('could not log event: {}'.format(str(e)))
                self.log.exception(traceback.format_exc())

            _messages.task_done()
            self.join()

class ConsumerServiceWrapper(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.log = SubParserLogger("CONSUMER-PROCESS", "WRAPPER") 
        Repository.dbType = Configuration().databaseType
        self.client = Repository.get_connection()
        self.client.connect()
        self.consumer = KafkaConsumer(
                                    'cape',
                                    bootstrap_servers=Configuration().kafka_master_server,
                                    auto_offset_reset='earliest',
                                    enable_auto_commit=True,
                                    auto_commit_interval_ms=1000,
                                    max_poll_interval_ms=1000,
                                    group_id='subparse-consumer',
                                    value_deserializer=self._deserialize
                                )
            
    def _deserialize(self, message):
        """
        Deserializes the messages that are received from Kafka, used in the actual Kafka Consumer Obejct
            when it is initialized
        """
        return json.loads(message.decode('utf-8')) 

    def get_messages(self):
        for message in self.consumer:
            self.log.info("Message: " + str(message))
            self.log.debug("Processing Message")
            _messages.put(message)
            self._create_thread()

    def _create_thread(self):
        self.log.info("Checking Count: " + str(_messages.qsize()))
        worker = ConsumerServiceThread(self.client)
        worker.setDaemon(True)
        worker.start()
        _workers.append(worker)
    
    def run(self):
        while True:
            self.get_messages()
            sleep(1)
            self.log.info("Checking again for messages")

class ConsumerProcessorService(BaseService):
    def __init__(self):
        super().__init__(
            name="subparse-consumer-service", pid_dir="/tmp/subparse/",
            subparselogname="CONSUMER-SERVICE")

        self.log = SubParserLogger("CONSUMER-PROCESS", "MAIN") 
        

    def run(self):
        try:
            self.log.info("Starting Consumer Manager....")
            RemoteManager.register('RemoteConsumerOperations', RemoteConsumerOperations)
            manager = RemoteManager(address=(Configuration().kafka_process_host, Configuration().kafka_process_port), authkey=b'secret')
            self.log.info("Trying to create thread for consumer..")
            wrapper = ConsumerServiceWrapper()
            wrapper.setDaemon(True)
            wrapper.start()
            self.log.info("Wrapper PID: " + str(wrapper.native_id))
            manager.get_server().serve_forever()
        except Exception as e:
            self.log.exception(e)

