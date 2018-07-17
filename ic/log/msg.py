#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создание и ведение лога системы.
"""

# --- Подключение библиотек ---
import sys
import traceback

try:
    import win32api
except:
    pass

# --- Функции ---


def msgErr(msg=''):
    """
    Выдает сообщение о последней ошибке в MessageBox.
    Эту функцию можно использовать только в блоке exception.
    @param msg: Текст сообщения.
    """
    trace = traceback.extract_tb(sys.exc_traceback)
    ltype = sys.exc_type
    last = len(trace) - 1

    if last >= 0:
        lt = trace[last]
        msg += ' in file: %s, func: %s, line: %i, \ntext: %s\ntype:%s' % (lt[0], lt[2], lt[1], lt[3], str(ltype))
        toMsg(msg)

    return msg


def toMsg(msg):
    """
    Выдает сообщение в MessageBox.
    @param msg: Текст сообщения.
    """
    return win32api.MessageBox(0, msg)
