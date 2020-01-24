from scraper.scraper_utils import config


class AtomicDict(dict):
    def add(self, obj):
        if obj is None:
            # Log
            return True
        title = obj['title']
        values = obj['values']
        res = title in self.keys()
        self[title] = values
        return res

    def add_all(self, objs):
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
