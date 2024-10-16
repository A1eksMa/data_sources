import unittest
from timing import *



class TestTiming(unittest.TestCase):

    def example(foo):
        """ Decorator, that create test example for `foo`. """
        def wrapper(self):
            foo(self)
        return wrapper

    # Test
    @example
    def test_timitng_init(self):
        """ Test: Initializate Timing() instans. """
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
        t = Timing()
        # Initializated by datetime:
        a = Timing(a)
        # Initializated by tuple:
        b = Timing(b)
        # Initializated by string (uti):
        c = Timing(c)
        # Initializated by string (default dt):
        d = Timing(d)
        # Initializated by integer:
        e = Timing(e)

        for i in (t,a,b,c,d,e):
            self.assertTrue(isinstance(i, Timing))


    @example
    def test_timitng_atributes_type(self):
        """
        Test: types of atributes of Timing() instans
        for each of initializate argument types.
        """

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
        t = Timing()
        # Initializated by datetime:
        a = Timing(a)
        # Initializated by tuple:
        b = Timing(b)
        # Initializated by string (uti):
        c = Timing(c)
        # Initializated by string (default dt):
        d = Timing(d)
        # Initializated by integer:
        e = Timing(e)

        for i in (t,a,b,c,d,e):
            self.assertTrue(isinstance(i.dt, datetime))
            self.assertTrue(isinstance(i.ut, float))
            self.assertTrue(isinstance(i.dts, str))
            self.assertTrue(isinstance(i.uts, str))
            self.assertTrue(isinstance(i.uti, int))


    def test_timitng_init_error(self):
        """ Negative test. """
        with self.assertRaises(AttributeError):
            Timing([])

        with self.assertRaises(AttributeError):
            Timing(None)

        with self.assertRaises(AttributeError):
            Timing(('',''))

        with self.assertRaises(ValueError):
            Timing('qwerty')

        with self.assertRaises(IndexError):
            Timing(1567)


if __name__ == '__main__':
    unittest.main()
