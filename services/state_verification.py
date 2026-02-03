# bot/services/state_verification.py

import discord
from typing import Tuple

from bot.config import STATE_FACTIONS


async def verify_state_faction(
    bot: discord.Client,
    user: discord.User,
    faction_key: str,
) -> Tuple[bool, str]:
    """
    Перевіряє, чи користувач має право на роль державної фракції.

    Повертає:
        (True, "") — якщо все ок
        (False, "текст помилки") — якщо перевірка не пройдена
    """

    # 1️⃣ Чи існує така фракція
    faction = STATE_FACTIONS.get(faction_key)
    if not faction:
        return False, "❌ Невідома фракція."

    guild = bot.get_guild(faction["guild_id"])
    if guild is None:
        return False, "⚠️ Бот не знайдений на сервері цієї фракції."

    # 2️⃣ Чи є користувач на сервері фракції
    member = guild.get_member(user.id)
    if member is None:
        return False, f"❌ Ви не є учасником серверу **{faction['label']}**."

    # 3️⃣ Чи є потрібна роль
    required_role_id = faction["required_role_id"]
    if required_role_id not in [role.id for role in member.roles]:
        return False, (
            f"❌ У вас немає ролі співробітника у **{faction['label']}**."
        )

    # ✔️ Успіх
    return True, ""
