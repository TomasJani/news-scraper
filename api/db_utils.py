import codecs
import json
import logging

from scraper import yesterday_time


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
