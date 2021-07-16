"""Cog module: General."""
from discord.ext import commands
import discord
import random


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Проверка пинга."""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def test(self, ctx):
        """Проверка бота, живой ли ещё."""
        list = [
            'https://tenor.com/view/cpr-cats-staying-alive-gif-7208628',
            'https://tenor.com/view/im-not-dead-i-survived-its-not-over-not-the-end-comeback-gif-14693671',
            'https://tenor.com/view/daddys-home2-daddys-home2gifs-will-ferrell-im-alive-revived-gif-9694359',
            'https://tenor.com/view/surprise-prank-alive-gif-10489120',
            'https://tenor.com/view/friends-ross-geller-david-schwimmer-im-still-alive-gif-15694188',
            'https://tenor.com/view/jay-and-silent-bob-it-is-a-great-day-to-be-alive-swaying-sway-gif-15828052',
            'https://tenor.com/view/cat-kitten-cute-adorable-paw-gif-17704239',
            'https://tenor.com/view/alive-are-you-alive-gif-18874177',
            'https://tenor.com/view/dog-pet-wake-up-bed-morning-gif-5196960',
            'https://tenor.com/view/poka-paka-fuck-nadoelo-nyet-gif-5487419'
        ]
        await ctx.send(random.choice(list))

    @commands.command(name='toprole', aliases=['top_role'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Command which shows the members Top Role."""
        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')


def setup(bot):
    bot.add_cog(General(bot))
