from os import environ

import toml

config = toml.load('config.toml')

BOT_TOKEN = environ.get('BOT_TOKEN')
APP_URL = environ.get('APP_URL')
SQLALCHEMY_DATABASE_URI = (
    'postgresql+psycopg2://postgres:{password}@{db}/postgres'.format(
        db=environ.get('DB'),
        password=environ.get('DB_PASSWORD')
    )
)
MASTER_USER = environ.get('MASTER_USER')
