from discord.ext import commands,tasks
from discord.utils import get
import discord
import logging
import os
import asyncio
from dotenv import load_dotenv
import yt_dlp


load_dotenv()

logging.basicConfig(level=logging.INFO)


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all(),application_id=int(os.getenv("BOT_ID")))
intents = discord.Intents.default()

intents.voice_states = True
ffmpeg_path = r'C:/ffmpeg/bin/ffmpeg.exe'


@bot.event
async def on_ready():
    print(f"pronto!, estou conectado como {bot.user}")
    print(ffmpeg_path)

caminho_diretorio = r'C:/Users/Winic/Desktop/project/bot'

if os.access(caminho_diretorio, os.W_OK):
    print(f"Voce tem permissao para gravar no diretorio',{caminho_diretorio})")
else:
    print('Você não tem permissão para gravar no diretório')

from comandos import setup as setup_comandos
setup_comandos(bot)


from musicas import setup as setup_comandos
setup_comandos(bot)


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)