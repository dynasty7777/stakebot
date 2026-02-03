# commands/demotion.py

import discord
from discord import app_commands
from datetime import datetime, timezone

from config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="зниження",
        description="Відправити звіт про зниження учасника.",
    )
    @app_commands.describe(
        користувач="Кого знижують (тег користувача)",
        був="Який ранг зараз",
        став="Який ранг буде",
        причина="Причина зниження",
    )
    async def зниження(
        interaction: discord.Interaction,
        користувач: discord.Member,
        був: str,
        став: str,
        причина: str,
    ):
        if користувач.id == interaction.user.id:
            return await interaction.response.send_message(
                "❌ Ви не можете знизити себе.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="📉 Звіт про зниження",
            color=discord.Color.orange(),
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="Знижений:",
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
            name="Знижує:",
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
            name="З якого рангу:",
            value=був,
            inline=False,
        )
        embed.add_field(
            name="На який ранг:",
            value=став,
            inline=True,
        )

        embed.add_field(
            name="Причина зниження:",
            value=причина,
            inline=False,
        )

        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed)
