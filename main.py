#!/usr/bin/env python
"""TVP bot discord."""
from datetime import datetime
from discord.ext import commands, tasks
from itertools import cycle
import config
import discord
import sqlite3
import os
import sys  # sys для вывода лога бота в консоль heroku


bot = commands.Bot(command_prefix=config.PREFIX,
                   intents=discord.Intents.all())
status = cycle(['.help', 'https://www.thevenusproject.com',
               'https://designing-the-future.org'])


@bot.event
async def on_ready():
    change_status.start()
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'✅ {current_time} Бот запущен')

    global base, cur
    base = sqlite3.connect(config.DB_NAME)
    cur = base.cursor()
    if base:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f'✅ {current_time} DB connected')


@bot.command(aliases=['l'])
@commands.has_permissions(administrator=True)
async def load(ctx, ext):
    """Подключает модуль к боту."""
    bot.load_extension(f'cogs.{ext}')
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'✅ {current_time} {ext} loaded')
    await ctx.send(f'✅ {ctx.author.mention} `{ext}` is loaded')


@bot.command(aliases=['u'])
@commands.has_permissions(administrator=True)
async def unload(ctx, ext):
    """Отключает модуль от бота."""
    bot.unload_extension(f'cogs.{ext}')
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'✅ {current_time} {ext} unloaded')
    await ctx.send(f'✅ {ctx.author.mention} `{ext}` is unloaded')


@bot.command(aliases=['r'])
@commands.has_permissions(administrator=True)
async def reload(ctx, ext):
    """Перезагружает модуль бота."""
    bot.unload_extension(f'cogs.{ext}')
    bot.load_extension(f'cogs.{ext}')
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'✅ {current_time} {ext} reloaded')
    await ctx.send(f'✅ {ctx.author.mention} `{ext}` is reloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.errors.MissingPermissions):
        msg = f'Sorry {ctx.message.author.mention}, you do not have permissions to do that!'
        await ctx.send(msg)

    print(ctx.command.name + " was invoked incorrectly.")
    print(error)


@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

bot.run(config.TOKEN)
sys.stdout.flush()
