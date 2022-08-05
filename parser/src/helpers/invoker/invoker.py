from src.helpers import Command

class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
        to the command

    Methods
    -------
        - set_on_start(self, command: Command): None
                Set pre-execution Command
            
        - set_on_finish(self, command: Command): None
                Set post-execution Command

        - execute(self): None:
                Set main execution Command
    """

    _on_start = None
    _on_finish = None

    def set_on_start(self, command: Command):
        """
        Set pre-execution Command
        """
        self._on_start = command

    def set_on_finish(self, command: Command):
        """
        Set post-execution Command
        """
        self._on_finish = command

    def execute(self) -> None:
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        if isinstance(self._on_start, Command):
            return self._on_start.execute()

        if isinstance(self._on_finish, Command):
            return self._on_finish.execute()
