import configparser
import os

from news_scraper.definitions import *
from news_scraper.ProjectVariables import ProjectVariables

config = configparser.ConfigParser()
config.read(f'{ROOT_DIR}/config.ini')

config = configparser.ConfigParser()
config.read(f'{ROOT_DIR}/config.ini')

directories = list(map(lambda data_directories: f'{SCRAPER_DIR}{data_directories}',
                       ['/data', '/logs', '/data/dennik_n', '/data/hlavne_spravy',
                        '/data/plus_7_dni', '/data/sme',
                        '/data/zem_a_vek']))
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

from news_scraper.execute import start, set_and_scrape
