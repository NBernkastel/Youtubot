from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.states.states import Subscribe
from src.utils.text_constants import SUB_START_TEXT

sub_router = Router()

@sub_router.message(F.content_type == 'message', Subscribe.sub_start)
async def sub_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, text=SUB_START_TEXT ,reply_markup=open_start_keyboard())