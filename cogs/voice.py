"""
Cog ext: Voice
"""
from discord.ext import commands
import config

class Voice(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.channels = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after) -> None:
        """Обработка события изменения состояния голосовых каналов."""
        try:
            if after.channel.id in config.VOICE_TRIGGER:
                # TODO
                # Log: user entered the channel
                category = after.channel.category
                if member.id in self.channels:
                    if category.id in self.channels[member.id]:
                        channel_id = self.channels[member.id][category.id]
                        channel = self.bot.get_channel(channel_id)
                    else:
                        channel = await category.create_voice_channel(f"{member.name}'s room")
                        await channel.set_permissions(member, connect=True, move_members=True, manage_channels=True)
                        if member.id in self.channels:
                            self.channels[member.id].update(
                                {category.id: channel.id})
                        else:
                            self.channels[member.id] = {
                                category.id: channel.id}

                else:
                    channel = await category.create_voice_channel(f"{member.name}'s room")
                    await channel.set_permissions(member, connect=True, move_members=True, manage_channels=True)
                    self.channels[member.id] = {category.id: channel.id}

                await member.move_to(channel)

                def check(x, y, z):
                    return len(channel.members) == 0

                await self.bot.wait_for('voice_state_update', check=check)
                await channel.delete()
                self.channels[member.id].pop(category.id, None)
                if not self.channels[member.id]:
                    del self.channels[member.id]

        except Exception:
            # TODO
            # Log: user leave the channel
            pass


def setup(bot) -> None:
    bot.add_cog(Voice(bot))
