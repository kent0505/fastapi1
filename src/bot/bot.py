from aiogram          import Bot, Dispatcher
from src.bot.handlers import router
import os
# import logging
# import asyncio

# bot = Bot(token=os.getenv("TOKEN", ""))
bot = Bot(token="1752591343:AAHvNFb73A4amAZ5dOd2xPgalsPOYjAxFW4")
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     try:
#         asyncio.run(main())
#     except:
#         print("STOPPED")

# cd Desktop/fullstack/blog && venv\Scripts\activate
# python src/bot/bot.py