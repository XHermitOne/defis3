#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Тест."""
import unittest
from ic.utils.icprotector import Protected, protect

class TestProtectClasses(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_protect_classes(self):
        """ test metod protect."""
        class A(Protected):
            __protected__ = ['a','b','f1']
            def __init__(self):
                self.a = 5
                self.b = 'be'
                self.c = 7
                
            def f(self):
                pass
                
            @protect
            def f1(self):
                pass
                
        obj = A()
        # тестируем gettattr
        try:
            obj.a
            raise NotImplementedError('Protect Attribute Error')
        except AttributeError:
            pass
        try:
            obj.b
            raise NotImplementedError('Protect Attribute Error')
        except AttributeError:
            pass
            
        obj.c
        # тестируем gettattr
        try:
            obj.a = 1
            raise NotImplementedError('Protect Attribute Error')
        except AttributeError:
            pass

        try:
            obj.f1()
            raise NotImplementedError('Protect Method Error')
        except AttributeError:
            pass
        
        obj.f()
        #A.Proxy.f1()
        #getattr(A, 'Proxy').f1(obj)
       
        #
        class B(A):
            __protected__ = ['a','b']
            def __init__(self):
                A.__init__(self)
                self.a = 7
            
            def f1(self):
                return self.a
                #getattr(A, 'Protected(A)').f1(self)
        b = B()
        print(b.f1())
        try:
            b.a
            raise NotImplementedError('Protect Attribute Error')
        except AttributeError:
            pass
        
def start_unitest(par=0):
    if par == 0:
        unittest.main()
        return
        
    lst = [
        TestProtectClasses, 
    ]
    
    for cls in lst:
        print('--- %s tests:' % cls.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest(1)
 