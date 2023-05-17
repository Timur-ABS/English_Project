from aiogram import types
from aiogram.types import ParseMode

async def echo_message(message: types.Message):
    text = f"Вы написали: {message.text}"
    await message.reply(text, parse_mode=ParseMode.HTML)
