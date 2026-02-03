# views/meeting_poll.py

import discord


class MeetingPollView(discord.ui.View):
    def __init__(self, faction_role: discord.Role):
        super().__init__(timeout=None)
        self.faction_role = faction_role
        self.yes_votes: set[int] = set()
        self.no_votes: set[int] = set()

    async def update_message(self, interaction: discord.Interaction):
        msg = interaction.message
        if msg is None:
            return

        if msg.embeds:
            embed = msg.embeds[0]
        else:
            embed = discord.Embed(
                title="Опитування щодо зборів з куратором",
                description=(
                    f"{self.faction_role.mention}\n"
                    "Чи потрібні вам **збори з куратором** на цьому тижні?"
                ),
            )

        if len(embed.fields) < 2:
            embed.clear_fields()
            embed.add_field(name="За ✅", value=str(len(self.yes_votes)), inline=True)
            embed.add_field(name="Проти ❌", value=str(len(self.no_votes)), inline=True)
        else:
            embed.set_field_at(
                0, name="За ✅", value=str(len(self.yes_votes)), inline=True
            )
            embed.set_field_at(
                1, name="Проти ❌", value=str(len(self.no_votes)), inline=True
            )

        await msg.edit(embed=embed, view=self)

    async def _handle_vote(self, interaction: discord.Interaction, vote: str):
        user_id = interaction.user.id

        if vote == "yes":
            self.no_votes.discard(user_id)
            self.yes_votes.add(user_id)
            text = "Ви відмітили, що **збори потрібні** ✅"
        else:
            self.yes_votes.discard(user_id)
            self.no_votes.add(user_id)
            text = "Ви відмітили, що **збори не потрібні** ❌"

        await interaction.response.send_message(text, ephemeral=True)
        await self.update_message(interaction)

    @discord.ui.button(
        label="Так, потрібні ✅",
        style=discord.ButtonStyle.success,
        custom_id="meeting_yes",
    )
    async def yes_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self._handle_vote(interaction, "yes")

    @discord.ui.button(
        label="Ні, не потрібні ❌",
        style=discord.ButtonStyle.danger,
        custom_id="meeting_no",
    )
    async def no_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self._handle_vote(interaction, "no")
