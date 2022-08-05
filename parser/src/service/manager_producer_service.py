from src.config import Configuration
from .base.remote_manager import RemoteManager
from src.service.commands.remote_commands import RemoteConsumerOperations

class ProducerProcessorManager(RemoteManager):
    def __init__(self, address=(Configuration().kafka_process_host, Configuration().kafka_process_port), authkey=b'secret', serializer='pickle', ctx=None) -> None:
        super().__init__(address, authkey, serializer, ctx)
        self.register('RemoteConsumerOperations')
        self.connect()
        self.commands = RemoteConsumerOperations()
