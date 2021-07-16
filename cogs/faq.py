"""Cog module: Faq."""
import discord
from discord.ext import commands
import random
import json
import sqlite3
import aiocron
import config
from datetime import datetime
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle
)


class Faq(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(self.bot)
        self.base = sqlite3.connect(config.DB_NAME)
        self.cur = self.base.cursor()

        # @aiocron.crontab("*/1 * * * *")
        @aiocron.crontab("0 10 * * *")  # Каждый день в 8 утра по МСК
        async def on_morning():
            data = self.get_faq()
            if data:
                msg = f"**♦ Рубрика «Вопрос дня»♦**\n**{data[1]}**\n{data[2]}"
                msg = (msg[:1998] + '..') if len(msg) > 2000 else msg
                channel = self.bot.get_channel(config.QDAY_CHANNEL_ID)
                id = int(data[0])
                await channel.send(
                    file=discord.File(r'./faq/audio/Faq#{}.mp3'.format(id)),
                    content=msg,
                    components=[
                        Button(
                            style=ButtonStyle.URL,
                            label="FAQ",
                            url=f"https://designing-the-future.org/the-venus-project-faq/#q{id}"),
                    ])
            else:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(
                    f'❌ {current_time} Что-то пошло не так. Вопрос дня не найден.')

    def get_faq(self):
        data = False
        r = self.cur.execute("SELECT * FROM answer_ids").fetchone()
        if r is not None:
            load = json.loads(r[0])
            if len(load) > 0:
                id = random.choice(load)
                load.remove(id)
                dump = json.dumps(load)

                self.cur.execute(f"UPDATE answer_ids SET `count`='{dump}'")
                self.base.commit()

                data = self.get_faq_by_id(id)

            else:
                count = self.count_all_questions()
                load = list(range(1, count+1))

                id = random.choice(load)
                load.remove(id)
                dump = json.dumps(load)

                self.cur.execute(f"UPDATE answer_ids SET `count`='{dump}'")
                self.base.commit()

                data = self.get_faq_by_id(id)

        return data

    def count_all_questions(self):
        r = self.cur.execute("SELECT COUNT(*) FROM faq").fetchone()
        return r[0]

    def get_faq_by_id(self, id):
        data = False
        r = self.cur.execute(
            f"SELECT id, q, a FROM faq WHERE id={id}").fetchone()
        if r is not None:
            data = r
        return data

    @commands.command(aliases=['фак', 'чаво'])
    async def faq(self, ctx, id=None):
        """Посылает в ФАК."""
        rnd_list = ['r', 'rnd', 'random', 'рнд', 'рандом']
        if id is None:
            rnd_list_text = '|'.join(rnd_list)
            return await ctx.send(f"```.faq <id:int> - введите номер вопроса\n.faq <{rnd_list_text}:str> - или показать рандомный```")
        # await ctx.send('Test')
        # await ctx.send(random.choice(list))
        try:
            id = int(id)
        except ValueError:
            if id in rnd_list:
                count = self.count_all_questions()
                total_questions = list(range(1, count+1))
                id = random.choice(total_questions)

        data = self.get_faq_by_id(int(id))
        if data:
            # await ctx.send(f"Вы хотите ответ на {id} вопрос?")
            msg = f"**{data[1]}**\n{data[2]}"
            msg = (msg[:1998] + '..') if len(msg) > 2000 else msg
            await ctx.send(
                file=discord.File(r'./faq/audio/Faq#{}.mp3'.format(id)),
                content=msg,
                components=[
                    Button(
                        style=ButtonStyle.URL,
                        label="FAQ",
                        url=f"https://designing-the-future.org/the-venus-project-faq/#q{id}"),
                ])
        else:
            await ctx.send(f'{ctx.author.mention} Ответа на вопрос с номером `{id}` не найдено, попробуйте ещё раз.')


def setup(bot):
    bot.add_cog(Faq(bot))
