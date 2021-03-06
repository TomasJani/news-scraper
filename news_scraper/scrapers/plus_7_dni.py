from typing import Dict

from bs4 import Tag

from news_scraper import scraper_utils, SCRAPER_DIR, ProjectVariables
from news_scraper.atomic_dict import AtomicDict
from news_scraper.enums.categories import Category
from news_scraper.enums.site import Site
from news_scraper.scraper_utils import list_to_dict, dict_to_list, load_json
from news_scraper.scrapers.abstract_scraper import Scraper


class Plus7Dni(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data: AtomicDict = list_to_dict(load_json(
            f'{SCRAPER_DIR}/data/{self.yesterday_time}.json')) or AtomicDict()
        self.site: Site = Site.Plus7Dni
        self.url: str = self.config.get('URL', self.site.value)

    @staticmethod
    def main() -> list:
        p7d = Plus7Dni()
        p7d.get_new_articles()
        print(len(p7d.data))
        return dict_to_list(p7d.data)

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page: str) -> AtomicDict:
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, self.site))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, self.site)}")
            return AtomicDict()

        current_content.find(class_='articles-quiz-popular').decompose()  # try/except

        for article in current_content.find_all(class_='article-tile'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article, self.site)

        return new_data

    @scraper_utils.validate_dict
    def scrape_article(self, article: Tag) -> Dict[str, dict]:
        return {
            'title': article.find(class_='article-tile__text').find('h2').get_text(),
            'values': {
                'site': self.site.value,
                'category': Category.HomeNews.value,
                'url': article.find(class_='heading')['href'],
                'time_published': self.parse_time(
                    article.find(class_='meta__item meta__item--datetime datetime-default')),
                'description': article.find(class_='perex').get_text().strip(),
                'photo': article.find('img')['data-src'],
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
                'author': article_content.find(class_='article-author').find('span').get_text(),
                'content': article_content.find(class_='article-body').get_text()
            }
        }

    def parse_time(self, time_tag: Tag) -> str:
        hours, minutes = time_tag.find(class_='datetime-time').get_text().split(':', 1)
        if time_tag.find(class_='datetime-today'):
            return f'{ProjectVariables.today_time} {hours.zfill(2)}:{minutes}'
        elif time_tag.find(class_='datetime-yesterday'):
            return f'{self.yesterday_time} {hours.zfill(2)}:{minutes}'
        else:
            year = time_tag.find(class_='datetime-year').get_text()
            day, month, _ = time_tag.find(class_='datetime-day-month').get_text().split('.', 2)
            return f'{year}-{month.zfill(2)}-{day.zfill(2)} {hours.zfill(2)}:{minutes}'
