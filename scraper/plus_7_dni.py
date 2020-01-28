from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class Plus7Dni(Scraper):
    def __init__(self):
        super().__init__()
        self.data = AtomicDict()
        self.yesterdays_data = self.load_json(f'data/plus_7_dni/{self.yesterday_time}.json')
        self.url = self.config.get('URL', 'Plus7Dni')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'Plus7Dni'))
        # current_content = self.get_file_content(self.url)
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'Plus7Dni')}")
            return AtomicDict()
        for article in current_content.find_all(class_='article-tile'):
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
            still_new = self.data.add_all(new_data, self.yesterdays_data)
            page += 1

        self.get_from_article()

    @scraper_utils.slow_down
    def get_from_article(self):
        for title, article_info in self.data.items():
            article_content = self.get_content(article_info['url'])
            if article_content is None:
                self.logging.error(
                    f"get_from_article got None content with url {self.get_content(article_info['url'])}")
                continue
            additional_data = self.scrape_content(title, article_content)
            self.data.add_additional_data(additional_data)
            self.logging.info(f'(({title})) added to file DB')

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


p7d = Plus7Dni()
p7d.get_new_articles()
print(len(p7d.data))
p7d.save_data_json(p7d.data, site='plus_7_dni')
