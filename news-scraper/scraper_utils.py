import time

from random import randint
from news_scraper import config, ProjectVariables

logging = ProjectVariables.root_logger


def slow_down(fn):
    def wrapper(*args, **kwargs):
        sleep_time = randint(1, int(config.get('Settings', 'WaitTime')))
        time.sleep(sleep_time)
        res = fn(*args, **kwargs)
        time.sleep(sleep_time)
        return res

    return wrapper


def validate_dict(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logging.error(f'validation problem\n{e}')
            return None

    return wrapper
