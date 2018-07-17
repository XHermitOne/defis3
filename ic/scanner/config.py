#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфигурационный файл.
"""

import os
import os.path

# Полный путь до исполняемого файла icscanner.py
DEFAULT_SCANNER_EXEC_FILENAME = os.path.join(os.path.dirname(__file__),
                                             'icscanner', 'icscanner.py')

PROFILE_SCAN_DIRNAME = '.icscanner'
DEFAULT_SCAN_PATH = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)+'/log'),
                                 PROFILE_SCAN_DIRNAME)


def get_glob_var(name):
    """
    Прочитать значение глобальной переменной.
    @type name: C{string}
    @param name: Имя переменной.
    """
    return globals()[name]


def set_glob_var(name, value):
    """
    Установить значение глобальной переменной.
    @type name: C{string}
    @param name: Имя переменной.
    @param value: Значение переменной.
    """
    globals()[name] = value
    return value
