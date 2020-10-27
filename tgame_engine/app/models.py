"""SQLAlchemy models."""
from datetime import datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.config import config

Base = declarative_base()


class User(Base):
    """User."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # noqa WPS125
    telegram_id = Column(Integer)
    story_branch = Column(String, default=config['start']['brunch'])
    point = Column(Integer, default=config['start']['point'])
    last_activity = Column(DateTime, default=datetime.utcnow())
    queue_message = relationship(
        'QueueMessage',
        back_populates='user',
    )

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
    
    def is_queue_overflow(self):
        return len(self.queue_message) >= 2


class QueueMessage(Base):
    """Queue for pending message send."""
    __tablename__ = 'queue_message'
    id = Column(Integer, primary_key=True)  # noqa WPS125
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="queue_message")
    start_typing_time = Column(DateTime)
    message_time = Column(DateTime)
    pre_message = Column(String, default=config['chat_actions']['typing'])
    message = Column(JSON)
    message_point = Column(String)
    marker = Column(JSON)
    is_story = Column(Boolean, default=True)
