from app import bot_engine
from time import sleep


def main():
    """Check queue and send message."""
    while True:
        bot_engine.send_typings()
        bot_engine.send_message_from_queue()
        sleep(1)
