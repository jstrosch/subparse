

class ServiceMessage(object):
    """
    Service Message 

    This is used as the message to interact between the background services and Kafka, 
        the Kafka ConsumerRecords value will contain the ServiceMessage which the Consumer Service
        will then be able to use for execution.
    """

    def __init__(self, topic: str, md5: str, 
        sample: str, type: str, first_seen: int = None, last_seen: int = None, 
        module: str = "", module_name: str = "", job_id: int = None) -> None:

        """
        Constructor for the ServiceMessage

        Parameters
        -----------
            - topic: str
                topic that the message is meant for with Kafka

            - md5: str
                md5 of the sample that is/was submitted
            
            - sample: str
                path to the sample that is/was submitted 

            - type: str
                message type to be used (ie: initialized, reporting, etc)

            - first_seen: int
                epoch time of when the first time this sample was submitted in the messaging system
            
            - last_seen: int
                epoch time of when the most recent message was sent

            - module: str
                the module class path that is to be used for processing 

            - module_name: str
                the name of the module that is to be used

            - job_id: int
                the job id that was created when submitted to CAPE V2
        """

        self.topic = topic
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.md5 = md5
        self.sample = sample
        self.type = type
        self.module = module
        self.module_name = module_name
        self.job_id = job_id
    
    def __str__(self) -> str:
        return "Last Seen: {} Job ID: {} Topic: {} MD5: {} Type: {} Module: {} Module Name: {}".format(self.last_seen, self.job_id, self.topic, self.md5, self.type, self.module, self.module_name)