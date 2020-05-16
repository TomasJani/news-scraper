import abc
import codecs
import json
from abc import ABC
from typing import Optional, Dict

import requests
from bs4 import BeautifulSoup, Tag

from news_scraper import scraper_utils, config, SCRAPER_DIR, ProjectVariables
from news_scraper.atomic_dict import AtomicDict

class Scraper(ABC):
    def __init__(self):
        self.yesterdays_data: AtomicDict = AtomicDict()
        self.data: AtomicDict = AtomicDict()
        self.url: Optional[str] = None
        self.config: dict = config
        self.yesterday_time: str = ProjectVariables.yesterday_time
        self.logging = ProjectVariables.root_logger

    def get_new_articles(self) -> None:
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

    @scraper_utils.slow_down
    def get_from_article(self) -> None:
        for title, article_info in self.data.items():
            article_content = self.get_content(article_info['url'])
            if article_content is None:
                self.logging.error(
                    f"get_from_article got None content with url {article_info['url']}")
                continue
            additional_data = self.scrape_content(title, article_content)
            self.data.add_additional_data(additional_data)
            try:
                self.logging.info(f'[[{article_info["site"]}]] (({title})) added to file DB')
            except UnicodeEncodeError as e:
                self.logging.info(f'((title was successfully added but can not be encoded))\n{e}')

    @abc.abstractmethod
    def get_new_articles_by_page(self, page: int) -> AtomicDict:
        """Method Doc"""

    @abc.abstractmethod
    def scrape_content(self, title: str, article_content: Tag) -> Dict[str, dict]:
        """Method Doc"""

    @staticmethod
    def url_of_page(url: str, page: str, site: str) -> str:
        if site == 'ZemAVek' or site == 'HlavneSpravy' or site == "DennikN":
            return f'{url}page/{page}'
        elif site == 'Plus7Dni':
            return url + str(page)
        elif site == 'SME':
            return f'{url}page={page}'
        else:
            raise NotImplemented

    @staticmethod
    def may_be_empty(dom_part: Optional[Tag], replacement='') -> str:
        if dom_part is None:
            return replacement
        else:
            return dom_part.get_text()

    @staticmethod
    def get_part(text: str, separator='', part=0) -> str:
        return text.split(separator, 1)[part].strip()

    @scraper_utils.slow_down
    def get_content(self, url: str) -> Optional[Tag]:
        try:
            res = requests.get(url)
            return BeautifulSoup(res.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logging.error(f'Problem with request.get called on url {url}\n{e}')
            return None
        except Exception as e:  # HtmlParser
            self.logging.error(f'Problem with beautiful soap parsing html at url {url}\n{e}')
            return None

    def get_file_website_content(self, path: str) -> object:
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                res = f.read()
                return BeautifulSoup(res, 'html.parser').body
        except Exception as e:
            self.logging.error(f'error with opening file {path}\n{e}')
            return ""

    def save_data_json(self, data: Dict[str, dict], site="") -> None:
        file = f'{SCRAPER_DIR}/data/{site}/{ProjectVariables.today_time}'
        try:
            with codecs.open(file, 'w', 'utf-8') as f:
                json.dump(data, sort_keys=True, indent=4, separators=(',', ': '), fp=f, ensure_ascii=False)
        except Exception as e:
            self.logging.error(f'save_data_json could not save data to {file}\n{e}')

    def load_json(self, path: str) -> dict:
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                read = f.read()
                return json.loads(read)
        except Exception as e:
            self.logging.error(f'load_json cannot harvest data from date {path}\n{e}')
            return {}
