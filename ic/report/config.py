#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Конфигурационный файл.
"""

import os
import os.path

DEFAULT_ENCODING = 'utf-8'

# Полный путь до исполняемого файла icreport.py
DEFAULT_REPORT_EXEC_FILENAME = os.path.join(os.path.dirname(__file__), 'icreport', 'icreport.py')

# Имя папки отчетов по умолчанию
DEFAULT_REPORT_DIRNAME = 'reports'


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
