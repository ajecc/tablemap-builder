import pickle


class TablemapArea:
    def __init__(self, id, x, y, w, h, label, is_bool_symbol=False):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.is_bool_symbol = False

    def to_json(self):
        bool_val = 0
        if self.is_bool_symbol: 
            bool_val = 1
        return f'{{"x": {self.x}, "y": {self.y}, "w": {self.w}, "h": {self.h}, "label": "{self.label}", "is_bool_symbol": {bool_val}}}'


class Tablemap:
    def __init__(self):
        self.tablemap_areas = []

    def add(self, x, y, w, h, label, is_bool_symbol=False):
        id = len(self.tablemap_areas) 
        self.tablemap_areas.append(TablemapArea(id, x, y, w, h, label, is_bool_symbol))
        self.tablemap_areas = sorted(self.tablemap_areas, key=lambda x: x.label)

    def remove(self, label):
        new_tablemap_areas = []
        for area in self.tablemap_areas:
            if area.label != label:
                new_tablemap_areas.append(area)
        self.tablemap_areas = new_tablemap_areas

    def to_json(self):
        json = '[\n'
        for i, tablemap_area in enumerate(self.tablemap_areas):
            json += tablemap_area.to_json()
            if i != len(self.tablemap_areas) - 1:
                json += ','
            json += '\n'
        json += ']'
        return json

    @staticmethod
    def load(pickle_path):
        return pickle.load(open(pickle_path, 'rb'))

    @staticmethod
    def dump(tablemap, pickle_path):
        pickle.dump(tablemap, open(pickle_path, 'wb'))
