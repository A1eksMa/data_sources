import unittest
import sys
sys.path.insert(0,'../')

from lib.cls_node import *
from lib.cls_source import *


class TestSource(unittest.TestCase):

    def example(foo):
        """ Decorator, that create test example for `foo`. """
        def wrapper(self):
            # create `test` folder
            path = Path.cwd() / 'test_source_instance'
            Node.new(path,
                     'test_source_instance',
                     type_node = "Source",
                     description='Test case for unittest.',
                       )

            foo(self)

            # remove `data.db`
            path_data = path / 'data.db'
            path_data.unlink()
            # remove `info.json`
            path_json = path / 'info.json'
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
        """ Test: Initializate Node() instans without `path` atribute. """
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
        path = Path.cwd() / 'test_source_instance'
        self.assertTrue(Source(path).info['type'] == 'Source')
        with self.assertRaises(KeyError): Source(path).info['qwerty']


    @example
    def test_bool_(self):
        """
        Test empty instance (without attributes('path','info','data') is False.
        """
        path = ''
        self.assertFalse(Source(path))
        path = Path.cwd() / 'test_source_instance'
        self.assertTrue(Source(path))

    @example
    def test_update_info(self):
        """ Test update_info() method. """
        path = Path.cwd() / 'test_source_instance'
        src = Source(path)
        src.info['qwerty'] = 123
        src.update_info()
        self.assertEqual(Source(path).info['qwerty'], 123)

    @example
    def test_class_name(self):
        """ Test class_name() method. """
        path = Path.cwd() / 'test_source_instance'
        src = Source(path)
        self.assertEqual(src.class_name(), 'Source')

    @example
    def test_types(self):
        """ Test types of atributes. """
        path = Path.cwd() / 'test_source_instance'
        src = Source(path)
        self.assertTrue(isinstance(src, Source))
        self.assertTrue(isinstance(src.path, Path))
        self.assertTrue(isinstance(src.info, dict))
        self.assertTrue(isinstance(src.info['type'], str))
        self.assertTrue(isinstance(src.info['name'], str))
        self.assertTrue(isinstance(src.info['description'], str))
        self.assertTrue(isinstance(src.info['keys'], tuple))
        self.assertTrue(isinstance(src.info['indicators'], list))


if __name__ == '__main__':
    unittest.main()
