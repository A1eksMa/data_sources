#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import unittest

def foo(x, y):
    return x + y


class TestFoo(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(foo(2, 2), 4)
    def test_truly(self):
        self.assertTrue(foo(2,2)==4)
        self.assertFalse(foo(2,2)!=4)
        self.assertFalse(foo(2,2)==4)

def main():
    print('Main mode')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('-t', '--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='Test mode')
    args = parser.parse_args()

    if args.test:
        unittest.main()
    else:
        main()
        unittest.main()
