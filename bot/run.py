import asyncio
import logging
from aiogram import Dispatcher,Bot
from config import TOKEN
from hendlers import router
from aiogram.client.bot import DefaultBotProperties


bot = Bot(token=TOKEN,default=DefaultBotProperties(parse_mode='HTML'))

dp = Dispatcher()


async def main():
    await bot.send_message(chat_id=1212795522, text="Bot ishga tushdi\n Og'abek")
    await bot.send_message(chat_id=5502720862, text="Bot ishga tushdi")
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')