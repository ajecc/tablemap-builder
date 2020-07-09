import pickle


class TablemapArea:
    def __init__(self, upper_x, upper_y, lower_x, lower_y, label, is_bool_symbol=False):
        self.upper_x = upper_x
        self.upper_y = upper_y
        self.lower_x = lower_x
        self.lower_y = lower_y
        self.label = label
        self.is_bool_symbol = False


class Tablemap:
    def __init__(self):
        self.tablemap_areas = []

    @staticmethod
    def load(pickle_path):
        return pickle.load(open(pickle_path, 'rb'))

    @staticmethod
    def dump(pickle_path, tablemap):
        pickle.dump(tablemap, open(pickle_path, 'wb'))
