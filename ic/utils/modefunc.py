#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Библиотека функций определения режима работы движка.
"""

from ic.kernel.ickernelmode import *

__version__ = (0, 1, 1, 1)

# Режим работы с БД
global DB_MODE
DB_MODE = None

# Режим работы с БД
DB_MONOPOLY = '-m'      # Монпольный режим работы с БД
DB_SHARE = '-s'         # Многопользовательский режим работы с БД


def isRuntimeMode():
    """
    Движок запущен?
    """
    global RUNTIME_MODE
    return RUNTIME_MODE


def setRuntimeMode(runtime_mode=True):
    """
    Установить признак режима исполнения.
    """
    global RUNTIME_MODE
    RUNTIME_MODE = runtime_mode


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
