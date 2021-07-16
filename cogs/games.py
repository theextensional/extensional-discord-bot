"""Cog module: Games."""
from discord.ext import commands
import random


class Games(commands.Cog, name='Развлечения'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball', aliases=['8b', 'шар'])
    async def _8ball(ctx, *, question):
        """Задай вопрос магическому шару."""
        response = [
            'Бесспорно',
            'Предрешено',
            'Никаких сомнений',
            'Определённо да',
            'Можешь быть уверен',
            'Мне кажется — «да»',
            'Вероятнее всего',
            'Хорошие перспективы',
            'Знаки говорят — «да»',
            'Пока не ясно, попробуй снова',
            'Спроси позже',
            'Лучше не рассказывать',
            'Сейчас нельзя подсказать',
            'Сконцентрируйся и спроси опять',
            'Даже не думай',
            'Мой ответ — «нет»',
            'По моим данным — «нет»',
            'Перспективы не очень хорошие',
            'Весьма сомнительно'
        ]
        await ctx.send(f'Вопрос: {question}\nОтвет: {random.choice(response)}')


def setup(bot):
    bot.add_cog(Games(bot))
