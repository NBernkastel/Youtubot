from typing import List

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.utils.text_constants import KEY_START_SUB, main_room1, main_room2, main_room3, main_room4, main_room5, \
    CHANNELS_ROOM_ADD_CHANNEL, ADMIN_GET_USERS_COUNT, ADMIN_CHANNELS_COUNT, ADMIN_GET_USER_REQ, BACK_TEXT, MAKE_SUB, \
    ACCEPT_SUB, DECLINE_SUB, SUB_CONTINUE, KEY_START_NOT_SUB, SUB_EXP, CHANNELS_ROOM_DELETE


def open_start_keyboard(free_sub: bool, sub_end: bool):
    keyboard_builder = ReplyKeyboardBuilder()
    if free_sub and not sub_end:
        button = KeyboardButton(text=KEY_START_SUB)
    if not free_sub and not sub_end:
        button = KeyboardButton(text=KEY_START_NOT_SUB)
    if sub_end:
        button = KeyboardButton(text=SUB_EXP)
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
    if len(channels) != 0:
        delete_button = KeyboardButton(text=CHANNELS_ROOM_DELETE)
        keyboard_builder.row(delete_button)
    keyboard_builder.row(back_button)
    return keyboard_builder.as_markup(resize_keyboard=True)


def channel_delete_keyboard(channels: List):
    keyboard_builder = ReplyKeyboardBuilder()
    channels_list = [KeyboardButton(text=channel) for channel in channels]
    for channel in channels_list:
        keyboard_builder.row(channel)
    back_button = KeyboardButton(text=BACK_TEXT)
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
    button_back = KeyboardButton(text=BACK_TEXT)
    keyboard_builder.row(button_get_all_users, button_get_all_channels)
    keyboard_builder.row(button_get_user_req, button_back)
    return keyboard_builder.as_markup(resize_keyboard=True)


def back_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_back = KeyboardButton(text=BACK_TEXT)
    keyboard_builder.row(button_back)
    return keyboard_builder.as_markup(resize_keyboard=True)


def sub_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    make_sub = InlineKeyboardButton(text=MAKE_SUB, callback_data="subscribe")
    keyboard_builder.add(make_sub)
    return keyboard_builder.as_markup(resize_keyboard=True)


def accept_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    accept_sub = InlineKeyboardButton(text=ACCEPT_SUB, callback_data=f"accept")
    decline_sub = InlineKeyboardButton(text=DECLINE_SUB, callback_data=f"decline")
    keyboard_builder.row(accept_sub, decline_sub)
    return keyboard_builder.as_markup(resize_keyboard=True)


def continue_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    button_cont = KeyboardButton(text=SUB_CONTINUE)
    keyboard_builder.row(button_cont)
    return keyboard_builder.as_markup(resize_keyboard=True)
