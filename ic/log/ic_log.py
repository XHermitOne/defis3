#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создание и ведение лога системы.
"""

# Подключение библотек
import sys
from . import iclog
import ic.utils.ic_util

# Константы и переменные
# Кодовая страница консоли
CONSOLE_ENCODING = None


def getConsoleEncoding():
    """
    Определить кодовую страницу консоли.
    """
    global CONSOLE_ENCODING
    if CONSOLE_ENCODING is None:
        if ic.utils.ic_util.isOSWindowsPlatform():
            CONSOLE_ENCODING = 'CP866'
        else:
            import locale
            CONSOLE_ENCODING = locale.getpreferredencoding()
    return CONSOLE_ENCODING


def icMsgErr(parent, msg):
    """
    Выдает сообщение о последней ошибке на экран.
    """
    return iclog.MsgLastError(parent, msg)


def icLogErr(msg=u''):
    """
    Выдает сообщение о последней ошибке в регистратор.
    Эту функцию можно использовать только в блоке exception.
    """
    return iclog.LogLastError(msg)


def icToLog(msg):
    """
    Выдает сообщение в регистратор (на консоль).
    @param msg: Текст сообщения.
    """
    return iclog.toLog(msg)


def icWin32Err():
    """
    Вывод ошибок Microsoft.
    """
    # Получено экспериментальным путем
    info = sys.exc_info()[1].args
    err_txt = str(info)
    f = open('win32.err', 'w')
    f.write(info[2])
    f.write(err_txt)
    f.close()
    return icToLog(err_txt)


def icODBCErr():
    """
    Вывод ошибок Microsoft ODBC.
    """
    # Получено экспериментальным путем
    err_txt = sys.exc_info()[1].args[2]
    return icToLog(err_txt)
