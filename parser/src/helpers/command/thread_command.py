from .command import Command
from abc import abstractmethod

class ThreadCommand(Command):

    """
    The Thread Command interface declares a method for executing a command 
        from the Thread Invoker

    Methods
    -------
        - execute(self): dict
                Abstract method that requires a concrete implementation.

        
    """
    def information(self) -> dict:
        raise Exception("[THREADING-COMMAND] INFORMATION METHOD NOT IMPLEMENTED")
