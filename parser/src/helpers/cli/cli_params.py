class CLI_Params(object):
    """
    CLI Parameters Object - Used for easier calling of arguments later when passed via terminal

    Attributes
    ----------  
        - reset: bool
                Reset flag passed. Signals reset of DB(s)

        - samples_dir: str
                Samples directory location. Used for sample parsing only. 

        - parsers: list
                List of parsers to be used. Passed from terminal via Comma Seperated List on parameter

        - enrichers: list 
                List of enrichers to be used. Passed from terminal via Comma Seperated List on parameter
                
        - update_enrichers: boolean
                Update/Re-execute Enrichers that have been ran on the samples

    Overloads
    ---------
        - __str__: 
                Returns a formatted string of the CLI Attributes

    """
    def __init__(
        self, reset: bool = False, enrichers: str = "", 
            samples_dir: str = "", verbose: bool = False, 
            watchdog: bool = False, update_enrichers: bool = False, isService: bool = False
    ) -> None:
        super().__init__()

        self.reset = reset
        self.samples_dir = samples_dir
        self.isService = isService
        
        try:
            if enrichers == None or len(enrichers) == 0:
                self.enrichers = []
            else:
                _ = enrichers.split(",")
                self.enrichers = [x.strip() for x in _]
        except Exception as e:
            self.enrichers = [enrichers]


        try:
            if verbose == None:
                self.verbose = False
            elif str(verbose).lower() == "true":
                self.verbose = True
            else: 
                self.verbose = False
        except Exception as e:
            self.verbose = False

        self.watchdog = watchdog
        self.update_enrichers = update_enrichers
        

    def __str__(self) -> str:
        return (
            f"Reset: {self.reset}, Enrichers: {self.enrichers}, Update Enrichers: {self.update_enrichers}, SamplesDir: {self.samples_dir}, Verbose: {self.verbose}, Watchdog: {self.watchdog}"
        )
