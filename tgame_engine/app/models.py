"""SQLAlchemy models."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # noqa WPS125
    telegram_id = Column(Integer)
    story_branch = Column(String)
    point = Column(Integer)
    last_activity = Column(DateTime, default=datetime.utcnow)
