"""Story engine."""
import json

from telebot import types

from app import bot, db_tools, models, story


def tell_story(user: models.User, user_answer: str = None):
    """Game flow.

    Parameters:
        user: player whom send story
    """
    user_marker = db_tools.get_marker_user_in_queue(user)
    if user_marker:
        db_tools.push_no_story_message_to_queue(
            user,
            story.get_marker_reaction(user_marker),
        )
    else:
        try:
            point = story.get_point(user, user_answer)
        except KeyError:
            db_tools.push_no_story_message_to_queue(
                user,
                story.get_unexpect_reaction(),
            )
        else:
            db_tools.push_story_message_to_queue(user, point)


def get_action(json_dump: str):
    marker = json.loads(json_dump)
    return marker.get('action')


def send_message_from_queue():
    """Send message to users."""
    queue = db_tools.get_users_for_message()
    for queue_item in queue:
        message = json.loads(queue_item.message)
        if queue_item.marker:
            marker = json.loads(queue_item.marker)
            if marker and marker.get('action') == 'end':
                db_tools.set_end(queue_item.user)

        chat_id = queue_item.user.telegram_id
        reply_markup = make_keyboard(message.get('answers'))

        if message.get('img'):
            bot.send_photo(
                chat_id=chat_id,
                photo=message['img'],
                reply_markup=reply_markup,
            )
        elif message.get('audio'):
            bot.send_voice(
                chat_id=chat_id,
                voice=message['audio'],
                reply_markup=reply_markup,
            )
        elif message.get('document'):
            bot.send_document(
                chat_id=chat_id,
                data=message['document'],
                reply_markup=reply_markup,
            )
        elif message.get('text'):
            bot.send_message(
                chat_id=chat_id,
                text=message['text'],
                reply_markup=reply_markup,
            )

        if queue_item.message_point:
            db_tools.set_story_point(queue_item.user, queue_item.message_point)

        if message.get('link'):
            db_tools.push_story_message_to_queue(
                queue_item.user, str(message.get('link'))
            )

        db_tools.delete_user_from_queue(queue_item)


def make_keyboard(buttons: dict = None) -> types.ReplyKeyboardMarkup:
    """Make telegram keyboard markup.

    Returns:
        telegram keyboard markup
    """
    if not buttons:
        return
    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    for button in buttons:
        keyboard.add(button)
    return keyboard


def send_typings():
    """Send chat status to users."""
    queue = db_tools.get_users_for_typing()
    for queue_item in queue:
        bot.send_chat_action(
            queue_item.user.telegram_id,
            queue_item.pre_message
        )


def stats(user: models.User):
    """Send game stats.

    Parameters:
        user: admin
    """
    text = '''
    Игроков - {players}
    Из них привели другие игроки - {share}
    Закончили игру - {fin}

    Вы привели - {referal_quantity}
    '''.format(
        players=db_tools.get_quantity_players(),
        share=db_tools.get_quantity_share(),
        fin=db_tools.get_quantity_fin_players(),
        referal_quantity=user.referal_quantity,
    )
    bot.send_message(user.telegram_id, text)
