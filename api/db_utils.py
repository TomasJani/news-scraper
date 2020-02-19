import codecs
import json
import logging

from api import yesterday_time, today_time


def load_yesterday_data():
    sites = ['dennik_n', 'hlavne_spravy', 'plus_7_dni', 'sme', 'zem_a_vek']  # try to make dynamic
    all_sites = {}
    for site in sites:
        path = f'scraper/data/{site}/{yesterday_time}.json'
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                res = f.read()
                all_sites = {**all_sites, **json.loads(res)}
        except Exception as e:
            logging.error(f'error with opening or reading file {path}\n{e}')
    return all_sites


def save_unsaved_db_data(data):
    try:
        with codecs.open(f'api/data/{today_time}.json', 'w', 'utf-8') as f:
            json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
    except Exception as e:
        logging.error(f'save_data_json could not save data to api/data/{today_time}.json\n{e}')
