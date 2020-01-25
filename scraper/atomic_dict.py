from scraper.bootstrap import config


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
        if objs is None:
            # Log
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

    def add_additional_data(self, additional_data):
        if additional_data is None:
            # Log
            return
        title = additional_data['title']
        new_values = additional_data['values']
        if self[title] is None:
            # Log
            return
        for key in new_values.keys():
            self[title][key] = new_values[key]
