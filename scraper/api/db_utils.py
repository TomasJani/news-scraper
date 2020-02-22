import codecs
import json
import logging

from scraper.api import yesterday_time, today_time, SCRAPER_DIR


def load_yesterday_data():
    sites = ['dennik_n', 'hlavne_spravy', 'plus_7_dni', 'sme', 'zem_a_vek']  # try to make dynamic
    all_sites = {}
    for site in sites:
        path = f'{SCRAPER_DIR}/data/{site}/{yesterday_time}.json'
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                res = f.read()
                all_sites = {**all_sites, **json.loads(res)}
        except Exception as e:
            logging.error(f'error with opening or reading file {path}\n{e}')
    return all_sites


def save_unsaved_db_data(data):
    path = f'{SCRAPER_DIR}/api/data/{today_time}.json'
    try:
        with codecs.open(path, 'w', 'utf-8') as f:
            json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
    except Exception as e:
        logging.error(f'save_data_json could not save data to {path}\n{e}')


def get_or_create(fn):
    def wrapper(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).first().id
        except AttributeError:  # ONLY IF NONE FOUND
            logging.info(f'{kwargs} is not in DB')
            try:
                return fn(cls, **kwargs)
            except Exception as e:
                logging.error(f'{kwargs} can not be added to DB\n{e}')
    return wrapper
