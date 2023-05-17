from aiogram import types
from aiogram.types import ParseMode
from database import db_connection
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types
from aiogram.types import ParseMode
from database import db_connection
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
import asyncio

import nltk

nltk.download('words')

from nltk.corpus import words


def is_english_word(word):
    return word.lower() in words.words()


async def message(message: types.Message):
    query = "SELECT * FROM users WHERE tg_id = %s"
    await db_connection.execute(query, message.chat.id)
    user = await db_connection.fetchone()
    if user['state'] == 'write_nick':
        await message.answer(text='Good choice 😉', reply_markup=ReplyKeyboardRemove())
        if message.text != '🎲 Use default nickname 🎲':
            query = "UPDATE users SET login = %s, state = %s WHERE id = %s"
            user['login'] = message.text
            await db_connection.execute(query, (message.text, 'finish_reg', user['id']))
        else:
            query = "UPDATE users SET state = %s WHERE id = %s"
            await db_connection.execute(query, ('finish_reg', user['id']))
        await message.answer(f"☺️ Welcome to the bot, *{user['login']}*\n\n"
                             f"📎 You now have *{user['point']}* points\n\n"
                             f"📋 To see the leaderboard press /leaderboard\n\n"
                             f"🟢 Click on the button to earn points", parse_mode=ParseMode.MARKDOWN,
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton('🚀 Play game', callback_data='play_game')).add(
                                 InlineKeyboardButton('🚁 View instructions', callback_data='view_instructions')
                             ))
    elif user['state'] == 'play_game':
        bot = message.bot
        message.text = message.text.replace(' ', '').replace(',', '').replace('.', '').replace('-', '').lower()
        f1, f2 = is_english_word(message.text), len(message.text) == 5
        if f1 and f2:
            query = "SELECT * FROM games WHERE tg_id = %s"
            await db_connection.execute(query, message.chat.id)
            game = await db_connection.fetchone()
            words_list = list(game['attempts'].split('_'))
            if message.text in words_list:
                mes = await bot.send_message(chat_id=user['tg_id'], text="😢 You have already sent this word!")
                await asyncio.sleep(3)
                await bot.delete_message(chat_id=user['tg_id'], message_id=mes.message_id)
            else:
                if game['guessed_word'] == message.text:
                    await bot.delete_message(chat_id=user['tg_id'], message_id=game['message_id'])
                    await bot.send_message(chat_id=user['tg_id'], text='🎉')
                    query = f"DELETE FROM games WHERE tg_id = {user['tg_id']}"
                    await db_connection.execute(query)
                    query = "UPDATE users SET point = point + 25, state = 'finish_game' WHERE tg_id = %s"
                    await db_connection.execute(query, message.chat.id)
                    await bot.send_message(chat_id=user['tg_id'],
                                           text='🎉 You managed to guess the word!\n\n👀 To view the leaderboard press /leaderboard\n\n'
                                                '💪 You can earn more points!',
                                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                               '🚀 New game', callback_data='play_game'
                                           )).add(
                                               InlineKeyboardButton("🏘 Main menu", callback_data='main_menu')
                                           ))
                    query = f"DELETE FROM games WHERE tg_id = {user['tg_id']}"
                    await db_connection.execute(query)
                    query = "UPDATE users SET state = 'finish_game' WHERE tg_id = %s"
                    await db_connection.execute(query, message.chat.id)

                else:
                    if len(game['attempts']) == 0:
                        words_list = []
                    words_list.append(message.text)
                    if len(words_list) == 6:
                        await bot.edit_message_text(chat_id=user['tg_id'], message_id=game['message_id'],
                                                    text="😭 I'm sorry, but you've wasted all your efforts\n\n😊 Try earning points in another game or try again",
                                                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                                        '🔄 Play again', callback_data='play_game'
                                                    )).add(
                                                        InlineKeyboardButton("🏘 Main menu", callback_data='main_menu')
                                                    ))
                        query = f"DELETE FROM games WHERE tg_id = {user['tg_id']}"
                        await db_connection.execute(query)
                        query = "UPDATE users SET state = 'finish_game' WHERE tg_id = %s"
                        await db_connection.execute(query, message.chat.id)
                    elif len(words_list) < 6:
                        cur = ''
                        gaps = {
                            0: 2,
                            1: 4,
                            2: 5,
                            3: 5,
                            4: 4,
                        }
                        # game['guessed_word']
                        attempts = ''
                        for i in range(len(words_list)):
                            cur_u = ''
                            cur_d = ''
                            for j in range(5):
                                if words_list[i][j] == game['guessed_word'][j]:
                                    cur_u += '🟢'
                                elif words_list[i][j] in game['guessed_word']:
                                    cur_u += '🟡'
                                else:
                                    cur_u += '⚪'
                                cur_u += ' '
                                cur_d += gaps[j] * ' ' + words_list[i][j]
                            cur += cur_u + '\n' + cur_d + '\n\n'
                            if i == 0:
                                attempts += words_list[i]
                            else:
                                attempts += '_' + words_list[i]
                        await bot.edit_message_text(chat_id=user['tg_id'], message_id=game['message_id'],
                                                    text="🕵️ We made a new word, try to guess.\n\n✍️ Write offers directly to the chat\n\n"
                                                         "🤖 Your attempts:\n\n" + cur,
                                                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                                        '🔄 Change word', callback_data='play_game'
                                                    )).add(
                                                        InlineKeyboardButton("🏘 Main menu", callback_data='main_menu'))
                                                    )
                        game['attempts'] = attempts
                        await db_connection.execute("UPDATE games set attempts = %s where id = %s",
                                                    (game['attempts'], game['id']))

        else:
            if not f1 and not f2:
                mes = await bot.send_message(chat_id=user['tg_id'], text="😢 There is no such word and the length does not match")
                await asyncio.sleep(3)
                await bot.delete_message(chat_id=user['tg_id'], message_id=mes.message_id)
            elif not f2:
                mes = await bot.send_message(chat_id=user['tg_id'], text="😭 Word length less than 5")
                await asyncio.sleep(3)
                await bot.delete_message(chat_id=user['tg_id'], message_id=mes.message_id)

            else:
                mes = await bot.send_message(chat_id=user['tg_id'], text="😭 There is no such word")
                await asyncio.sleep(3)
                await bot.delete_message(chat_id=user['tg_id'], message_id=mes.message_id)
        await message.delete()
