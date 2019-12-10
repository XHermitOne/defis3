#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Произвести адаптацию всех сгенерированных модулей Python сгенерированных wxFormBuilder
для использования в программе с текущей версией wxPython.
"""

import sys
import os
import os.path

# sys.path.append('/home/xhermit/dev/prj/work/defis3')

from ic.log import log
from ic.editor import wxfb_manager

# SIGNATURE_WXFB_PY = '## Python code generated with wxFormBuilder'


def adapt_form_py(py_filename):
    """
    Адаптация конкретного модуля Python.
    :param py_filename: Полное имя файла модуля Python.
    :return: True / False.
    """
    if os.path.exists(py_filename) and os.path.isfile(py_filename):
        return wxfb_manager.adapt_wxformbuilder_py(py_filename)
    else:
        log.warning(u'Не определен файл модуля <%s>' % py_filename, bForcePrint=True)
    return False


def adapt(source):
    """
    Произвести адаптацию Python модулей форм wxFormBuilder.
    :param source: Источник. Может быть файл модуля или папка.
    :return: True/False.
    """
    log.info(u'Обрабатываемый источник для адаптации <%s>' % str(source), bForcePrint=True)
    if os.path.exists(source) and os.path.isfile(source):
        result = adapt_form_py(source)
        if result:
            log.info(u'Адаптация прошла успешно', bForcePrint=True)
        else:
            log.error(u'Ошибка адаптации', bForcePrint=True)

        return result
    else:
        log.warning(u'Не обрабатываемый тип источника <%s>' % str(source), bForcePrint=True)
    return False


if __name__ == '__main__':
    adapt(*sys.argv[1:])
