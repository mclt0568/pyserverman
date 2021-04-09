class LoggedExceptions(Exception):
	def __init__(self,message, logger=None):
		self.message = message
		if logger:
			logger.log(message, logtype="error")
		super().__init__(self.message)

class ConfigError(LoggedExceptions):
	pass