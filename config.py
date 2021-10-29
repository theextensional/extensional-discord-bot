"""Configuration."""
import os 
import sys


PREFIX = '+'
DB_NAME = 'bot.db'
# QDAY_CHANNEL_ID = int
# CH_BUMP = int
# ROLE_BUMP = int
VOICE_TRIGGER = os.environ.get("VOICE_TRIGGER").split(",")
print(VOICE_TRIGGER)
sys.stdout.flush()
# VK_API_TOKEN = str
# VK_API_VERSION = float
# VK_DOMAIN = str
# VK_GROUP_ID = int
# VK_DATA_FILE = str  # example './data/vk_last_post.json'
# CH_VK_POSTS = int
