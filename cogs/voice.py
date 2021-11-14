"""
Cog ext: Voice
"""
from discord.ext import commands
import config
import firebase_admin
from firebase_admin import db
import json


class Voice(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        #  подключаем firebase
        cred_obj = firebase_admin.credentials.Certificate(json.loads(config.FIREBASE_CERTIFICATE))
        default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': config.DB_URL
        })
        self.ref = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after) -> None:
        """Обработка события изменения состояния голосовых каналов."""
        self.ref = self.ref if self.ref else db.reference(f"server/{member.guild.id}/channels")
        
        if before.channel:
            if self.ref.child(str(before.channel.id)).get() and len(before.channel.members) == 0:
                await before.channel.delete()
                self.ref.child(str(before.channel.id)).set({})
        
        if after.channel:
            if after.channel.id in config.VOICE_TRIGGER:
                # TODO
                # Log: user entered the channel
                category = after.channel.category
                channel = await category.create_voice_channel(f"{member.name}'s room")
                await channel.set_permissions(member, connect=True, move_members=True, manage_channels=True)
                self.ref.update({channel.id: True})
                await member.move_to(channel)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.remove_empty_channels()

    async def remove_empty_channels(self) -> None:
        ref = db.reference("/server")
        servers = ref.get()
        if not servers:
            return
        for server_id, channel_dict in servers.items():
            for channel_id in channel_dict["channels"]:
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    if not channel.members:
                        await channel.delete()
                        ref.child(str(server_id)).child("channels").child(str(channel_id)).set({})
                else:
                    ref.child(str(server_id)).child("channels").child(str(channel_id)).set({})



def setup(bot) -> None:
    bot.add_cog(Voice(bot))
