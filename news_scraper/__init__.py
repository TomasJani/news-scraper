import configparser
import logging
import os

from datetime import datetime, timedelta
from news_scraper.definitions import *

config = configparser.ConfigParser()
config.read(f'{ROOT_DIR}/config.ini')

today_time = datetime.utcnow().strftime(TIME_FORMAT)
yesterday_time = (datetime.utcnow() - timedelta(days=1)).strftime(TIME_FORMAT)

config = configparser.ConfigParser()
config.read(f'{ROOT_DIR}/config.ini')

directories = list(map(lambda data_directories: f'{SCRAPER_DIR}{data_directories}', ['/data', '/logs', '/data/dennik_n', '/data/hlavne_spravy',
                                                             '/data/plus_7_dni', '/data/sme', '/data/zem_a_vek']))
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'{SCRAPER_DIR}/logs/{today_time}.log', mode='w', encoding='windows-1250')
handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
root_logger.addHandler(handler)


def update_time():
    global today_time
    global yesterday_time
    global root_logger
    global handler
    today_time = datetime.now().strftime(TIME_FORMAT)
    yesterday_time = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
    handler.close()
    handler.baseFilename = f'{SCRAPER_DIR}/logs/{today_time}.log'
    root_logger.addHandler(handler)


from news_scraper.execute import start, set_and_scrape
