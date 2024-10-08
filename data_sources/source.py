import json
import shelve
from pathlib import Path

_JSON = 'info.json'
_DATA = 'data' # for file name: `data.db`

class Source():
    """
    """

    def __init__(self, path: str):
        """
        """
        if path and Path(path).is_dir():
            self.path = Path(path)

            path_json = self.path / _JSON

            if path_json.exists():
                with open(path_json, 'r') as file:
                    self.info = json.load(file)
                    if 'keys' in self.info.keys():
                        self.info['keys'] = tuple(self.info['keys'])

                    if self.info['type'] == self.class_name():

                        path_data = self.path / _DATA

                        with shelve.open(path_data) as data:
                            self.data = data

    def __bool__(self) -> bool:
        """
        Instance is True, if it have three valid attribures:
            - 'path',
            - 'info',
            - 'data'.
        """
        return all(i in self.__dict__.keys() for i in ('path', 'info', 'data'))

    def __repr__(self):
        """
        Print general info about instance.
        """
        s = str(type(self)) + "\n"
        for i, val in self.info.items():
            s += str(i) + ": " + str(val) +"\n"
        return s

    @staticmethod
    def new(path: str,
            name: str,
            description = str(),
            keys = tuple(),
            indicators = list(),
            ):
        """
        Create a new instance with a folder and files structure.
        """
        # create folder
        path = Path(path)
        if not (path.exists() and path.is_dir()):
            path.mkdir(parents=True, exist_ok=True)
        # create `info.json`
        data = {'type': Source(path).class_name(),
                'name': name,
                'description': description,
                'keys': keys,
                'indicators': indicators,
                }
        path_json = path / _JSON
        with open(path_json, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        # create `data.db`
        path_data = path / str(_DATA + '.db')
        with shelve.open(path / _DATA) as data:
            pass
        return Source(path)

    def class_name(self):
        """
        Return name of class as String.
        """
        s = str(type(self))    # smth like a "<class '__main__.Source'>"
        i = s[::-1].find(".")
        s = s[-i:-2]
        return s

    def update_info(self):
        """
        Rewrite `info.json` file from `self.info` atribute.
        """
        path_json = self.path / _JSON
        with open(path_json, 'w') as file:
            json.dump(self.info, file, ensure_ascii=False, indent=4)
