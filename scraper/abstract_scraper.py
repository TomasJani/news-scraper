import codecs
import configparser
import json
import urllib

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')

    @staticmethod
    def get_content(url):
        res = requests.get(url) # validate
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.body

    @staticmethod
    def get_file_content(path):
        with codecs.open(path, 'r', 'utf-8') as f:
            res = f.read()
            return BeautifulSoup(res, 'html.parser').body

    @staticmethod
    def url_of_page(url, page):
        return url + f'page/{page}'

    @staticmethod
    def save_data_json(data, file):
        with open(file, 'w') as f:
            json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)


