"""Bot app."""
from fastapi import FastAPI
import telebot
from app import config

bot = telebot.TeleBot(config.BOT_TOKEN)
app = FastAPI()


@app.post('/'+config.BOT_TOKEN)
async def getMessage(message):
    print(message)
    bot.process_new_updates([
            telebot.types.Update.de_json(
                message
            )
    ])
    return message, 200

url = 'https://' + config.APP_URL + config.BOT_TOKEN
bot.remove_webhook()
bot.set_webhook(url)
