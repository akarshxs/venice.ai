import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db
from handlers import user, admin

async def main():
    init_db()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(admin.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
