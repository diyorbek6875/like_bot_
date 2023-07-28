import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from likedb import LikeDB
TOKEN=os.environ['TOKEN']

db = LikeDB('db.json')

def main(update, context):
    bot = context.bot

    chat_id = update.message.chat.id
    text = "Send me a photo"

    bot.sendMessage(chat_id=chat_id, text=text)

def count(update, context):
    query = update.callback_query

    message_id = query.message.message_id
    data = query.data
    chat_id = query.message.chat.id
    
    if data == 'like_emoji':
        db.add_like(chat_id, message_id)
        query.answer(text="You liked the photo")

    elif data == 'dislike_emoji':
        db.add_dislike(chat_id, message_id)
        query.answer(text="You disliked the photo")

    likes = db.get_likes(message_id)
    dislikes = db.get_dislikes(message_id)
    button1 = InlineKeyboardButton(text=f'👍 {likes}', callback_data="like_emoji")
    button2 = InlineKeyboardButton(text=f'👎 {dislikes}', callback_data="dislike_emoji")
    keyboard = InlineKeyboardMarkup([[button1, button2]])

    query.edit_message_reply_markup(reply_markup=keyboard)

def photo(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    photo = update.message.photo[-1].file_id

    message_id = update.message.message_id

    db.add_image(str(message_id+1))

    button1 = InlineKeyboardButton(text='👍', callback_data="like_emoji")
    button2 = InlineKeyboardButton(text='👎', callback_data="dislike_emoji")
    keyboard = InlineKeyboardMarkup([[button1, button2]])
    
    bot.sendPhoto(chat_id=chat_id, photo=photo, reply_markup=keyboard)

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', main))  
dp.add_handler(CallbackQueryHandler(count))
dp.add_handler(MessageHandler(Filters.photo, photo))

updater.start_polling()
updater.idle()