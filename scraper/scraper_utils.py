import configparser
import time

config = configparser.ConfigParser()
config.read('../config.ini')


def slow_down(fn):
    def wrapper(*args, **kwargs):
        sleep_time = int(config.get('Settings', 'WaitTime'))
        time.sleep(sleep_time)
        res = fn(*args, **kwargs)
        time.sleep(sleep_time)
        return res

    return wrapper

# Random scrape time
