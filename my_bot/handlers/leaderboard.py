import time

from aiogram import types
from aiogram.types import ParseMode
from database import db_connection
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup


async def leaderboard_command(message: types.Message):
    query = "SELECT * FROM users"
    await db_connection.execute(query)
    users = await db_connection.fetchall()
    sorted_data = sorted(users, key=lambda x: x['point'], reverse=True)[0:10]
    nt = {
        0: "🥇",
        1: "🥈",
        2: "🥉",
    }

    cur = ''
    for i in range(len(sorted_data)):
        if i < 3:
            cur += str(nt.get(i, i + 1)) + ' ' + sorted_data[i]['login'] + ' *' + str(sorted_data[i]['point']) + '*\n\n'
        else:
            cur += str(i + 1) + '. ' + sorted_data[i]['login'] + ' *' + str(sorted_data[i]['point']) + '*\n'
    await message.answer(f"🏆 Now you can see the top {min(10, len(sorted_data))} best players\n\n" + cur,
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=InlineKeyboardMarkup().add(
                             InlineKeyboardButton("🏘 Main menu", callback_data='main_menu')))
