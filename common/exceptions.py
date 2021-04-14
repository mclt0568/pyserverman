from typing import Any
from .logging import Logger, LogLevelName


class LoggedException(Exception):
    def __init__(self, message: Any, logger: Logger=None):
        self.message = message
        if logger:
            logger.log(message, level=LogLevelName.EXCEPTION)
        super().__init__(self.message)


class ConfigError(LoggedException):
    pass
