"""SQLAlchemy models."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from app.config import config

Base = declarative_base()


class User(Base):
    """User."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # noqa WPS125
    telegram_id = Column(Integer)
    story_branch = Column(String, default=config['start']['branch'])
    point = Column(Integer, default=config['start']['point'])
    last_activity = Column(DateTime, default=datetime.utcnow)
