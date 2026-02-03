# views/kick_view.py

import discord


class KickFromDiscordView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member_id = member.id

    @discord.ui.button(
        label="Вигнати з Discord",
        style=discord.ButtonStyle.danger,
        emoji="🔨",
        custom_id="kick_from_discord_button",
    )
    async def kick_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        guild = interaction.guild
        if guild is None:
            return await interaction.response.send_message(
                "⚠️ Не вдалося визначити сервер.", ephemeral=True
            )

        member = guild.get_member(self.member_id)
        if member is None:
            return await interaction.response.send_message(
                "⚠️ Цього користувача вже немає на сервері.",
                ephemeral=True,
            )

        if not guild.me.guild_permissions.kick_members:
            return await interaction.response.send_message(
                "❌ У мене немає права виганяти учасників (Kick Members).",
                ephemeral=True,
            )

        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message(
                "❌ У вас немає прав на вигнання учасників.",
                ephemeral=True,
            )

        try:
            await member.kick(
                reason=f"Вигнано через команду звільнення. Ініціатор: {interaction.user}"
            )
        except discord.Forbidden:
            return await interaction.response.send_message(
                "❌ Не можу вигнати цього користувача. Можливо, його роль вища за мою.",
                ephemeral=True,
            )
        except discord.HTTPException:
            return await interaction.response.send_message(
                "⚠️ Сталася помилка при спробі вигнати користувача.",
                ephemeral=True,
            )

        await interaction.response.send_message(
            f"✅ Користувача {member.mention} вигнано з серверу.",
            ephemeral=True,
        )

        button.disabled = True
        await interaction.message.edit(view=self)
