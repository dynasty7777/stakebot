# commands/dismissal.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from bot.config import FOOTER_TEXT
from bot.views import KickFromDiscordView


def setup(bot):
    @bot.tree.command(
        name="звільнення",
        description="Відправити повідомлення про звільнення учасника.",
    )
    @app_commands.describe(
        користувач="Кого звільняють (тег користувача)",
        static_id="Номер паспорта (StaticID, лише цифри)",
        ранг="З якого рангу звільнений",
        причина="Причина звільнення",
    )
    async def звільнення(
        interaction: discord.Interaction,
        користувач: discord.Member,
        static_id: str,
        ранг: str,
        причина: str,
    ):
        if користувач.id == interaction.user.id:
            return await interaction.response.send_message(
                "❌ Ви не можете звільнити самі себе.",
                ephemeral=True,
            )

        if not static_id.isdigit():
            return await interaction.response.send_message(
                "❌ Номер паспорта (StaticID) має містити лише цифри.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="📉 Звіт про звільнення",
            color=discord.Color.red(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Звільнений:",
            value=f"{користувач.mention}",
            inline=False,
        )
        embed.add_field(
            name="Ім’я та Прізвище:",
            value=f"{користувач.display_name}",
            inline=True,
        )
        embed.add_field(
            name="Номер паспорта (StaticID):",
            value=static_id,
            inline=True,
        )

        embed.add_field(
            name="Звільняє:",
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
            name="З якого рангу звільнений:",
            value=ранг,
            inline=False,
        )
        embed.add_field(
            name="Причина звільнення:",
            value=причина,
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        view = KickFromDiscordView(користувач)

        await interaction.response.send_message(embed=embed, view=view)
