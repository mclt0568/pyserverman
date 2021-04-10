from logger import LogLevelName


class LoggedException(Exception):
    def __init__(self, message, logger=None):
        self.message = message
        if logger:
            logger.log(message, level=LogLevelName.EXCEPTION)
        super().__init__(self.message)


class ConfigError(LoggedException):
    pass
