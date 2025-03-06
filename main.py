import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import router
from database import create_tables

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())