"""Story loader."""
import json
from app import models
from random import choice

with open('story.json') as json_file:
    story = json.load(json_file)

with open('answ.json') as json_file:
    answers = json.load(json_file)


def get_message(story_point: str) -> dict:
    """Find story message from point.

    Parameters:
        story_point: point in story

    Returns:
        message
    """
    return story[story_point]


def get_point(user: models.User, user_msg: str = None) -> str:
    """Find story point from answers or from last for user.

    Parameters:
        user: player
        user_msg: message from user

    Returns:
        story point
    """
    if not user_msg:
        return str(user.point)
    return str(answers[user_msg])


def get_unexpect_reaction() -> dict:
    """Find unexpect reaction.

    Returns:
        message
    """
    return choice(story['unexpect'])
