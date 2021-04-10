import discord


def generate_error(title, description, prompt, message):
    embed = discord.Embed(
        title=f"錯誤: {title}", description=description, color=discord.Color.from_rgb(229, 115, 115))
    embed.add_field(name="提示", value=prompt, inline=False)
    embed.add_field(name="Traceback",
                    value=f"`{message.content.strip()}`", inline=False)
    return embed


def generate_success(description, targets=None):
    embed = discord.Embed(title=f"指令已完成", description=description,
                          color=discord.Color.from_rgb(129, 199, 132))
    if targets:
        embed.add_field(name="對象", value="\n".join(targets), inline=False)
    return embed
