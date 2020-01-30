#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Библиотека функций определения режима работы движка.
"""

from ic.kernel.ickernelmode import *

__version__ = (0, 1, 2, 1)

# Режим работы с БД
global DB_MODE
DB_MODE = None

# Режим работы с БД
DB_MONOPOLY = '-m'      # Монпольный режим работы с БД
DB_SHARE = '-s'         # Многопользовательский режим работы с БД


def isRuntimeMode():
    """
    Движок запущен в режиме ИСПОЛНЕНИЕ В СРЕДЕ GUI?
    """
    global RUNTIME_MODE
    return RUNTIME_MODE


def setRuntimeMode(runtime_mode=True):
    """
    Установить признак режима ИСПОЛНЕНИЕ В СРЕДЕ GUI.
    """
    global RUNTIME_MODE
    RUNTIME_MODE = runtime_mode
    if RUNTIME_MODE:
        # Если включается режим GUI, то надо выключить режим консоли
        global CONSOLE_MODE
        CONSOLE_MODE = False


def isConsoleMode():
    """
    Движок запущен в режиме ИСПОЛНЕНИЕ В КОНСОЛЬНОЙ СРЕДЕ?
    """
    global CONSOLE_MODE
    return CONSOLE_MODE


def setConsoleMode(console_mode=True):
    """
    Установить признак режима ИСПОЛНЕНИЕ В КОНСОЛЬНОЙ СРЕДЕ.
    """
    global CONSOLE_MODE
    CONSOLE_MODE = console_mode
    if CONSOLE_MODE:
        # Если включается режим консоли, то надо выключить режим GUI
        global RUNTIME_MODE
        RUNTIME_MODE = False


def isEditorMode():
    """
    Движок запущен в режиме РЕДАКТОРА?
    Считается что если ни один из режимов иполнения не запущен,
    то это режим редактирования!
    """
    global RUNTIME_MODE
    global CONSOLE_MODE
    return not RUNTIME_MODE and not CONSOLE_MODE


def getDBMode():
    """
    Режим работы с БД.
    """
    global DB_MODE
    return DB_MODE


def setDBMode(db_mode=DB_SHARE):
    """
    Устаонвить режим работы с БД.
    """
    global DB_MODE
    DB_MODE = db_mode


def isDebugMode():
    """
    Отладка?
    """
    global DEBUG_MODE
    return DEBUG_MODE


def setDebugMode(debug_mode=True):
    """
    Установить признак режима отладки.
    """
    global DEBUG_MODE
    DEBUG_MODE = debug_mode
