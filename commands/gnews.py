import discord
from discord import app_commands
from datetime import datetime, timezone
from config import FOOTER_TEXT


async def setup(bot):

    @bot.tree.command(name="gnews", description="Державна хвиля")
    @app_commands.describe(
        час="Час ефіру",
        фракція="Назва фракції"
    )
    async def gnews(
        interaction: discord.Interaction,
        час: str,
        фракція: str
    ):
        now = datetime.now(timezone.utc)

        embed = discord.Embed(
            title="📻 Державна хвиля — офіційне повідомлення",
            color=discord.Color.gold(),
        )

        embed.add_field(
            name="⚡ Фракція:",
            value=f"**{фракція}**",
            inline=False
        )

        embed.add_field(
            name="🕒 Час ефіру:",
            value=f"**{час}**",
            inline=False
        )

        embed.add_field(
            name="🔊 Повідомлення",
            value=(
                "На цей час державна хвиля **зайнята для проведення "
                "офіційних звернень.**\n"
                "Будь ласка, **не порушуйте Закон «Про державну хвилю "
                "штату Сан-Андреас».**"
            ),
            inline=False
        )

        embed.add_field(
            name="📅 Дата зайняття:",
            value=now.strftime("%d %B %Y %H:%M"),
            inline=False
        )

        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/747/747376.png"
        )

        embed.set_footer(
            text=f"{FOOTER_TEXT} • {now.strftime('%d/%m/%Y %H:%M')}",
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        await interaction.response.send_message(embed=embed)
