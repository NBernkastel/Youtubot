from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from src.utils.text_constants import HELP_TEXT

help_router = Router()

@help_router.message(Command("help"))
async def help_hand(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, HELP_TEXT)