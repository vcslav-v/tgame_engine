"""Bot app."""
import telebot
from flask import Flask, request


from app import config

bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)


from app import bot_routers


@app.route("/"+config.BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([
            telebot.types.Update.de_json(
                request.stream.read().decode("utf-8")
            )
    ])
    return 'ok', 200


@app.route("/")
def test():
    return 'ok', 200


url = 'https://' + config.APP_URL + config.BOT_TOKEN
bot.remove_webhook()
bot.set_webhook(url)
