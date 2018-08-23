#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции проверки наличия примонтированного каталога документов.
"""

import os
import os.path
import ic
from ic.log import log

# Version
__version__ = (0, 0, 1, 1)


def validZipDocCatalog(zipdoc_dir=None):
    """
    Проверка корректного примонтированного каталога документов.
    @return: True/False.
    """
    try:
        if zipdoc_dir is None:
            zipdoc_dir = ic.settings.archive.SETTINGS.zipdoc_dir.get()
        is_valid_dir = validZipDocDir(zipdoc_dir)
        is_empty_dir = isEmptyDir(zipdoc_dir)
        is_doc_catalog_dir = os.path.exists(os.path.join(zipdoc_dir, 'doc_catalog'))
        return is_doc_catalog_dir and not is_empty_dir
    except:
        log.fatal(u'Ошибка функции валидации папки каталога документов')
    return False
        
    
def validZipDocDir(zipdoc_dir=None):
    """
    Проверка наличия папки каталога документов.
    @return: True/False.
    """
    if zipdoc_dir is None:
        zipdoc_dir = ic.settings.archive.SETTINGS.zipdoc_dir.get()
    return os.path.exists(zipdoc_dir)
    

def isEmptyDir(dirname):
    """
    Проверка пустой папки.
    @return: True/False.
    """
    if not os.path.exists(dirname):
        return True
    return os.listdir(dirname) < 2
