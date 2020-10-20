from app import config, bot

def main():
    url = 'https://' + config.APP_URL + config.BOT_TOKEN
    bot.remove_webhook()
    bot.set_webhook(url)