import time

from aiogram import types
from aiogram.types import ParseMode
from database import db_connection
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


async def start_command(message: types.Message):
    query = "SELECT * FROM users WHERE tg_id = %s"
    await db_connection.execute(query, message.chat.id)
    star_key = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🎲 Use default nickname 🎲'))
    user = await db_connection.fetchone()
    if user is None:
        await message.answer(text="👋 Hey there! 👋\n\n🤖 I'm your English language learning bot. \n\n" \
                                  "🏇 Let's get started! 😎 Please, enter your username. 🔠", reply_markup=star_key)
        await db_connection.create_user(message.chat.id)

    else:
        await message.answer(f"☺️ Welcome to the bot, *{user['login']}*\n\n"
                             f"📎 You now have *{user['point']}* points\n\n"
                             f"📋 To see the leaderboard press /leaderboard\n\n"
                             f"🟢 Click on the button to earn points", parse_mode=ParseMode.MARKDOWN,
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton('🚀 Hard game (25 point)', callback_data='play_game')).add(
                                 InlineKeyboardButton('🏎 Simple game (+- 1 point)', callback_data='sim_game')
                             ).add(
                                 InlineKeyboardButton('🚁 View instructions', callback_data='view_instructions')
                             ))
