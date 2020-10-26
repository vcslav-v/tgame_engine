"""Story engine."""
from telebot import types

from app import bot, models, story, db_tools


def tell_story(user: models.User, user_answer: str = None):
    """Game flow.

    Parameters:
        user: player whom send story
    """
    point = story.get_point(user, user_answer)
    send_story_message(user, point)
    db_tools.set_story_point(user, point)


def send_story_message(user: models.User, point: str) -> int:
    """Send story message.

    Parameters:
        user: player whom send story
        point: story point
    """
    message = story.get_message(point)

    if message['img']:
        bot.send_photo(
            chat_id=user.telegram_id,
            photo=message['img'],
            reply_markup=make_keyboard(message['answers']),
        )
    if message['audio']:
        bot.send_voice(
            chat_id=user.telegram_id,
            voice=message['audio'],
            reply_markup=make_keyboard(message['answers']),
        )
    if message['document']:
        bot.send_document(
            chat_id=user.telegram_id,
            data=message['document'],
            reply_markup=make_keyboard(message['answers']),
        )
    if message['text']:
        bot.send_message(
            chat_id=user.telegram_id,
            text=message['text'],
            reply_markup=make_keyboard(message['answers']),
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
