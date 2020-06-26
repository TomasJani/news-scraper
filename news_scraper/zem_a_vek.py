from datetime import datetime
from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, DATE_TIME_FORMAT, SCRAPER_DIR
from news_scraper.abstract_scraper import Scraper
from news_scraper.atomic_list import AtomicList


class ZemAVek(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicList = self.load_json(
            f'{SCRAPER_DIR}/data/zem_a_vek/{self.yesterday_time}.json') or AtomicList()
        self.url: str = self.config.get('URL', 'ZemAVek')

    @staticmethod
    def main() -> None:
        zav = ZemAVek()
        zav.get_new_articles()
        print(len(zav.data))
        zav.save_data_json(zav.data, site='zem_a_vek')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicList:
        new_data = AtomicList()
        current_content = self.get_content(self.url_of_page(self.url, page, 'ZemAVek'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'ZemAVek')}")
            return AtomicList()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article: Tag) -> Dict[str, dict]:
        return {
            'title': article.h3.a.text,
            'site': 'zem_a_vek',
            'category': 'domov',
            'url': article.find('a')['href'],
            'time_published': ZemAVek.time_formater(article),
            'description': article.find('p').get_text(),
            'photo': article.find('img')['data-lazy-src'],
            'tags': '',
            'author': '',
            'content': ''
        }

    @staticmethod
    def time_formater(article: Tag) -> str:
        corrected_datetime = article.find('time')['datetime'][:-2] + ':' + article.find('time')['datetime'][-2:]
        return datetime.fromisoformat(corrected_datetime).strftime(DATE_TIME_FORMAT)

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(title: str, article_content: Tag) -> Dict[str, dict]:
        return {
            'title': title,
            'tags': ZemAVek.get_correct_tags(article_content),
            'author': article_content.find(class_='author').find('a').get_text(),
            'content': ZemAVek.get_correct_content(article_content)
        }

    @staticmethod
    def get_correct_tags(article_content: Tag) -> str:
        if article_content.find(class_='tags') is not None:
            return article_content.find(class_='tags').get_text().split(' ', 2)[2]
        else:
            return ''

    @staticmethod
    def get_correct_content(article_content: Tag) -> str:
        text = article_content.find(class_='entry-content')
        for script in text.find_all('script'):
            script.decompose()
        return Scraper.get_part(text.get_text(), separator='Zdroje:', part=0)
