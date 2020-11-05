"""Bot web points."""
from app import bot, db_tools, bot_engine, config


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    user = db_tools.get_user(msg.from_user.id, msg.text)
    bot_engine.tell_story(user)


@bot.message_handler(commands=['restart'])
def restart(msg):
    user = db_tools.get_user(msg.from_user.id)
    db_tools.restart_story(user)
    bot_engine.tell_story(user)


@bot.message_handler(commands=['hardreset'])
def hard_reset(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        user = db_tools.get_user(msg.from_user.id)
        db_tools.delete_user(user)


@bot.message_handler(commands=['stats'])
def stats(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        user = db_tools.get_user(msg.from_user.id)
        bot_engine.stats(user)


@bot.message_handler(commands=['clean'])
def clean(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        db_tools.clean_queue()


@bot.message_handler(content_types=['text'])
def text(msg):
    user = db_tools.get_user(msg.from_user.id)
    if not user.is_queue_overflow():
        bot_engine.tell_story(user, msg.text)


@bot.message_handler(content_types=['photo'])
def photo(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        bot.send_message(
            chat_id=msg.from_user.id,
            text=msg.photo[-1].file_id,
        )


@bot.message_handler(content_types=['voice'])
def voice(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        bot.send_message(
            chat_id=msg.from_user.id,
            text=msg,
        )


@bot.message_handler(content_types=['document'])
def doc(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        bot.send_message(
            chat_id=msg.from_user.id,
            text=msg,
        )


@bot.message_handler(content_types=['audio'])
def audio(msg):
    if msg.from_user.id == int(config.MASTER_USER):
        bot.send_message(
            chat_id=msg.from_user.id,
            text=msg,
        )
