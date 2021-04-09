from global_modules import *
import discord
import traceback

from discord.channel import CategoryChannel

class DiscordWrapper(discord.Client):
	intentions = {}

	def register_intentions(self,trigger):
		def wrapper(function):
			self.intentions[trigger] = function
			return function
		return wrapper

	async def on_ready(self):
		logger.log(f"Signed in as {self.user}")
	async def on_error(self,event,*args,**kwargs):
		logger.log(traceback.format_exc(),logtype="exception")
	async def on_message(self,message):
		content = message.content.strip().lower()
		if content in self.intentions:
			await self.intentions[content](self,message)