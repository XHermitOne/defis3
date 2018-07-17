#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль тестов для проверки XML конвертера.
"""

import os
import os.path
import sys

import unittest


class icXML2DICTTests(unittest.TestCase):
    """
    Тесты для проверки XML конвертера.
    """
    def setUp(self):
        sys.path.append(os.getcwd())
            
    def test_rep_all_dbf(self):
        """
        Тестирование генерации отчета.
        """
        from . import xml2dict

        result=xml2dict.XmlFile2Dict('./services/convert/testfiles/SF02.xml')
        self.assertNotEqual(result,None)


def run_test():
    """
    Запуск тестирования.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(icXMLConvertTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    unittest.main()
