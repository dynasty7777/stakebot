import discord
from discord import app_commands

from config import FAMILY_TICKET_PANEL_CHANNEL_ID
from views.family_tickets_view import CreateTicketView


@app_commands.command(
    name="send_family_tickets",
    description="Надіслати панель тікетів у канал Family"
)
@app_commands.default_permissions(administrator=True)
async def send_family_tickets(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Цю команду можна використовувати лише на сервері.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(FAMILY_TICKET_PANEL_CHANNEL_ID)

    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message(
            "error",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🎫 Сімейна підтримка",
        description=(
            "Натисни кнопку нижче, щоб створити звернення\n\n"
            "Буде створено канал, у котрий будете додані Ви, та адміністратори."
        ),
        color=discord.Color.blurple()
    )

    await channel.send(embed=embed, view=CreateTicketView())
    await interaction.response.send_message(
        f"Панель відправлена в {channel.mention}",
        ephemeral=True
    )


def setup(bot):
    bot.tree.add_command(send_family_tickets)