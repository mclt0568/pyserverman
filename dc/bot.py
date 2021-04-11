from common.logging import LogLevel, LogLevelName
from typing import Callable
from dc import embeds
import asyncio
import dc
import discord
import traceback
import common
import shlex


class Bot(discord.Client):
    config: common.Config
    logger: common.Logger

    intention_handlers = {}

    default_guild: discord.Guild
    default_channel: discord.TextChannel

    def __init__(self, config: common.Config, logger: common.Logger):
        super().__init__()

        self.config = config
        self.logger = logger

        self.default_guild = None
        self.default_channel = None
    async def initialize_default_guild_channel(self):
        #get guild
        self.default_guild = self.get_guild(self.config["bot"]["guild"])
        if self.default_guild:
            self.logger.log(f"Bound to guild: {self.default_guild}")
        else:
            self.logger.log("Unable to find guild. (Wrong ID might be set in config.json)",level=LogLevelName.WARNING)

        #get channel
        channels = self.get_all_channels()
        self.default_channel = None
        for i in channels:
            if type(i) == discord.channel.TextChannel and i.id == self.config["bot"]["channel"]:
                self.default_channel = i
        if self.default_channel:
            self.logger.log(f"Bound to channel: {self.default_channel}")
        else:
            self.logger.log("Unable to find channel. (Wrong ID might be set in config.json)\nAborting bounded guild.",level=LogLevelName.WARNING)

    def intention(self, trigger: str, require_admin: bool = True) -> None:
        def wrapper(func: Callable):
            self.register_intention(trigger, func, require_admin)
        return wrapper

    def register_intention(self, trigger: str, handler: Callable, require_admin: bool):
        self.intention_handlers[trigger] = dc.Handler(handler, require_admin)

    async def on_ready(self):
        self.logger.log(f"Signed in as {self.user}")
        if self.config["bot"]["guild"] and self.config["bot"]["channel"]:
            await self.initialize_default_guild_channel()
        else:
            self.logger.log("Default guild and channel has not set in config.json.\nIt is recommended to bind the bot to a channel", level=LogLevelName.WARNING)
        if self.default_channel:
            await self.default_channel.send(
                embed=embeds.EmptySuccessEmbed("伺服娘登場",f"成功登入爲 {self.user}")
            )

    async def on_error(self, event, *args, **kwargs):
        traceback_message = traceback.format_exc()
        self.logger.log(traceback_message,
                        level=common.LogLevelName.EXCEPTION)
        print(traceback_message.split("\n"))
        if self.default_channel:
            await self.default_channel.send(
                embed=embeds.ExceptionEmbed(
                    traceback_message.split("\n")[-2],
                    event,
                    traceback_message
                )
            )

    def is_intention(self, raw_intention: str):
        return raw_intention[0] == "[" and raw_intention[-1] == "]" and raw_intention in self.intention_handlers

    async def on_message(self, message: discord.Message) -> None:
        if self.default_channel and message.channel.id != self.default_channel.id:
            return
        raw_msg = message.content.strip()
        if not raw_msg:
            return
        msg = raw_msg.lower()
        raw_msg_pieces = shlex.split(raw_msg)
        msg_pieces = shlex.split(msg)

        if self.is_intention(msg_pieces[0]):
            self.logger.log(
                f"{message.author.name}#{message.author.discriminator} executed: {raw_msg}")

            handler = self.intention_handlers[msg_pieces[0]]
            if handler.require_admin and str(message.author.id) not in self.config["admins"]:
                await message.channel.send(
                    embed=embeds.ErrorEmbed("Permission Denied","This action or intention requires admin privilege.","Use [list-admins] to see a list of admins",message)
                )
                return

            await handler(dc.Context(self, message, raw_msg_pieces))
