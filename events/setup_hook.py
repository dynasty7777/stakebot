# events/setup_hook.py

import discord
from bot.config import GUILD_IDS

async def setup_hook(bot):
    """
    Синхронізація slash-команд з конкретними серверами
    """
    print("🔄 Починаю синхронізацію команд...")

    for guild_id in GUILD_IDS:
        try:
            guild = discord.Object(id=guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ Синхронізовано {len(synced)} команд у гільдії {guild_id}")
        except Exception as e:
            print(f"⚠️ Помилка синхронізації для {guild_id}: {e}")

    print("🎉 Усі команди успішно синхронізовано!")
