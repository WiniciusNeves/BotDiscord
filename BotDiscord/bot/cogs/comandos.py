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
    async def ajuda(self, ctx):  # Adicione 'self' como primeiro parâmetro
        page1 = discord.Embed(
            title="Comandos do Bot (Página 1)",
            description="Aqui estão os comandos disponíveis:",
            color=0x9400d3
        )
        page1.add_field(name="!ajuda", value="Mostra esta mensagem de ajuda.", inline=False)
        page1.add_field(name="!criador", value="Mostra informações sobre o criador do bot.", inline=False)
        page1.add_field(name="!biblioteca", value="Mostra o link para a biblioteca.", inline=False)
        page1.add_field(name="!v", value="Mostra a versão do bot.", inline=False)
        page1.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

        page2 = discord.Embed(
            title="Comandos do Bot (Página 2)",
            description="Aqui estão os comandos disponíveis para tocar músicas:",
            color=0x9400d3
        )
        page2.add_field(name="!play", value="Toca uma música.", inline=False)
        page2.add_field(name="!stop", value="Sai da chamada de voz.", inline=False)
        page2.add_field(name="!skip", value="Pula uma música.", inline=False)
        page2.add_field(name="!pause", value="Para de tocar.", inline=False)
        page2.add_field(name="!unpause", value="Retoma a reprodução.", inline=False)
        page2.add_field(name="!lista", value="Mostra a lista de músicas.", inline=False)
        page2.add_field(name="!limpar", value="Limpa a lista de músicas.", inline=False)
        page2.set_thumbnail(url="https://i.imgur.com/5Igo0sG.gif")

        pages = [page1, page2]

        message = await ctx.send(embed=pages[self.current_page])
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == "▶️":
                    self.current_page = (self.current_page + 1) % len(pages)
                elif str(reaction.emoji) == "◀️":
                    self.current_page = (self.current_page - 1) % len(pages)

                await message.edit(embed=pages[self.current_page])
                await message.remove_reaction(reaction, user)
            except TimeoutError:
                break

    @commands.command(name="criador")
    async def criador(self, ctx):
        embed = Embed(
            title="Aqui está o link para o criador:",
            description="Clique no botão para acessar.",
            color=0x9400d3
        )
        embed.set_thumbnail(url="https://i.pinimg.com/originals/2f/5c/c5/2f5cc5163100018a4e2670a01b77672e.gif")

        # Criar o botão
        button = Button(
            label="Visite o site do criador.",
            style=ButtonStyle.url,
            url="https://linktr.ee/winiciusneves"
        )

        # Adicionar o botão a uma 'view'
        view = View()
        view.add_item(button)

        # Enviar a mensagem com a embed e a 'view' que contém o botão
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
