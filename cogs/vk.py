"""
Cog ext: VK
"""
from discord.ext import commands, tasks
from discord import Embed
import requests
import json
import os.path
from random import randrange
import config


class VK(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.author = self.get_author()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.get_last_vk_post.start()

    @tasks.loop(minutes=5)
    async def get_last_vk_post(self):
        """Get new VK posts."""
        items = sorted(self.vk_wall_get(),
                       key=lambda k: k.get('date', 0), reverse=True)

        first_item_time = items[0]['date']
        last_post_time = self.vk_posts_data_read()

        if last_post_time < first_item_time:
            self.vk_posts_data_write(first_item_time)
            await self.vk_post_send(items[0])

    def vk_wall_get(self) -> list:
        """Get VK posts from the wall of group."""
        params = {'access_token': config.VK_API_TOKEN,
                  'v': config.VK_API_VERSION,
                  'domain': config.VK_DOMAIN,
                  'count': 3}
        response = requests.get('https://api.vk.com/method/wall.get', params)

        return response.json()['response']['items']

    @commands.command()
    async def vkpost(self, ctx, id: int = None) -> None:
        """Get VK post by id and send to channel."""
        item = self.get_by_id(int(id)) if id else self.vk_wall_get_rnd()
        await self.vk_post_send(item)

    def get_by_id(self, id: int) -> list:
        """Get VK post by id."""
        params = {'access_token': config.config.VK_API_TOKEN,
                  'v': config.VK_API_VERSION,
                  'domain': config.VK_DOMAIN,
                  'posts': f"-{self.author['id']}_{int(id)}"}

        response = requests.get(
            'https://api.vk.com/method/wall.getById', params)

        return response.json()['response'][0]

    def vk_wall_get_rnd(self) -> dict:
        """Получает рандомный пост VK со стены группы."""
        offset = randrange(int(self.vk_wall_count()))

        params = {'access_token': config.config.VK_API_TOKEN,
                  'v': config.VK_API_VERSION,
                  'domain': config.VK_DOMAIN,
                  'count': 1,
                  'offset': offset}

        response = requests.get('https://api.vk.com/method/wall.get', params)

        return response.json()['response']['items'][0]

    def vk_wall_count(self) -> int:
        """Подсчитывает количество постов в группе."""
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={'access_token': config.VK_API_TOKEN,
                                        'v': config.VK_API_VERSION,
                                        'domain': config.VK_DOMAIN,
                                        'count': 1})

        return int(response.json()['response']['count'])

    def get_author(self) -> dict:
        """Получает данные о группе."""
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params={'access_token': config.VK_API_TOKEN,
                                        'v': config.VK_API_VERSION,
                                        'group_id': config.VK_DOMAIN,
                                        'count': 1})
        return response.json()['response'][0]

    def vk_posts_data_read(self) -> int:
        """Read data from the file."""
        if os.path.isfile(config.VK_DATA_FILE):
            with open(config.VK_DATA_FILE, 'r', encoding='utf-8') as f:
                return int(json.load(f))
        return int(0)

    def vk_posts_data_write(self, data) -> None:
        """Write data to file."""
        with open(config.VK_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    async def vk_post_send(self, item, *channel) -> None:
        """Send VK post to channel."""
        if 'post_type' in item and item['post_type'] == 'post':
            post_url = f"https://vk.com/{config.VK_DOMAIN}?w=wall{item['owner_id']}_{item['id']}"
            image = None

            if 'copy_history' in item:
                item = item['copy_history'][0]

            description = item['text'] if item['text'] else ''
            if description and len(description) > 1200:
                description = description[:500].split('.')[:-1]
                description = '.'.join(description) + '.'
                description += f'\n[Показать полностью...]({post_url})'

            if 'attachments' in item:

                if item['attachments'][0]['type'] == 'poll':
                    return

                if item['attachments'][0]['type'] == 'link':
                    image = item['attachments'][0]['link']['photo']['sizes'].pop()
                    description = item['attachments'][0]['link']['title']

                if item['attachments'][0]['type'] == 'album':
                    image = item['attachments'][0]['album']['thumb']['sizes'].pop()

                if item['attachments'][0]['type'] == 'photo':
                    image = item['attachments'][0]['photo']['sizes'].pop()

                if item['attachments'][0]['type'] == 'video':
                    image = item['attachments'][0]['video']['image'].pop()

            else:
                return

            embed_json = {
                "description": description,
                # "thumbnail": {"url": self.author['photo_200']},
                "image": image,
                "author": {"name": self.author['name'],
                           "url": post_url,
                           "icon_url": self.author['photo_50']},
                "color": 2590709}

            embed = Embed().from_dict(embed_json)
            channel = self.bot.get_channel(config.CH_VK_POSTS)
            await channel.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(VK(bot))
