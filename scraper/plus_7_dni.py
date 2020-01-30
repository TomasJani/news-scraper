from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class Plus7Dni(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(f'scraper/data/plus_7_dni/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'Plus7Dni')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'Plus7Dni'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'Plus7Dni')}")
            return AtomicDict()

        current_content.find(class_='articles-quiz-popular').decompose()

        for article in current_content.find_all(class_='article-tile'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.find(class_='article-tile__text').find('h2').get_text(),
            'values': {
                'url': article.find(class_='heading')['href'],
                'time_published': article.find(class_='meta__item meta__item--datetime datetime-default').get_text(),
                'description': article.find(class_='perex').get_text().strip(),
                'photo': article.find('img')['data-src'],
                'tags': '',
                'author': '',
                'content': ''
            }
        }

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(title, article_content):
        return {
            'title': title,
            'values': {
                'tags': '',
                'author': article_content.find(class_='article-author').find('span').get_text(),
                'content': article_content.find(class_='article-body').get_text()
            }
        }
