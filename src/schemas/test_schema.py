from datetime import datetime
from pydantic import BaseModel, Field

"""
В данном файле описываются схемы данных(внутри БД) для модуля user_fabric.py
"""


class UserCreate(BaseModel):
    chat_id: int = Field(examples=[5])
    text: str = Field(examples=["Отличное приложение!"])
