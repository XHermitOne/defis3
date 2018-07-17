#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Тестируем каталог."""
import unittest
from ic.kernel import icexceptions
from ic.db import icsimpledataset
import ic
prj_dir = '../testprj/testprj/'

data = [
    ('1','2','3','4'),
    ('2','2','3','4'),
    ('3','2','3','4'),
    ('4','2','3','4'),
    ('5','2','3','4'),
    ('6','2','3','4'),
]
class TestBuff(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_CChangeBuff(self):
        """ test ."""
        r1 = data[0]
        r2 = data[1]
        buff = icsimpledataset.CChangeBuff([0])
        buff.reg_add(r1)
        k1 = ('1',)
        self.failUnlessEqual(buff.add_rows_dct[k1], r1)
        buff.reg_del(r1)
        self.failUnlessEqual(buff.del_rows_dct[k1], r1)
        self.failUnlessEqual(k1 in buff.add_rows_dct, False)
        
        buff.reg_update(r1)
        self.failUnlessEqual(buff.update_rows_dct[k1], r1)

        buff.reg_add(r1)
        self.failUnlessEqual(k1 in buff.del_rows_dct, False)
        self.failUnlessEqual(k1 in buff.update_rows_dct, True)
        
def start_unitest(par=0):
    if par == 0:
        unittest.main()
        return
        
    lst = [
        TestBuff, 
    ]
    
    for cls in lst:
        print('--- %s tests:' % cls.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest(0)
    
