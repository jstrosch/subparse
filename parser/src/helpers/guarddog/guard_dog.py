from watchdog.events import PatternMatchingEventHandler
from src.main.main import Main

class GuardDogHandler(PatternMatchingEventHandler):
    """
    Gaurd Dog Handler for watching the sample directory that was given when the program is in service mode

    Attributes
    ----------
        - callback: null
                Function to execute when an event is triggered.
        
        - logger: Logger
                Logger Object that was passed to be used for output to console and file for events.

        - config: 
                Configuration Object that will be used for the instance

    Methods
    -------
        - on_created(event): null
                Executes the callback when an event is triggered.
    """
    def __init__(self, callback, main: Main):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=['*'],
                                                             ignore_directories=True, case_sensitive=False)
        self.callback = callback
        self.main = main
  
    def on_created(self, event):
        """
        Executes the callback when an event is triggered

        Parameters
        ----------
            - event: PatternMatchingEventHandler
                    Event that is being triggered
        
        Returns
        -------
        None
        """
        self.callback(event.src_path, self.main)