import common


class LoggedException(Exception):
    def __init__(self, message, logger=None):
        self.message = message
        if logger:
            logger.log(message, level=common.LogLevelName.EXCEPTION)
        super().__init__(self.message)


class ConfigError(LoggedException):
    pass
