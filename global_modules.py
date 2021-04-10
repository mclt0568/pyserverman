import config_controls as c
import logger as l

logger = l.logger()
configs = c.ConfigControls()
configs.read_configs()

import discord_wrapper as d
discord_client = d.DiscordWrapper()