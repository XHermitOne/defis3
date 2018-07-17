#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс описания источника данных.
"""


class icSourceInterface:
    """
    Интерфейс классов данных системы.
    """

    def __init__(self, DBRes_=None):
        """
        Конструктор.
        @param DBRes_: Ресурс описания БД.
        """
        pass
        
    def CreateDBConnection(self, DB_):
        """
        Создать коннекшн по описанию БД.
        @param DB_: Описание БД.
        @return: Возвращает объект коннекшн.
        """
        pass
        
    def LockTable(self, name):
        """
        Блокирует таблицу.
        """
        pass
        
    def unLockTable(self, name):
        """
        Разблокирует таблицу.
        """        
        pass
        
    def LockRec(self, name, id):
        """
        Блокировка записи.
        """
        pass
        
    def unLockRec(self, name, id):
        """
        Разблокирует запись.
        """
        pass
        
    def IsLockTable(self, name):
        """
        Возвращает признак блокировки таблицы.
        """
        pass
        
    def IsLockRec(self, name, id):
        """
        Возвращает признак блокировки записи.        
        """
        pass
