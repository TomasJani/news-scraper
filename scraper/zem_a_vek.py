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
        if current_content is None:
            self.logging.error(f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page)}")
            return AtomicDict()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    def get_new_articles(self):
        page = 1
        still_new = True
        max_page = int(self.config.get('Settings', 'MaxPages'))
        while still_new and page <= max_page:
            new_data = self.get_new_articles_by_page(page)
            if len(new_data) == 0:
                self.logging.error(f'get_new_articles is not getting new data from {self.url} at {page} page')
            still_new = self.data.add_all(new_data)
            page += 1

        self.get_from_article()

    @scraper_utils.slow_down
    def get_from_article(self):
        for title, article_info in self.data.items():
            article_content = self.get_content(article_info['url'])
            if article_content is None:
                self.logging.error(f"get_from_article got None content with url {self.get_content(article_info['url'])}")
                continue
            additional_data = self.scrape_content(title, article_content)
            self.data.add_additional_data(additional_data)
            self.logging.info(f'(({title})) was successfully added to file DB')

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.h3.a.text,
            'values': {
                'url': article.find('a')['href'],
                'time_published': article.find('time')['datetime'],
                'description': article.find('p').get_text(),
                'photo': article.find('img')['src'],  # Parse URL
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
                'tags': article_content.find(class_='tags').get_text(),  # Parse Tags
                'author': article_content.find(class_='author').find('a').get_text(),
                'content': article_content.find(class_='entry-content').get_text()
            }
        }


zav = ZemAVek()
zav.get_new_articles()
print(len(zav.data))
zav.save_data_json(zav.data)
