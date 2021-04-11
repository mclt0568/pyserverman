from typing import List
import discord
import dc


class Context:
    bot: dc.Bot
    message: discord.Message
    args: List[str]

    def __init__(self, bot: dc.Bot, message: discord.Message, args: List[str]) -> None:
        self.bot = bot
        self.message = message
        self.args = args
