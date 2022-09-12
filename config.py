"""Configuration."""
import json
import os

from dotenv import load_dotenv

load_dotenv()  # для доступности переменных из файла ".env" в переменых окружения

TOKEN: str = str(os.environ.get("TOKEN"))
FIREBASE_CERTIFICATE = os.environ.get("FIREBASE_CERTIFICATE")
DB_URL = os.environ.get("DB_URL")
PREFIX: str = "."
DB_NAME: str = "bot.db"
QDAY_CHANNEL_ID: int = 0
CH_BUMP: int = 0
ROLE_BUMP: int = 0
VOICE_TRIGGER: list = [
    int(x) for x in os.environ.get("VOICE_TRIGGER").split(",")
]
VK_API_TOKEN: str = ""
VK_API_VERSION: float = 0
VK_DOMAIN: str = ""
VK_GROUP_ID: int = 0
VK_DATA_FILE: str = "./data/vk_last_post.json"
CH_VK_POSTS: int = 0
GSPREAD_CREDENTIALS: dict = json.loads(
    str(os.environ.get("GSPREAD_CREDENTIALS"))
)
SHEET_UID: str = str(os.environ.get("SHEET_UID"))
