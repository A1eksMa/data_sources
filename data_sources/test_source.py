import json
import shelve
import unittest
from pathlib import Path

from source import Source


class TestSourceMethods(unittest.TestCase):

    def example(foo):
        """ Decorator, that create test example for `foo`. """
        def wrapper(self):
            # create `test` folder
            path = Path.cwd() / 'test'
            if not (path.exists() and path.is_dir()):
                path.mkdir(parents=True, exist_ok=True)
            # create `info.json`
            data = {'type': 'Source()',
                    'name': 'test',
                    'description': 'Test case for unittest.',
                    'keys': tuple(),
                    'indicators': list()}
            path_json = path / 'info.json'
            with open(path_json, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            # create `data.db`
            path_data = path / 'data.db'
            with shelve.open(path / 'data') as data:
                pass

            foo(self)

            # remove `data.db`
            path_data.unlink()
            # remove `info.json`
            path_json.unlink()
            # remove `test` folder.
            if path.is_dir() and not any(path.iterdir()): path.rmdir()

        return wrapper

    # Test
    @example
    def test_init_1(self):
        """ Test: invalid types for a path raise a TypeError. """
        # Empty path
        with self.assertRaises(TypeError): Source()
        # Path is an integer
        path = 123
        with self.assertRaises(TypeError): Source(path)
        # Path is a tuple
        path = (123, 'qwerty')
        with self.assertRaises(TypeError): Source(path)
        # Path is a tuple of Paths
        path = (Path.cwd(), Path.cwd())
        with self.assertRaises(TypeError): Source(path)

    @example
    def test_init_2(self):
        """ Test: Initializate Source() instans without `path` atribute. """
        # Fall-in-False path:
        path = ''
        with self.assertRaises(AttributeError): Source(path).path
        path =()
        with self.assertRaises(AttributeError): Source(path).path
        path = []
        with self.assertRaises(AttributeError): Source(path).path
        path = False
        with self.assertRaises(AttributeError): Source(path).path
        path = 0
        with self.assertRaises(AttributeError): Source(path).path
        path = None
        with self.assertRaises(AttributeError): Source(path).path

        # Folder path not exists
        path = 'qwerty'
        with self.assertRaises(AttributeError): Source(path).path

    @example
    def test_init_4(self):
        """ Positive test: instance creates with a `path` atribute. """
        path = Path.cwd()
        self.assertTrue(isinstance(Source(path), Source))
        self.assertTrue(isinstance(Source(path).path, Path))

    @example
    def test_init_5(self):
        """ Test: access to `info` atribute. """
        path = Path.cwd() / 'test'
        self.assertTrue(Source(path).info['type'] == 'Source()')
        with self.assertRaises(KeyError): Source(path).info['qwerty']


    @example
    def test_bool_(self):
        """ Test: empty instance (without attributes('path','info','data')
        is False. """
        path = ''
        self.assertFalse(Source(path))
        path = Path.cwd() / 'test'
        self.assertTrue(Source(path))

    @example
    def test_update_info_1(self):
        """ Test update_info() method. """
        path = Path.cwd() / 'test'
        src = Source(path)
        src.info['qwerty'] = 123
        src.update_info()
        self.assertEqual(Source(path).info['qwerty'], 123)

if __name__ == '__main__':
    unittest.main()
