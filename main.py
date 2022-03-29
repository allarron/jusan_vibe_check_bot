#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

usersChatId = []

def start(update, context):
    usersChatId.append({'id' : update.message.chat.id, 'username': update.message.chat.username})
    
    startText = "Привет, поделись своим настроением на данный момент:"
    keyboard = [
        [
            InlineKeyboardButton("😁", callback_data='happy'),
            InlineKeyboardButton("😋", callback_data='sweets'),
            InlineKeyboardButton("😡", callback_data='angry')
        ],

        [
            InlineKeyboardButton("🤒", callback_data='sick'),
            InlineKeyboardButton("😭", callback_data='cry'),
            InlineKeyboardButton("😱", callback_data='shook')
        ], 
        
        [
            InlineKeyboardButton("🍽", callback_data='starved'),
            InlineKeyboardButton("😖", callback_data='unwell'),
            InlineKeyboardButton("☕", callback_data='tea')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(startText, reply_markup= reply_markup)

def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    kek = list({v['id']:v for v in usersChatId}.values())

    if (update.callback_query.message.chat.username):
        username = update.callback_query.message.chat.username
    else:
        username = "у этого пользователя нет юзернейма"
    mention = f"[ {username} ](tg://user?id={str(update.callback_query.message.chat.id)})"
    message = ''
    sticker = ''

    match query.data:
        case 'happy': 
            message = f"{mention} чувствует себя прекрасно"
            sticker = "CAACAgIAAxkBAAP2YkNGpY0F-7gDz41sMGI1QsL3AQ0AAmcPAAJN4hlJZYQBM89MqZIjBA"
        case 'sweets': 
            message = f"у {mention} есть вкусняшки, которыми он хочет поделиться"
        case 'angry': 
            message = f"{mention} сейчас на грани срыва - лучше этого пользователя не беспокоить"
            sticker = "CAACAgIAAxkBAAP3YkNHooZt1XsYqpDMVYUrZVrsGr4AAoYXAAIMMRFJpqr6orGvWRsjBA"
        case 'sick': 
            message = f"{mention} чувствует себя неважно - не отказался бы от вкусняшек"
        case 'cry': 
            message = f"у {mention} горят дедлайны - "
            sticker = "CAACAgIAAxkBAAP4YkNHyjbmdHuTFvLY5tq1rnnSWwgAArMRAAKESJFJt-GUmEZTeu4jBA"
        case 'shook': 
            message = f"{mention} в культурном шоке"
            sticker = "CAACAgIAAxkBAAP5YkNH4wAB1o9m-re2jNpelq3-JC0wAAK5EAACJW4YSYtyK3DI_g-mIwQ"
        case 'unwell': 
            message = f"{mention} подавился грустью - несите ему чашку чая и конфеты"
            sticker = "CAACAgIAAxkBAAP6YkNH--Tx-b3nFwfnmBpEuNsQmtUAAmIFAAI_lcwKQIh5F4bgTIwjBA"
        case 'tea': 
            message = f"{mention} зовет всех на чай - ШӘЙҒААА, ШӘЙ ІШЕМІЗ"
        case 'starved': 
            message = f"{mention} проголодался и крадется на кухню"
            sticker = "CAACAgIAAxkBAAP7YkNIKfmjvPZVI-ghKP11CBn3P-AAAnwqAALgo4IHkNG4BzV321kjBA"

    

    for user in kek:
        context.bot.send_message(chat_id=user['id'], text=message, parse_mode="Markdown")
        if sticker != '':
            context.bot.send_sticker(chat_id=user['id'], sticker=sticker)
        


def main():
    updater = Updater("5141127153:AAG3F8jvy4Nr_PN5nEJjB282ZRl1FbWKG_k", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()