from global_modules import *
import discord
import traceback

from discord.channel import CategoryChannel


class DiscordWrapper(discord.Client):
    intentions = {}

    def register_intentions(self, trigger):
        def wrapper(function):
            self.intentions[trigger] = function
            return function
        return wrapper

    async def on_ready(self):
        logger.log(f"Signed in as {self.user}")

    async def on_error(self, event, *args, **kwargs):
        logger.log(traceback.format_exc(), logtype="exception")

    def is_intention(self, raw_intention: str):
        return raw_intention[0] == "[" and raw_intention[-1] == "]" and raw_intention in self.intentions

    async def on_message(self, message):
        raw_msg = message.content
        msg = raw_msg.strip().lower()
        if not msg:
            return

        msg_pieces = msg.split(" ")

        if self.is_intention(msg_pieces[0]):
            if message.author.id not in configs.current_config["default_admins"]:
                await message.channel.send("權限不足")
                return

            logger.log(
                f"{message.author.name}#{message.author.discriminator} is trying to execute the following intention: {msg_pieces[0]}")
            logger.log(f"Original message goes like:")
            logger.log(f"\t{message.content}")

            await self.intentions[msg_pieces[0]](self, message, raw_msg.split(" ")[1:])
