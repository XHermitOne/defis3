#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовый интерфейс к объектам драйверов конвертера данных.
"""


class icConvertDriverInterface:
    """
    Базовый интерфейс к объектам драйверов конвертера данных.
    """
    def __init__(self, component_spc=None):
        """
        Конструктор.
        """
        self.resource = component_spc
        
    def getDataByName(self, Name_):
        """
        Получить данные по имени.
        """
        return None
        
    def setDataByName(self, Name_, Value_):
        """
        Сохранить данные по имени.
        """
        pass
        
    def getDataByIdx(self, Idx_):
        """
        Получить данные по индексу.
        """
        return None
        
    def setDataByIdx(self, Idx_, Value_):
        """
        Установить данные по индексу.
        """
        pass
        
    def getDataByNameIdx(self, Name_, Idx_):
        """
        Получить данные по имени и индексу.
        """
        return None
        
    def setDataByNameIdx(self, Name_, Idx_, Value_):
        """
        Установить данные по имени и индексу.
        """
        pass
        
    def First(self):
        """
        Переход на первый индекс.
        """
        pass
        
    def Last(self):
        """
        Переход на последний индекс.
        """
        pass
        
    def Next(self):
        """
        Переход  к следующему элементу.
        """
        pass
        
    def Prev(self):
        """
        Переход к предыдущему элементу.
        """
        pass
        
    def IsEnd(self):
        """
        Проверка достижения конца последовательности данных.
        """
        return False
        
    def IsBegin(self):
        """
        Проверка достижения начала последорвательности данных.
        """
        return False
