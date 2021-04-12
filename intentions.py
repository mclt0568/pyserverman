from constants import *
import dc
import discord
import io

@bot.intention("[add-admin]")
async def add_admin(ctx: dc.Context):
    """Add user(s) to the admin list"""
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
        embed=dc.CommandSuccessListEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names,
            list_title="User(s) added:"
        )
    )


@bot.intention("[remove-admin]")
async def remove_admin(ctx: dc.Context):
    """Remove user(s) from the admin list"""
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
        embed=dc.CommandSuccessListEmbed(
            "Successfuly added user(s) to admin group",
            targets=user_names,
            list_title="User(s) removed:"
        )
    )


@bot.intention("[get-user-id]", require_admin=False)
async def get_user_id(ctx: dc.Context):
    """Retrieve the user id for user(s)"""
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
        embed=dc.CommandSuccessDictEmbed(
            description="",
            targets=username_id_s,
        )
    )


@bot.intention("[list-admins]", require_admin=False)
async def list_admins(ctx: dc.Context):
    """Retrieve list of admins"""
    admin_ids = [int(i) for i in ctx.bot.config["admins"]]

    if not admin_ids:
        await ctx.message.channel.send(
            # embed=dc.CommandSuccessEmbed(
            #     title="The admin list is empty.",
            #     description="\nPlease add at least 1 user's user ID in config.json as the first admin.\nID should be in string."
            # )
            embed=dc.InformationListEmbed(
                title="The admin list is empty",
                description="Please add at least 1 user's user ID in config.json as the first admin.\nID should be in string."
            )
        )
        return

    admin_names = []
    for i in admin_ids:
        admin = await ctx.bot.fetch_user(int(i))
        admin_names.append(admin.name)

    await ctx.message.channel.send(
        embed=dc.InformationListEmbed(
            title="",
            description="",
            list_title="List of admins",
            targets=admin_names,
        )
    )


@bot.intention("[list-servers]")
async def list_servers(ctx: dc.Context):
    """List all server(s)"""
    server_dicts = config["servers"]
    server_names = []
    for server_dict in server_dicts:
        server_names.append(server_dict["name"])
    server_objects = {}
    for server_name in server_names:
        temp_server = None
        for server in servers:
            if server.name == server_name:
                temp_server = server
        server_objects[server_name] = temp_server
    messages = [
        f"[{'Running' if j.is_running() else 'Idel'}] "+str(i)
        for i, j in server_objects.items()
    ]
    await ctx.message.channel.send(
        embed=dc.InformationListEmbed(
            title="Query result(s)",
            description="",
            list_title="List of server(s):",
            targets=messages
        )
    )


@bot.intention("[help]", require_admin=False)
async def command_help(ctx: dc.Context):
    """Show help message"""
    embed = dc.GeneralInformationEmbed(
        "Intentions' Help", "Type `[intention_name] arg_1 arg_2 ... arg_n` to execute an intention"
    )
    for intention_name, intention_handler in ctx.bot.intention_handlers.items():
        embed.add_field(name=intention_name,
                        value=intention_handler.func.__doc__, inline=False)
    await ctx.message.channel.send(
        embed=embed
    )

@bot.intention("[dump-log]", require_admin=True)
async def dump_log(ctx:dc.Context):
    """Dump the log of this bot as a file, and upload it to the text channel"""
    data = ctx.bot.logger.read_file_as_string()
    await ctx.message.channel.send(
        file=discord.File(
            fp = io.StringIO(data),
            filename="Log.txt"
        )
    )

@bot.intention("[run-command]")
async def run_command(ctx: dc.Context):
    """Run command on target server"""
    if len(ctx.args) < 2:
        await ctx.message.channel.send(
            embed=dc.ErrorEmbed(
                "Argument Error",
                "Missing arguments",
                "Syntax: [run-command] <server_name> <command>",
                ctx.message
            )
        )
        return

    server_name = ctx.args[0]

    command_args = ctx.args[1:]

    for server in servers:
        if server_name == server.name:
            server.run_command(" ".join(command_args))

    await ctx.message.channel.send(embed=dc.CommandSuccessEmbed("", ""))
