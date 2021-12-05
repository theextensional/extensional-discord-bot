"""Cog module: Moderation."""
from nextcord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def clear(self, ctx, amount=0):
        """Удаляет указанное количество сообщений."""
        amount = int(amount)
        await ctx.channel.purge(limit=amount+1)


def setup(bot):
    bot.add_cog(Moderation(bot))
