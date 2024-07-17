from aiogram          import Bot, Dispatcher
from src.bot.handlers import router
from src.core.config  import settings
import os
# import logging
# import asyncio

bot = Bot(token=settings.token)
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