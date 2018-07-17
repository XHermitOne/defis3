#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тестирование схемы данных.
"""

import ic
import unittest
import datetime
import time
import wx
import os, os.path
from . import filter_py_funcs as pyf


class TestFilterFucs(unittest.TestCase):
    def __init__(self, *arg, **kwarg):
        unittest.TestCase.__init__(self, *arg, **kwarg)

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_py_str_funcs(self):
        """
        Тестируем логические python функции.
        """
        res = pyf.py_left_equal('123hhhhh', '123')
        self.failUnlessEqual(res, True)
        res = pyf.py_right_equal('123hhhhh-', 'h-')
        self.failUnlessEqual(res, True)
        res = pyf.py_contain('***123***', '123')
        self.failUnlessEqual(res, True)
        res = pyf.py_not_contain('***123***', '123')
        self.failUnlessEqual(res, False)
        res = pyf.py_not_contain('***123***', '777')
        self.failUnlessEqual(res, True)
        res = pyf.py_into('123', '123999')
        self.failUnlessEqual(res, True)
        res = pyf.py_not_into('123', 'pp12')
        self.failUnlessEqual(res, True)


if __name__ == '__main__':
    unittest.main()
