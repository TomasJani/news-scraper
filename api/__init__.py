import configparser
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta

today_time = datetime.now().strftime("%b_%d_%Y")
yesterday_time = (datetime.now() - timedelta(days=1)).strftime("%b_%d_%Y")


def update_time():
    global today_time
    global yesterday_time
    today_time = datetime.now().strftime("%b_%d_%Y")
    yesterday_time = (datetime.now() - timedelta(days=1)).strftime("%b_%d_%Y")


config = configparser.ConfigParser()
config.read('config.ini')

for directory in ['api/data', 'api/logs']:
    if not os.path.exists(directory):
        os.makedirs(directory)

logging.basicConfig(filename=f'api/logs/{today_time}.log',
                    format='%(asctime)s :: %(levelname)s = %(message)s',
                    level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
db = SQLAlchemy(app)

from api import routes
