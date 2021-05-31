from typing import List

import discord

from .bot import Bot


class Context:
    def __init__(self, bot: Bot, message: discord.Message, args: List[str]) -> None:
        self.bot = bot
        self.message = message
        self.args = args
