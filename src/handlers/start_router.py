from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.db.models import Users
from src.handlers.help_router import help_hand
from src.keyboards.keyboards import open_start_keyboard
from src.services.user_service import UserService
from src.states.states import PrivateRoom, Subscribe
from src.utils.dependencies.user_fabric import user_service_fabric
from src.utils.text_constants import START_PHOTO, START_GREETING

start_router = Router()


@start_router.message(CommandStart(), StateFilter(None))
async def start_command(message: Message, state: FSMContext,
                        user_service: UserService = user_service_fabric()):
    user: Users = await user_service.get_user_by_id(message.chat.id)
    if not user:
        await user_service.create_user({'chat_id': message.chat.id, 'username': message.chat.username})
    if not user.does_free_sub_used:
        await state.set_state(Subscribe.free)
        await bot.send_photo(message.chat.id, photo=START_PHOTO, caption=START_GREETING,
                             reply_markup=open_start_keyboard(free_sub=True, sub_end=False))
    else:
        if user.subscribe_end and user.subscribe_end > datetime.now():
            await state.set_state(PrivateRoom.main_room)
            await bot.send_photo(message.chat.id, photo=START_PHOTO, caption=START_GREETING,
                                 reply_markup=open_start_keyboard(free_sub=False, sub_end=False))
        else:
            await state.set_state(Subscribe.sub_check)
            await bot.send_photo(message.chat.id, photo=START_PHOTO, caption=START_GREETING,
                                 reply_markup=open_start_keyboard(free_sub=False, sub_end=True))
    await help_hand(message, state)

# @start_router.message(F.content_type == 'photo')
# async def handle_user_photo(message: Message):
#     photo_file_id = message.photo[-1].file_id
#     print(photo_file_id)
