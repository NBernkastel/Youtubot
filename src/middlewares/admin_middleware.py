from typing import Callable, Awaitable, Dict, Any
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.db.models import Users
from src.services.user_service import UserService
from src.utils.dependencies.user_fabric import user_service_fabric


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
            user_service: UserService = user_service_fabric(),
    ) -> Any:
        user_data: Users = await user_service.get_user_by_id(event.chat.id)

        if user_data.is_admin and event.chat.id > 0:
            return await handler(event, data)
        else:
            await event.answer('Вы не являетесь администратором!')
