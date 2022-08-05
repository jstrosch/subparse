from abc import ABC, abstractmethod

class DBConfiguration(ABC):

    @abstractmethod
    def collection(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def batch_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def timeout(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def max_retries(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def retry_on_timeout(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def host(self):
        raise NotImplementedError