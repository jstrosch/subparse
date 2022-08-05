from abc import ABC, abstractmethod

class SandBox(ABC):

    @abstractmethod
    def get_job_report(self, job_id: int) -> dict:
        pass

    @abstractmethod
    def submit_report_to_elastic(self, report: dict, message: dict) -> bool:
        pass

    @abstractmethod
    def job_status(self, job_id: str) -> dict:
        pass

    @abstractmethod
    def sandbox_status(self) -> dict:
        pass
    
    @abstractmethod
    def sample_exists(self, md5: str) -> bool:
        pass

    @abstractmethod
    def submit_job(self, message: dict) -> bool:
        pass

