import asyncio
from datetime import datetime
from typing import List

from config import bot
from src.db.models import Users
from src.services.user_service import UserService
from src.utils.dependencies.user_fabric import user_service_fabric
from src.utils.text_constants import SUB_WAS_ENDED


async def sub_task():
    while True:
        user_service: UserService = user_service_fabric()
        users: List[Users] = await user_service.get_all_users()
        for user in users:
            if user.subscribe_end and user.subscribe_end < datetime.now():
                await user_service.update_user(user.chat_id, {'subscribe_end': None})
                await bot.send_message(user.chat_id, SUB_WAS_ENDED)
        await asyncio.sleep(86400)
