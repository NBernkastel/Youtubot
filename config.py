import sqlalchemy
import os
import dotenv
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

load_dotenv()


class EnvSettings(BaseSettings):
    class config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class BotSettings(EnvSettings):
    TOKEN: str

class RedisSettings(EnvSettings):
    REDIS_URL: str


class PostgresSettings:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")


postgres_settings = PostgresSettings()

REDIRECT_URL = "urn:ietf:wg:oauth:2.0:oob"
MODER_CHAT_ID = -4583801709
bot_settings = BotSettings()
redis_settings = RedisSettings()
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]
storage = RedisStorage.from_url(redis_settings.REDIS_URL)
default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=bot_settings.TOKEN, default=default)
dp = Dispatcher(storage=storage)
