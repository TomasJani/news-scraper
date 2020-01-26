import codecs
import json
import requests
from scraper.bootstrap import today_time, config, logging
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.config = config
        self.logging = logging

    def get_content(self, url):
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logging.error(f'Problem with request.get called on url {url}\n{e}')
            return None
        except Exception as e: # HtmlParser
            self.logging.error(f'Problem with beautiful soap parsing html at url {url}\n{e}')
        else:
            return soup.body

    @staticmethod
    def get_file_content(path):
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                res = f.read()
                return BeautifulSoup(res, 'html.parser').body
        except Exception as e:
            logging.error(f'error with opening file {path}\n{e}')
            return ""

    @staticmethod
    def url_of_page(url, page):
        return url + f'page/{page}'

    @staticmethod
    def save_data_json(data, file=f'data/{today_time}.json'):
        try:
            with open(file, 'w') as f:
                json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
        except Exception as e:
            logging.error(f'save_data_json could not save data to {file}\n{e}')
