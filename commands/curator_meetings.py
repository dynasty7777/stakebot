# commands/curator_meetings.py

import discord
from discord import app_commands

from views import MeetingPollView
from checks import has_meeting_permission

from config import FOOTER_TEXT


def setup(bot):
    @bot.tree.command(
        name="куратор_збори",
        description="Запитати у фракції, чи потрібні збори з куратором цього тижня.",
    )
    @app_commands.describe(
        faction_role="Роль фракції, яку треба тегнути (наприклад, @FIB / @LSPD / @GOV)",
    )
    @has_meeting_permission()
    async def curator_meeting(
        interaction: discord.Interaction,
        faction_role: discord.Role,
    ):
        view = MeetingPollView(faction_role=faction_role)

        embed = discord.Embed(
            title="Опитування щодо зборів з куратором",
            description=(
                f"{faction_role.mention}\n"
                "Чи потрібні вам **збори з куратором** на цьому тижні?"
            ),
        )

        embed.add_field(name="За ✅", value="0", inline=True)
        embed.add_field(name="Проти ❌", value="0", inline=True)
        embed.set_footer(text=FOOTER_TEXT)

        await interaction.response.send_message(embed=embed, view=view)
