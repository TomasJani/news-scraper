import configparser
import os

from datetime import datetime, timedelta

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s = %(message)s'
TIME_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = f'{TIME_FORMAT} %H:%M'
WEB_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
today_time = datetime.utcnow().strftime(TIME_FORMAT)
yesterday_time = (datetime.utcnow() - timedelta(days=1)).strftime(TIME_FORMAT)


def update_time():
    global today_time
    global yesterday_time
    today_time = datetime.now().strftime(TIME_FORMAT)
    yesterday_time = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)


config = configparser.ConfigParser()
config.read('config.ini')

for directory in ['scraper/data', 'scraper/logs', 'scraper/data/dennik_n', 'scraper/data/hlavne_spravy',
                  'scraper/data/plus_7_dni', 'scraper/data/sme',
                  'scraper/data/zem_a_vek']:  # dynamic from config sections
    if not os.path.exists(directory):
        os.makedirs(directory)

from scraper.execute import start, set_and_scrape
