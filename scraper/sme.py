import logging

from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class SME(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(f'scraper/data/sme/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'SME')

    @staticmethod
    def main():
        sme = SME()
        sme.get_new_articles()
        print(len(sme.data))
        sme.save_data_json(sme.data, site='sme')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'SME'))
        if current_content is None:
            logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'SME')}")
            return AtomicDict()
        for article in current_content.find_all(class_='js-article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @scraper_utils.validate_dict
    def scrape_article(self, article):
        return {
            'title': article.h2.a.text,
            'values': {
                'site': 'sme',
                'url': article.find('a')['href'],
                'time_published': article.find('small').get_text(),
                'description': article.find('p').get_text().split('   ', 1)[0],
                'photo': SME.get_correct_photo(article),
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
                'author': Scraper.may_be_empty(article_content.find(class_='article-published-author'), replacement="SME"),
                'content': SME.get_correct_content(article_content)
            }
        }

    @staticmethod
    def get_correct_photo(article):
        try:
            return article.find('img')['data-src']
        except:  # make safe
            try:
                return article.find('img')['src']
            except:
                logging.error('photo can not be found')

    @staticmethod
    def get_correct_content(article_content):
        text = article_content.find('article')
        for script in text.find_all('script'):
            script.decompose()
        for ad in text.find_all(class_='artemis-promo-labels'):
            ad.decompose()
        text.find(class_='share-box').decompose()
        return text.get_text().strip()
