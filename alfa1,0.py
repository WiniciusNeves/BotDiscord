import discord
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
intents = discord.Intents.default()
intents.voice_states = True

@bot.event
async def on_ready():
    print(f"pronto!, estou conectado como {bot.user}")

@bot.command(name="ajuda")
async def send_message(ctx):
    # Create an embed object
    embed = discord.Embed(
        title="Comandos do Bot",
        description="Aqui estão os comandos disponíveis:",
        color=0x9400d3  # Green color
    )
    # Add commands to the embed
    embed.add_field(name="!ajuda", value="Mostra esta mensagem de ajuda.", inline=False)
    embed.add_field(name="!criador", value="Mostra informações sobre o criador do bot.", inline=False)
    embed.add_field(name="!biblioteca", value="Mostra o link para a biblioteca.", inline=False)
    embed.add_field(name="!v", value="Mostra a versão do bot.", inline=False)
    # Set the GIF image
    embed.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

    # Send the embed in the current context
    await ctx.send(embed=embed)

@bot.command(name="criador")
async def send_message(ctx):
    embed = discord.Embed(
        title="Aqui esta o link para o criador:",
        description="https://linktr.ee/winiciusneves",
        color=0x9400d3  # Green color
    )
    embed.set_thumbnail(url="https://i.pinimg.com/originals/2f/5c/c5/2f5cc5163100018a4e2670a01b77672e.gif")
    await ctx.send(embed=embed)

@bot.command(name="biblioteca")
async def send_message(ctx):
    embed = discord.Embed(
        title="Biblioteca do Discord",
        description="Clique no link abaixo para acessar a biblioteca do Discord:",
        color=0x9400d3  # Dodger blue color
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1179409324611747921/1184231893554696202/fly-logo-60x60p.png?ex=658b38e5&is=6578c3e5&hm=7d4f4f1860e4cfed7e3e18a477c22ae46679b16990d6d277149fe497cdf0a6a0&")
    embed.add_field(name="Link da Biblioteca", value="[Clique aqui](https://discord.gg/mfZ2GuT5kg)", inline=False)
    
    await ctx.send(embed=embed)  

@bot.command(name="v")
async def send_message(ctx):
    response = "versão: 1.0"
    await ctx.send(response)



bot.run("TOken aqui")
