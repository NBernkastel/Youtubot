import sqlalchemy
import os
import dotenv
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


class PostgresSettings:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")


postgres_settings = PostgresSettings()

bot_settings = BotSettings()

default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=bot_settings.TOKEN, default=default)
dp = Dispatcher()
