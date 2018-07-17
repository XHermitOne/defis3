#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тестируем функции безопасности.
"""
import unittest
from ic.interfaces import icabstract
from ic.kernel import icexceptions

class TestAbstract(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_abstract_class(self):
        """ test abstract class."""
        class A:
            def f(self): 
                icabstract.abstract()


        class B(A):
            pass

        class C(A):
            def f(self):
                pass
            
        try:
            a = A()
            a.f()
            self.failUnlessEqual('NotImplementedError', False)
        except NotImplementedError:
            pass

        try:
            b = B()
            b.f()
            self.failUnlessEqual('NotImplementedError', False)
        except NotImplementedError:
            pass
            
        c = C()
        c.f()
        
def start_unitest(par=0):
    if par == 0:
        unittest.main()
        return
        
    lst = [
        TestAbstract, 
    ]
    
    for cls in lst:
        print('--- %s tests:' % cls.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest(1)
    
