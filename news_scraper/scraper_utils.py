import codecs
import json
import time

from random import randint
from news_scraper import config, ProjectVariables, SCRAPER_DIR
from news_scraper.atomic_dict import AtomicDict

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


def load_json(path: str) -> list:
    try:
        with codecs.open(path, 'r', 'utf-8') as f:
            read = f.read()
            return json.loads(read)
    except Exception as e:
        logging.error(f'load_json cannot harvest data from date {path}\n{e}')
        return []


def save_data_json(data: list) -> None:
    file = f'{SCRAPER_DIR}/data/{ProjectVariables.today_time}.json'
    try:
        with codecs.open(file, 'a+', 'utf-8') as f:
            json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
    except Exception as e:
        logging.error(f'save_data_json could not save data to {file}\n{e}')


def dict_to_list(data: AtomicDict) -> list:
    list_data = []
    for title, article in data.items():
        article['title'] = title
        list_data.append(article)

    return list_data


def list_to_dict(data: list) -> AtomicDict:
    dict_data = AtomicDict()
    for article in data:
        title = article["title"]
        del article["title"]
        dict_data[title] = article

    return dict_data
