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
    try:
        queue = db_tools.get_users_for_message()
    except:
        return
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
            _user = queue_item.user
            tg_id = str(_user.telegram_id)
            db_tools.push_story_message_to_queue(
                _user, str(message.get('link')), tg_id
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
    try:
        queue = db_tools.get_users_for_typing()
    except:
        return
    for queue_item in queue:
        try:
            bot.send_chat_action(
                queue_item.user.telegram_id,
                queue_item.pre_message
            )
        except Exception:
            db_tools.session.delete(queue_item)
            db_tools.session.commit()


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


def user_info(user: models.User, tg_id: int):
    try:
        target_user = db_tools.get_user(tg_id)
    except:
        return
    if not target_user:
        return
    if target_user.queue_message:
        place_queue = db_tools.session.query(models.QueueMessage).filter_by(
            user=target_user,
        ).first()
        message = place_queue.message
        referal_need = place_queue.referal_need
    else:
        message, referal_need = 'No', 'No'

    text = '''
    Игрок - {tg_id}
    Сейчас на  - {point}
    Привёл - {referal_quantity}
    В очереди - {message}
    referal_need - {referal_need}
    '''.format(
        tg_id=target_user.telegram_id,
        point=target_user.point,
        referal_quantity=target_user.referal_quantity,
        message = message,
        referal_need = referal_need,
    )
    bot.send_message(user.telegram_id, text)


def check_command(user: models.User, message: str):
    if message[:4] == 'kuku':
        if message[4:7] == 'inf':
            try:
                tg_id_target = int(message[7:].strip())
            except:
                return
            user_info(user, tg_id_target)
        elif message[4:7] == 'sgp':
            point, tg_user_id = message[7:].strip().split('-')
            try:
                target_user = db_tools.get_user(tg_user_id)
            except:
                return
            db_tools.set_story_point(target_user, point)
    else:
        tell_story(user, message)

