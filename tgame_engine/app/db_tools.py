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


def get_user(telegram_id: int) -> models.User:
    """Return user if one exist or add new user to db.

    Parameters:
        telegram_id: telegram id

    Returns:
        User object
    """

    user = session.query(models.User).filter_by(
        telegram_id=telegram_id
    ).first()
    if user:
        return user
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
    user.last_activity = datetime.utcnow
    session.add(user)
    session.commit()


def set_story_point(user: models.User, point: str):
    """Remember where user in story.

    Parameters:
        user: player
        point: story point
    """
    user.point = int(point)
    user.last_activity = datetime.utcnow
    session.add(user)
    session.commit()


def get_users_for_typing() -> List[models.QueueMessage]:
    """Return users whom have to send 'typing'.

    Returns:
        list of users
    """
    users = session.query(models.QueueMessage).filter(
        models.QueueMessage.start_typing_time <= datetime.utcnow()
    ).all()
    return users


def get_users_for_message() -> List[models.QueueMessage]:
    """Return users whom have to send message.

    Returns:
        list of users
    """
    users = session.query(models.QueueMessage).filter(
        models.QueueMessage.message_time <= datetime.utcnow()
    ).all()
    return users


def push_story_message_to_queue(user: models.User, point: str):
    """Put story message to queue.

    Parameters:
        user: player
        point: story point
    """
    message = story.get_message(point)

    if message['img']:
        pre_message = cfg['chat_actions']['upload_photo']
    elif message['audio']:
        pre_message = cfg['chat_actions']['record_audio']
    elif message['document']:
        pre_message = cfg['chat_actions']['upload_document']
    elif message['text']:
        pre_message = cfg['chat_actions']['typing']

    message_time = datetime.utcnow() + timedelta(seconds=int(message['timeout']))
    start_typing_time = message_time - timedelta(
        seconds=cfg['chat_actions']['time_before']
    )

    session.add(models.QueueMessage(
        user=user,
        start_typing_time=start_typing_time,
        message_time=message_time,
        pre_message=pre_message,
        message=json.dumps(message),
        message_point=point,
    ))
    session.commit()


def delete_user_from_queue(queue_item: models.QueueMessage):
    """Delete user from queue.

    Parameters:
        queue_item: which item delete
    """
    session.delete(queue_item)
    session.commit()
