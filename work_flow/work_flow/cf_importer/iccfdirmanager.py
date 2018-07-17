#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс работы с папкой конфигурации 1с, разобранной V8Unpack.
"""
import os
import os.path

from .cf_obj import iccfroot
from ic.log import log


class icCFDirManager:
    """
    Класс работы с папкой конфигурации 1с, разобранной V8Unpack v2.0.
    """
    
    def __init__(self, cf_dirname=None):
        """
        Конструктор.
        @param cf_dirname: Папка конфигурации 1с.
        """
        self.cf_dir = cf_dirname
        
        # Корневой элемент дерева объектов конфигурации
        self.cf_root = None
        
    def buildMetaObjects(self, cf_dirname=None):
        """
        Построить дерево объектов конфигурации.
        @param cf_dirname: Папка конфигурации 1с.
        """
        if cf_dirname:
            self.cf_dir = cf_dirname

        log.debug(u'Построение дерева метаобъектов конфигурации 1с <%s>' % self.cf_dir)

        # Очистить предыдущее дерево объектов
        self.cf_root = None
        self.cf_root = iccfroot.icCFRoot(None, None, self.cf_dir)
        self.cf_root.build()


def test():
    """
    """
    cur_dir = os.getcwd()
    # cf_dir=os.path.dirname(cur_dir)+'/testcf'
    cf_dir = os.path.dirname(cur_dir)+'/tst_doc'
    print('CF DIR:::', cf_dir)
    cf = icCFDirManager(cf_dir)
    cf.buildObjects()
    
if __name__ == '__main__':
    test()
