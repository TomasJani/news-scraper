from scraper import scraper_utils, today_time, yesterday_time, root_logger as logging
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class Plus7Dni(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(f'scraper/data/plus_7_dni/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'Plus7Dni')

    @staticmethod
    def main():
        p7d = Plus7Dni()
        p7d.get_new_articles()
        print(len(p7d.data))
        p7d.save_data_json(p7d.data, site='plus_7_dni')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'Plus7Dni'))
        if current_content is None:
            logging.error(
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
                'site': 'plus_7_dni',
                'category': 'domov',
                'url': article.find(class_='heading')['href'],
                'time_published': Plus7Dni.parse_time(
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
    def scrape_content(title, article_content):
        return {
            'title': title,
            'values': {
                'author': article_content.find(class_='article-author').find('span').get_text(),
                'content': article_content.find(class_='article-body').get_text()
            }
        }

    @staticmethod
    def parse_time(time_tag):
        hours, minutes = time_tag.find(class_='datetime-time').get_text().split(':', 1)
        if time_tag.find(class_='datetime-today'):
            return f'{today_time} {hours.zfill(2)}:{minutes}'
        elif time_tag.find(class_='datetime-yesterday'):
            return f'{yesterday_time} {hours.zfill(2)}:{minutes}'
        else:
            year = time_tag.find(class_='datetime-year').get_text()
            day, month, _ = time_tag.find(class_='datetime-day-month').get_text().split('.', 2)
            return f'{year}-{month.zfill(2)}-{day.zfill(2)} {hours.zfill(2)}:{minutes}'
