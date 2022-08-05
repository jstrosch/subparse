import logging
from ..colors import SubPaserColors
class CustomConsoleFormatter(logging.Formatter):
    """
    Custom logger formatter

    Methods
    -------
        - format(self, record): str
                Formats the record for the logger.
    """
    format = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"

    FORMATS = {
        logging.DEBUG: SubPaserColors.GREEN + format + SubPaserColors.RESET,
        logging.INFO: SubPaserColors.BLUE + format + SubPaserColors.RESET,
        logging.WARNING: SubPaserColors.YELLOW + format + SubPaserColors.RESET,
        logging.WARN: SubPaserColors.YELLOW + format + SubPaserColors.RESET,
        logging.ERROR: SubPaserColors.RED + format + SubPaserColors.RESET,
        logging.CRITICAL: SubPaserColors.RED + format + SubPaserColors.RESET
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
