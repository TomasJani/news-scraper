import re
from datetime import datetime
from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, DATE_TIME_FORMAT, SCRAPER_DIR
from news_scraper.enums.categories import Category
from news_scraper.enums.site import Site
from news_scraper.scrapers.abstract_scraper import Scraper
from news_scraper.atomic_dict import AtomicDict
from news_scraper.scraper_utils import dict_to_list, list_to_dict


class HlavneSpravy(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicDict = list_to_dict(self.load_json(
            f'{SCRAPER_DIR}/data/{self.yesterday_time}.json')) or AtomicDict()
        self.site: Site = Site.HlavneSpravy
        self.url: str = self.config.get('URL', self.site.value)

    @staticmethod
    def main() -> list:
        hs = HlavneSpravy()
        hs.get_new_articles()
        print(len(hs.data))
        return dict_to_list(hs.data)

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicDict:
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, self.site))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, self.site)}")
            return AtomicDict()
        for article in current_content.find_all(class_='t6'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article, self.site)

        return new_data

    @scraper_utils.validate_dict
    def scrape_article(self, article: Tag) -> Dict[str, dict]:
        return {
            'title': article.h3.text,
            'values': {
                'site': self.site.value,
                'category': Category.HomeNews.value,
                'url': article.find('a')['href'],
                'time_published': datetime.utcnow().strftime(DATE_TIME_FORMAT),
                'description': Scraper.get_part(article.find('p').get_text(), separator='   ', part=1),
                'photo': re.search(r"background-image: url\('(.*?)'\);",
                                   article.find(class_='post-thumb')['style']).group(1),
                'tags': '',
                'author': '',
                'content': ''
            }
        }

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(title: str, article_content: Tag) -> Dict[str, dict]:
        return {
            'title': title,
            'values': {
                'content': HlavneSpravy.get_correct_content(article_content)
            }
        }

    @staticmethod
    def get_correct_content(article_content: Tag) -> str:
        text = article_content.find(class_='article-content')
        for script in text.find_all('script'):
            script.decompose()
        return Scraper.get_part(text.get_text(), separator='Nahlásiť chybu v článku', part=0)
