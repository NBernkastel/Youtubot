from datetime import datetime
from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from config import bot
from src.db.models import Channels
from src.keyboards.keyboards import main_room_keyboard, room1_keyboard, channel_room_keyboard, back_keyboard
from src.middlewares.sub_middleware import SubMiddleware
from src.services.channel_service import ChannelService
from src.services.log_service import LogService
from src.services.scv_service import CSVService
from src.services.youtube_service import YoutubeService
from src.states.states import PrivateRoom
from src.utils.dependencies.channel_fabric import channel_service_fabric
from src.utils.dependencies.log_fabric import log_service_fabric
from src.utils.dependencies.youtube_fabric import youtube_service_fabric
from src.utils.text_constants import MAIN_ROOT_TEXT, main_room1, CHANNELS_ROOM_ERROR_TEXT, CHANNELS_ROOM_LIST, \
    CHANNELS_ROOM_ADD_CHANNEL, CHANNEL_ROOM_ADD, CHANNEL_ROOM, main_room2, main_room_period, main_room3, main_room4, \
    main_room5, BACK_TEXT, SUB_CONTINUE, KEY_START_NOT_SUB, CHANNEL_ROOM_ADD_ERROR, CHANNEL_AUTH_ERROR, main_room_error, \
    MAIN_ROOM_NO_CHANNELS, NO_DATA_TEXT

private_rooms_router = Router()
private_rooms_router.message.middleware(SubMiddleware())


@private_rooms_router.message(F.text == SUB_CONTINUE)
async def from_sub_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_room)
    await private_rooms_hand1(message, state)


@private_rooms_router.message(F.text.in_([SUB_CONTINUE, KEY_START_NOT_SUB]), PrivateRoom.main_room)
async def private_rooms_hand1(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, MAIN_ROOT_TEXT, reply_markup=main_room_keyboard())
    await state.set_state(PrivateRoom.second_stage_rooms)


# # Channels hands
@private_rooms_router.message(F.text == main_room2, PrivateRoom.second_stage_rooms)
async def private_rooms_hand2(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_views)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room3, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand3(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_videos)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room4, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand4(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_subs)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room5, PrivateRoom.second_stage_rooms)
async def channel_rooms_hand5(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_period_enter_for_agv_view)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == BACK_TEXT, StateFilter(PrivateRoom.main_period_enter_for_views,
                                                               PrivateRoom.main_period_enter_for_videos,
                                                               PrivateRoom.main_period_enter_for_subs,
                                                               PrivateRoom.main_period_enter_for_agv_view))
async def main_req_back_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_room)
    await private_rooms_hand1(message, state)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.main_period_enter_for_views)
async def get_views_hand(message: Message, state: FSMContext,
                         youtube_service: YoutubeService = youtube_service_fabric(),
                         channel_service: ChannelService = channel_service_fabric(),
                         log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        if len(channels) == 0:
            await bot.send_message(message.chat.id, MAIN_ROOM_NO_CHANNELS)
            return
        result_data = []
        end_sum = 0
        for channel in channels:
            result = await youtube_service.get_views_by_date(date[0], date[1], message.chat.id, channel.channel_name)
            res_sum = [res[1] for res in result]
            result_data.append([channel.channel_url, sum(res_sum)])
            end_sum += sum(res_sum)
        result_data.append([end_sum])
        filename = await CSVService.create_csv_file(result_data)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption='Всего просмотров - ' + str(end_sum),
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': 'All', 'req_name': 'period of view',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.main_room)
        await private_rooms_hand1(message, state)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.main_period_enter_for_subs)
