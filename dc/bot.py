from typing import Callable
import dc
import discord
import traceback
import common
import shlex


class Bot(discord.Client):
    config: common.Config
    logger: common.Logger

    intention_handlers = {}

    def __init__(self, config: common.Config, logger: common.Logger):
        super().__init__()

        self.config = config
        self.logger = logger

    def intention(self, trigger: str, require_admin: bool = True) -> None:
        def wrapper(func: Callable):
            self.register_intention(trigger, func, require_admin)
        return wrapper

    def register_intention(self, trigger: str, handler: Callable, require_admin: bool):
        self.intention_handlers[trigger] = dc.Handler(handler, require_admin)

    async def on_ready(self):
        self.logger.log(f"Signed in as {self.user}")

    async def on_error(self, event, *args, **kwargs):
        self.logger.log(traceback.format_exc(),
                        level=common.LogLevelName.EXCEPTION)

    def is_intention(self, raw_intention: str):
        return raw_intention[0] == "[" and raw_intention[-1] == "]" and raw_intention in self.intention_handlers

    async def on_message(self, message: discord.Message) -> None:
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
                await message.channel.send("權限不足")
                return

            await handler(dc.Context(self, message, raw_msg_pieces))
