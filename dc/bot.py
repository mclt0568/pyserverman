from typing import Callable, Dict
import discord
import traceback
import common
import dc


class Bot(discord.Client):
    intentions: Dict[str, Callable] = {}

    def __init__(self, config: common.Config, logger: common.Logger):
        super().__init__()

        self.config = config
        self.logger = logger

    def intention(self, trigger: str) -> None:
        def wrapper(func: Callable):
            self.register_intention(trigger, func)
        return wrapper

    def register_intention(self, trigger: str, handler: Callable):
        self.intentions[trigger] = handler

    async def on_ready(self):
        self.logger.log(f"Signed in as {self.user}")

    async def on_error(self, event, *args, **kwargs):
        self.logger.log(traceback.format_exc(),
                        level=common.LogLevelName.EXCEPTION)

    def is_intention(self, raw_intention: str):
        return raw_intention[0] == "[" and raw_intention[-1] == "]" and raw_intention in self.intentions

    async def on_message(self, message: discord.Message) -> None:
        raw_msg = message.content.strip()
        if not raw_msg:
            return
        msg = raw_msg.lower()

        raw_msg_pieces = raw_msg.split(" ")
        msg_pieces = msg.split(" ")

        if self.is_intention(msg_pieces[0]):
            self.logger.log(
                f"{message.author.name}#{message.author.discriminator} executed: {raw_msg}")

            if message.author.id not in self.config["admins"]:
                await message.channel.send("權限不足")
                return

            await self.intentions[msg_pieces[0]](dc.Context(self, message, raw_msg_pieces))
