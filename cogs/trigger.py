"""
Cog: Trigger
Срабатывает на слова-триггеры в сообщениях дискорда из списка в гугл-таблице.
"""
import io
import json
import re
from datetime import datetime

import aiohttp
import config
import gspread
import pytz
from gspread import Worksheet
from nextcord import Embed, File, Member, Message
from nextcord.ext import commands

TRIGGER_PREFIX = "+ "


class Trigger(commands.Cog):
    def __init(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        # Only Users messages
        if not message.author.bot:
            sh = await self.get_sheet()

            all_values = sh.get_all_values()
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

                    if (includes == "FALSE" and trigger == string) or (
                        includes == "TRUE" and trigger in string
                    ):
                        answer = [content, embed, attachments]
                        break

                # RegExp
                else:
                    result = re.match(trigger, msg_lower, re.IGNORECASE)
                    if result:
                        answer = [content, embed, attachments]
                        break

            if answer:
                file = embed = files = None
                content, embed_str, urls = answer

                if embed_str:
                    embed_dict = json.loads(embed_str)
                    embed = Embed.from_dict(embed_dict)

                if urls:
                    urls = urls.split("\n")
                    length = len(urls)
                    if length == 1:
                        filename = urls[0].rsplit("/", 1)[-1]
                        async with aiohttp.ClientSession() as session:
                            async with session.get(urls[0]) as resp:
                                data = io.BytesIO(await resp.read())
                                file = File(data, filename)
                    if length > 1:
                        files = []
                        for url in urls:
                            filename = url.rsplit("/", 1)[-1]
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as resp:
                                    data = io.BytesIO(await resp.read())
                                    files.append(File(data, filename))

                await message.reply(
                    content=content, files=files, file=file, embed=embed
                )

                # TODO counter

        # Add trigger
        if message.reference is not None and message.content.startswith(
            TRIGGER_PREFIX
        ):
            # If User more than 90 days in this server
            if (
                isinstance(message.author, Member)
                and message.author.joined_at
                and (datetime.now(tz=pytz.UTC) - message.author.joined_at).days
                >= 90
            ):
                # If not exist
                sh = await self.get_sheet()
                trigger = message.content.lstrip(TRIGGER_PREFIX).strip()
                cell = sh.find(trigger)  # Find a cell with exact string value

                if not cell:
                    msg = (
                        await message.channel.fetch_message(
                            message.reference.message_id
                        )
                        if message.reference.message_id
                        else None
                    )

                    if msg:
                        ignoreCase = True
                        includes = False
                        content = msg.content
                        attachments = (
                            "\n".join(
                                [
                                    attachment.url
                                    for attachment in msg.attachments
                                ]
                            )
                            if msg.attachments
                            else None
                        )
                        embed = (
                            msg.embeds.pop(0).to_dict()
                            if msg.embeds
                            and not msg.content
                            and not attachments
                            else None
                        )
                        note = "Добавил " + message.author.name

                        data = [
                            trigger,
                            ignoreCase,
                            includes,
                            content,
                            embed,
                            attachments,
                            note,
                        ]
                        sh.append_row(data)

                        await message.delete(delay=5)
                        await message.reply(
                            content=f"Триггер `{trigger}` успешно создан",
                            delete_after=5,
                        )
                else:
                    await message.delete(delay=5)
                    await message.reply(
                        content=f"Триггер `{trigger}` уже создан",
                        delete_after=5,
                    )

    async def get_sheet(self) -> Worksheet:
        gc = gspread.service_account_from_dict(config.GSPREAD_CREDENTIALS)
        sh = gc.open_by_key(config.SHEET_UID)
        return sh.sheet1


def setup(bot) -> None:
    bot.add_cog(Trigger(bot))
