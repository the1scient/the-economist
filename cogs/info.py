import time
import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from utils import default


class Informacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("economist.json")
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Verificar latência do BOT. """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong! Respondido <:verificacao:732675855440019538>")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=['joinme', 'join', 'botinvite', 'convidar', 'convite'])
    async def invite(self, ctx):
        """ Convide-me para o seu servidor :smile: """
        user = ctx.message.author
        if not user:
            await ctx.send(f"Algo deu errado ao tentar achar tal usuário **{user}**")

        try:
            await user.send(f"**{ctx.author.name}** Olá! Obrigado pela atenção, sinta-se livre para me testar/usar em seu servidor! Aqui está seu link: \n<{discord.utils.oauth_url(self.bot.user.id)}>")
            await ctx.send(f"✉️ Enviei meu link de convite para **{user}**")
        except discord.Forbidden:
            await ctx.send("DM's bloqueados para este usuário.")

   

    @commands.command(aliases=['servidor', 'feedbackserver'])
    async def botserver(self, ctx):
        """ Get an invite to our support server! """
        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 86484642730885120:
            return await ctx.send(f"**Here you go {ctx.author.name} 🍻\n<{self.config.botserver}>**")

        await ctx.send(f"**{ctx.author.name}** this is my home you know :3")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ Sobre o BOT """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embedColour = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Última inicialização", value=default.timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Dono{'' if len(self.config.owners) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.owners]),
            inline=True)
        embed.add_field(name="Utilizando atualmente", value="discord.py", inline=True)
        embed.add_field(name="Total de servidores", value=f"{len(ctx.bot.guilds)} ( média: {avgmembers} usuários/servidor )", inline=True)
        embed.add_field(name="Comandos disponíveis", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="[BETA] RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ Sobre **{ctx.bot.user}** | **{self.config.version}**", embed=embed)

        @commands.command(aliases='ajuda')
        async def help(self, ctx):
            author = ctx.message.author

            embed = discord.Embed(colour=embedColour)
            embed.set_thumbnail(url=ctx.bot.user.avatar_url)
            embed.add_field(name="Comando de teste", value="test macaco")
            await ctx.send("Enviei os comandos no seu privado.")
            await author.send(embed)
            


def setup(bot):
    bot.add_cog(Informacao(bot))
