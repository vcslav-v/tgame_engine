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
    story_branch = Column(String, default=config['start']['brunch'])
    point = Column(Integer, default=config['start']['point'])
    last_activity = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return """telegram_id: {telegram_id},
        story_branch: {story_branch},
        point: {point},
        last_activity: {last_activity}
        """.format(
            telegram_id=self.telegram_id,
            story_branch=self.story_branch,
            point=self.point,
            last_activity=self.last_activity,
        )
