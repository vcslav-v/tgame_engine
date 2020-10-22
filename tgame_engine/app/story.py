"""Story loader."""
import json


def get_story() -> dict:
    """Load story.

    Returns:
        story
    """
    with open('story.json') as json_file:
        story = json.load(json_file)
    return story


story = get_story
