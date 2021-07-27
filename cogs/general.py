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
        """Проверка пользователей, живые ли ещё."""
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
            'https://tenor.com/view/poka-paka-fuck-nadoelo-nyet-gif-5487419',
            'https://tenor.com/view/cat-ready-cool-cat-ready-im-ready-sunglass-cute-gif-13422475',
            'https://tenor.com/view/eyeroll-kitten-snl-gif-22362392',
            'https://tenor.com/view/elephant-hug-cuddle-friends-gif-11770357',
            'https://tenor.com/view/hugging-day-national-hugging-day-hug-embrace-bromance-gif-11138412',
            'https://tenor.com/view/cats-ear-bite-spooning-neko-cuddle-gif-12221450',
            'https://tenor.com/view/ok-cat-smile-creepy-gif-20018005',
            'https://tenor.com/view/grilla-yes-hell-thumbs-up-grills-gif-10889686',
            'https://tenor.com/view/crazy-old-man-hammer-gif-13923772',
            'https://tenor.com/view/pug-pug-life-halloween-dog-costumes-gif-10966471',
            'https://tenor.com/view/angry-panda-mascot-mad-%E7%8B%82%E8%BA%81-gif-3456638',
            'https://tenor.com/view/i-see-no-problem-here-crazy-eyes-gif-12788383',
            'https://tenor.com/view/sassy-cats-angry-mad-ok-gif-9934420',
            'https://tenor.com/view/cute-cat-funny-scared-gif-14753822',
            'https://tenor.com/view/mash-alan-alda-hawkeye-pierce-nail-file-listening-gif-5070149',
            'https://tenor.com/view/dbfz-gif-21452746',
            'https://tenor.com/view/futurama-serious-stare-suspicious-gif-5319823',
            'https://tenor.com/view/fry-futurama-time-frozen-timelapse-gif-4674694',
            'https://tenor.com/view/futurama-hypnotoad-hypnotic-hypno-all-hail-hypnotoad-gif-3690710',
            'https://tenor.com/view/futurama-futurama-fry-futurama-bender-bender-and-fry-water-fight-gif-20974416',
            'https://tenor.com/view/viralhog-cute-cat-tounge-tounge-out-tounge-playing-gif-12380813',
            'https://tenor.com/view/cat-broken-cat-cat-drinking-cat-licking-cat-air-gif-20661740',
            'https://tenor.com/view/gtfoh-move-it-bye-kick-cat-gif-14440241',
            'https://tenor.com/view/hello-kitty-miss-you-hello-kitty-cat-gif-14510827',
            'https://tenor.com/view/shaq-cat-shaquille-o-neal-shaq-shake-shaq-shimmy-gif-4882069',
            'https://tenor.com/view/cat-high-five-cool-gif-9379608',
            'https://tenor.com/view/cat-funny-cat-scratch-itchy-gif-5673230',
            'https://tenor.com/view/yes-sir-ana-kendrick-salute-wink-sir-yes-sir-gif-12726647',
            'https://tenor.com/view/jump-cat-beanie-bag-plop-gif-15507441',
            'https://tenor.com/view/sleepy-doze-off-subway-fall-tired-gif-11265004',
            'https://tenor.com/view/cat-sleepy-sleeping-kitten-gif-8836425',
            'https://tenor.com/view/licky-pout-seductive-pretty-gif-15792279'
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
