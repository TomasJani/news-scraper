from datetime import datetime
from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, DATE_TIME_FORMAT, SCRAPER_DIR
from news_scraper.abstract_scraper import Scraper
from news_scraper.atomic_dict import AtomicDict


class DennikN(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicDict = self.load_json(
            f'{SCRAPER_DIR}/data/dennik_n/{self.yesterday_time}.json') or AtomicDict()
        self.url: str = self.config.get('URL', 'DennikN')

    @staticmethod
    def main() -> None:
        dn = DennikN()
        dn.get_new_articles()
        print(len(dn.data))
        dn.save_data_json(dn.data, site='dennik_n')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicDict:
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'DennikN'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'DennikN')}")
            return AtomicDict()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article: Tag) -> Dict[str, dict]:
        return {
            'title': article.span.text,
            'values': {
                'site': 'dennik_n',
                'category': 'domov',
                'url': article.find(class_='a_art_b').find('a', recursive=False)['href'],
                'time_published': datetime.fromisoformat(article.find('time')['datetime']).strftime(DATE_TIME_FORMAT),
                'description': Scraper.may_be_empty(article.find('p')),
                'photo': DennikN.get_photo(article),
                'tags': '',
                'author': Scraper.may_be_empty(article.find(class_='e_terms_author'), replacement='DENNÍK N'),
                'content': ''
            }
        }

    @scraper_utils.validate_dict
    def scrape_content(self, title: str, article_content) -> Dict[str, dict]:
        return {
            'title': title,
            'values': {
                'tags': self.get_correct_tags(article_content),
                'content': DennikN.get_correct_content(article_content)
            }
        }

    @staticmethod
    def get_photo(article: Tag) -> str:
        if article.find('img') is not None:
            return article.find('img')['data-src']
        else:
            return ""

    def get_correct_content(self, article_content: Tag) -> str:
        if article_content.find(class_='a_single__post') is not None:
            return article_content.find(class_='a_single__post').get_text()
        elif article_content.find(class_='b_single_main') is not None:
            return article_content.find(class_='b_single_main').get_text()
        else:
            self.logging.error('get_correct_content can not find correct classes')
            return ""

    @staticmethod
    def get_correct_tags(article_content: Tag) -> str:
        find_tag = article_content.find(class_='e_terms')
        if find_tag is not None:
            find_tag.find('time').decompose()
            return find_tag.get_text(separator=', ')
        elif article_content.find(class_='e_tag') is not None:
            return article_content.find(class_='e_tag').get_text()
        else:
            return ""
