from datetime import datetime
from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, DATE_TIME_FORMAT, SCRAPER_DIR
from news_scraper.atomic_dict import AtomicDict
from news_scraper.enums.categories import Category
from news_scraper.enums.site import Site
from news_scraper.scraper_utils import list_to_dict, dict_to_list, load_json
from news_scraper.scrapers.abstract_scraper import Scraper


class ZemAVek(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicDict = list_to_dict(load_json(
            f'{SCRAPER_DIR}/data/{self.yesterday_time}.json')) or AtomicDict()
        self.site: Site = Site.ZemAVek
        self.url: str = self.config.get('URL', self.site.value)

    @staticmethod
    def main() -> list:
        zav = ZemAVek()
        zav.get_new_articles()
        print(len(zav.data))
        return dict_to_list(zav.data)

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicDict:
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, self.site))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, self.site)}")
            return AtomicDict()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article, self.site)

        return new_data

    @scraper_utils.validate_dict
    def scrape_article(self, article: Tag) -> Dict[str, dict]:
        return {
            'title': article.h3.a.text,
            'values': {
                'site': self.site.value,
                'category': Category.HomeNews.value,
                'url': article.find('a')['href'],
                'time_published': ZemAVek.time_formater(article),
                'description': article.find('p').get_text(),
                'photo': article.find('img')['data-lazy-src'],
                'tags': '',
                'author': '',
                'content': ''
            }
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
            'values': {
                'tags': ZemAVek.get_correct_tags(article_content),
                'author': article_content.find(class_='author').find('a').get_text(),
                'content': ZemAVek.get_correct_content(article_content)
            }
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
