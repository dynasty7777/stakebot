# events/on_ready.py

import discord
from bot.config import BOT_STATUS

async def on_ready():
    """
    Викликається, коли бот повністю запущений
    """
    activity = discord.CustomActivity(name=BOT_STATUS)
    await discord.Client.change_presence(
        discord.Client,  # хак, бо ми підвʼязуємо через bot.event
        status=discord.Status.dnd,
        activity=activity
    )
    print("✅ Бот успішно підключився до Discord")
