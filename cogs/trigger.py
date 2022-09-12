"""
Cog: Trigger
Срабатывает на слова-триггеры в сообщениях дискорда из списка в гугл-таблице.
"""
import io
import json
import re

import aiohttp
import config
import gspread
from nextcord import Embed, File, Message
from nextcord.ext import commands


class Trigger(commands.Cog):
    def __init(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        # Реагировать только на сообщения пользователей
        if not message.author.bot:
            gc = gspread.service_account_from_dict(config.GSPREAD_CREDENTIALS)
            sh = gc.open_by_key(config.SHEET_UID)

            all_values = sh.sheet1.get_all_values()
            all_values.pop(0)

            msg = message.content
            msg_lower = message.content.lower()
            answer = None
            for row in all_values:
                (
                    trigger,
                    ignoreCase,
                    includes,
                    content,
                    embed,
                    attachments,
                    note,
                    random,
                    count,
                ) = row
                string = msg

                if ignoreCase and includes:
                    if ignoreCase == "TRUE":
                        trigger = trigger.lower()
                        string = msg_lower
                    # Полное совпадение
                    if includes == "FALSE" and trigger == string:
                        answer = [content, embed, attachments]
                        break
                    # Частичное совпадение
                    if includes == "TRUE" and trigger in string:
                        answer = [content, embed, attachments]
                        break

                # Если пусты оба, значит это регулярное выражение
                else:
                    result = re.match(trigger, msg_lower, re.IGNORECASE)
                    if result:
                        answer = [content, embed, attachments]
                        break

            if answer:
                file = embed = None
                content, embed_str, url = answer

                if embed_str:
                    embed_dict = json.loads(embed_str)
                    embed = Embed.from_dict(embed_dict)

                if url:
                    filename = url.rsplit("/", 1)[-1]
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status != 200:
                                print("Could not download file...")

                            data = io.BytesIO(await resp.read())
                            file = File(data, filename)

                await message.reply(content=content, file=file, embed=embed)


def setup(bot) -> None:
    bot.add_cog(Trigger(bot))
