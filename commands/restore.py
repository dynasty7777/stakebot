# commands/restore.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="відновлення",
        description="Відправити звіт про відновлення учасника після звільнення.",
    )
    @app_commands.describe(
        користувач="Кого відновлюють (тег користувача)",
        ранг="На який ранг відновлено",
        причина="Причина відновлення",
    )
    async def відновлення(
        interaction: discord.Interaction,
        користувач: discord.Member,
        ранг: str,
        причина: str,
    ):
        embed = discord.Embed(
            title="🔄 Звіт про відновлення",
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Відновлений:",
            value=f"{користувач.mention}",
            inline=False,
        )
        embed.add_field(
            name="Ім’я та Прізвище:",
            value=f"{користувач.display_name}",
            inline=True,
        )
        embed.add_field(
            name="Discord ID:",
            value=f"{користувач.id}",
            inline=True,
        )

        embed.add_field(
            name="Відновлює:",
            value=f"{interaction.user.mention}",
            inline=False,
        )
        embed.add_field(
            name="Ім’я та Прізвище:",
            value=f"{interaction.user.display_name}",
            inline=True,
        )
        embed.add_field(
            name="Discord ID:",
            value=f"{interaction.user.id}",
            inline=True,
        )

        embed.add_field(
            name="На який ранг відновлено:",
            value=ранг,
            inline=False,
        )
        embed.add_field(
            name="Причина відновлення:",
            value=причина,
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
