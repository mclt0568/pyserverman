from typing import List
import discord
import datetime


class GeneralErrorEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.from_rgb(229, 115, 115)
        )

        self.set_author(name="Title Name",
                        icon_url="https://i.imgur.com/2P3wrqJ.png")


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


class GeneralSuccessEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.from_rgb(129, 199, 132)
        )

        self.set_author(name="Title Name",
                        icon_url="https://i.imgur.com/V02otDl.png")


class CommandSuccessEmbed(GeneralSuccessEmbed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            description=description
        )
        self._author["name"] = "Command Executed Successfully"


class CommandSuccessListEmbed(GeneralSuccessEmbed):
    def __init__(self, description: str, list_title: str, targets: List[str] = None) -> None:
        super().__init__(
            title=f"Command Result(s)",
            description=description,
        )

        self._author["name"] = "Command Executed Successfully"

        if targets:
            self.add_field(
                name=list_title,
                value="\n".join(targets),
                inline=False
            )


class CommandSuccessDictEmbed(GeneralSuccessEmbed):
    def __init__(self, description: str, targets: List[str] = None) -> None:
        super().__init__(
            title=f"Command Result(s)",
            description=description,
        )

        self._author["name"] = "Command Executed Successfully"

        for key, value in targets.items():
            self.add_field(
                name=key,
                value=value,
                inline=False
            )


class GeneralInformationEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.from_rgb(144, 202, 249)
        )

        self.set_author(name="Information",
                        icon_url="https://i.imgur.com/eTX8lt7.png")


class InformationListEmbed(GeneralInformationEmbed):
    def __init__(self, title: str, description: str, targets: List[str] = [], list_title: str = ""):
        super().__init__(
            title=title,
            description=description,
        )

        if targets:
            self.add_field(
                name=list_title,
                value="\n".join([str(i) for i in targets]),
                inline=False
            )


class GeneralWarningEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.from_rgb(255, 183, 77)
        )

        self.set_author(
            name="Warning", icon_url="https://i.imgur.com/4ASct3T.png")


class BotNametagEmbed(discord.Embed):
    def __init__(self, client: discord.Client) -> None:
        super().__init__(
            title=f"Successfully Signed In!",
            description="I am now available.",
            color=discord.Color.from_rgb(255, 245, 157)
        )
        self.discord_client = client

    async def init_all_fields(self):
        self.set_author(name="Saluton!",
                        icon_url="https://i.imgur.com/IHMCgh5.png")
        self.set_thumbnail(url=self.discord_client.user.avatar_url)
        self.add_field(name="Bot Name",
                       value=self.discord_client.user.name, inline=True)
        self.add_field(
            name="Bot ID", value=self.discord_client.user.id, inline=True)
        self.add_field(name="Login Time", value=datetime.datetime.now().strftime(
            "%d-%b-%Y, %H:%M:%S"), inline=True)
        self.add_field(
            name="Source", value="http://www.github.com/mclt0568/pyserverman", inline=True)
        self.add_field(name="Getting Started",
                       value="Type `[help]` to get started!", inline=True)
        self.set_footer(
            text="This bot has been bounded to this channel. Commands in other channels will not be processed.")
