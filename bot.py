# bot.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.config import GUILD_IDS, BOT_STATUS
from bot.commands import setup_commands

load_dotenv()

TOKEN = os.getenv("TOKEN")

# intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    activity = discord.CustomActivity(name=BOT_STATUS)
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f"✅ Бот запущений як {bot.user}")


@bot.event
async def setup_hook():
    print("🔄 Починаю синхронізацію команд...")

    setup_commands(bot)

    for guild_id in GUILD_IDS:
        try:
            guild = discord.Object(id=guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ Синхронізовано {len(synced)} команд у гільдії {guild_id}")
        except Exception as e:
            print(f"⚠️ Помилка синхронізації для {guild_id}: {e}")

    print("🎉 Синхронізація завершена!")


bot.run(TOKEN)
