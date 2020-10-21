"""Bot web points."""
from app import bot


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    bot.send_message(msg.chat.id, msg)
