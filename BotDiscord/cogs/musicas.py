import discord
import yt_dlp
import asyncio

from discord.utils import get
from discord.ext.commands import Bot
from discord.ui import View
from discord.ext import commands, tasks

class Musicas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.executing_commands = asyncio.Lock()

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': False,  
    }
    ffmpeg_options = {
        'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    yytdl = yt_dlp.YoutubeDL(ytdl_format_options)

    @staticmethod
    def search_youtube(arg):
        try:
            with Musicas.yytdl:
                info = Musicas.yytdl.extract_info(f"ytsearch:{arg}", download=False)
                if 'entries' in info:
                    videos = info['entries']
                    return [Musicas.extract_video_info(video) for video in videos if video]
                else:
                    return [Musicas.extract_video_info(info)]
        except Exception as e:
            print(f"Erro durante a pesquisa no YouTube: {e}")
            return []

    @staticmethod
    def extract_video_info(info):
        source = info.get('url', '')
        title = info.get('title', '')
        artist = info.get('artist') or info.get('uploader', 'Desconhecido')
        duration = info.get('duration', 0)
        thumbnail = info.get('thumbnail', '')

        print(f"URL: {source}, Title: {title}, Artist: {artist}, Duration: {duration}, Thumbnail: {thumbnail}")

        return {'source': source, 'title': title, 'artist': artist, 'duration': duration, 'thumbnail': thumbnail}
    
    @staticmethod
    def format_duration(duration_in_seconds):
        hours, remainder = divmod(duration_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        else:
            return f"{int(minutes):02}:{int(seconds):02}"

    @commands.command(name='play')
    async def play(self, ctx, *, search: str):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            embed = discord.Embed(
                title="Erro",
                description="Você não está em um canal de voz.",
                color=0x9400D3
            )
            await ctx.send(embed=embed)
            return

        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)


        if voice_client is None:
            await channel.connect()
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)


        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = []

        songs = Musicas.search_youtube(search)
        if songs:
            self.queue[ctx.guild.id].extend(songs)

            for song in songs:
                await ctx.send(f"**{song['title']}** de **{song['artist']}** foi adicionada à lista de reprodução.")
            if not voice_client.is_playing() and not voice_client.is_paused():
                await self.play_next(ctx)
        else:
            await ctx.send("Não encontrei a música ou playlist requisitada.")

    async def play_next(self, ctx):
        try:
            async with self.executing_commands:
                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                if voice_client and voice_client.is_connected():
                    if len(self.queue[ctx.guild.id]) > 0:

                        song = self.queue[ctx.guild.id][0]
                        current_position = len(self.queue[ctx.guild.id])  
                        self.queue[ctx.guild.id].pop(0)

                        source = song['source']
                        voice_client.play(discord.FFmpegPCMAudio(source, **Musicas.ffmpeg_options),
                                        after=lambda e: self.bot.loop.create_task(self.play_next(ctx)) if self.queue[ctx.guild.id] else None)

                        embed = discord.Embed(
                            title=f"Tocando agora - {song['title']}",
                            color=0x9400D3
                        )
                        embed.set_thumbnail(url=song['thumbnail'])

                        embed.add_field(name="Artista", value=song['artist'], inline=True)
                        embed.add_field(name="Duração", value=Musicas.format_duration(song['duration']), inline=True)
                        embed.add_field(name="Posição na fila", value=str(current_position), inline=True)

                        view = Musicas.MusicMenuView(ctx, song)
                        await ctx.send(embed=embed, view=view)
                    else:
                        await ctx.send("A lista de reprodução está vazia.")
                        if voice_client.is_connected():
                            await voice_client.disconnect()
                else:
                    await ctx.send()
        except Exception as e:
            print(f"Erro durante a reprodução da próxima música: {e}")
            voice_client = None 

    class MusicMenuView(discord.ui.View):
        def __init__(self, ctx, song, **kwargs):
            super().__init__(**kwargs)
            self.ctx = ctx
            self.song = song
            self.timeout = None 

        async def interaction_check(self, interaction):
            return interaction.user == self.ctx.author

        async def invoke_command(self, command_music):
            command = self.ctx.bot.get_command(command_music)
            if command:
                await self.ctx.invoke(command)

        @discord.ui.button(label='Pause', style=discord.ButtonStyle.primary, emoji='⏸️', custom_id='pause')
        async def pause(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'pause'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de pausa: {e}")

        @discord.ui.button(label='Unpause', style=discord.ButtonStyle.success, emoji='▶️', custom_id='unpause')
        async def unpause(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'unpause'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de despausar: {e}")

        @discord.ui.button(label='Skip', style=discord.ButtonStyle.secondary, emoji='⏭️', custom_id='skip')
        async def skip(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'skip'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de pular: {e}")

        @discord.ui.button(label='Lista', style=discord.ButtonStyle.success, emoji='📜', custom_id='lista')
        async def lista(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'lista'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de mostrar a lista: {e}")

        @discord.ui.button(label='Limpar', style=discord.ButtonStyle.grey, emoji='🗑️', custom_id='limpar_command')
        async def limpa(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'limpar'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de limpar a lista: {e}")

        @discord.ui.button(label='Sair', style=discord.ButtonStyle.danger, emoji='🚪', custom_id='stop')
        async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                command_name = 'stop'
                await self.invoke_command(command_name)
                await interaction.response.defer()
            except Exception as e:
                print(f"Erro durante a interação de parar: {e}")





    @commands.command(name='skip')
    async def skip(self, ctx):
        try:
            async with self.executing_commands:
                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                if voice_client and voice_client.is_playing():
                    voice_client.stop()
                    embed = discord.Embed(
                        title="Música pulada",
                        description="A próxima música será reproduzida em breve.",
                        color=0x9400d3
                    )
                    embed.set_thumbnail(url="https://gifs.eco.br/wp-content/uploads/2022/09/gifs-de-musica-9.gif")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Nenhuma música está sendo tocada no momento.")
        except Exception as e:
            print(f"Erro durante o comando 'skip': {e}")

    @commands.command(name='stop')
    async def stop_music(self, ctx):
        try:
            async with self.executing_commands:
                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
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
        except Exception as e:
            print(f"Erro durante o comando 'stop': {e}")

    @commands.command(name='pause')
    async def pause_music(self, ctx):
        try:
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
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
        except Exception as e:
            print(f"Erro durante o comando 'pause': {e}")

    @commands.command(name='unpause')
    async def unpause_music(self, ctx):
        try:
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
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
        except Exception as e:
            print(f"Erro durante o comando 'unpause': {e}")

    @commands.command(name='lista')
    async def show_queue(self, ctx):
        try:
            guild_id = ctx.guild.id
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)  

            if guild_id in self.queue and len(self.queue[guild_id]) > 0:
                current_position = 1
                queue_list = []

                for index, song in enumerate(self.queue[guild_id]):
                    queue_list.append(
                        f"{index + 1}. **{song['title']}** (Posição na fila: {current_position})"
                    )
                    current_position += 1

                current_song = (
                    f"Próxima música tocando: **{self.queue[guild_id][0]['title']}**"
                    if voice_client and voice_client.is_playing()
                    else "Não há música sendo reproduzida no momento."
                )

                


                next_song = (
                    f"Próxima música a tocar: **{self.queue[guild_id][1]['title']}**"
                    if len(self.queue[guild_id]) > 1
                    else "Não há próxima música na fila."
                )

                queue_embed = discord.Embed(
                    title="Lista de Reprodução",
                    description="\n".join(queue_list) + f"\n\n{current_song}\n{next_song}",
                    color=0x9400d3
                )
                await ctx.send(embed=queue_embed)

            else:
                await ctx.send("Não há músicas na lista de reprodução. Adicione uma com o comando `!play`.")
        except Exception as e:
            print(f"Erro durante o comando 'lista': {e}")

    @commands.command(name='limpar')
    async def clear_queue(self, ctx):
        try:
            guild_id = ctx.guild.id
            if guild_id in self.queue and self.queue[guild_id]:
                self.queue[guild_id] = []
                await ctx.send("A lista foi limpada.")
            else:
                await ctx.send("A lista já está vazia.")
        except Exception as e:
            print(f"Erro durante o comando 'limpar': {e}")

async def setup(bot):
    await bot.add_cog(Musicas(bot))