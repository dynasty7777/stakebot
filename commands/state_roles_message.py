# bot/commands/state_roles_message.py

import discord
from discord import app_commands

from config import STATE_CHANNEL_ID, FOOTER_TEXT
from views.state_roles_view import StateRolesView


def setup(bot: discord.Client):
    @bot.tree.command(
        name="state_roles_message",
        description="Відправити повідомлення для отримання ролей державних фракцій"
    )
    async def state_roles_message(interaction: discord.Interaction):
        # 🔒 За бажанням: можна обмежити команду правами
        # if not interaction.user.guild_permissions.administrator:
        #     return await interaction.response.send_message(
        #         "❌ У вас немає прав.", ephemeral=True
        #     )

        channel = interaction.client.get_channel(STATE_CHANNEL_ID)
        if channel is None:
            return await interaction.response.send_message(
                "❌ Канал State Fractions не знайдено.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="🏛️ State Fractions | Stake RP",
            description=(
                "**Вітаємо у State Fractions!**\n"
                "Примітка: для отримання ролі <@&1389903927918461011> потрібно бути\n"
                "учасником офіційного серверу державної структури\n"
                "та мати у ньому фракційні ролі."
            ),
            color=discord.Color.blurple(),
        )

        # 🔹 КАРТИНКА (URL з Discord / Imgur)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1399037972019548251/1428658553488539648/STAKE.png?ex=69825836&is=698106b6&hm=966f80103a0fbfa7ba46545a5aad7eac6ccbc36ecf2620a4595631a8cdf74725&"  # ⬅️ ВСТАВ СВОЮ КАРТИНКУ
        )

        embed.set_footer(text=FOOTER_TEXT)

        view = StateRolesView()

        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(
            "✅ Повідомлення успішно відправлено.",
            ephemeral=True,
        )
