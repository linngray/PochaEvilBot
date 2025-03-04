import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from modules import welcome

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(welcome.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
