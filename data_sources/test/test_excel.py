from pathlib import Path
import unittest
import sys
sys.path.insert(0,'../')

from lib.cls_excel import *


class TestExcelFile(unittest.TestCase):

    # Test
    def test_init_1(self):
        """ Test: invalid types for a path raise a TypeError. """
        # Empty path
        with self.assertRaises(TypeError): ExcelFile()
        # Path is an integer
        path = 123
        with self.assertRaises(TypeError): ExcelFile(path)
        # Path is a tuple
        path = (123, 'qwerty')
        with self.assertRaises(TypeError): ExcelFile(path)
        # Path is a tuple of Paths
        path = (Path.cwd(), Path.cwd())
        with self.assertRaises(TypeError): ExcelFile(path)

    def test_init_2(self):
        """ Positive test: instance creates with a `path` atribute. """
        path = Path.cwd() / "test_data/upd1.xlsx"
        self.assertTrue(isinstance(ExcelFile(path), ExcelFile))

    def test_ExcelFile_type(self):
        """ Test: types of ExcelFile() methods return. """
        path = Path.cwd() / "test_data/upd1.xlsx"
        e = ExcelFile(path)
        self.assertTrue(isinstance(e.rows(), list))
        self.assertTrue(isinstance(e.columns(), list))
        self.assertTrue(isinstance(e.dict(), dict))


if __name__ == '__main__':
    unittest.main()
