from __future__ import annotations
from .command import Command
from abc import abstractmethod


class ServiceCommand(Command):
    """
    The Service Command interface declares a method for executing a command 
        from the Service Consumer

    Methods
    -------
        - execute(self): dict
                Abstract method that requires a concrete implementation.

        
    """

    @abstractmethod
    def service_initialize(self, message):
        pass

    @abstractmethod
    def service_processing(self, message):
        pass

    @abstractmethod
    def service_reporting(self, message):
        pass

    @abstractmethod
    def service_error(self, message):
        pass