async def get_subs_hand(message: Message, state: FSMContext,
                        youtube_service: YoutubeService = youtube_service_fabric(),
                        channel_service: ChannelService = channel_service_fabric(),
                        log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        if len(channels) == 0:
            await bot.send_message(message.chat.id, MAIN_ROOM_NO_CHANNELS)
            return
        result_data = []
        end_sum = 0
        for channel in channels:
            result = await youtube_service.get_subscribers_gained_by_date(date[0], date[1], message.chat.id,
                                                                          channel.channel_name)
            result_data.append([channel.channel_url, result[1]])
            end_sum += result[1]
        result_data.append([end_sum])
        filename = await CSVService.create_csv_file(result_data)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption='Всего подписчиков - ' + str(end_sum),
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': 'All', 'req_name': 'period of subs',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.main_room)
        await private_rooms_hand1(message, state)
    except:
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.main_period_enter_for_agv_view)
async def get_agv_hand(message: Message, state: FSMContext,
                       youtube_service: YoutubeService = youtube_service_fabric(),
                       channel_service: ChannelService = channel_service_fabric(),
                       log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        if len(channels) == 0:
            await bot.send_message(message.chat.id, MAIN_ROOM_NO_CHANNELS)
            return
        result_data = []
        end_sum_time = []
        end_sum_per = []
        result_time_sum = []
        result_per_sum = []
        for channel in channels:
            result_time = await youtube_service.get_average_view_duration_by_date(date[0], date[1], message.chat.id,
                                                                                  channel.channel_name)
            result_percent = await youtube_service.get_average_view_percentage_by_date(date[0], date[1],
                                                                                       message.chat.id,
                                                                                       channel.channel_name)
            for i in range(len(result_time)):
                result_time_sum.append(result_time[i][1])
                result_per_sum.append(result_percent[i][1])
            result_data.append(
                [channel.channel_url, round(sum(result_time_sum) / len(result_time_sum), 2),
                 round(sum(result_per_sum) / len(result_per_sum), 2)])
            end_sum_time.append(round(sum(result_time_sum) / len(result_time_sum), 2))
            end_sum_per.append(round(sum(result_per_sum) / len(result_per_sum), 2))
        end_sum_time = round(sum(end_sum_time) / len(end_sum_time), 2)
        end_sum_per = round(sum(end_sum_per) / len(end_sum_per), 2)
        result_data.append([end_sum_time, end_sum_per])
        filename = await CSVService.create_csv_file(result_data)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption=f'Между {date[0]} и {date[1]} было:\n{end_sum_time} минут среднего просмотра\n{end_sum_per} средний процент просмотра видео',
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': 'All', 'req_name': 'period of agv view',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.main_room)
        await private_rooms_hand1(message, state)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.main_period_enter_for_videos)
async def get_vid_hand(message: Message, state: FSMContext,
                       youtube_service: YoutubeService = youtube_service_fabric(),
                       channel_service: ChannelService = channel_service_fabric(),
                       log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        channels: List[Channels] = await channel_service.get_all_user_channels(message.chat.id)
        if len(channels) == 0:
            await bot.send_message(message.chat.id, MAIN_ROOM_NO_CHANNELS)
            return
        result_data = []
        end_result = 0
        for channel in channels:
            result = await youtube_service.get_video_count_by_date(date[0], date[1], message.chat.id,
                                                                   channel.channel_name)
            end_result += len(result)
            result_data.append([channel.channel_url, len(result)])
        result_data.append([end_result])
        filename = await CSVService.create_csv_file(result_data)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption='Всего видео - ' + str(end_result),
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': 'All', 'req_name': 'period of videos',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.main_room)
        await private_rooms_hand1(message, state)
    except:
        await bot.send_message(message.chat.id, main_room_error)


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
    video = FSInputFile('./public/vid.mp4')
    await bot.send_video(message.chat.id, video, caption=CHANNEL_ROOM_ADD, reply_markup=back_keyboard())


@private_rooms_router.message(F.document, PrivateRoom.send_file)
async def add_channel_file_hand(message: Message, state: FSMContext,
                                youtube_service: YoutubeService = youtube_service_fabric()):
    try:
        file = await bot.get_file(message.document.file_id)
        file_data = await bot.download_file(file.file_path)
        content = file_data.read().decode()
        analytic_url, analytic_flow = await youtube_service.get_analytic_login_url(youtube_credits=content)
        await state.update_data({'analytic_flow': analytic_flow, 'content': content})
        await bot.send_message(message.chat.id,
                               f'Перейдите по ссылке и выберете нужный google аккаунт\nИ отправте код [Кликните сюда]({analytic_url})',
                               parse_mode='Markdown')
        await state.set_state(PrivateRoom.get_analytic_code)
    except:
        await bot.send_message(message.chat.id, CHANNEL_ROOM_ADD_ERROR)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.send_file)
