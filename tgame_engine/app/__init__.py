"""Bot app."""
from fastapi import FastAPI
import telebot
from app import config

bot = telebot.TeleBot(config.BOT_TOKEN)
app = FastAPI()


@app.post('/'+config.BOT_TOKEN)
async def getMessage(message):
    bot.process_new_updates([
            telebot.types.Update.de_json(
                message
            )
    ])
    return message, 200


bot.remove_webhook()
bot.set_webhook(url=config.APP_URL+config.BOT_TOKEN)
