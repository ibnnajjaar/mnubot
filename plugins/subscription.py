from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('subscribe'))
def subscribe_to_subjects(bot, message: Message):
   message.reply(
      "shit",
      reply_markup = InlineKeyboardMarkup([
         [
            InlineKeyboardButton("✅ AI", 'subject_ai'),
            InlineKeyboardButton("Robotics", 'subject_robotics'),
         ]
      ])
   )
