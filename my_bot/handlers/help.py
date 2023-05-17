from aiogram import types
from aiogram.types import ParseMode


async def help_command(message: types.Message):
    await message.answer("If you have any problems or suggestions feel free to email @TimurkaABS")
