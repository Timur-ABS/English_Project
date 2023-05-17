from aiogram import types
from database import db_connection
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.types import ParseMode
from database import db_connection
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

import random


async def callback_query_handler(cal: types.CallbackQuery):
    if cal.data == 'play_game':
        await cal.answer("😎 Let's start")
        query = "UPDATE users SET state = %s WHERE tg_id = %s"
        await db_connection.execute(query, ('play_game', cal.message.chat.id))
        query = f"DELETE FROM games WHERE tg_id = {cal.message.chat.id}"
        await db_connection.execute(query)
        words = ['rinse', 'boost', 'trade', 'value', 'brand', 'model', 'cheer', 'reply', 'tough', 'shift', 'money',
                 'blame', 'fault', 'prove', 'vague']
        query = f"INSERT INTO games (tg_id, guessed_word, attempts, message_id) VALUES ({cal.message.chat.id}, '{words[random.randint(0, len(words) - 1)]}', '',{cal.message.message_id})"
        await db_connection.execute(query)
        await cal.message.edit_text("🕵️ We made a new word, try to guess.\n\n✍️ Write offers directly to the chat\n\n"
                                    "🤖 Your attempts:",
                                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                        '🔄 Change word', callback_data='play_game'
                                    )).add(
                                        InlineKeyboardButton("🏘 Main menu", callback_data='main_menu')
                                    ))
    elif cal.data == 'main_menu':
        query = "SELECT * FROM users WHERE tg_id = %s"
        await db_connection.execute(query, cal.message.chat.id)
        user = await db_connection.fetchone()
        await cal.message.edit_text(
            f"☺️ Welcome to the bot, *{user['login']}*\n\n"
            f"📎 You now have *{user['point']}* points\n\n"
            f"📋 To see the leaderboard press /leaderboard\n\n"
            f"🟢 Click on the button to earn points", parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('🚀 Play game', callback_data='play_game')).add(
                InlineKeyboardButton('🚁 View instructions', callback_data='view_instructions')
            )
        )
        query = f"DELETE FROM games WHERE tg_id = {cal.message.chat.id}"
        await db_connection.execute(query)
