import abc
import codecs
import json
import requests

from abc import ABC
from scraper import scraper_utils
from scraper.atomic_dict import AtomicDict
from scraper import today_time, config, yesterday_time, root_logger as logging, SCRAPER_DIR
from bs4 import BeautifulSoup


class Scraper(ABC):
    def __init__(self):
        self.yesterdays_data = AtomicDict()
        self.data = AtomicDict()
        self.url = None
        self.config = config
        self.yesterday_time = yesterday_time

    def get_new_articles(self):
        page = 1
        still_new = True
        max_page = int(self.config.get('Settings', 'MaxPages'))
        while still_new and page <= max_page:
            new_data = self.get_new_articles_by_page(page)
            if len(new_data) == 0:
                logging.error(f'get_new_articles is not getting new data from {self.url} at {page} page')
            still_new = self.data.add_all(new_data, self.yesterdays_data)
            page += 1

        self.get_from_article()

    @scraper_utils.slow_down
    def get_from_article(self):
        for title, article_info in self.data.items():
            article_content = self.get_content(article_info['url'])
            if article_content is None:
                logging.error(
                    f"get_from_article got None content with url {article_info['url']}")
                continue
            additional_data = self.scrape_content(title, article_content)
            self.data.add_additional_data(additional_data)
            try:
                logging.info(f'[[{article_info["site"]}]] (({title})) added to file DB')
            except UnicodeEncodeError as e:
                logging.info(f'((title was successfully added but can not be encoded))\n{e}')

    @abc.abstractmethod
    def get_new_articles_by_page(self, page):
        """Method Doc"""

    @abc.abstractmethod
    def scrape_content(self, title, article_content):
        """Method Doc"""

    @staticmethod
    def url_of_page(url, page, site):
        if site == 'ZemAVek' or site == 'HlavneSpravy' or site == "DennikN":
            return f'{url}page/{page}'
        elif site == 'Plus7Dni':
            return url + str(page)
        elif site == 'SME':
            return f'{url}page={page}'
        else:
            raise NotImplemented

    @staticmethod
    def may_be_empty(fn, replacement=''):
        if fn is None:
            return replacement
        else:
            return fn.get_text()

    @staticmethod
    def get_part(text, separator='', part=0):
        return text.split(separator, 1)[part].strip()

    @staticmethod
    @scraper_utils.slow_down
    def get_content(url):
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f'Problem with request.get called on url {url}\n{e}')
            return None
        except Exception as e:  # HtmlParser
            logging.error(f'Problem with beautiful soap parsing html at url {url}\n{e}')
        else:
            return soup.body

    @staticmethod
    def get_file_content(path):
        try:
            with codecs.open(path, 'r', 'windows-1250') as f:
                res = f.read()
                return BeautifulSoup(res, 'html.parser').body
        except Exception as e:
            logging.error(f'error with opening file {path}\n{e}')
            return ""

    @staticmethod
    def save_data_json(data, site=""):
        file = f'{SCRAPER_DIR}/data/{site}/{today_time}.json'
        try:
            with codecs.open(file, 'w', 'utf-8') as f:
                json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
        except Exception as e:
            logging.error(f'save_data_json could not save data to {file}\n{e}')

    @staticmethod
    def load_json(file):
        try:
            with codecs.open(file, 'r', 'windows-1250') as f:
                read = f.read()
                return json.loads(read)
        except Exception as e:
            logging.error(f'load_json cannot harvest data from date {file}\n{e}')
            return {}
