# commands/promotion.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="підвищення",
        description="Відправити звіт про підвищення",
    )
    @app_commands.describe(
        користувач="Кого підвищують (тег користувача)",
        static_id="Номер паспорта (StaticID, лише цифри)",
        був="Попередній ранг",
        став="Новий ранг",
        причина="Причина підвищення",
    )
    async def підвищення(
        interaction: discord.Interaction,
        користувач: discord.Member,
        static_id: str,
        був: str,
        став: str,
        причина: str,
    ):
        if користувач.id == interaction.user.id:
            return await interaction.response.send_message(
                "❌ Ви не можете підвищити самі себе.",
                ephemeral=True,
            )

        if not static_id.isdigit():
            return await interaction.response.send_message(
                "❌ Номер паспорта (StaticID) має містити лише цифри.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="📈 Звіт про підвищення",
            color=discord.Color.blurple(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Підвищується:",
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
            name="Підвищує:",
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

        embed.add_field(name="Був:", value=був, inline=False)
        embed.add_field(name="Став:", value=став, inline=True)
        embed.add_field(
            name="Причина підвищення:",
            value=причина,
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
