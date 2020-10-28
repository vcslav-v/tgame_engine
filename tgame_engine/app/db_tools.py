"""Database tools."""

from datetime import datetime, timedelta
import json
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from app import models, story, config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)()

cfg = config.config


def clean_queue():
    """Clean queue."""
    users = session.query(models.QueueMessage).all()
    for user in users:
        session.delete(user)
    session.commit()


def get_user(telegram_id: int, text: str = None) -> models.User:
    """Return user if one exist or add new user to db.

    Parameters:
        telegram_id: telegram id
        text: command text

    Returns:
        User object
    """

    user = session.query(models.User).filter_by(
        telegram_id=telegram_id
    ).first()
    if user:
        return user
    if text:
        add_referal(text)
    user = models.User(telegram_id=telegram_id)
    session.add(user)
    session.commit()
    return user


def restart_story(user: models.User):
    """Restart story progress for user.

    Parameters:
        user: player
    """
    user.point = cfg['start']['point']
    user.story_branch = cfg['start']['brunch']
    user.last_activity = datetime.utcnow()
    session.add(user)
    session.commit()


def set_story_point(user: models.User, point: str):
    """Remember where user in story.

    Parameters:
        user: player
        point: story point
    """
    user.point = int(point)
    user.last_activity = datetime.utcnow()
    session.add(user)
    session.commit()


def get_users_for_typing() -> List[models.QueueMessage]:
    """Return users whom have to send 'typing'.

    Returns:
        list of users
    """
    users = session.query(
        models.QueueMessage,
    ).join(
        models.User
    ).filter(
            models.QueueMessage.start_typing_time <= datetime.utcnow()
    ).filter(
            models.QueueMessage.referal_need <= models.User.referal_quantity
    ).all()
    return users


def get_users_for_message() -> List[models.QueueMessage]:
    """Return users whom have to send message.

    Returns:
        list of users
    """
    users = session.query(models.QueueMessage).filter(
        models.QueueMessage.message_time <= datetime.utcnow()
    ).filter(
        models.QueueMessage.referal_need <= models.QueueMessage.user.referal_quantity # noqa E501
    ).all()
    return users


def push_story_message_to_queue(user: models.User, point: str):
    """Put story message to queue.

    Parameters:
        user: player
        point: story point
    """
    message = story.get_message(point)

    if '{share_url}' in message['text']:
        message['text'].format(
            share_url='https://t.me/{BOT_NAME}?start={telegram_id}'.format(
                BOT_NAME=config.BOT_NAME,
                telegram_id=user.telegram_id
            ))

    if message['img']:
        pre_message = cfg['chat_actions']['upload_photo']
    elif message['audio']:
        pre_message = cfg['chat_actions']['record_audio']
    elif message['document']:
        pre_message = cfg['chat_actions']['upload_document']
    elif message['text']:
        pre_message = cfg['chat_actions']['typing']

    message_time = datetime.utcnow() + timedelta(
        seconds=int(message['timeout'])
    )
    start_typing_time = message_time - timedelta(
        seconds=cfg['chat_actions']['time_before']
    )

    referal_need = message['marker'].get(
        'referal_need'
    ) if message['marker'] else 0

    session.add(models.QueueMessage(
        user=user,
        start_typing_time=start_typing_time,
        message_time=message_time,
        pre_message=pre_message,
        message=json.dumps(message),
        message_point=point,
        marker=json.dumps(message['marker']),
        referal_need=referal_need or 0,
    ))
    session.commit()


def delete_user_from_queue(queue_item: models.QueueMessage):
    """Delete user from queue.

    Parameters:
        queue_item: which item delete
    """
    session.delete(queue_item)
    session.commit()


def push_no_story_message_to_queue(user: models.User, message: dict):
    """Put no story message to queue.

    Parameters:
        user: player
        message: message dict
    """

    if message.get('img'):
        pre_message = cfg['chat_actions']['upload_photo']
    elif message.get('audio'):
        pre_message = cfg['chat_actions']['record_audio']
    elif message.get('document'):
        pre_message = cfg['chat_actions']['upload_document']
    elif message.get('text'):
        pre_message = cfg['chat_actions']['typing']

    message_time = datetime.utcnow() + timedelta(
        seconds=int(message['timeout'])
    )
    start_typing_time = message_time - timedelta(
        seconds=cfg['chat_actions']['time_before']
    )

    session.add(models.QueueMessage(
        user=user,
        start_typing_time=start_typing_time,
        message_time=message_time,
        pre_message=pre_message,
        message=json.dumps(message),
        is_story=False,
    ))
    session.commit()


def get_marker_user_in_queue(user: models.User) -> dict:
    """Find and return marker if user in queue.

    Parameters:
        user: player

    Returns:
        marker or None
    """
    queue_place = session.query(
        models.QueueMessage
    ).filter_by(user=user, is_story=True).first()
    if queue_place and queue_place.marker:
        return json.loads(queue_place.marker)


def add_referal(text: str):
    """Check and add referal.

    Parameters:
        text: start message text
    """
    parent_id = text[7:]
    if not parent_id:
        return
    try:
        parent_id = int(parent_id)
    except ValueError:
        return

    parent = session.query(models.User).filter_by(
        telegram_id=parent_id
    ).first()
    if not parent:
        return
    parent.referal_quantity += 1
    session.add(parent)
    session.commit()


def delete_user(user: models.User):
    """Delete user.

    Parameters:
        user: player
    """
    session.delete(user)
    session.commit()
