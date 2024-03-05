# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import logging

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.datetime.functions.dtnow import dtnow_utc
from core.log.classes.log import Log
from core.log.classes.log_collection import LogCollection
from core.log.exceptions import InvalidLogLevelError


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOGGER
# └─────────────────────────────────────────────────────────────────────────────────────


class Logger:
    """An logger utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of key
    key: str

    # Declare type of log level
    log_level: int | None

    # Declare type of log format
    log_format: str | None

    # Declare type of log limit
    log_limit: int | None

    # Declare type of logs by key
    _logs_by_key: dict[str | None, LogCollection]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        key: str,
        log_level: int | None = None,
        log_format: str | None = None,
        log_limit: int | None = None,
    ) -> None:
        """Init Method"""

        # Check if log level is invalid
        if log_level is not None and log_level not in logging._levelToName:
            # Raise InvaidLogLevelError
            raise InvalidLogLevelError(log_level)

        # Set key
        self.key = key

        # Set log level
        self.log_level = log_level

        # Get log format
        log_format = (
            log_format or "%(asctime)s | %(levelname)7s | %(name)s | %(message)s"
        )

        # Set log format
        self.log_format = log_format

        # Set log limit
        self.log_limit = log_limit

        # Initialize and set logger
        self._logger = logging.getLogger(key)

        # Disable logger propogation to root logger
        self._logger.propagate = False

        # Initialize handler
        handler = logging.StreamHandler()

        # Check if log log level is not None
        if log_level is not None:
            # Set log log level
            handler.setLevel(log_level)

        # Initialize and add formatter
        handler.setFormatter(logging.Formatter(log_format))

        # Add handler to logger
        self._logger.addHandler(handler)

        # Initialize logs by key
        self._logs_by_key = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD LOG FILE
    # └─────────────────────────────────────────────────────────────────────────────────

    def add_log_file(
        self,
        file_path: str,
        log_level: int | None = None,
        log_format: str | None = None,
    ) -> None:
        """Adds a log file to the logger"""

        # Initialize handler
        handler = logging.FileHandler(file_path)

        # Get log level
        log_level = log_level if log_level is not None else self.log_level

        # Check if log log level is not None
        if log_level is not None:
            # Set log log level
            handler.setLevel(log_level)

        # Get log format
        log_format = log_format if log_format is not None else self.log_format

        # Check if log format is not None
        if log_format is not None:
            # Initialize and add formatter
            handler.setFormatter(logging.Formatter(log_format))

        # Set log file handler
        self._logger.addHandler(handler)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CRITICAL
    # └─────────────────────────────────────────────────────────────────────────────────

    def critical(
        self,
        message: str,
        key: str | None = None,
        exception: Exception | None = None,
    ) -> bool:
        """Prints and stores a critical message"""

        # Log message
        return self.log(
            message=message, level=logging.CRITICAL, key=key, exception=exception
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DEBUG
    # └─────────────────────────────────────────────────────────────────────────────────

    def debug(self, message: str, key: str | None = None) -> bool:
        """Prints and stores a debug message"""

        # Log message
        return self.log(message=message, level=logging.DEBUG, key=key)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ERROR
    # └─────────────────────────────────────────────────────────────────────────────────

    def error(
        self,
        message: str,
        key: str | None = None,
        exception: Exception | None = None,
    ) -> bool:
        """Prints and stores a error message"""

        # Log message
        return self.log(
            message=message, level=logging.ERROR, key=key, exception=exception
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INFO
    # └─────────────────────────────────────────────────────────────────────────────────

    def info(self, message: str, key: str | None = None) -> bool:
        """Prints and stores a info message"""

        # Log message
        return self.log(message=message, level=logging.INFO, key=key)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOG
    # └─────────────────────────────────────────────────────────────────────────────────

    def log(
        self,
        message: str,
        level: int,
        key: str | None = None,
        exception: Exception | None = None,
    ) -> bool:
        """Prints and stores a log message"""

        # Define log functions
        log_funcs = {
            logging.DEBUG: self._logger.debug,
            logging.INFO: self._logger.info,
            logging.WARN: self._logger.warn,
            logging.WARNING: self._logger.warning,
            logging.ERROR: self._logger.error,
            logging.CRITICAL: self._logger.critical,
        }

        # Check if log level is invalid
        if level not in log_funcs:
            # Raise InvaidLogLevelError
            raise InvalidLogLevelError(level)

        # Get log function
        log_func = log_funcs[level]

        # Get timestamp
        timestamp = dtnow_utc()

        # Log message
        log_func(message)

        # Initialize Log instance
        log = Log(
            key=key,
            timestamp=timestamp,
            message=message,
            level=level,
            exception=exception,
        )

        # Get logs
        logs = self._logs_by_key.setdefault(key, LogCollection(size=self.log_limit))

        # Add log to logs
        logs.add(log)

        # Return True
        return True

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ UPDATE LOG LIMIT BY KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def update_log_limit_by_key(self, key: str | None, limit: int | None) -> None:
        """Updates a log collection size by key"""

        # Check if key in logs by key
        if key in self._logs_by_key:
            # Update size
            self._logs_by_key[key].update_size(size=limit)

        # Otherwise create new log collection
        else:
            self._logs_by_key[key] = LogCollection(size=limit)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ WARN
    # └─────────────────────────────────────────────────────────────────────────────────

    def warn(self, message: str, key: str | None = None) -> bool:
        """Prints and stores a warn message"""

        # Log message
        return self.log(message=message, level=logging.WARNING, key=key)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ WARNING
    # └─────────────────────────────────────────────────────────────────────────────────

    def warning(self, message: str, key: str | None = None) -> bool:
        """Prints and stores a warning message"""

        # Log message
        return self.log(message=message, level=logging.WARNING, key=key)
