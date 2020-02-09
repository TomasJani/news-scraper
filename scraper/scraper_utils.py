import time
import logging

from random import randint
from scraper import config


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
            res = fn(*args, **kwargs)
        except Exception as e:  # Correct exceptions
            logging.error(f'validation problem\n{e}')
            return None
        else:
             return res

    return wrapper

# Random scrape time
# If running longer than x -> Kill
# Delete files after a while
