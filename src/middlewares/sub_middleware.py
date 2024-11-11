from datetime import datetime
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.db.models import Users
from src.handlers.subscrite_router import sub_hand
from src.services.user_service import UserService
from src.states.states import Subscribe
from src.utils.dependencies.user_fabric import user_service_fabric


class SubMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
            user_service: UserService = user_service_fabric(),
    ) -> Any:
        user_data: Users = await user_service.get_user_by_id(event.chat.id)
        if user_data.subscribe_end and user_data.subscribe_end > datetime.now() and event.chat.id > 0:
                return await handler(event, data)
        else:
            state = data.get('state')
            if state:
                await state.set_state(Subscribe.sub_check)
            return await sub_hand(event, state)
