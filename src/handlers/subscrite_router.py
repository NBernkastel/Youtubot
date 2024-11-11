from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot, MODER_CHAT_ID
from src.keyboards.keyboards import sub_keyboard, accept_keyboard, continue_keyboard
from src.services.bill_service import BillService
from src.services.user_service import UserService
from src.states.states import Subscribe, PrivateRoom
from src.utils.dependencies.bill_fabric import bill_service_fabric
from src.utils.dependencies.user_fabric import user_service_fabric
from src.utils.text_constants import SUB_START_TEXT, ABOUT_SUB, SUB_ERROR, SUB_ACCEPT

sub_router = Router()


@sub_router.message(Subscribe.sub_check)
async def sub_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, text=SUB_START_TEXT, reply_markup=sub_keyboard())


@sub_router.callback_query(F.data == "subscribe")
async def add_sub(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Subscribe.get_photo)
    await bot.send_message(callback_query.message.chat.id, text=ABOUT_SUB)


@sub_router.message(F.content_type == 'photo', Subscribe.get_photo)
async def get_sub_photo_hand(message: Message, state: FSMContext):
    await state.set_state(Subscribe.decline)
    await bot.send_photo(MODER_CHAT_ID, photo=message.photo[-1].file_id, reply_markup=accept_keyboard(),
                         caption=str(message.chat.id))


@sub_router.callback_query(F.data == 'decline')
async def decline_sub(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(int(callback_query.message.caption), text=SUB_ERROR)
    await bot.send_message(int(callback_query.message.caption), text=SUB_START_TEXT, reply_markup=sub_keyboard())


@sub_router.callback_query(F.data == 'accept')
async def decline_sub(callback_query: CallbackQuery, state: FSMContext,
                      bill_service: BillService = bill_service_fabric(),
                      user_service: UserService = user_service_fabric()):
    end_time = datetime.now() + timedelta(days=30)
    await bill_service.add_bill({'user_id': int(callback_query.message.caption), 'date': datetime.now()})
    await user_service.update_user(int(callback_query.message.caption), {'subscribe_end': end_time})
    await state.set_state(PrivateRoom.main_room)
    await bot.send_message(int(callback_query.message.caption), text=SUB_ACCEPT + end_time.strftime('%Y.%m.%d'),
                           reply_markup=continue_keyboard())
