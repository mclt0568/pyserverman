from constants import *
import dc


@bot.intention("[add-admin]")
async def add_admin(ctx: dc.Context):
    if not ctx.message.mentions:
        await ctx.message.channel.send(
            embed=dc.ErrorEmbed(
                "Argument Error",
                "No mantions found.",
                "Syntax: [add-admin] @user_1 @user_2 .. @user_n",
                ctx.message
            )
        )
        return
    user_names = [i.name for i in ctx.message.mentions]
    for user in ctx.message.mentions:
        config.add_admin(str(user.id))
    await ctx.message.channel.send(
        embed=dc.SuccessEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names
        )
    )


@bot.intention("[remove-admin]")
async def remove_admin(ctx: dc.Context):
    if not ctx.message.mentions:
        await ctx.message.channel.send(
            embed=dc.ErrorEmbed(
                "Argument Error",
                "No mantions found.",
                "Syntax: [remove-admin] @user_1 @user_2 .. @user_n",
                ctx.message
            )
        )
        return
    user_names = [i.name for i in ctx.message.mentions]
    for user in ctx.message.mentions:
        config.remove_admin(str(user.id))
    await ctx.message.channel.send(
        embed=dc.SuccessEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names
        )
    )


@bot.intention("[get-user-id]", require_admin=False)
async def get_user_id(ctx: dc.Context):
    if not ctx.message.mentions:
        await ctx.message.channel.send(
            embed=dc.ErrorEmbed(
                "Argument Error",
                "No mantions found.",
                "Syntax: [get-user-id] @user_1 @user_2 .. @user_n",
                ctx.message
            )
        )
        return

    username_id_s = {}

    for user in ctx.message.mentions:
        username_id_s[user.name] = str(user.id)

    await ctx.message.channel.send(
        embed=dc.DictEmbed(username_id_s)
    )
