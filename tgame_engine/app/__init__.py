"""Bot app."""
import json

import telebot
from flask import Flask, request

from app import config

bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)


from app import bot_routers


@app.route('/'+config.BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([
            telebot.types.Update.de_json(
                request.stream.read().decode("utf-8")
            )
    ])
    return 'ok', 200


@app.route('/test/', methods=['GET'])
def test():
    with open('hi.txt', 'r') as file:
        result = file.read()
    return result


@app.route('/patreon/', methods=['POST'])
def patreon():
    data = json.loads(request.stream.read().decode('utf-8'))
    with open('hi.txt', 'w') as file:
        file.write(str(data))
    if data['data']['type'] == 'member':
        bot.send_message(config.MASTER_USER, data['data']['attributes']['email'])
        bot.send_message(config.MASTER_USER, data['data']['attributes']['patron_status'])
    elif data['data']['type'] == 'pledge':
        bot.send_message(config.MASTER_USER, data['included'][0]['attributes']['email'])
        bot.send_message(config.MASTER_USER, data['included'][1]['amount_cents'])
    return 'ok', 200


url = 'https://' + config.APP_URL + config.BOT_TOKEN
bot.remove_webhook()
bot.set_webhook(url)
