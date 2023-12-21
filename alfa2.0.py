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
    embed.add_field(name="!stop", value="vai sair da chamada de voz.", inline=False)
    embed.add_field(name="!skip", value="pula uma música.", inline=False)
    embed.add_field(name="!pause", value="vai parar de tocar", inline=False)
    embed.add_field(name="!lista", value="mostra a lista de musicas (que vai ser reproduzida do bot).", inline=False)
    embed.add_field(name="!limpar", value="limpa a lista de musicas.", inline=False)

    # Set the GIF image
    embed.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

    # Send the embed in the current context
    await ctx.send(embed=embed)

@bot.command(name="criador")
async def send_message(ctx):
    embed = discord.Embed(
        title="Aqui está o link para o criador:",
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
    response = "versão: 2.0"
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
  'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}
yytdl = yt_dlp.YoutubeDL(ytdl_format_options)

def search_youtube(arg):
  with yytdl:
    try:
      info = yytdl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    except Exception:
      return False
  return {'source': info['url'], 'title': info['title']}

@bot.command(name='play')
async def play(ctx, *, search: str):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        embed = discord.Embed(
            title="Erro",
            description="Cade vocé, não estou de achando em um canal.",
            color=0x9400d3
        )

        await ctx.send(embed=embed)
        return

    channel = ctx.author.voice.channel

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
        voice_client.play(discord.FFmpegPCMAudio(song['source'], executable='ffmpeg', **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))

        # Exibir a embed da música em reprodução
        current_song_embed = discord.Embed(
            title="Tocando agora:",
            description=song['title'],
            color=0x9400d3
        )
        await ctx.send(embed=current_song_embed)
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
    embed = discord.Embed(
      title="Música pausada",
      description="A música foi pausada.",
      color=0x9400d3
    )
    embed.set_thumbnail(url="https://i.pinimg.com/originals/13/ab/d6/13abd67ac86fd7e60e04186139810666.gif")
    await ctx.send(embed=embed)
  else:
    await ctx.send("Não há nada sendo reproduzido no momento.")
    
@bot.command(name='unpause')
async def unpause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_paused():
      voice_client.resume()
      embed = discord.Embed(
      title="Música retomada",
      description="A reprodução foi retomada.",
      color=0x9400d3
    )
      embed.set_thumbnail(url="https://i.pinimg.com/originals/17/4a/7b/174a7b3b9997b30150305fb49e968ed2.gif")
      await ctx.send(embed=embed)
    else:
        await ctx.send("Não há música pausada atualmente.")
        

@bot.command(name='lista')
async def show_queue(ctx):
    guild_id = ctx.guild.id
    if guild_id in queue and len(queue[guild_id]) > 0:
        queue_list = [f"{index + 1}. {song['title']}" for index, song in enumerate(queue[guild_id])]
        current_song = "A proxima musica é: " + queue[guild_id][0]['title'] if bot.voice_clients and bot.voice_clients[0].is_playing() else ""
        
        queue_embed = discord.Embed(
            title="Lista de Reprodução",
            description="\n".join(queue_list) + f"\n\n{current_song}",
            color=0x9400d3  # Cor da embed (pode ser ajustada conforme desejado)
        )
        await ctx.send(embed=queue_embed)
    else:
        await ctx.send("A fila está vazia.")

@bot.command(name='limpa')
async def clear_queue(ctx):
  guild_id = ctx.guild.id
  if guild_id in queue:
    queue[guild_id] = []
    await ctx.send("A lista foi limpa.")
  else:
    await ctx.send("A lista já está vazia.")


@bot.command()
@commands.is_owner()
async def sync(ctx, guild=None):
    print("Comando de sincronização iniciado.")
    try:
        if guild is None:
            await bot.tree.sync()
        else:
            await bot.tree.sync(guild=discord.Object(id=int(guild)))
        print("Sincronização concluída com sucesso.")
        await ctx.send("**Sincronizado!**")
    except Exception as e:
        print(f"Erro durante a sincronização: {e}")
        await ctx.send("Ocorreu um erro durante a sincronização.")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
