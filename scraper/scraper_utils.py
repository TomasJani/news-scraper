import configparser
import time
from random import randint

config = configparser.ConfigParser()
config.read('../config.ini')


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
        except:  # Correct exceptions
            print('error in scrape')
            return None
        else:
            return res

    return wrapper

# Random scrape time
