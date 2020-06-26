from typing import Dict, Union

from news_scraper import config, ProjectVariables
from functools import wraps

logging = ProjectVariables.root_logger


def accepts_list(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if isinstance(args[1], dict) or isinstance(args[1], list):
            return fn(*args, **kwargs)
        else:
            logging.error(f'{fn.__name__} received None or other type')
            return True
    return wrapper


class AtomicList(list):
    def __init__(self):
        super().__init__()
        self.titles: list = []

    @accepts_list
    def add(self, obj: dict, yesterday_data=None) -> bool:
        yesterday_data = yesterday_data or AtomicList()
        title = obj['title']
        if title in self.titles or title in yesterday_data.titles:
            return True
        self.append(obj)
        self.titles.append(title)
        return False

    @accepts_list
    def add_all(self, objs: list, yesterday_data=None) -> bool:
        yesterday_data = yesterday_data or AtomicList()
        max_collisions = int(config.get('Settings', 'MaxCollisions'))
        for article in objs:
            res = self.add(article, yesterday_data=yesterday_data)
            if res:
                max_collisions -= 1
            if max_collisions == 0:
                return False
        return True

    @accepts_list
    def add_additional_data(self, additional_data: dict) -> None:
        title = additional_data['title']
        if self.get(title) is None:
            logging.error(f'title {title} was not find in data list')
            return
        for key in additional_data.keys():
            self.get(title)[key] = additional_data[key]

    def get(self, key: Union[str, int]):
        if isinstance(key, str):
            try:
                title_index = self.titles.index(key)
            except ValueError:
                return None
            return self[title_index]
        return self[key]

