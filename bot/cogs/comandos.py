# cogs/comandos.py

import discord
from discord.ext import commands
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ajuda")
    async def ajuda(self, ctx):
        page1 = discord.Embed(
            title="Olá. Poro chegou para ajudar!",
            description="Confira abaixo a lista de comandos que Poro separou para você:",
            color=0x9400d3
        )
        page1.add_field(name="!play", value="!play (link do Youtube aqui) para tocar uma música.", inline=False)
        page1.add_field(name="!stop", value="Remove o bot de música da sala.", inline=False)
        page1.add_field(name="!skip", value="Pula uma música.", inline=False)
        page1.add_field(name="!pause", value="Pausa o bot de música.", inline=False)
        page1.add_field(name="!unpause", value="Despausa o bot de música.", inline=False)
        page1.add_field(name="!lista", value="Mostra a lista de músicas.", inline=False)
        page1.add_field(name="!limpar", value="Limpa a lista de músicas.", inline=False)

        page1.add_field(name="!biblioteca", value="Mostra o link para a biblioteca.", inline=False)
        page1.add_field(name="!criador", value="Mostra informações sobre o criador do bot.", inline=False)
        page1.add_field(name="!v", value="Mostra a versão do bot.", inline=False)
        page1.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

        await ctx.send(embed=page1)

    @commands.command(name="criador")
    async def criador(self, ctx):
        embed = discord.Embed(
            title="Aqui está o link para o criador:",
            description="https://linktr.ee/winiciusneves",
            color=0x9400d3
        )
        embed.set_thumbnail(url="https://i.pinimg.com/originals/2f/5c/c5/2f5cc5163100018a4e2670a01b77672e.gif")
        await ctx.send(embed=embed)

    @commands.command(name="biblioteca")
    async def biblioteca(self, ctx):
        embed = discord.Embed(
            title="Biblioteca da FLY Tale",
            description="Clique no link abaixo para acessar a biblioteca da guilda FLY Tale.",
            color=0x9400d3
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1179409324611747921/1184231893554696202/fly-logo-60x60p.png?ex=658b38e5&is=6578c3e5&hm=7d4f4f1860e4cfed7e3e18a477c22ae46679b16990d6d277149fe497cdf0a6a0&")
        embed.add_field(name="Link da Biblioteca", value="[Clique aqui](https://discord.gg/mfZ2GuT5kg)", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="v")
    async def versao(self, ctx):
        response = "versão: 2.5"
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Commands(bot))
