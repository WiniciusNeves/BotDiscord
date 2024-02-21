# cogs/comandos.py

import discord
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import Button, View
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_page = 0

    @commands.command(name="ajuda")
    async def ajuda(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Olá. Poro chegou para ajudar!",
            description="Confira abaixo a lista de comandos que Poro separou para você:",
            color=0x9400d3
        )
        embed.add_field(name="!play", value= "!play (link/nome do Youtube aqui) para tocar uma música.", inline=False)
        embed.add_field(name="!stop", value= "Remove o bot de música da sala.", inline=False)
        embed.add_field(name="!pause", value= "Pula uma música.", inline=False)
        embed.add_field(name="!unpause", value= "Pausa o bot de música.", inline=False)
        embed.add_field(name="!lista", value= "Mostra a lista de músicas.", inline=False)
        embed.add_field(name="!limpar", value= "Limpa a lista de reprodução.", inline=False)
        embed.add_field(name="!biblioteca", value= "Mostra a biblioteca da guilda.", inline=False)
        embed.add_field(name="!criador", value= "Mostra informações sobre o criador do bot.", inline=False)
        embed.add_field(name="!v", value= "Mostra a versão do bot.", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/312655199678365707/a_feeb488d9aa642a2979d54803fac65ea.gif")

        await ctx.send(embed=embed)


    @commands.command(name="criador")
    async def criador(self, ctx):
        embed = Embed(
            title="Aqui está o link para o criador:",
            description="Clique no botão para acessar.",
            color=0x9400d3
        )
        embed.set_thumbnail(url="https://i.pinimg.com/originals/2f/5c/c5/2f5cc5163100018a4e2670a01b77672e.gif")

        button = Button(
            label="Visite o site do criador.",
            style=ButtonStyle.url,
            url="https://linktr.ee/winiciusneves"
        )

        view = View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

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