async def add_channel_file_error(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, CHANNEL_ROOM_ADD_ERROR)


@private_rooms_router.message(F.text == BACK_TEXT, StateFilter(PrivateRoom.send_file, PrivateRoom.get_analytic_code,
                                                               PrivateRoom.get_data_code))
async def add_channel_file_error(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.second_stage_rooms)
    await channels_room_hand(message, state)


@private_rooms_router.message(PrivateRoom.get_analytic_code)
async def get_analytic_code(message: Message, state: FSMContext,
                            youtube_service: YoutubeService = youtube_service_fabric()):
    data = await state.get_data()
    analytic_flow = data.get('analytic_flow')
    content = data.get('content')
    creds_analytic = await youtube_service.res_analytic_token(message.text, analytic_flow)
    await state.update_data({'creds_analytic': creds_analytic})
    data_url, data_flow = await youtube_service.get_data_login_url(youtube_credits=content)
    await state.update_data({'data_flow': data_flow})
    await bot.send_message(message.chat.id,
                           f'Первая ссылка подтверждена, теперь надо повторить эту операцию еще раз [Вторая ссылка]({data_url})',
                           parse_mode='Markdown')
    await state.set_state(PrivateRoom.get_data_code)


@private_rooms_router.message(PrivateRoom.get_data_code)
async def get_analytic_code(message: Message, state: FSMContext,
                            youtube_service: YoutubeService = youtube_service_fabric()):
    data = await state.get_data()
    creds_analytic = data.get('creds_analytic')
    data_flow = data.get('data_flow')
    youtube_creds = data.get('content')
    creds_data = await youtube_service.res_data_token(message.text, data_flow)
    try:
        await youtube_service.get_authenticated_service(message.chat.id, youtube_credits=youtube_creds,
                                                        creds_analytic=creds_analytic, creds_data=creds_data, auth=True)
    except:
        await state.set_state(PrivateRoom.main_room)
        await bot.send_message(message.chat.id, CHANNEL_AUTH_ERROR)
        await private_rooms_hand1(message, state)
        return
    await state.set_state(PrivateRoom.main_room)
    await private_rooms_hand1(message, state)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.channel_state)
async def channel_rooms_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.in_req)
    data = await state.get_data()
    if not data.get("channel_name"):
        await state.update_data(channel_name=message.text)
    await bot.send_message(message.chat.id, CHANNEL_ROOM, reply_markup=channel_room_keyboard())


@private_rooms_router.message(F.text == BACK_TEXT, PrivateRoom.in_req)
async def back_to_main_room_hand1(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_room)
    await private_rooms_hand1(message, state)


@private_rooms_router.message(F.text == BACK_TEXT, PrivateRoom.channel_state)
async def back_to_main_room_hand2(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.main_room)
    await private_rooms_hand1(message, state)


@private_rooms_router.message(F.text == BACK_TEXT, PrivateRoom.back_to_channel)
async def back_to_channel_room_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.channel_state)
    await channel_rooms_hand(message, state)


@private_rooms_router.message(F.text == main_room2, PrivateRoom.in_req)
async def in_req_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_views)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room3, PrivateRoom.in_req)
async def in_req_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_videos)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room4, PrivateRoom.in_req)
async def in_req_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_subs)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == main_room5, PrivateRoom.in_req)
async def in_req_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.period_enter_for_agv_view)
    await bot.send_message(message.chat.id, main_room_period, reply_markup=back_keyboard())


@private_rooms_router.message(F.text == BACK_TEXT,
                              StateFilter(PrivateRoom.period_enter_for_views, PrivateRoom.period_enter_for_videos,
                                          PrivateRoom.period_enter_for_subs, PrivateRoom.period_enter_for_agv_view))
