from __future__ import annotations
from abc import ABC, abstractmethod

class Command(ABC):
    """
    The Command interface declares a method for executing a command.

    Methods
    -------
        - execute(self): dict
                Abstract method that requires a concrete implementation.
    """

    @abstractmethod
    def execute(self) -> dict:
        """
        Abstract method to implement. Used by the invoker pattern.

        Returns
        -------
        Dictionary
        """
        pass

    @abstractmethod
    def information(self) -> dict:
        """
        Compatiblity information

        Returns
        -------
        Dictionary
        """
        pass
