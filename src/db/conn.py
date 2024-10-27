from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import postgres_settings
from sqlalchemy import create_engine, MetaData, NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{postgres_settings.POSTGRES_USER}:{postgres_settings.POSTGRES_PASSWORD}@{postgres_settings.POSTGRES_HOST}:{postgres_settings.POSTGRES_PORT}/{postgres_settings.POSTGRES_DB}"
Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
async_session_maker: AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)



