import discord
from discord.ext import commands
import yt_dlp
import asyncio
from discord.utils import get

def setup(bot):
    queue = {}
    executing_commands = asyncio.Lock()

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
                description="Cade você, não estou te achando em um canal.",
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
            await ctx.send(f"**{song['title']}** foi adicionada à lista de reprodução.")
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

            current_song_embed = discord.Embed(
                title="Tocando agora:",
                description=song['title'],
                color=0x9400d3
            )
            await ctx.send(embed=current_song_embed)
        else:
        
            embed = discord.Embed(
                title="Não tem mais músicas para reproduzir.",
                description="Desconectando do canal de voz...",
                color=0x9400d3
            )
            embed.set_thumbnail(url="https://i.pinimg.com/564x/25/be/a0/25bea0b38f45e67b0a53736809f2604a.jpg")
            await ctx.send(embed=embed)

            if voice_client:
                await voice_client.disconnect()
            return  

    @bot.command(name='skip')
    async def skip(ctx):
        async with executing_commands:
            voice_client = get(bot.voice_clients, guild=ctx.guild)
            if voice_client and voice_client.is_playing():
                voice_client.stop()  # O callback 'after' se encarregará de tocar a próxima música.
                embed = discord.Embed(
                    title="Música pulada",
                    description="A próxima música será reproduzida em breve.",
                    color=0x9400d3
                )
                embed.set_thumbnail(url="https://gifs.eco.br/wp-content/uploads/2022/09/gifs-de-musica-9.gif")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Nenhuma música está sendo tocada no momento.")

    @bot.command(name='stop')
    async def stop(ctx):
        async with executing_commands:
            voice_client = get(bot.voice_clients, guild=ctx.guild)
            if voice_client is not None:
                await voice_client.disconnect()
                embed = discord.Embed(
                    title="Saindo da chamada de voz",
                    description="Não querem mais eu aqui?",
                    color=0x9400d3
                )
                embed.set_thumbnail(url="https://gifs.eco.br/wp-content/uploads/2022/03/gif-animado-dando-tchau-20.gif")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Nenhum bot de chamada de voz está conectado.")

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
            current_song = "A próxima música é: " + queue[guild_id][0]['title'] if bot.voice_clients and bot.voice_clients[0].is_playing() else ""

            queue_embed = discord.Embed(
                title="Lista de Reprodução",
                description="\n".join(queue_list) + f"\n\n{current_song}",
                color=0x9400d3  # Cor da embed (pode ser ajustada conforme desejado)
            )
            await ctx.send(embed=queue_embed)
        else:
            await ctx.send("Não tem uma próxima música para ser reproduzida, adicione uma com o comando `!play`.")

    @bot.command(name='limpa')
    async def clear_queue(ctx):
        guild_id = ctx.guild.id
        if guild_id in queue:
            queue[guild_id] = []
            await ctx.send("A lista foi limpa.")
        else:
            await ctx.send("A lista já está vazia.")
