# commands/hiring_no_discord.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="прийняття_без_діскорду",
        description="Відправити звіт про прийняття користувача, який відсутній в Discord.",
    )
    @app_commands.describe(
        нікнейм="Ім’я та прізвище гравця (вручну)",
        static_id="StaticID гравця (вручну)",
        ранг="На який ранг прийнятий",
        причина="Причина прийняття",
    )
    async def прийняття_без_діскорду(
        interaction: discord.Interaction,
        нікнейм: str,
        static_id: str,
        ранг: str,
        причина: str,
    ):
        embed = discord.Embed(
            title="📋 Звіт про прийняття (без Discord)",
            color=discord.Color.red(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="Прийнятий:", value=f"**{нікнейм}**", inline=False)
        embed.add_field(name="Static ID:", value=static_id, inline=True)
        embed.add_field(name="Ранг:", value=ранг, inline=True)

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

        embed.add_field(name="Причина прийняття:", value=причина, inline=False)
        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
