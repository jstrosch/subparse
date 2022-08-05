import logging

class CustomFileFormatter(logging.Formatter):
    """
    Custom logger formatter

    Methods
    -------
        - format(self, record): str
                Formats the record for the logger.
    """
    format = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format,
        logging.WARN: format
    }

    def format(self, record):
        """
        Formats the record given for the logger

        Parameters
        ----------
            - record: LogRecord, required
                    The log record to format.

        Returns
        -------
        String
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)