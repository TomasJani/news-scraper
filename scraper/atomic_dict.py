from scraper.bootstrap import config, logging


def accepts_dict(fn):
    def wrapper(*args, **kwargs):
        if isinstance(args[1], dict):
            return fn(*args, **kwargs)
        else:
            raise NotImplemented

    return wrapper


class AtomicDict(dict):
    @accepts_dict
    def add(self, obj):
        if obj is None:
            logging.error('add received None object')
            return True
        title = obj['title']
        values = obj['values']
        res = title in self.keys()
        self[title] = values
        return res

    @accepts_dict
    def add_all(self, objs):
        if objs is None:
            logging.error('add_all received None object')
            return True
        max_collisions = int(config.get('Settings', 'MaxCollisions'))
        for title, values in objs.items():
            res = self.add({
                'title': title,
                'values': values
            })
            if res:
                max_collisions -= 1
            if max_collisions == 0:
                return False
        return True

    @accepts_dict
    def add_additional_data(self, additional_data):
        if additional_data is None:
            logging.error('add_additional_data received None object')
            return
        title = additional_data['title']
        new_values = additional_data['values']
        if self[title] is None:
            logging.error(f'title {title} was not find in data list')
            return
        for key in new_values.keys():
            self[title][key] = new_values[key]