async def in_req_back_hand(message: Message, state: FSMContext):
    await state.set_state(PrivateRoom.channel_state)
    await channel_rooms_hand(message, state)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.period_enter_for_views)
async def in_req_hand(message: Message, state: FSMContext,
                      youtube_service: YoutubeService = youtube_service_fabric(),
                      log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_views_by_date(date[0], date[1], message.chat.id, channel_name)
        end_sum = 0
        for res in result:
            end_sum += res[1]
        filename = await CSVService.create_csv_file(result)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file, caption='Всего просмотров - ' + str(end_sum))
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': channel_name, 'req_name': 'period of view',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.channel_state)
        await channel_rooms_hand(message, state)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.period_enter_for_subs)
async def in_req_hand(message: Message, state: FSMContext,
                      youtube_service: YoutubeService = youtube_service_fabric(),
                      log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_subscribers_gained_by_date(date[0], date[1], message.chat.id, channel_name)
        filename = await CSVService.create_csv_file(result[0])
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file, caption='Всего подписчиков - ' + str(result[1]),
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': channel_name, 'req_name': 'period of subs',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.channel_state)
        await channel_rooms_hand(message, state)
    except:
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.period_enter_for_agv_view)
async def in_req_hand(message: Message, state: FSMContext,
                      youtube_service: YoutubeService = youtube_service_fabric(),
                      log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result_times = await youtube_service.get_average_view_duration_by_date(date[0], date[1], message.chat.id,
                                                                               channel_name)
        result_percents = await youtube_service.get_average_view_percentage_by_date(date[0], date[1], message.chat.id,
                                                                                    channel_name)
        result_data = []
        result_avg_view = []
        result_avg_per = []
        for i in range(len(result_times)):
            result_data.append([result_times[i][0], result_percents[i][1], result_times[i][1]])
            result_avg_view.append(result_times[i][1])
            result_avg_per.append(result_percents[i][1])
        result_avg_view = round(sum(result_avg_view) / len(result_avg_view), 2)
        result_avg_per = round(sum(result_avg_per) / len(result_avg_per), 2)
        result_data.append([date[0], date[1], result_avg_view, result_avg_per])
        filename = await CSVService.create_csv_file(result_data)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption=f'Между {date[0]} и {date[1]} было:\n{result_avg_view} минут среднего просмотра\n{result_avg_per} средний процент просмотра видео',
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': channel_name, 'req_name': 'period of agv view',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.channel_state)
        await channel_rooms_hand(message, state)
    except:
        await bot.send_message(message.chat.id, main_room_error)


@private_rooms_router.message(F.text != BACK_TEXT, PrivateRoom.period_enter_for_videos)
async def in_req_hand(message: Message, state: FSMContext,
                      youtube_service: YoutubeService = youtube_service_fabric(),
                      log_service: LogService = log_service_fabric()):
    date = message.text.split(' ')
    try:
        state_data = await state.get_data()
        channel_name = state_data.get("channel_name")
        result = await youtube_service.get_video_count_by_date(date[0], date[1], message.chat.id,
                                                               channel_name)
        filename = await CSVService.create_csv_file(result)
        file = FSInputFile(filename)
        try:
            await bot.send_document(message.chat.id, file,
                                    caption='Всего видео - ' + str(len(result)),
                                    reply_markup=back_keyboard())
        except:
            await bot.send_message(message.chat.id, NO_DATA_TEXT)
        await CSVService.delete_csv_file(file_path=filename)
        await log_service.create_log(
            {'user_id': message.chat.id, 'channel_name': channel_name, 'req_name': 'period of videos',
             'start_date': datetime.strptime(date[0], "%Y-%m-%d"), 'end_date': datetime.strptime(date[1], "%Y-%m-%d"),
             'date': datetime.now()})
        await state.set_state(PrivateRoom.channel_state)
        await channel_rooms_hand(message, state)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, main_room_error)
