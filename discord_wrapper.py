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

    async def on_message(self, message):
        content = message.content.strip().lower()
        if not content:
            return
        if content[0] == "[" and content.split(" ")[0][-1] == "]" and content.split(" ")[0] in self.intentions:
            if message.author.id not in configs.current_config["default_admins"]:
                await message.channel.send("權限不足")
                return
            logger.log(
                f"{message.author.name}#{message.author.discriminator} is trying to execute the following intention: {content.split(' ')[0]}")
            logger.log(f"Original message goes like:")
            logger.log(f"\t{message.content}")
            await self.intentions[content.split(" ")[0]](self, message, message.content.split(" ")[1:])
