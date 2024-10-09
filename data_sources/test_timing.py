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
        b = ('2020-01-01 00:00:00', '20'+'%y-%m-%d %H:%M:%S')
        
        # Default empty value:
        t = Timing()
        # Initializated by datetime:
        a = Timing(a)
        # Initializated by tuple:
        b = Timing(b)
        
        self.assertTrue(isinstance(t, Timing))
        self.assertTrue(isinstance(a, Timing))
        self.assertTrue(isinstance(b, Timing))
    
    @example
    def test_timitng_atributes_type(self):
        """ Test: types of atributes of Timing() instans. """
        # Examles
        # datetime
        a = datetime.now()
        # tuple
        b = ('2020-01-01 00:00:00', '20'+'%y-%m-%d %H:%M:%S')
        
        # Default empty value:
        t = Timing()
        # Initializated by datetime:
        a = Timing(a)
        # Initializated by tuple:
        b = Timing(b)
   
        for i in (t,a,b):
            self.assertTrue(isinstance(i.dt, datetime))
            self.assertTrue(isinstance(i.ut, float))
            self.assertTrue(isinstance(i.dts, str))
            self.assertTrue(isinstance(i.uts, str))
            self.assertTrue(isinstance(i.uti, int))


if __name__ == '__main__':
    unittest.main()
