# bot/views/state_roles_view.py

import discord
from discord import ui, Interaction

from bot.config import (
    STATE_FACTIONS,
    STATE_MAIN_GUILD_ID,
    STATE_MEMBER_ROLE_ID,
)
from bot.services.state_verification import verify_state_faction


class StateFactionSelect(ui.Select):
    def __init__(self, view: "StateRolesView"):
        self.parent_view = view

        options = [
            discord.SelectOption(
                label=faction["label"],
                value=key,
            )
            for key, faction in STATE_FACTIONS.items()
        ]

        super().__init__(
            placeholder="Оберіть сервер / фракцію",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction):
        self.parent_view.user_choices[interaction.user.id] = self.values[0]

        await interaction.response.defer(ephemeral=True)


class GetStateRoleButton(ui.Button):
    def __init__(self, view: "StateRolesView"):
        super().__init__(
            label="Отримати роль",
            style=discord.ButtonStyle.success,
        )
        self.parent_view = view

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id

        if user_id not in self.parent_view.user_choices:
            return await interaction.response.send_message(
                "❌ Спочатку оберіть сервер / фракцію.",
                ephemeral=True,
            )

        faction_key = self.parent_view.user_choices[user_id]

        # 🔍 перевірка фракції
        ok, error = await verify_state_faction(
            interaction.client,
            interaction.user,
            faction_key,
        )
        if not ok:
            return await interaction.response.send_message(
                error, ephemeral=True
            )

        # 🏛️ State сервер
        state_guild = interaction.client.get_guild(STATE_MAIN_GUILD_ID)
        member = state_guild.get_member(user_id)

        roles_to_add = []

        state_role = state_guild.get_role(STATE_MEMBER_ROLE_ID)
        if state_role and state_role not in member.roles:
            roles_to_add.append(state_role)

        faction_role_id = STATE_FACTIONS[faction_key]["give_role_id"]
        faction_role = state_guild.get_role(faction_role_id)
        if faction_role and faction_role not in member.roles:
            roles_to_add.append(faction_role)

        if not roles_to_add:
            return await interaction.response.send_message(
                "ℹ️ У вас вже є всі необхідні ролі.",
                ephemeral=True,
            )

        try:
            await member.add_roles(
                *roles_to_add,
                reason="State faction verification",
            )
        except discord.Forbidden:
            return await interaction.response.send_message(
                "❌ У мене немає прав видавати ролі.",
                ephemeral=True,
            )

        await interaction.response.send_message(
            "✅ Ролі успішно видані!",
            ephemeral=True,
        )


class StateRolesView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_choices: dict[int, str] = {}

        self.add_item(StateFactionSelect(self))
        self.add_item(GetStateRoleButton(self))
