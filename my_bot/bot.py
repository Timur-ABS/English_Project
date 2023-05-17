import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from my_bot.handlers import register_handlers


API_TOKEN = '6136256059:AAGQyeCjq6L7p5FWP9UAss_EdxGB1BoI_0o'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

register_handlers(dp)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
