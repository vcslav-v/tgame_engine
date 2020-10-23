"""Story loader."""
import json

with open('story.json') as json_file:
    story = json.load(json_file)


def get_message(point: int) -> dict:
    """Find need message with point.

    Parameters:
        point: story point

    Returns:
        message
    """
    return story[str(point)]
