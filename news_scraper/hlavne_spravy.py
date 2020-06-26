import re
from datetime import datetime
from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, DATE_TIME_FORMAT, SCRAPER_DIR
from news_scraper.abstract_scraper import Scraper
from news_scraper.atomic_list import AtomicList


class HlavneSpravy(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicList = self.load_json(
            f'{SCRAPER_DIR}/data/hlavne_spravy/{self.yesterday_time}.json') or AtomicList()
        self.url: str = self.config.get('URL', 'HlavneSpravy')

    @staticmethod
    def main() -> None:
        hs = HlavneSpravy()
        hs.get_new_articles()
        print(len(hs.data))
        hs.save_data_json(hs.data, site='hlavne_spravy')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicList:
        new_data = AtomicList()
        current_content = self.get_content(self.url_of_page(self.url, page, 'HlavneSpravy'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'HlavneSpravy')}")
            return AtomicList()
        for article in current_content.find_all(class_='t6'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article: Tag) -> Dict[str, str]:
        return {
            'title': article.h3.text,
            'site': 'hlavne_spravy',
            'category': 'domov',
            'url': article.find('a')['href'],
            'time_published': datetime.utcnow().strftime(DATE_TIME_FORMAT),
            'description': Scraper.get_part(article.find('p').get_text(), separator='   ', part=1),
            'photo': re.search(r"background-image: url\('(.*?)'\);",
                               article.find(class_='post-thumb')['style']).group(1),
            'tags': '',
            'author': 'HLAVNÉ SPRÁVY',
            'content': ''

        }

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(title: str, article_content: Tag) -> Dict[str, str]:
        return {
            'title': title,
            'content': HlavneSpravy.get_correct_content(article_content)
        }

    @staticmethod
    def get_correct_content(article_content: Tag) -> str:
        text = article_content.find(class_='article-content')
        for script in text.find_all('script'):
            script.decompose()
        return Scraper.get_part(text.get_text(), separator='Nahlásiť chybu v článku', part=0)
