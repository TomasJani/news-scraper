import configparser
import logging
import os
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

for directory in ['scraper/data', 'scraper/logs', 'scraper/data/dennik_n', 'scraper/data/hlavne_spravy',
                  'scraper/data/plus_7_dni', 'scraper/data/sme', 'scraper/data/zem_a_vek']:
    if not os.path.exists(directory):
        os.makedirs(directory)

logging.basicConfig(filename=f'scraper/logs/{today_time}.log',
                    format='%(asctime)s :: %(filename)s :: %(levelname)s = %(message)s',
                    level=logging.INFO)
