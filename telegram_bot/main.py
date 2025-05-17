import asyncio
import os

from aiogram import Dispatcher
from dotenv import load_dotenv

import auth
from bot_instance import bot
from scheduler import start_scheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DJANGO_API_URL = os.getenv("DJANGO_API_URL")


async def main():
    dp = Dispatcher()
    dp.include_router(auth.router)

    start_scheduler()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
