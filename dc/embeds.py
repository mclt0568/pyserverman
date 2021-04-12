from typing import Dict, List
from discord.enums import _is_descriptor
import discord
import datetime

class GeneralErrorEmbed(discord.Embed):
    def __init__(self,title,description):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.from_rgb(229, 115, 115)
        )

        self.set_author(name="Title Name", icon_url="https://i.imgur.com/2P3wrqJ.png")

class ErrorEmbed(GeneralErrorEmbed):
    def __init__(self, title: str, description: str, prompt: str, message: discord.Message) -> None:
        super().__init__(
            title=title,
            description=description,
        )

        self.add_field(
            name="Prompt",
            value=prompt,
            inline=False
        )
        self.add_field(
            name="Traceback",
            value=f"`{message.content.strip()}`",
            inline=False
        )

        self._author["name"] = "An user error has occurred:"

class ExceptionEmbed(GeneralErrorEmbed):
    def __init__(self, exception_name: str, event: str, full_traceback: str) -> None:
        super().__init__(
            title=f"{exception_name}",
            description=f"Unexpected Exception has occurred during {event}\nPlease report this to the admin with the traceback.",
        )
        self.add_field(
            name="Full Traceback",
            value=f"```{full_traceback}```",
            inline=False
        )

        self._author["name"] = "An unexpected exception has occurred (Fatal):"

class EmptySuccessEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            color=discord.Color.from_rgb(129, 199, 132),
            description=description
        )
        self.set_author(name="Command Executed Successfuly", icon_url="https://i.imgur.com/V02otDl.png")

class SuccessEmbed(discord.Embed):
    def __init__(self, description: str, targets: List[str] = None) -> None:
        super().__init__(
            title=f"Command Result(s)",
            description=description,
            color=discord.Color.from_rgb(129, 199, 132)
        )

        self.set_author(name="Command Executed Successfuly", icon_url="https://i.imgur.com/V02otDl.png")

        if targets:
            self.add_field(
                name="Objects",
                value="\n".join(targets),
                inline=False
            )


class DictEmbed(discord.Embed):
    def __init__(self, dict: Dict[str, str]):
        super().__init__(
            title=f"Command Result(s)",
            color=discord.Color.from_rgb(129, 199, 132)
        )

        self.set_author(name="Command Executed Successfuly", icon_url="https://i.imgur.com/V02otDl.png")

        for key, value in dict.items():
            self.add_field(
                name=key,
                value=value,
                inline=False
            )


class StringEmbed(discord.Embed):
    def __init__(self, string):
        super().__init__(
            title=f"Command Result(s)",
            color=discord.Color.from_rgb(129, 199, 132),
            description=string
        )

        self.set_author(name="Command Executed Successfuly", icon_url="https://i.imgur.com/V02otDl.png")


class ListEmbed(discord.Embed):
    def __init__(self, name: str, list: List[str]):
        super().__init__(
            title="Command Result(s)",
            color=discord.Color.from_rgb(129, 199, 132)
        )

        self.add_field(
            name=name,
            value="\n".join(list)
        )

        self.set_author(name="Command Executed Successfuly", icon_url="https://i.imgur.com/V02otDl.png")


class BotNametagEmbed(discord.Embed):
    def __init__(self, client:discord.Client) -> None:
        super().__init__(
            title=f"Successful Signed In!",
            description="I am now available.",
            color=discord.Color.from_rgb(129, 199, 132)
        )
        self.discord_client = client
    async def init_all_fields(self):
        self.set_author(name="Saluton!", icon_url="https://i.imgur.com/IHMCgh5.png")
        self.set_thumbnail(url=self.discord_client.user.avatar_url)
        self.add_field(name="Bot Name", value=self.discord_client.user.name, inline=True)
        self.add_field(name="Bot ID", value=self.discord_client.user.id, inline=True)
        self.add_field(name="Login Time", value=datetime.datetime.now().strftime("%d-%b-%Y, %H:%M:%S"), inline=True)
        self.add_field(name="Source", value="http://www.github.com/mclt0568/pyserverman", inline=True)
        self.add_field(name="Getting Started", value="Type `[help]` to get started!", inline=True)
        self.set_footer(text="This bot has been bounded to this channel. Commands in other channels will not be processed.")