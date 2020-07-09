from tablemap import Tablemap
import os


class TablemapFileManager:
    def __init__(self):
        self.tablemap = None 
        self.tablemap_dir = None 
        self.tablemap_name = None 

    def new_tablemap(self, tablemap_dir, tablemap_name):
        self.tablemap_dir = tablemap_dir
        self.tablemap_name = tablemap_name
        self.tablemap = Tablemap

    def load_tablemap(self, tablemap_dir, tablemap_name):
        self.tablemap_dir = tablemap_dir
        self.tablemap_name = tablemap_name
        self.tablemap = Tablemap.load(os.path.join(self.tablemap_dir, f'{self.tablemap_name}.pickle'))

    def can_save_tablemap(self):
        return self.tablemap is not None

    def save_tablemap(self):
        if not self.can_save_tablemap():
            print('No tablemap has been loaded')
            return
        Tablemap.dump(self.tablemap, os.path.join(self.tablemap_dir, f'{self.tablemap_name}.pickle'))
        # TODO: save jsons as well
