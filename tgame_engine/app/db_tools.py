"""Database tools."""

from app import models, session


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
