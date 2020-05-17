from typing import Dict

from news_scraper import config, ProjectVariables
from functools import wraps

logging = ProjectVariables.root_logger


def accepts_dict(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if isinstance(args[1], dict):
            return fn(*args, **kwargs)
        else:
            logging.error(f'{fn.__name__} received None or other type')
            return True
    return wrapper


class AtomicDict(dict):
    @accepts_dict
    def add(self, obj: dict, yesterday_data=None) -> bool:
        if yesterday_data is None:
            yesterday_data = AtomicDict()
        title = obj['title']
        values = obj['values']
        if title in self.keys() or title in yesterday_data.keys():
            return True
        self[title] = values
        return False

    @accepts_dict
    def add_all(self, objs: Dict[str, dict], yesterday_data=None) -> bool:
        if yesterday_data is None:
            yesterday_data = AtomicDict()
        max_collisions = int(config.get('Settings', 'MaxCollisions'))
        for title, values in objs.items():
            res = self.add({
                'title': title,
                'values': values
            }, yesterday_data=yesterday_data)
            if res:
                max_collisions -= 1
            if max_collisions == 0:
                return False
        return True

    @accepts_dict
    def add_additional_data(self, additional_data: dict) -> None:
        title = additional_data['title']
        new_values = additional_data['values']
        if self[title] is None:
            logging.error(f'title {title} was not find in data list')
            return
        for key in new_values.keys():
            self[title][key] = new_values[key]
