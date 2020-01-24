from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class ZemAVek(Scraper):
    def __init__(self):
        super().__init__()
        self.data = AtomicDict()
        self.yesterdays_data = {}
        self.url = self.config.get('URL', 'ZemAVek')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page))
        # current_content = self.get_file_content(self.url)
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data.copy()

    def get_new_articles(self):
        page = 1
        still_new = True
        max_page = int(self.config.get('Settings', 'MaxPages'))
        while still_new and page <= max_page:
            new_data = self.get_new_articles_by_page(page)
            still_new = self.data.add_all(new_data)
            page += 1

    @scraper_utils.slow_down
    def get_from_article(self):
        for article in self.data:
            article_content = self.get_content(article.url)
            self.data[article.title] = {
                'tags': article_content.find('tags').text,
                'author': article_content.find('sab-author').text,
                'content': ''  # every p till h3
            }

    def still_new_articles(self, new_data):
        return len(new_data.keys() & self.yesterdays_data.keys()) <= 1

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.h3.a.text,
            'values': {
                'url': article.a['href'],
                'time_published': article.find('time')['datetime'],
                'description': article.p.text,
                'photo': article.img['src'],
                'tags': [],
                'author': '',
                'content': ''
            }
        }

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_content(article_content):
        return {
            'title': article_content.title,
            'values': {
                'tags': article_content.find('tags').text,
                'author': article_content.find('sab-author').text,
                'content': ''  # every p till h3
            }
        }


zav = ZemAVek()
zav.get_new_articles()
print(len(zav.data))
for key, values in zav.data.items():
    print(key)
zav.save_data_json(zav.data, 'out.json')
