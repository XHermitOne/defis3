#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Глобальные переменные.
"""

# ЯДРО СИСТЕМЫ
KERNEL = None

# Доступ к методанным
metadata = None

# Доступ к схемам
schemas = None

# Доступ к настройкам проекта
settings = None


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
