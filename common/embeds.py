from typing import List
import discord


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
