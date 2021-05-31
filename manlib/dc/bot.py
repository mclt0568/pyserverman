import shlex
import traceback
from typing import Callable

import discord

import manlib
from .context import Context
from .embeds import BotNametagEmbed, ErrorEmbed, ExceptionEmbed
from .handler import Handler


class Bot(discord.Client):
    def __init__(self, config: manlib.Config, logger: manlib.Logger) -> None:
        super().__init__()

        self.config = config
        self.logger = logger

        self.intention_handlers = {}

        self.default_guild = None
        self.default_channel = None

    async def initialize_default_guild_channel(self) -> None:
        # get guild
        self.default_guild = self.get_guild(self.config["bot"]["guild"])
        if self.default_guild:
            self.logger.log(f"Bound to guild: {self.default_guild}")
        else:
            self.logger.log(
                "Unable to find guild. (Wrong ID might be set in config.json)", level=manlib.LogLevelName.WARNING)

        # get channel
        channels = self.get_all_channels()
        self.default_channel = None
        for i in channels:
            if type(i) == discord.channel.TextChannel and i.id == self.config["bot"]["channel"]:
                self.default_channel = i
        if self.default_channel:
            self.logger.log(f"Bound to channel: {self.default_channel}")
        else:
            self.logger.log(
                "Unable to find channel. (Wrong ID might be set in config.json)\nAborting bounded guild.",
                level=manlib.LogLevelName.WARNING)

    def intention(self, trigger: str, require_admin: bool = True):
        def wrapper(func: Callable):
            self.register_intention(trigger, func, require_admin)

        return wrapper

    def register_intention(self, trigger: str, handler: Callable, require_admin: bool) -> None:
        self.intention_handlers[trigger] = Handler(handler, require_admin)

    async def on_ready(self):
        self.logger.log(f"Signed in as {self.user}")
        if self.config["bot"]["guild"] and self.config["bot"]["channel"]:
            await self.initialize_default_guild_channel()
        else:
            self.logger.log(
                "Default guild and channel has not set in config.json.\nIt is recommended to bind the bot to a channel",
                level=manlib.LogLevelName.WARNING)
        if self.default_channel:
            nametag = BotNametagEmbed(self)
            await nametag.init_all_fields()
            await self.default_channel.send(
                embed=nametag
            )

    async def on_error(self, event, *args, **kwargs):
        traceback_message = traceback.format_exc()
        self.logger.log(traceback_message,
                        level=manlib.LogLevelName.EXCEPTION)
        if self.default_channel:
            await self.default_channel.send(
                embed=ExceptionEmbed(
                    traceback_message.split("\n")[-2],
                    event,
                    traceback_message
                )
            )

    def is_intention(self, raw_intention: str) -> bool:
        return raw_intention[0] == "[" and raw_intention[-1] == "]" and raw_intention in self.intention_handlers

    async def on_message(self, message: discord.Message):
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
            if handler.require_admin and not admin.is_admin(message.author.id):
                await message.channel.send(
                    embed=ErrorEmbed("Permission Denied", "This action or intention requires admin privilege.",
                                     "Use [list-admins] to see a list of admins", message)
                )
                return

            await handler(Context(self, message, raw_msg_pieces[1:]))
