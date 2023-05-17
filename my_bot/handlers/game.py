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
                InlineKeyboardButton('🚀 Hard game (25 point)', callback_data='play_game')).add(
                InlineKeyboardButton('🏎 Simple game (+- 1 point)', callback_data='sim_game')
            ).add(
                InlineKeyboardButton('🚁 View instructions', callback_data='view_instructions')
            )
        )
        query = f"DELETE FROM games WHERE tg_id = {cal.message.chat.id}"
        await db_connection.execute(query)
    elif cal.data == 'view_instructions':
        await cal.message.edit_text("If you don't understand something, you can ask @TimurkaABS",
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('🚁 View instructions', callback_data='view_instructions')))
    else:
        words = {
            "cabbage": "A leafy green or purple plant, used as a vegetable.",
            "eggplant": "A purple, aubergine-colored vegetable that is related to tomatoes and potatoes.",
            "garlic": "A strong-smelling pungent-tasting bulb, used as a flavoring in cooking and in herbal medicine.",
            "ginger": "A hot, fragrant spice made from the rhizome of a plant. It is chopped or powdered for cooking, preserved in syrup, or candied.",
            "mint": "A fragrant plant used in cooking or for its aromatic oil. Also a term for perfect or as new condition.",
            "pineapple": "A tropical fruit with a spiky outer skin and sweet insides.",
            "shrimp": "A small free-swimming crustacean with an elongated body, typically marine and frequently harvested for food.",
            "tuna": "A large and swift fish that is popular in cooking, particularly in Japan.",
            "zucchini": "A type of summer squash that is green and commonly used in cooking.",
            "barbecue": "A method of cooking that involves grilling food slowly, with low heat and smoke.",
            "boil": "To heat a liquid to a point where it starts to turn into a gas.",
            "chop": "To cut something into small pieces with repeated sharp blows using an axe or knife.",
            "fry": "To cook over direct heat in hot oil or fat.",
            "rinse": "To wash something in clean water.",
            "stir": "To mix an ingredient into a liquid or other substance by moving an implement such as a spoon in a circular motion.",
            "dumpster": "A large container for rubbish, especially one used by several households or businesses.",
            "be a fad": "To be something that is very popular for a short time, then forgotten.",
            "be a thing of the past": "To be something that no longer exists or happens.",
            "be all the rage": "To be very popular or fashionable at the moment.",
            "be fashionable": "To be in accordance with the current style or trend.",
            "be old-fashioned": "To be not in accordance with the latest style or trend.",
            "be on the way out": "To be in the process of becoming obsolete or out of date.",
            "be the latest thing": "To be the newest and most exciting thing that everyone is talking about or wants.",
            "be the next big thing": "To be something (such as a trend or product) that is currently growing in popularity and expected to be very popular soon.",
            "be trendy": "To be very fashionable or up to date.",
            "come back in style": "To become fashionable or popular again after being out of favor or forgotten.",
            "gain interest/popularity": "To become more popular or interesting to more people.",
            "go out of style": "To become less popular or fashionable.",
            "lose interest/popularity": "To become less popular or interesting to people.",
            "be worth it": "To be deserving of the time, effort, or money spent on it.",
            "boost": "To increase or improve something, such as sales or morale.",
            "can’t afford": "Not having enough money to pay for something.",
            "take a salary cut": "To agree to accept less money than you were earning before.",
            "trade": "To exchange something, such as goods or services, in a transaction.",
            "value": "The worth or importance of something.",
            "audience": "The group of people who watch, read, or listen to something.",
            "celebrity": "A famous person, often in entertainment or sports.",
            "comedian": "A person who entertains by telling jokes or acting in a way that makes people laugh.",
            "designer": "A person who plans the form, look, or workings of something before it's made or built, typically by drawing it in detail.",
            "DJ": "A person who introduces and plays recorded popular music on radio.",
            "entertainer": "A person, such as a singer, dancer, or comedian, whose job is to entertain others.",
            "filmmaker": "A person, such as a director or producer, who makes films/movies.",
            "hero": "A person who is admired for their courage, outstanding achievements, or noble qualities.",
            "icon": "A person or thing regarded as a representative symbol or as worthy of admiration.",
            "model": "A person employed to display clothes by wearing them.",
            "producer": "A person responsible for the financial and managerial aspects of making a movie or broadcast or for staging a play, opera, etc.",
            "performer": "A person who entertains an audience, for example by acting, singing, or dancing on stage.",
            "ad / advertisement": "A notice or announcement in a public medium promoting a product, service, or event.",
            "brand": "A type of product manufactured by a particular company under a particular name.",
            "commercial": "A television or radio advertisement.",
            "fashion statement": "A manner of dress or the creation of an ensemble that is seen as influential.",
            "logo": "A symbol or design that serves to identify an organization or institution.",
            "merchandise": "Goods to be bought and sold.",
            "merchandising": "The activity of promoting the sale of goods, especially by their presentation in retail outlets.",
            "products": "An article or substance that is manufactured or refined for sale.",
            "slogan": "A short and striking or memorable phrase used in advertising.",
            "sponsor": "An individual or organization that provides funds for a project or activity carried out by another.",
            "status symbol": "A possession that is taken to indicate a person's wealth or high social or professional status.",
            "tuna": "A large and active predatory schooling fish of the mackerel family. Also, a common ingredient in sandwiches and salads.",
            "zucchini": "A type of summer squash that is commonly green and typically prepared as a vegetable in cooking.",
            "barbecue": "A method of cooking that involves grilling food, especially meat, over an open fire or on a grill.",
            "boil": "To cook or be cooked by immersing in boiling water or stock.",
            "chop": "To cut something into small pieces with repeated sharp blows using an axe or knife.",
            "fry": "To cook over direct heat in hot oil or fat.",
            "rinse": "To wash something in clean water to remove soap, detergent, dirt, or impurities.",
            "be a fad": "To be something that is extremely popular for a short period of time and then quickly becomes unfashionable.",
            "be a thing of the past": "To be something that has existed or happened in the past but does not exist or happen now.",
            "be all the rage": "To be very popular or fashionable at a particular time or among a particular group of people.",
            "be fashionable": "To be popular, especially in a way that changes often and quickly, based on what is currently considered attractive and appropriate.",
            "be old-fashioned": "To be no longer fashionable or modern.",
            "be on the way out": "To be becoming unfashionable or obsolete.",
            "be the latest thing": "To be the most recent development or fashion.",
            "be the next big thing": "To be expected to become extremely popular or successful in the future.",
            "be trendy": "To be very fashionable or up to date.",
            "come back in style": "To become fashionable or popular again after being out of favor or forgotten.",
            "gain interest/popularity": "To become more popular or interesting to more people.",
            "go out of style": "To become less popular or fashionable.",
            "lose interest/popularity": "To become less popular or interesting to people.",
            "be worth it": "To be deserving of the time, effort, or money spent on it.",
            "boost": "To increase or improve something, such as sales or morale.",
            "can’t afford": "Not having enough money to pay for something.",
            "take a salary cut": "To agree to accept less money than you were earning before.",
            "trade": "To exchange something, such as goods or services, in a transaction.",
            "value": "The worth or importance of something.",
        }
        sp = ['cabbage', 'eggplant', 'garlic', 'ginger', 'mint', 'pineapple', 'shrimp', 'tuna', 'zucchini', 'barbecue',
              'boil',
              'chop', 'fry', 'rinse', 'stir', 'dumpster', 'be a fad', 'be a thing of the past', 'be all the rage',
              'be fashionable', 'be old-fashioned', 'be on the way out', 'be the latest thing', 'be the next big thing',
              'be trendy', 'come back in style', 'gain interest/popularity', 'go out of style',
              'lose interest/popularity',
              'be worth it', 'boost', 'can’t afford', 'take a salary cut', 'trade', 'value', 'audience', 'celebrity',
              'comedian', 'designer', 'DJ', 'entertainer', 'filmmaker', 'hero', 'icon', 'model', 'producer',
              'performer',
              'ad / advertisement', 'brand', 'commercial', 'fashion statement', 'logo', 'merchandise', 'merchandising',
              'products', 'slogan', 'sponsor', 'status symbol']
        d = 58
        if cal.data == 'sim_game':
            ind = random.randint(0, d - 1)
            decrip = words[sp[ind]]
            kl = InlineKeyboardMarkup()
            indexes = []
            for i in range(4):
                indexes.append(random.randint(0, d - 1))
            indexes[random.randint(0, 3)] = ind
            for i in range(4):
                kl.add(InlineKeyboardButton(sp[indexes[i]], callback_data=f'sim_game_{indexes[i]}_{ind}'))
            kl.add(InlineKeyboardButton("🏘 Main menu", callback_data='main_menu'))
            await cal.message.edit_text(
                f"🕵️‍♂️ We riddled the word\n\nDescription:{decrip}\n\n🎯 Choose the right answer, but if you make a mistake, we deduct points.",
                reply_markup=kl)
        else:
            spp = list(cal.data.split('_'))
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('🔄 Play again', callback_data='sim_game'))
            kl.add(InlineKeyboardButton("🏘 Main menu", callback_data='main_menu'))
            if int(spp[-1]) == int(spp[-2]):
                await cal.message.edit_text("🥳 Congratulations, you guessed the words correctly. You earned 1 point",
                                            reply_markup=kl)
                query = "UPDATE users SET point = point + 1, state = 'finish_game' WHERE tg_id = %s"
                await db_connection.execute(query, cal.message.chat.id)
            else:
                await cal.message.edit_text(
                    f"😔 In the last assignment, the correct word was {sp[int(spp[-1])]}. You miss 1 point",
                    reply_markup=kl)

                query = "UPDATE users SET point = point - 1, state = 'finish_game' WHERE tg_id = %s"
                await db_connection.execute(query, cal.message.chat.id)
