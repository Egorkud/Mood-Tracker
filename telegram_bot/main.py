import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import auth

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DJANGO_API_URL = os.getenv("DJANGO_API_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp = Dispatcher()
    dp.include_router(auth.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
