from datetime import datetime

from scraper import scraper_utils, DATE_TIME_FORMAT, root_logger as logging, SCRAPER_DIR
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class ZemAVek(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(
            f'{SCRAPER_DIR}/data/zem_a_vek/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'ZemAVek')

    @staticmethod
    def main():
        zav = ZemAVek()
        zav.get_new_articles()
        print(len(zav.data))
        zav.save_data_json(zav.data, site='zem_a_vek')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'ZemAVek'))
        if current_content is None:
            logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'ZemAVek')}")
            return AtomicDict()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.h3.a.text,
            'values': {
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
        }

    @staticmethod
    def time_formater(article):
        corrected_datetime = article.find('time')['datetime'][:-2] + ':' + article.find('time')['datetime'][-2:]
        return datetime.fromisoformat(corrected_datetime).strftime(DATE_TIME_FORMAT)

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(title, article_content):
        return {
            'title': title,
            'values': {
                'tags': ZemAVek.get_correct_tags(article_content),
                'author': article_content.find(class_='author').find('a').get_text(),
                'content': ZemAVek.get_correct_content(article_content)
            }
        }

    @staticmethod
    def get_correct_tags(article_content):
        if article_content.find(class_='tags') is not None:
            return article_content.find(class_='tags').get_text().split(' ', 2)[2]
        else:
            ""

    @staticmethod
    def get_correct_content(article_content):
        text = article_content.find(class_='entry-content')
        for script in text.find_all('script'):
            script.decompose()
        return Scraper.get_part(text.get_text(), separator='Zdroje:', part=0)
