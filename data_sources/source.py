import json
import shelve
from pathlib import Path
import unittest

_JSON = 'info.json'
_DATA = 'data'

class Source():
    """
    """

    def __init__(self, path: str):
        """ """
        if path and Path(path).is_dir():
            self.path = Path(path)

            path_json = self.path / _JSON

            if path_json.exists():
                with open(path_json, 'r') as file:
                    self.info = json.load(file)

                    if self.info['type'] == 'Source()':

                        path_data = self.path / _DATA

                        with shelve.open(path_data) as data:
                            self.data = data


    def __bool__(self):
        """ """
        return all(i in self.__dict__.keys() for i in ('path', 'info', 'data'))

    def __repr__(self):
        """ """
        s = str(type(self)) + "\n"
        for i, val in self.info.items():
            s += str(i) + ": " + str(val) +"\n"
        return s

    def update_info(self):
        """ """
        path_json = self.path / _JSON
        with open(path_json, 'w') as file:
            json.dump(self.info, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    """ Construct test instance of Source() class """
    path = Path().cwd()
    src = Source(path)
    src.info = {'type': 'Source()'}
    src.update_info()
    print(src)
