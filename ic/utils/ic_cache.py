#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль управления буферезированными данными.
@type systemCach: C{icCache}
@var systemCace: Системный буфер.
"""

import copy

__named_cache__ = {}


class icCache:
    """
    Класс поддержки буферов.
    """

    def __init__(self, name='__noname__', maxSize=None, fltFunc=None):
        """ 
        Конструктор буфера.
        """
        if name:
            global __named_cache__
            if name not in __named_cache__:
                __named_cache__[name] = {}
            self.cache = __named_cache__[name]

        #   Имя буфера
        self.name = name
        #   Максимальный размер буфера
        self.maxSize = maxSize
        #   Функция, фильтрующая буфер
        self.filterFunc = fltFunc
        
    def add(self, classObj, id, obj):
        """ 
        Добавляет объект в буфер класса.
        @type classObj: C{string}
        @param classObj: Имя класса буфера.
        @param id: Идентификатор объекта.
        @param obj: Объект, которых кладется в буфер.
        """
        if classObj in self.cache:
            self.cache[classObj][id] = obj
        else:
            self.cache[classObj] = {id: obj}
            
        #   Фильтация буфера
        if self.maxSize and self.maxSize < len(self.cache[classObj].keys()) and self.filterFunc:
            self.filterFunc(self)
            
    def hasObject(self, classObj, id):
        try:
            self.cache[classObj][id]
            return True
        except:
            return False
            
    def get(self, classObj, id, bCopy=False):
        """ 
        Возвращает объект из буфера.
        @type classObj: C{string}
        @param classObj: Имя класса буфера.
        @param id: Идентификатор объекта.
        @param obj: Объект, которых кладется в буфер.
        @type bCopy: C{bool}
        @param bCopy: Признак возвата копии объекта.
        """
        if bCopy:
            return copy.deepcopy(self.cache[classObj][id])
        else:
            return self.cache[classObj][id]
            
    def clear(self, classObj=None):
        """ 
        Чистит буфер класса.
        @type classObj: C{string}
        @param classObj: Имя класса буфера.
        """
        if classObj in self.cache:
            return self.cache.pop(classObj)
        elif classObj == None:
            self.cache = dict()

    def getAll(self, bCopy=False):
        """
        Получить буфер полностью.
        @type bCopy: C{bool}
        @param bCopy: Признак возвата копии.
        """
        if bCopy:
            return copy.deepcopy(self.cache)
        return self.cache


#   Системный буфер
systemCache = icCache()


if __name__ == '__main__':
    c1 = icCache('1001')
    c1.add('class1', 1, 'object')
    print(__named_cache__)

