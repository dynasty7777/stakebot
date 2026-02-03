# commands/hiring.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from bot.config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="прийняття",
        description="Відправити звіт про прийняття нового учасника.",
    )
    @app_commands.describe(
        користувач="Кого прийнято (тег користувача)",
        ранг="На який ранг прийнято",
        причина="Причина прийняття",
    )
    async def прийняття(
        interaction: discord.Interaction,
        користувач: discord.Member,
        ранг: str,
        причина: str,
    ):
        if користувач.id == interaction.user.id:
            return await interaction.response.send_message(
                "❌ Ви не можете прийняти самі себе.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="📝 Звіт про прийняття",
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Прийнятий:",
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
            name="Приймає:",
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
            name="На який ранг прийнято:",
            value=ранг,
            inline=False,
        )
        embed.add_field(
            name="Причина прийняття:",
            value=причина,
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
