"""Database tools."""

from app import models, session
from app.config import config


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
    user.point = config['start']['point']
    user.story_branch = config['start']['brunch']
    session.add(user)
    session.commit()


def set_story_point(user: models.User, point: str):
    """Remember where user in story.

    Parameters:
        user: player
        point: story point
    """
    user.point = int(point)
    session.add(user)
    session.commit()
