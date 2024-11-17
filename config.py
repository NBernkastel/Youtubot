import os
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
REDIRECT_URL = "urn:ietf:wg:oauth:2.0:oob"
MODER_CHAT_ID = -4583801709
TOKEN = os.getenv("TOKEN")
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]
storage = RedisStorage.from_url(REDIS_URL)
default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=TOKEN, default=default)
dp = Dispatcher(storage=storage)
