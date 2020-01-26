import configparser
import logging
from datetime import datetime
from datetime import timedelta

today_time = datetime.now().strftime("%b_%d_%Y")
yesterday_time = (datetime.now() - timedelta(days=1)).strftime("%b_%d_%Y")

config = configparser.ConfigParser()
config.read('../config.ini')

logging.basicConfig(filename=f'logs/{today_time}.log',
                    format='%(asctime)s :: %(filename)s :: %(levelname)s = %(message)s',
                    level=logging.INFO)
