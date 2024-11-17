from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
async_session_maker: AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
