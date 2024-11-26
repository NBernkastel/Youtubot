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
    is_admin: Mapped[bool] = mapped_column(default=False)


class Channels(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.chat_id"))
    channel_name: Mapped[str] = mapped_column(nullable=False)
    channel_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    youtube_credits: Mapped[str] = mapped_column(nullable=False, default=None)
    youtube_analytic_token: Mapped[str] = mapped_column(nullable=False, default=None)
    youtube_data_token: Mapped[str] = mapped_column(nullable=False, default=None)


class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.chat_id"))
    channel_name: Mapped[str] = mapped_column(nullable=False)
    req_name: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=True, default=None)
    end_date: Mapped[datetime] = mapped_column(nullable=True, default=None)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())



class Bills(Base):
    __tablename__ = 'bills'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.chat_id"))
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())