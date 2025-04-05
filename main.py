from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command,CommandStart
from config import BOT_TOKEN
from handlers import start_handler, show_all_operations, router
from updateRouter import up_router
import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.include_router(up_router)

@dp.message(CommandStart())
async def handle_start(message: Message):
    await start_handler(message)

@dp.message(lambda m: m.text == "📋 Подивитись усі операціїї")
async def handle_all(message: Message):
    await show_all_operations(message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot off')

