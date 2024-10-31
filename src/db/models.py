from typing import (
    List,
    Optional
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from datetime import datetime
from src.db.conn import Base


class Users(Base):
    __tablename__ = "user"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    subscribe_end: Mapped[datetime] = mapped_column(nullable=True, default=None)
    does_free_sub_used: Mapped[bool] = mapped_column(nullable=False, default=False)


class Channels(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.chat_id"))
    channel_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    youtube_credits: Mapped[str] = mapped_column(nullable=False, default=None)


class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.chat_id"))
    channel_name: Mapped[str] = mapped_column(nullable=False)
    req_name: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=True, default=None)
    end_date: Mapped[datetime] = mapped_column(nullable=True, default=None)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
