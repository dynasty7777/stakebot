import discord

from config import (
    FAMILY_TICKET_CATEGORY_ID,
    FAMILY_TICKET_LOG_CHANNEL_ID,
    FAMILY_TICKET_STAFF_ROLE_IDS
)


async def send_ticket_log(guild: discord.Guild, embed: discord.Embed):
    log_channel = guild.get_channel(FAMILY_TICKET_LOG_CHANNEL_ID)
    if isinstance(log_channel, discord.TextChannel):
        try:
            await log_channel.send(embed=embed)
        except Exception as e:
            print(f"[FamilyTickets] Помилка логування: {e}")


def build_staff_overwrites(guild: discord.Guild) -> dict:
    overwrites = {}

    for role_id in FAMILY_TICKET_STAFF_ROLE_IDS:
        role = guild.get_role(role_id)
        if role:
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
                manage_messages=True,
                attach_files=True,
                embed_links=True
            )

    return overwrites


class DeleteTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Delete Ticket",
        style=discord.ButtonStyle.danger,
        custom_id="family_ticket_delete"
    )
    async def delete_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                "Цю кнопку можна використовувати лише в текстовому каналі.",
                ephemeral=True
            )
            return

        member = interaction.user
        if not isinstance(member, discord.Member):
            await interaction.response.send_message(
                "Не вдалося визначити користувача.",
                ephemeral=True
            )
            return

        is_staff = any(role.id in FAMILY_TICKET_STAFF_ROLE_IDS for role in member.roles)
        if not is_staff:
            await interaction.response.send_message(
                "Видаляти тикети може лише staff.",
                ephemeral=True
            )
            return

        channel = interaction.channel

        await interaction.response.send_message(
            "Видаляю тикет...",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🗑 Ticket Deleted",
            description=f"Тикет `{channel.name}` видалив {interaction.user.mention}",
            color=discord.Color.red()
        )
        await send_ticket_log(interaction.guild, embed)

        try:
            await channel.delete(reason=f"Family ticket deleted by {interaction.user} ({interaction.user.id})")
        except Exception as e:
            print(f"[FamilyTickets] Не вдалося видалити канал: {e}")


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.secondary,
        custom_id="family_ticket_close"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                "Цю кнопку можна використовувати лише в текстовому каналі.",
                ephemeral=True
            )
            return

        channel = interaction.channel
        guild = interaction.guild
        topic = channel.topic or ""

        owner_id = None
        if topic.startswith("ticket_owner_id:"):
            try:
                owner_id = int(topic.split("ticket_owner_id:")[1].strip())
            except Exception:
                owner_id = None

        owner = guild.get_member(owner_id) if owner_id else None

        if owner:
            try:
                await channel.set_permissions(
                    owner,
                    view_channel=False,
                    send_messages=False,
                    read_message_history=False
                )
            except Exception as e:
                print(f"[FamilyTickets] Не вдалося змінити права owner: {e}")

        embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=(
                f"Тикет закрив {interaction.user.mention}.\n\n"
                f"Якщо питання вирішене — staff може видалити тикет кнопкою нижче."
            ),
            color=discord.Color.orange()
        )

        await interaction.response.send_message(
            embed=embed,
            view=DeleteTicketView()
        )

        log_embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=f"Тикет `{channel.name}` закрив {interaction.user.mention}",
            color=discord.Color.orange()
        )
        await send_ticket_log(guild, log_embed)


class CreateTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.green,
        emoji="🎫",
        custom_id="family_ticket_create"
    )
    async def create_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        guild = interaction.guild
        member = interaction.user

        if not isinstance(member, discord.Member):
            await interaction.response.send_message(
                "Не вдалося визначити користувача.",
                ephemeral=True
            )
            return

        category = guild.get_channel(FAMILY_TICKET_CATEGORY_ID)
        if not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "Категорія тикетів не знайдена. Перевір FAMILY_TICKET_CATEGORY_ID.",
                ephemeral=True
            )
            return

        # Перевірка на вже відкритий тикет
        for ch in category.channels:
            if isinstance(ch, discord.TextChannel) and ch.topic == f"ticket_owner_id:{member.id}":
                await interaction.response.send_message(
                    f"У тебе вже є відкритий тикет: {ch.mention}",
                    ephemeral=True
                )
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True
            )
        }
        overwrites.update(build_staff_overwrites(guild))

        safe_name = "".join(c.lower() for c in member.name if c.isalnum() or c in ("-", "_"))
        if not safe_name:
            safe_name = f"user-{member.id}"

        channel_name = f"family-ticket-{safe_name}"[:95]

        try:
            ticket_channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                topic=f"ticket_owner_id:{member.id}",
                reason=f"Family ticket created by {member} ({member.id})"
            )
        except Exception as e:
            print(f"[FamilyTickets] Не вдалося створити канал: {e}")
            await interaction.response.send_message(
                "Не вдалося створити тикет.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🎫 Family Ticket",
            description=(
                f"{member.mention}, твій тикет створено.\n\n"
                f"Опиши свою проблему або питання одним повідомленням.\n"
                f"Коли питання буде вирішене — натисни **Close Ticket**."
            ),
            color=discord.Color.green()
        )
        embed.add_field(name="Owner", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=str(member.id), inline=True)

        try:
            await ticket_channel.send(
                content=member.mention,
                embed=embed,
                view=CloseTicketView()
            )
        except Exception as e:
            print(f"[FamilyTickets] Не вдалося надіслати стартове повідомлення: {e}")

        log_embed = discord.Embed(
            title="🎫 Ticket Created",
            description=f"Тикет {ticket_channel.mention} створив {member.mention}",
            color=discord.Color.green()
        )
        await send_ticket_log(guild, log_embed)

        await interaction.response.send_message(
            f"Тикет створено: {ticket_channel.mention}",
            ephemeral=True
        )