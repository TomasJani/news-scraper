from scraper import scraper_utils
from scraper.abstract_scraper import Scraper
from scraper.atomic_dict import AtomicDict


class DennikN(Scraper):
    def __init__(self):
        super().__init__()
        self.yesterdays_data = self.load_json(f'scraper/data/dennik_n/{self.yesterday_time}.json') or AtomicDict()
        self.url = self.config.get('URL', 'DennikN')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = AtomicDict()
        current_content = self.get_content(self.url_of_page(self.url, page, 'DennikN'))
        if current_content is None:
            self.logging.error(
                f"get_new_articles_by_page got None content with url {self.url_of_page(self.url, page, 'DennikN')}")
            return AtomicDict()
        for article in current_content.find_all('article'):
            scraped_article = self.scrape_article(article)
            new_data.add(scraped_article)

        return new_data

    @staticmethod
    @scraper_utils.validate_dict
    def scrape_article(article):
        return {
            'title': article.span.text,
            'values': {
                # 'url': article.find('a')['href'],
                'url': article.find(class_='a_art_b').find('a', recursive=False)['href'],
                'time_published': article.find('time').get_text(),
                'description': Scraper.may_be_empty(article.find('p')),
                'photo': DennikN.get_photo(article),
                'tags': '',
                'author': Scraper.may_be_empty(article.find(class_='e_terms_author')),
                'content': ''
            }
        }

    @staticmethod
    def get_photo(article):
        if article.find('img') is not None:
            return article.find('img')['data-src']
        else:
            return ""

    @scraper_utils.validate_dict
    def scrape_content(self, title, article_content):
        return {
            'title': title,
            'values': {
                'tags': self.get_correct_tags(article_content),
                'content': self.get_correct_content(article_content)
            }
        }

    def get_correct_content(self, article_content):
        if article_content.find(class_='a_single__post') is not None:
            return article_content.find(class_='a_single__post').get_text()
        elif article_content.find(class_='b_single_main') is not None:
            return article_content.find(class_='b_single_main').get_text()
        else:
            self.logging.error('get_correct_content can not find correct classes')
            return ""

    def get_correct_tags(self, article_content):
        if article_content.find(class_='e_terms') is not None:
            return article_content.find(class_='e_terms').get_text()
        elif article_content.find(class_='e_tag') is not None:
            return article_content.find(class_='e_tag').get_text()
        else:
            return ""
