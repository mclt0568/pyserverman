import common

config = common.Config()
logger = common.Logger()

bot = common.DiscordWrapper(config, logger)
