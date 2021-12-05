"""StarBoard Cog."""
from nextcord.ext import commands
from nextcord import Forbidden


class StarBoard(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)

        content = message.content if message.content else None
        file, files = None, None

        if payload.emoji.name == 'copy':

            if len(message.attachments) > 1:
                files = [await file.to_file() for file in message.attachments]

            elif message.attachments:
                file = await message.attachments[0].to_file()

            if not content and not file and not files:
                return print(f'StarBoard log: Sorry, message is empty\nhttps://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}')

            try:
                await user.send(content=content, file=file, files=files)
            except Forbidden:
                print(f'StarBoard log: Cannot send messages to {user.name}')


def setup(bot) -> None:
    bot.add_cog(StarBoard(bot))
