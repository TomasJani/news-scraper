import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import today_time, yesterday_time, config, root_logger as logging, SCRAPER_DIR


for directory in [f'{SCRAPER_DIR}/api/data']:  # refactor
    if not os.path.exists(directory):
        os.makedirs(directory)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
db = SQLAlchemy(app)

from scraper.api import routes

db.create_all()
