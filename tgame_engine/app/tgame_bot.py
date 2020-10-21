"""Bot web points."""
from app import bot, db_tools


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    user = db_tools.get_user(msg.from_user.id)
    send_story_message(user)
    
