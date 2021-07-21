"""Cog module: Intelligent bump."""
from discord.ext import commands, tasks
import time
import config


class Bump(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._tasks = []
        self.msg_list = []
        self.time_diff = 120  # seconds

    @commands.Cog.listener('on_message')
    async def intelbump(self, message):

        if message.channel.id == config.CH_BUMP:
            if message.embeds:

                msg = None
                embed_data = message.embeds[0].to_dict()

                if 'description' in embed_data and 'Server bumped' in embed_data['description']:
                    msg = '```!bump```'
                if 'title' in embed_data and 'Сервер Up' in embed_data['title']:
                    msg = '```S.up```'

                if msg:
                    now = time.time()
                    if self._tasks:
                        diff = now - self.msg_list[0][0]
                        if diff < self.time_diff:
                            self.msg_list[0] = [now, '\n'.join(
                                [self.msg_list[0][1], msg])]
                            task = self._tasks[0]
                            task.restart()
                        else:
                            self.msg_list += [[now, msg]]
                            self.task_launcher()
                    else:
                        self.msg_list = [[now, msg]]
                        self.task_launcher()

    async def return_pass(self):
        """Returns pass"""
        pass

    # The `args` are the arguments passed into the loop
    def task_launcher(self, *args, **interval):
        """Creates new instances of `tasks.Loop`"""
        new_task = tasks.loop(hours=4, count=1)(self.return_pass)
        new_task.after_loop(self.after_task)
        new_task.start()
        self._tasks.append(new_task)

    async def after_task(self):
        """Task after loop"""
        if self._tasks[0].is_being_cancelled():
            return
        channel = self.bot.get_channel(config.CH_BUMP)
        msg = self.msg_list.pop(0)
        await channel.send(f'Эй <@&{config.ROLE_BUMP}> пора вводить команды:\n{msg[1]}')
        self._tasks.pop(0)


def setup(bot):
    bot.add_cog(Bump(bot))
