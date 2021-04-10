import config_controls as c
import logger as l
import discord_wrapper as d

logger = l.logger()
configs = c.ConfigControls()
configs.read_configs()
discord_client = d.DiscordWrapper()