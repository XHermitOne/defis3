#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестируем работу поддержки доступа к метаописаниям ресурсов через точку.
"""
#This file was originally generated by PyScripter's unitest wizard

import unittest
import ic.kernel.ic_dot_use as ic_dot_use
from ic.engine import glob_functions
from ic.utils import modefunc
from ic.kernel import ickernel

def init_tutorial_enviroment():
    modefunc.setRuntimeMode(False)
    glob_functions.icEditorLogin(None, None, '-s', PrjDir_='C:/defis/tutorial/tutorial/', DEBUG_MODE=False)

class TesticDotUseMeta(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_DotUse(self):
        """
        Простой тест доступа к ресурсу.
        """
        init_tutorial_enviroment()
        
        metadata=ic_dot_use.icMetaDataDotUse()
        print('DotUse TEST START')
        tst=metadata.THIS.frm.test1_form.Panel.test1_panel
        print('DotUse>>>',tst)
        print('DotUse passport>>>',tst.passport())
        frm = tst.create(parent=None)
        print('DotUse create>>>',frm)
        frm.Show()
        
        
#    def testgetConnection(self):
#        pass
#
#    def testgetClassName(self):
#        pass
#
#    def testdelete(self):
#        pass
#
#    def testdel_where(self):
#        pass
#
#    def testadd(self):
#        pass
#
#    def testupdate(self):
#        pass
#
#    def testget(self):
#        pass
#
#    def testget_where(self):
#        pass
#
#    def testis_id(self):
#        pass
#
#    def testcount(self):
#        pass
#
#    def testselect(self):
#        pass
#
#    def testlistRecs(self):
#        pass
#
#    def testqueryAll(self):
#        pass
#
#    def testqueryRecs(self):
#        pass
#
#    def testexecuteSQL(self):
#        pass
#
#    def testdrop(self):
#        pass
#
#    def testLock(self):
#        pass
#
#    def testunLock(self):
#        pass
#
#    def testLockObject(self):
#        pass
#
#    def testunLockObject(self):
#        pass

def start_unitest():
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TesticDotUseMeta)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest()
    
