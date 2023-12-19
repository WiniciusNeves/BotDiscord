
from discord.ext import commands,tasks
import discord
import logging
import os
import asyncio
from dotenv import load_dotenv

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

@bot.command()
@commands.is_owner() 
async def sync(ctx,guild=None):
    if guild == None:
        await bot.tree.sync()
    else:
        await bot.tree.sync(guild=discord.Object(id=int(guild)))
    await ctx.send("**Sincronizado!** ")

async def main():
    async with bot:
        for filename in os.listdir('c:\\Users\\Winic\\Desktop\\project\\bot\\cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')

             
        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

asyncio.run(main())
