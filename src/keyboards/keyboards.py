from typing import List

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.utils.text_constants import KEY_START_SUB, main_room1, main_room2, main_room3, main_room4, main_room5, \
    CHANNELS_ROOM_ADD_CHANNEL, ADMIN_GET_USERS_COUNT, ADMIN_CHANNELS_COUNT, ADMIN_GET_USER_REQ, BACK_TEXT


def open_start_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text=KEY_START_SUB)
    keyboard_builder.row(button)
    return keyboard_builder.as_markup(resize_keyboard=True)


def main_room_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_channels = KeyboardButton(text=main_room1)
    button_all_views_in_period = KeyboardButton(text=main_room2)
    button_video_in_period = KeyboardButton(text=main_room3)
    button_subs_in_period = KeyboardButton(text=main_room4)
    button_avg_pers_and_time = KeyboardButton(text=main_room5)
    keyboard_builder.row(button_channels, button_all_views_in_period)
    keyboard_builder.row(button_video_in_period, button_subs_in_period)
    keyboard_builder.row(button_avg_pers_and_time)
    return keyboard_builder.as_markup(resize_keyboard=True)


def room1_keyboard(channels: List):
    keyboard_builder = ReplyKeyboardBuilder()
    if len(channels) == 0:
        button_channel_add = KeyboardButton(text=CHANNELS_ROOM_ADD_CHANNEL)
    else:
        channels_list = [KeyboardButton(text=channel) for channel in channels]
        button_channel_add = KeyboardButton(text=CHANNELS_ROOM_ADD_CHANNEL)
        for channel in channels_list:
            keyboard_builder.row(channel)
    back_button = KeyboardButton(text=BACK_TEXT)
    keyboard_builder.row(button_channel_add)
    keyboard_builder.row(back_button)
    return keyboard_builder.as_markup(resize_keyboard=True)


def channel_room_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_all_views_in_period = KeyboardButton(text=main_room2)
    button_video_in_period = KeyboardButton(text=main_room3)
    button_subs_in_period = KeyboardButton(text=main_room4)
    button_avg_pers_and_time = KeyboardButton(text=main_room5)
    back_button = KeyboardButton(text=BACK_TEXT)
    keyboard_builder.row(button_all_views_in_period, button_subs_in_period)
    keyboard_builder.row(button_video_in_period)
    keyboard_builder.row(button_avg_pers_and_time, back_button)
    return keyboard_builder.as_markup(resize_keyboard=True)


def admin_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_get_all_users = KeyboardButton(text=ADMIN_GET_USERS_COUNT)
    button_get_all_channels = KeyboardButton(text=ADMIN_CHANNELS_COUNT)
    button_get_user_req = KeyboardButton(text=ADMIN_GET_USER_REQ)
    keyboard_builder.row(button_get_all_users, button_get_all_channels)
    keyboard_builder.row(button_get_user_req)
    return keyboard_builder.as_markup(resize_keyboard=True)


def back_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_back = KeyboardButton(text=BACK_TEXT)
    keyboard_builder.row(button_back)
    return keyboard_builder.as_markup(resize_keyboard=True)
