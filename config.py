"""Configuration."""
print("config.py open")
sys.stdout.flush()
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN: str = os.environ.get('TOKEN')
PREFIX: str = os.environ.get('PREFIX')
DB_NAME: str = os.environ.get('DB_NAME')
QDAY_CHANNEL_ID: int = 0
CH_BUMP: int = 0
ROLE_BUMP: int = 0
VOICE_TRIGGER: list = [int(x) for x in os.environ.get("VOICE_TRIGGER").split(",")]
VK_API_TOKEN: str = ''
VK_API_VERSION: float = 0
VK_DOMAIN: str = ''
VK_GROUP_ID: int = 0
VK_DATA_FILE: str = './data/vk_last_post.json'
CH_VK_POSTS: int = 0
