import unittest
import sys
sys.path.insert(0,'../')

from lib.cls_node import *


class TestNodeMethods(unittest.TestCase):

    def example(foo):
        """ Decorator, that create test example for `foo`. """
        def wrapper(self):
            # create `test` folder
            path = Path.cwd() / 'test'
            Node.new(path,
                       'test',
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
        with self.assertRaises(TypeError): Node()
        # Path is an integer
        path = 123
        with self.assertRaises(TypeError): Node(path)
        # Path is a tuple
        path = (123, 'qwerty')
        with self.assertRaises(TypeError): Node(path)
        # Path is a tuple of Paths
        path = (Path.cwd(), Path.cwd())
        with self.assertRaises(TypeError): Node(path)

    @example
    def test_init_2(self):
        """ Test: Initializate Node() instans without `path` atribute. """
        # Fall-in-False path:
        path = ''
        with self.assertRaises(AttributeError): Node(path).path
        path =()
        with self.assertRaises(AttributeError): Node(path).path
        path = []
        with self.assertRaises(AttributeError): Node(path).path
        path = False
        with self.assertRaises(AttributeError): Node(path).path
        path = 0
        with self.assertRaises(AttributeError): Node(path).path
        path = None
        with self.assertRaises(AttributeError): Node(path).path

        # Folder path not exists
        path = 'qwerty'
        with self.assertRaises(AttributeError): Node(path).path

    @example
    def test_init_4(self):
        """ Positive test: instance creates with a `path` atribute. """
        path = Path.cwd()
        self.assertTrue(isinstance(Node(path), Node))
        self.assertTrue(isinstance(Node(path).path, Path))

    @example
    def test_init_5(self):
        """ Test: access to `info` atribute. """
        path = Path.cwd() / 'test'
        self.assertTrue(Node(path).info['type'] == 'Node')
        with self.assertRaises(KeyError): Node(path).info['qwerty']


    @example
    def test_bool_(self):
        """
        Test empty instance (without attributes('path','info','data') is False.
        """
        path = ''
        self.assertFalse(Node(path))
        path = Path.cwd() / 'test'
        self.assertTrue(Node(path))

    @example
    def test_update_info(self):
        """ Test update_info() method. """
        path = Path.cwd() / 'test'
        src = Node(path)
        src.info['qwerty'] = 123
        src.update_info()
        self.assertEqual(Node(path).info['qwerty'], 123)

    @example
    def test_class_name(self):
        """ Test class_name() method. """
        path = Path.cwd() / 'test'
        src = Node(path)
        self.assertEqual(src.class_name(), 'Node')

    @example
    def test_types(self):
        """ Test types of atributes. """
        path = Path.cwd() / 'test'
        src = Node(path)
        self.assertTrue(isinstance(src, Node))
        self.assertTrue(isinstance(src.path, Path))
        self.assertTrue(isinstance(src.info, dict))
        self.assertTrue(isinstance(src.info['type'], str))
        self.assertTrue(isinstance(src.info['name'], str))
        self.assertTrue(isinstance(src.info['description'], str))
        self.assertTrue(isinstance(src.info['keys'], tuple))
        self.assertTrue(isinstance(src.info['indicators'], list))

if __name__ == '__main__':
    unittest.main()
