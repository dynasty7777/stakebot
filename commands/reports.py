# commands/report.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from bot.config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="звіт",
        description="Відправити звіт про дію з працівником (підвищення, зниження, звільнення тощо).",
    )
    @app_commands.describe(
        працівник="Ім’я та Прізвище працівника (тег користувача)",
        static_id="Номер паспорта (StaticID, лише цифри)",
        дія="Дія, наприклад: Підвищення / Зниження / Звільнення",
        ранг="Ранг працівника (текст + цифра)",
        причина="Причина дії",
    )
    async def звіт(
        interaction: discord.Interaction,
        працівник: discord.Member,
        static_id: str,
        дія: str,
        ранг: str,
        причина: str,
    ):
        if not static_id.isdigit():
            return await interaction.response.send_message(
                "❌ Номер паспорта (StaticID) має містити лише цифри.",
                ephemeral=True,
            )

        дата = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        embed = discord.Embed(
            title="📋 Нова кадрова дія",
            color=discord.Color.red(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Ім’я та Прізвище Працівника:",
            value=f"{працівник.display_name} | {працівник.mention}",
            inline=False,
        )
        embed.add_field(name="Номер паспорта (StaticID):", value=static_id, inline=False)
        embed.add_field(name="Дія:", value=дія, inline=False)
        embed.add_field(name="Ранг:", value=ранг, inline=False)
        embed.add_field(name="Причина:", value=причина, inline=False)
        embed.add_field(name="Дата:", value=дата, inline=False)

        embed.add_field(
            name="Виконавець:",
            value=f"{interaction.user.display_name} | {interaction.user.mention}",
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
