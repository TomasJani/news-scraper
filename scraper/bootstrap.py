import configparser
import logging

from datetime import datetime

today_time = datetime.now().strftime("%b_%d_%Y")

config = configparser.ConfigParser()
config.read('../config.ini')

logging.basicConfig(filename=f'logs/{today_time}.log',
                    format='%(asctime)s :: %(filename)s :: %(levelname)s = %(message)s',
                    level=logging.INFO)
