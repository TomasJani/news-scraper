import abc
import codecs
import json
import requests

from abc import ABC
from scraper import scraper_utils
from scraper.atomic_dict import AtomicDict
from scraper.bootstrap import today_time, config, logging, yesterday_time
from bs4 import BeautifulSoup


class Scraper(ABC):
    def __init__(self):
        self.data = AtomicDict()
        self.config = config
        self.logging = logging
        self.yesterday_time = yesterday_time

    def get_new_articles(self):
        page = 1
        still_new = True
        max_page = int(self.config.get('Settings', 'MaxPages'))
        while still_new and page <= max_page:
            new_data = self.get_new_articles_by_page(page)
            if len(new_data) == 0:
                self.logging.error(f'get_new_articles is not getting new data from {self.url} at {page} page')
            still_new = self.data.add_all(new_data, self.yesterdays_data)
            page += 1

        self.get_from_article()

    @abc.abstractmethod
    def get_new_articles_by_page(self, page):
        """Method Doc"""

    @scraper_utils.slow_down
    def get_from_article(self):
        for title, article_info in self.data.items():
            article_content = self.get_content(article_info['url'])
            if article_content is None:
                self.logging.error(
                    f"get_from_article got None content with url {self.get_content(article_info['url'])}")
                continue
            additional_data = self.scrape_content(title, article_content)
            self.data.add_additional_data(additional_data)
            self.logging.info(f'(({title})) added to file DB')

    @abc.abstractmethod
    def scrape_content(self, title, article_content):
        """Method Doc"""

    def get_content(self, url):
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logging.error(f'Problem with request.get called on url {url}\n{e}')
            return None
        except Exception as e:  # HtmlParser
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

    def load_json(self, file):
        try:
            with codecs.open(file, 'r', 'utf-8') as f:
                read = f.read()
                return json.loads(read)
        except Exception as e:
            self.logging.error(f'load_json cannot harvest data from date {file}\n{e}')
            return {}

    @staticmethod
    def url_of_page(url, page, site):
        if site == 'ZemAVek' or site == 'HlavneSpravy':
            return url + f'page/{page}'
        elif site == 'Plus7Dni':
            return url + str(page)

    @staticmethod
    def save_data_json(data, file=f'data/{today_time}.json', site=""):  # Refactor
        try:
            with codecs.open(f'data/{site}/{today_time}.json', 'w', 'utf-8') as f:
                json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
        except Exception as e:
            logging.error(f'save_data_json could not save data to {file}\n{e}')
