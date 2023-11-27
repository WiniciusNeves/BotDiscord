import discord
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"pronto!, estou conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "palavrao" in message.content:
        await message.channel.send(f"Por favor , {message.author.name}, nao use palavrao")

        await message.delete()

        await bot.process_commands(message)

@bot.command(name="oi")
async def send_message(ctx):
    name = ctx.author.name

    response = "ola,"+ name

    await ctx.send(response)  

@bot.command(name="criador")
async def send_message(ctx):
    criador = "@Winicius Neves" 
    response = "Opa eu sou o criador "+criador+" desse bot e muito mais, seja bem vindo"

    await ctx.send(response)



bot.run("seu tokem aqui")
