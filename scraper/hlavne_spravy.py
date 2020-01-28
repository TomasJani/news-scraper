from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class HlavneSpravy(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(f'data/hlavne_spravy/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'HlavneSpravy')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'HlavneSpravy'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'HlavneSpravy')}")
            return AtomicDict()
        for article in current_content.find_all(class_='t6'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.h3.text,
            'values': {
                'url': article.find('a')['href'],
                'time_published': '',
                'description': article.find('p').get_text(),
                'photo': article.find(class_='post-thumb')['style'],
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
                'time_published': article_content.find(class_='article-content').find('p').get_text(),
                'tags': '',
                'author': '',  # Reconsider
                'content': article_content.find(class_='article-content').get_text().strip()
            }
        }


hs = HlavneSpravy()
hs.get_new_articles()
print(len(hs.data))
hs.save_data_json(hs.data, site='hlavne_spravy')
