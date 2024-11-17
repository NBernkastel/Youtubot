import asyncio
import logging
import sys

from aiogram.fsm.storage.redis import RedisStorage

from config import dp, bot, redis_settings
from src.handlers.admin_router import admin_router
from src.handlers.help_router import help_router
from src.handlers.private_rooms_router import private_rooms_router
from src.handlers.start_router import start_router
from src.handlers.subscrite_router import sub_router
from src.utils.sub_task import sub_task


async def start():
    dp.include_routers(start_router)
    dp.include_routers(help_router)
    dp.include_routers(sub_router)
    dp.include_routers(private_rooms_router)
    dp.include_routers(admin_router)
    asyncio.create_task(sub_task())
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())