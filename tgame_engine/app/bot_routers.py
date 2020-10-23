"""Bot web points."""
from app import bot, db_tools, bot_engine


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    user = db_tools.get_user(msg.from_user.id)
    bot_engine.tell_story(user)


@bot.message_handler(content_types=['text'])
def text(msg):
    user = db_tools.get_user(msg.from_user.id)
    bot_engine.tell_story(user, msg.text)
