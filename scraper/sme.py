from scraper import scraper_utils, root_logger as logging, SCRAPER_DIR
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class SME(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(
            f'{SCRAPER_DIR}/data/sme/{self.yesterday_time}.json') or AtomicDict()
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
                'category': 'domov',
                'url': article.find('a')['href'],
                'time_published': SME.get_correct_date(article.find('small').get_text()),
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
                'author': Scraper.may_be_empty(article_content.find(class_='article-published-author'),
                                               replacement="SME"),
                'content': SME.get_correct_content(article_content)
            }
        }

    @staticmethod
    def get_correct_photo(article):
        try:
            return article.find('img')['data-src']
        except TypeError:
            try:
                return article.find('img')['src']
            except TypeError:
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

    @staticmethod
    def get_correct_date(time_str):
        months = ['', 'jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']
        time_str = time_str.translate({ord(i): None for i in '.,'})
        day, month, year, _, time, _ = time_str.split(' ')
        month_str = '{:02d}'.format(months.index(month))
        return f'{year}-{month_str}-{day} {time}'
