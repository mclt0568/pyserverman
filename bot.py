from constants import *
import dc
import common

@bot.intention("[add-admin]")
async def add_admin(ctx: dc.Context):
    if not ctx.message.mentions:
        await ctx.message.channel.send(
            embed=common.ErrorEmbed(
                "Argument Error",
                "No mantions found.",
                "Syntax: [add-admin] @user_1 @user_2 .. @user_n",
                ctx.message
            )
        )
        return
    user_names = [i.name for i in ctx.message.mentions]
    for user in ctx.message.mentions:
        config.add_admin(user.id)
    await ctx.message.channel.send(
        embed=common.SuccessEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names
        )
    )


@bot.intention("[remove-admin]")
async def remove_admin(ctx: dc.Context):
    if not ctx.message.mentions:
        await ctx.message.channel.send(
            embed=common.ErrorEmbed(
                "Argument Error",
                "No mantions found.",
                "Syntax: [remove-admin] @user_1 @user_2 .. @user_n",
                ctx.message
            )
        )
        return
    user_names = [i.name for i in ctx.message.mentions]
    for user in ctx.message.mentions:
        config.remove_admin(user.id)
    await ctx.message.channel.send(
        embed=common.SuccessEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names
        )
    )


def start(token: str):
    bot.run(token)
