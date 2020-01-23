from scraper import scraper_utils
from scraper.abstract_scraper import Scraper


class ZemAVek(Scraper):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.yesterdays_data = {}
        self.url = self.config.get('URL', 'ZemAVek')

    @scraper_utils.slow_down
    def get_new_articles_by_page(self, page):
        new_data = {}
        current_content = self.get_content(self.url_of_page(self.url, page))
        for article in current_content.find_all('article'):
            title = article.h3.a.text
            new_data[title] = {
                'url': article.a['href'],
                'time_published': article.find('time')['datetime'],
                'description': article.p.text,
                'photo': article.img['src'],
                'tags': [],
                'author': '',
                'content': ''
            }  # atomic

        return new_data.copy()

    def get_new_articles(self):
        page = 1
        max_page = int(self.config.get('Settings', 'MaxPages'))
        new_data = {}
        while self.still_new_articles(new_data) and page <= max_page:
            self.data = {**self.data, **new_data} # define as plus in atomic dict
            new_data = self.get_new_articles_by_page(page)
            page += 1

        self.data = {**self.data, **{k: v for k, v in new_data.items() if k not in self.yesterdays_data}}  # Refactor

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


zav = ZemAVek()
zav.get_new_articles()
zav.save_data_json(zav.data, 'out.json')
