from abc import ABC, abstractmethod

class Client(ABC):

    @abstractmethod
    def query(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def create_table(self):
        raise NotImplementedError

    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def bulk_add(self, data: dict = None):
        raise NotImplementedError

    @abstractmethod
    def bulk_delete(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError
    
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def check_table(self):
        raise NotImplementedError

    @abstractmethod
    def threading_callback(self, data: dict, total_count: int, isService: bool):
        raise NotImplementedError

    @abstractmethod
    def update_sandbox_data(self, report: dict, message: object, isEnricher: bool = True):
        raise NotImplementedError