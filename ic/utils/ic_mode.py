#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Библиотека функций определения режима работы движка.
"""

# --- Подключение пакетов ---
from ic.kernel.ickernelmode import *

# --- Константы ---

# Режим работы с БД
global DB_MODE
DB_MODE = None

# Режим работы с БД
DB_MONOPOLY = '-m'      # Монпольный режим работы с БД
DB_SHARE = '-s'         # Многопользовательский режим работы с БД

# --- Функции ---


def isRuntimeMode():
    """
    Движок запущен?
    """
    global RUNTIME_MODE
    return RUNTIME_MODE


def setRuntimeMode(RuntimeMode_=True):
    """
    Установить признак режима исполнения.
    """
    global RUNTIME_MODE
    RUNTIME_MODE = RuntimeMode_


def getDBMode():
    """
    Режим работы с БД.
    """
    global DB_MODE
    return DB_MODE


def setDBMode(DBMode_=DB_SHARE):
    """
    Устаонвить режим работы с БД.
    """
    global DB_MODE
    DB_MODE = DBMode_


def isDebugMode():
    """
    Отладка?
    """
    global DEBUG_MODE
    return DEBUG_MODE


def setDebugMode(DebugMode_=True):
    """
    Установить признак режима отладки.
    """
    global DEBUG_MODE
    DEBUG_MODE = DebugMode_
