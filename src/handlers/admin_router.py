from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile, InputFile, FSInputFile

from config import bot
from src.db.models import Logs
from src.handlers.private_rooms_router import private_rooms_hand1
from src.keyboards.keyboards import admin_keyboard, back_keyboard
from src.middlewares.admin_middleware import AdminMiddleware
from src.services.channel_service import ChannelService
from src.services.log_service import LogService
from src.services.scv_service import CSVService
from src.services.user_service import UserService
from src.states.states import AdminState
from src.utils.dependencies.channel_fabric import channel_service_fabric
from src.utils.dependencies.log_fabric import log_service_fabric
from src.utils.dependencies.user_fabric import user_service_fabric
from src.utils.text_constants import ADMIN_TEXT, ADMIN_GET_USERS_COUNT, ADMIN_CHANNELS_COUNT, ADMIN_GET_USER_REQ, \
    ADMIN_ENTER_UID, BACK_TEXT, ADMIN_WRONG_DATA, ADMIN_NO_LOGS

admin_router = Router()

admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command("admin"))
async def main_admin_hand(message: Message, state: FSMContext):
    await state.set_state(AdminState.admin_room)
    await bot.send_message(message.chat.id, ADMIN_TEXT, reply_markup=admin_keyboard())


@admin_router.message(F.text == ADMIN_GET_USERS_COUNT, AdminState.admin_room)
async def help_hand(message: Message, state: FSMContext, user_service: UserService = user_service_fabric()):
    users = await user_service.get_all_users()
    await bot.send_message(message.chat.id, str(len(users)))


@admin_router.message(F.text == ADMIN_CHANNELS_COUNT, AdminState.admin_room)
async def help_hand(message: Message, state: FSMContext, channel_service: ChannelService = channel_service_fabric()):
    channels = await channel_service.get_all_channels()
    await bot.send_message(message.chat.id, str(len(channels)))


@admin_router.message(F.text == ADMIN_GET_USER_REQ, AdminState.admin_room)
async def help_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, ADMIN_ENTER_UID, reply_markup=back_keyboard())
    await state.set_state(AdminState.uid_enter)


@admin_router.message(F.text != BACK_TEXT, AdminState.uid_enter)
async def log_hand(message: Message, state: FSMContext, log_service: LogService = log_service_fabric()):
    try:
        logs: List[Logs] = await log_service.get_logs(int(message.text))
    except:
        await bot.send_message(message.chat.id, ADMIN_WRONG_DATA)
        return
    data = []
    for log in logs:
        data.append([log.user_id, log.channel_name, log.req_name, log.start_date, log.end_date, log.date])
    if len(data) > 0:
        data.insert(0, ['chat_id', 'channel_name', 'req_type', 'start_date', 'end_date', 'date'])
        filename = await CSVService.create_csv_file(data)
        file = FSInputFile(filename)
        await bot.send_document(message.chat.id, file)
        await CSVService.delete_csv_file(file_path=filename)
        await main_admin_hand(message, state)
    else:
        await bot.send_message(message.chat.id, ADMIN_NO_LOGS)
        await main_admin_hand(message, state)


@admin_router.message(F.text == BACK_TEXT, AdminState.uid_enter)
async def back_hand(message: Message, state: FSMContext):
    await main_admin_hand(message, state)


@admin_router.message(F.text == BACK_TEXT, AdminState.admin_room)
async def back_hand(message: Message, state: FSMContext):
    await private_rooms_hand1(message, state)
