from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.db.models import Channels
from src.keyboards.keyboards import main_room_keyboard, room1_keyboard, channel_room_keyboard, back_keyboard
from src.services.channel_service import ChannelService
from src.services.youtube_service import YoutubeService
from src.states.states import PrivateRoom
from src.utils.dependencies.channel_fabric import channel_service_fabric
from src.utils.dependencies.youtube_fabric import youtube_service_fabric
from src.utils.text_constants import MAIN_ROOT_TEXT, main_room1, CHANNELS_ROOM_ERROR_TEXT, CHANNELS_ROOM_LIST, \
    CHANNELS_ROOM_ADD_CHANNEL, CHANNEL_ROOM_ADD, CHANNEL_ROOM, main_room2, main_room_period, main_room3, main_room4, \
    main_room5

private_rooms_router = Router()


@private_rooms_router.message(PrivateRoom.main_room)
async def private_rooms_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, MAIN_ROOT_TEXT, reply_markup=main_room_keyboard())
    await state.set_state(PrivateRoom.second_stage_rooms)


# # Channels hands
@private_rooms_router.message(F.text == main_room2, PrivateRoom.second_stage_rooms)
async def private_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_views)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room3, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_videos)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room4, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_subs)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room5, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_agv_view)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(PrivateRoom.main_period_enter_for_views)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric(),
                             channel_service: ChannelService = channel_service_fabric()):
    date = message.text.split(' ')
    end_result = 0
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        for channel in channels:
            result = await youtube_service.get_views_by_date(date[0], date[1], message.chat.id, channel.channel_name)
            end_result += result
        await bot.send_message(message.chat.id, f'In period bettwin {date[0]} and {date[1]} was {end_result} views')
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.main_period_enter_for_subs)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric(),
                             channel_service: ChannelService = channel_service_fabric()):
    date = message.text.split(' ')
    end_result = 0
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        for channel in channels:
            result = await youtube_service.get_subscribers_gained_by_date(date[0], date[1], message.chat.id,
                                                                          channel.channel_name)
            end_result += result
        await bot.send_message(message.chat.id, f'In period bettwin {date[0]} and {date[1]} was {end_result} subs')
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.main_period_enter_for_agv_view)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric(),
                             channel_service: ChannelService = channel_service_fabric()):
    date = message.text.split(' ')
    end_result_time = []
    end_result_percent = []
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        for channel in channels:
            result_time = await youtube_service.get_average_view_duration_by_date(date[0], date[1], message.chat.id,
                                                                                  channel.channel_name)
            result_percent = await youtube_service.get_average_view_percentage_by_date(date[0], date[1],
                                                                                       message.chat.id,
                                                                                       channel.channel_name)
            end_result_time.append(result_time)
            end_result_percent.append(result_percent)
        end_result_time = sum(end_result_time) / len(end_result_time)
        end_result_percent = sum(end_result_percent) / len(end_result_percent)
        await bot.send_message(message.chat.id,
                               f'In period bettwin {date[0]} and {date[1]} was {end_result_time} avg time view and {end_result_percent} avg perc view')
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.main_period_enter_for_videos)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric(),
                             channel_service: ChannelService = channel_service_fabric()):
    date = message.text.split(' ')
    end_result = 0
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        for channel in channels:
            result = await youtube_service.get_video_count_by_date(date[0], date[1], message.chat.id,
                                                                   channel.channel_name)
            end_result += result
        await bot.send_message(message.chat.id,
                               f'In period bettwin {date[0]} and {date[1]} was {end_result} video published')
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


# One channel hands

@private_rooms_router.message(F.text == main_room1, PrivateRoom.second_stage_rooms)
async def channels_room_hand(message: Message, state: FSMContext,
                             channel_service: ChannelService = channel_service_fabric()):
    channels = await channel_service.get_all_user_channels(message.chat.id)
    channels = [channel.channel_name for channel in channels]
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
                                youtube_service: YoutubeService = youtube_service_fabric()):
    await state.set_state(PrivateRoom.auth)
    file = await bot.get_file(message.document.file_id)
    file_data = await bot.download_file(file.file_path)
    content = file_data.read().decode()
    await youtube_service.get_authenticated_service(uid=message.chat.id, youtube_credits=content)


@private_rooms_router.message(PrivateRoom.channel_state)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.in_req)
    data = await state.get_data()
    if not data.get("channel_name"):
        await state.update_data(channel_name=message.text)
    await bot.send_message(message.chat.id, CHANNEL_ROOM, reply_markup=channel_room_keyboard())


@private_rooms_router.message(F.text == main_room2, PrivateRoom.in_req)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_views)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room3, PrivateRoom.in_req)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_videos)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room4, PrivateRoom.in_req)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_subs)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(F.text == main_room5, PrivateRoom.in_req)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_agv_view)
    await bot.send_message(message.chat.id, main_room_period)


@private_rooms_router.message(PrivateRoom.period_enter_for_views)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_views_by_date(date[0], date[1], message.chat.id, channel_name)
        await bot.send_message(message.chat.id, f'In period bettwin {date[0]} and {date[1]} was {result} views',
                               reply_markup=back_keyboard())
        await state.set_state(PrivateRoom.channel_state)
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.period_enter_for_subs)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_subscribers_gained_by_date(date[0], date[1], message.chat.id, channel_name)
        await bot.send_message(message.chat.id, f'In period bettwin {date[0]} and {date[1]} was {result} subs',
                               reply_markup=back_keyboard())
        await state.set_state(PrivateRoom.channel_state)
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.period_enter_for_agv_view)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result_time = await youtube_service.get_average_view_duration_by_date(date[0], date[1], message.chat.id,
                                                                              channel_name)
        result_percent = await youtube_service.get_average_view_percentage_by_date(date[0], date[1], message.chat.id,
                                                                                   channel_name)
        await bot.send_message(message.chat.id,
                               f'In period bettwin {date[0]} and {date[1]} was {result_time} avg time view and {result_percent} avg perc view',
                               reply_markup=back_keyboard())
        await state.set_state(PrivateRoom.channel_state)
    except:
        await bot.send_message(message.chat.id, 'Try one more time')


@private_rooms_router.message(PrivateRoom.period_enter_for_videos)
async def channel_rooms_hand(message: Message, state: FSMContext,
                             youtube_service: YoutubeService = youtube_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_video_count_by_date(date[0], date[1], message.chat.id,
                                                               channel_name)
        await bot.send_message(message.chat.id,
                               f'In period bettwin {date[0]} and {date[1]} was {result} video published',
                               reply_markup=back_keyboard())
        await state.set_state(PrivateRoom.channel_state)
    except:
        await bot.send_message(message.chat.id, 'Try one more time')
