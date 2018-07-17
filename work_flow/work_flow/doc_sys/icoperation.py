#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль определения операций.
Операции запускаются документами на выполнение (метод do)
либо отмена операции (метод undo).
"""

# Подключение библиотек
from ic.components import icwidget

# Версия
__version__ = (0, 0, 0, 3)


# Спецификация

SPC_IC_OPERATION = dict({'type': 'Operation',
                         'name': 'default',
                         'description': '',     # Описание
                         'prev_do': None,       # Скрипт, запускаемый перед выполнением операции
                         'post_do': None,       # Скрипт, запускаемый после выполнения операции
                         'prev_undo': None,     # Скрипт, запускаемый перед выполнением отмены операции
                         'post_undo': None,     # Скрипт, запускаемый после выполнения отмены операции
                         '__parent__': icwidget.SPC_IC_SIMPLE,
                         })

    
class icOperationInterface:
    """
    Интерфейс абстрактной операции.
    """
    
    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        self._parent = parent

    def getName(self):
        """
        Имя объекта
        """
        return None

    def do(self):
        """
        Запуск выполнения операции.
        @return: True/False.
        """
        return False

    def undo(self):
        """
        Запуск выполнения отмены операции.
        @return: True/False.
        """
        return False


class icOperationPrototype(icOperationInterface):
    """
    Абстрактная операция.
    Атрибуты спецификации:
        operation_table - Имя таблицы операций движения
        prev_do - Скрипт, запускаемый перед выполнением операции
        post_do - Скрипт, запускаемый после выполнения операции
        prev_undo - Скрипт, запускаемый перед выполнением отмены операции
        post_undo - Скрипт, запускаемый после выполнения отмены операции
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        icOperationInterface.__init__(self, parent)


# Спецификация
SPC_IC_FUNCOPERATION = dict({'type': 'FuncOperation',
                             'do_func': None,   # Функция выполнения операции
                             'undo_func': None, # Функция выполнения отмены операции
                             '__parent__': SPC_IC_OPERATION,
                             })


class icFuncOperationProto(icOperationPrototype):
    """
    Функциональная операция.
    Методы выполнения и отмены задаются функциями пользователя.
    Атрибуты спецификации:
        do_func - Функция выполнения операции
        undo_func - Функция выполнения отмены операции
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icOperationPrototype.__init__(self, *args, **kwargs)

    def do(self):
        """
        Запуск выполнения операции.
        @return: True/False.
        """
        return False

    def undo(self):
        """
        Запуск выполнения отмены операции.
        @return: True/False.
        """
        return False
