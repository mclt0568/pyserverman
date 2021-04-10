from re import T
from global_modules import *
import generate_embeds
import discord

@discord_client.register_intentions("[add-admin]")
async def add_admin(client: discord.Client, message: discord.Message, args:str):
	if not message.mentions:
		await message.channel.send(
			embed=generate_embeds.generate_error(
				"Argument Error",
				"No mantions found.",
				"Syntax: [add-admin] @user_1 @user_2 .. @user_n",
				message
			)
		)
		return
	user_names = [i.name for i in message.mentions]
	for user in message.mentions:
		configs.add_admin(user.id)
	await message.channel.send(
		embed=generate_embeds.generate_success(
			"Successfuly added user(s) to admin group",
			targets=user_names
		)
	)
