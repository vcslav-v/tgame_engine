"""Story engine."""
from telebot import types

from app import bot, models
from app.story import story


def send_story_message(user: models.User):
    """Send story message.

    Parameters:
        user: player whom send story
    """
    message = story[user.story_branch][user.point]
    if message['img']:
        bot.send_photo(
            chat_id=user.telegram_id,
            photo=message['img'],
            reply_markup=make_keyboard(story['answers']),
        )
    if message['audio']:
        bot.send_voice(
            chat_id=user.telegram_id,
            voice=message['audio'],
            reply_markup=make_keyboard(story['answers']),
        )
    if message['document']:
        bot.send_document(
            chat_id=user.telegram_id,
            data=message['document'],
            reply_markup=make_keyboard(story['answers']),
        )
    if message['text']:
        bot.send_message(
            chat_id=user.telegram_id,
            text=message['text'],
            reply_markup=make_keyboard(story['answers']),
        )


def make_keyboard(buttons: dict) -> types.ReplyKeyboardMarkup:
    """Make telegram keyboard markup.

    Returns:
        telegram keyboard markup
    """
    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    for button in buttons:
        keyboard.add(button)
    return keyboard
