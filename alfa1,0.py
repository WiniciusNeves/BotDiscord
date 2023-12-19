from discord.ext import commands,tasks
from discord.utils import get
import discord
import logging
import os
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

@bot.command(name="ajuda")
async def send_message(ctx):
    # Create an embed object
    embed = discord.Embed(
        title="Comandos do Bot",
        description="Aqui estão os comandos disponíveis:",
        color=0x9400d3 
    )
    # Add commands to the embed
    embed.add_field(name="!ajuda", value="Mostra esta mensagem de ajuda.", inline=False)
    embed.add_field(name="!criador", value="Mostra informações sobre o criador do bot.", inline=False)
    embed.add_field(name="!biblioteca", value="Mostra o link para a biblioteca.", inline=False)
    embed.add_field(name="!v", value="Mostra a versão do bot.", inline=False)
    embed.add_field(name="!play", value="toca uma música.", inline=False)
    embed.add_field(name="!stop", value="para de tocar uma música.", inline=False)
    embed.add_field(name="!skip", value="pula uma música.", inline=False)
    embed.add_field(name="!lista", value="mostra a lista de musicas (que vai ser reproduzida)do bot.", inline=False)

    # Set the GIF image
    embed.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

    # Send the embed in the current context
    await ctx.send(embed=embed)

@bot.command(name="criador")
async def send_message(ctx):
    embed = discord.Embed(
        title="Aqui esta o link para o criador:",
        description="https://linktr.ee/winiciusneves",
        color=0x9400d3  
    )
    embed.set_thumbnail(url="https://i.pinimg.com/originals/2f/5c/c5/2f5cc5163100018a4e2670a01b77672e.gif")
    await ctx.send(embed=embed)

@bot.command(name="biblioteca")
async def send_message(ctx):
    embed = discord.Embed(
        title="Biblioteca do Discord",
        description="Clique no link abaixo para acessar a biblioteca do Discord:",
        color=0x9400d3 
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1179409324611747921/1184231893554696202/fly-logo-60x60p.png?ex=658b38e5&is=6578c3e5&hm=7d4f4f1860e4cfed7e3e18a477c22ae46679b16990d6d277149fe497cdf0a6a0&")
    embed.add_field(name="Link da Biblioteca", value="[Clique aqui](https://discord.gg/mfZ2GuT5kg)", inline=False)
    
    await ctx.send(embed=embed)  


@bot.command(name="v")
async def send_message(ctx):
    response = "versão: 1.0"
    await ctx.send(response)

queue = {}
ytdl_format_options = {
  'format': 'bestaudio/best',
  'quiet': True,
  'extractaudio': True,
  'audioformat': 'mp3',
  'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
  'restrictfilenames': True,
  'noplaylist': True,
}
ffmpeg_options = {
  'before_options': '-f lavfi -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}
yytdl = yt_dlp.YoutubeDL(ytdl_format_options)

def search_youtube(arg):
  with yytdl:
    try:
      info = yytdl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    except Exception:
      return False
  return {'source': info['formats'][0]['url'], 'title': info['title']}

@bot.command(name='play')
async def play(ctx, *, search: str):
  channel = ctx.message.author.voice.channel
  if channel is None:
    await ctx.send("Você precisa estar em um canal de voz para tocar uma música.")
    return

  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if voice_client is None:
    await channel.connect()
    voice_client = get(bot.voice_clients, guild=ctx.guild)

  if ctx.guild.id not in queue:
    queue[ctx.guild.id] = []

  song = search_youtube(search)
  if song:
    queue[ctx.guild.id].append(song)
    await ctx.send(f"{song['title']} foi adicionada à fila.")
  else:
    await ctx.send("Não encontrei a música requisitada.")

  if not voice_client.is_playing() and not voice_client.is_paused():
    await play_next(ctx)

async def play_next(ctx):
  guild_id = ctx.guild.id
  voice_client = get(bot.voice_clients, guild=ctx.guild)

  if queue[guild_id]:
    song = queue[guild_id].pop(0)
    voice_client.play(discord.FFmpegPCMAudio(song['source'], executable='ffmpeg', options=ffmpeg_options))
    await ctx.send(f"Tocando agora: {song['title']}")
  else:
    await ctx.send("A fila está vazia.")

    if voice_client:
      await voice_client.disconnect()

@bot.command(name='stop')
async def stop(ctx):
  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if voice_client is not None:
    await voice_client.disconnect()
    embed = discord.Embed(
      title="saindo da chamada de voz",
      description="não querem mais eu aqui ?",
      color=0x9400d3
    )
    embed.set_thumbnail(url="https://gifs.eco.br/wp-content/uploads/2022/03/gif-animado-dando-tchau-20.gif")
    await ctx.send(embed=embed)
  else:
    await ctx.send("Nenhum bot de chamada de voz está conectado.")

@bot.command(name='skip')
async def skip(ctx):
  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if voice_client and voice_client.is_playing():
    voice_client.stop()
    await play_next(ctx)
    embed = discord.Embed(
      title="Música pulada",
      description="A próxima música está sendo reproduzida.",
      color=0x9400d3
    )
    embed.set_thumbnail(url="https://gifs.eco.br/wp-content/uploads/2022/09/gifs-de-musica-9.gif")
    await ctx.send(embed=embed)
  else:
    await ctx.send("Nenhuma música está sendo tocada no momento.")

@bot.command(name='pause')
async def pause(ctx):
  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if voice_client and voice_client.is_playing():
    voice_client.pause()
    await ctx.send("A reprodução foi pausada.")
  else:
    await ctx.send("Não há nada sendo reproduzido no momento.")

@bot.command(name='lista')
async def show_queue(ctx):
  guild_id = ctx.guild.id
  if guild_id in queue and len(queue[guild_id]) > 0:
    msg = "Fila:\n" + "\n".join([song['title'] for song in queue[guild_id]])
    await ctx.send(msg)
  else:
    await ctx.send("A fila está vazia.")

@bot.command(name='limpa')
async def clear_queue(ctx):
  guild_id = ctx.guild.id
  if guild_id in queue:
    queue[guild_id] = []
    await ctx.send("A fila foi limpa.")
  else:
    await ctx.send("A fila já está vazia.")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
