from typing import Dict, List
import discord
from discord.enums import _is_descriptor


class ErrorEmbed(discord.Embed):
    def __init__(self, title: str, description: str, prompt: str, message: discord.Message) -> None:
        super().__init__(
            title=f"錯誤: {title}",
            description=description,
            color=discord.Color.from_rgb(229, 115, 115)
        )

        self.add_field(
            name="提示",
            value=prompt,
            inline=False
        )
        self.add_field(
            name="Traceback",
            value=f"`{message.content.strip()}`",
            inline=False
        )

class ExceptionEmbed(discord.Embed):
    def __init__(self, exception_name: str, event: str, full_traceback: str) -> None:
        super().__init__(
            title=f"發生不可預期的異常: {exception_name}",
            description=f"在執行 {event} 事件時發生不可預期的異常\n請聯繫管理員",
            color=discord.Color.from_rgb(229, 115, 115)
        )
        self.add_field(
            name="Full Traceback",
            value=f"```{full_traceback}```",
            inline=False
        )

class EmptySuccessEmbed(discord.Embed):
    def __init__(self, title, description):
        super().__init__(
            title=title,
            color=discord.Color.from_rgb(129, 199, 132),
            description=description
        )

class SuccessEmbed(discord.Embed):
    def __init__(self, description: str, targets: List[str] = None) -> None:
        super().__init__(
            title=f"指令已完成",
            description=description,
            color=discord.Color.from_rgb(129, 199, 132)
        )

        if targets:
            self.add_field(
                name="對象",
                value="\n".join(targets),
                inline=False
            )


class DictEmbed(discord.Embed):
    def __init__(self, dict: Dict[str, str]):
        super().__init__(
            title=f"指令結果",
            color=discord.Color.from_rgb(129, 199, 132)
        )

        for key, value in dict.items():
            self.add_field(
                name=key,
                value=value,
                inline=False
            )


class StringEmbed(discord.Embed):
    def __init__(self, string):
        super().__init__(
            title=f"指令結果",
            color=discord.Color.from_rgb(129, 199, 132),
            description=string
        )


class ListEmbed(discord.Embed):
    def __init__(self, name: str, list: List[str]):
        super().__init__(
            title="指令結果",
            color=discord.Color.from_rgb(129, 199, 132)
        )

        self.add_field(
            name=name,
            value="\n".join(list)
        )
