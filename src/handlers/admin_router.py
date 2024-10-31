from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.keyboards.keyboards import admin_keyboard
from src.utils.text_constants import ADMIN_TEXT

admin_router = Router()


@admin_router.message(Command("admin"))
async def help_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, ADMIN_TEXT, reply_markup=admin_keyboard())