from discord.ext import commands
import discord
import logging
import os
from dotenv import load_dotenv
import tracemalloc

tracemalloc.start()

load_dotenv()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

ffmpeg_path = r'C:/ffmpeg/bin/ffmpeg.exe'

bot = commands.Bot(command_prefix="!", intents=intents, application_id=int(os.getenv("BOT_ID")))

@bot.event
async def on_ready():
    print(f"Pronto! Estou conectado como {bot.user}")
    await bot.load_extension("cogs.comandos")
    await bot.load_extension("cogs.musicas")
    await bot.tree.sync()

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)