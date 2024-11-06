import unittest
import sys
sys.path.insert(0,'../')

from lib.cls_times import *



class TestTimes(unittest.TestCase):

    def example(foo):
        """ Decorator, that create test cases for `foo`. """
      
        def wrapper(self):
            # Examles
            # datetime
            a = datetime.now()
            # tuple
            b = ('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            # string(uti)
            c = "1729001345584581"
            # string (default datetime)
            d = "2024-10-15 17:09:05.584581"
            # Integer
            e = 1729001345584581

            # Default empty value:
            t = Times()
            # Initializated by datetime:
            a = Times(a)
            # Initializated by tuple:
            b = Times(b)
            # Initializated by string (uti):
            c = Times(c)
            # Initializated by string (default dt):
            d = Times(d)
            # Initializated by integer:
            e = Times(e)

            cases = (t,a,b,c,d,e)
            
            
            foo(self, cases)
        return wrapper

    # Test
    @example
    def test_times_init(self,cases):
        """ Test: Initializate Times() instans. """
        for i in cases:
            self.assertTrue(isinstance(i, Times))

    @example
    def test_times_atributes_type(self, cases):
        """
        Test: types of atributes of Times() instans
        for each of initializate argument types.
        """
        for i in cases:
            self.assertTrue(isinstance(i.dt, datetime))
            self.assertTrue(isinstance(i.ut, float))
            self.assertTrue(isinstance(i.dts, str))
            self.assertTrue(isinstance(i.uts, str))
            self.assertTrue(isinstance(i.uti, int))


    def test_timitng_init_error(self):
        """ Negative test. """
        with self.assertRaises(AttributeError):
            Times([])

        with self.assertRaises(AttributeError):
            Times(None)

        with self.assertRaises(AttributeError):
            Times(('',''))

        with self.assertRaises(ValueError):
            Times('qwerty')

        with self.assertRaises(IndexError):
            Times(1567)


if __name__ == '__main__':
    unittest.main()
