from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.keyboards.keyboards import main_room_keyboard, room1_keyboard, channel_room_keyboard
from src.services.channel_service import ChannelService
from src.services.youtube_service import YoutubeService
from src.states.states import PrivateRoom
from src.utils.dependencies.channel_fabric import channel_service_fabric
from src.utils.text_constants import MAIN_ROOT_TEXT, main_room1, CHANNELS_ROOM_ERROR_TEXT, CHANNELS_ROOM_LIST, \
    CHANNELS_ROOM_ADD_CHANNEL, CHANNEL_ROOM_ADD, CHANNEL_ROOM

private_rooms_router = Router()


@private_rooms_router.message(PrivateRoom.main_room)
async def private_rooms_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, MAIN_ROOT_TEXT, reply_markup=main_room_keyboard())
    await state.set_state(PrivateRoom.second_stage_rooms)


@private_rooms_router.message(F.text == main_room1, PrivateRoom.second_stage_rooms)
async def channels_room_hand(message: Message, state: FSMContext):
    channels = ['Test1', 'Test2']
    await state.set_state(PrivateRoom.channel_state)
    if len(channels) == 0:
        await bot.send_message(message.chat.id, CHANNELS_ROOM_ERROR_TEXT, reply_markup=room1_keyboard(channels))
    else:
        channels_str = '\n'.join(channels)
        await bot.send_message(message.chat.id, CHANNELS_ROOM_LIST + channels_str,
                               reply_markup=room1_keyboard(channels))


@private_rooms_router.message(F.text == CHANNELS_ROOM_ADD_CHANNEL, PrivateRoom.channel_state)
async def add_channel_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.send_file)
    await bot.send_message(message.chat.id, CHANNEL_ROOM_ADD)


@private_rooms_router.message(PrivateRoom.send_file)
async def add_channel_file_hand(message: Message, state: FSMContext,
                                channel_service: ChannelService = channel_service_fabric()):
    await state.set_state(PrivateRoom.auth)
    file = await bot.get_file(message.document.file_id)
    file_data = await bot.download_file(file.file_path)
    content = file_data.read().decode()
    await channel_service.add_channel(
        {'user_id': message.chat.id, 'channel_name': "TEST DATA", 'youtube_credits': content})
    await YoutubeService.get_authenticated_service()


@private_rooms_router.message(PrivateRoom.channel_state)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, CHANNEL_ROOM, reply_markup=channel_room_keyboard())
    await YoutubeService.get_views_by_date("2023-01-01", "2023-01-31")
