# checks/permissions.py

import discord
from discord import app_commands
from bot.config import ALLOWED_ROLE_IDS


def has_meeting_permission():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False

        member: discord.Member = interaction.user
        allowed = any(role.id in ALLOWED_ROLE_IDS for role in member.roles)

        if not allowed:
            await interaction.response.send_message(
                "⚠️ У вас немає прав використовувати цю команду.",
                ephemeral=True,
            )

        return allowed

    return app_commands.check(predicate)
