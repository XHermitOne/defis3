#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Описание источников сигналов.
"""

from . import icsignal

__version__ = (0, 1, 1, 1)


class icSignalSrc:
    """
    Базовый класс описания источников сигналов.
    """

    def __init__(self, passport, *arg, **kwarg):
        """
        Конструктор.
        
        :type passport: C{icobject.icObjectPassport}
        :param passport: Паспорт объекта источника.
        """
        self.kernel = None
        self.passport = passport
        
    def generate(self, *arg, **kwarg):
        """
        Функция генерация сигнала.
        """
        pass
        
    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return icsignal.icSignal.__name__

    
class icWxEvtSignalSrc(icSignalSrc):
    """
    Описание источника, который генерирует сигнал по событийному механизму библиотеки
    wx.
    """
    def __init__(self, passport, event_id, bSkip=True, *arg, **kwarg):
        """
        Конструктор.
        
        :type passport: C{icobject.icObjectPassport}
        :param passport: Паспорт объекта источника.
        :type event_id: C{int}
        :param event_id: Идентификатор события. Пример: wx.EVT_LEFT_DOWN.
        """
        icSignalSrc.__init__(self, passport)
        self.event_id = event_id
        self.bSkip = bSkip
        
    def generate(self, event, obj):
        """
        Генерация сигнала.
        
        :type event: C{wx.Event}
        :param event: Событие, по которому генерируется сигнал.
        """
        return icsignal.icWxEvtSignal(self.passport, obj, event)
        
    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return self.event_id.eventType[0]

    def isWxSkip(self):
        """
        Признак продолжения обработки синеал wx механизмом.
        """
        return self.bSkip


class icChangedAttrSrc(icSignalSrc):
    """
    Генератор сигнала на изменение заданого атрибута объекта.
    """
    def __init__(self, passport, attr, *arg, **kwarg):
        """
        Конструктор.
        
        :type passport: C{icobject.icObjectPassport}
        :param passport: Паспорт объекта источника.
        :type attr: C{string}
        :param attr: Имя атрибута объекта.
        """
        icSignalSrc.__init__(self, passport)
        self.attr = attr
        
    def generate(self, attr=None, value=None, obj=None):
        """
        Генерация сигнала.
        
        :type attr: C{string}
        :param attr: Имя атрибута объекта.
        """
        if not attr:
            attr = self.attr
            
        return icsignal.icChangedAttrSignal(self.passport, attr, value, obj)

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'ChangedAttr', self.attr


class icPreFuncSrc(icSignalSrc):
    """
    Генератор сигнала на вызов определенной функции объекта.
    """

    def __init__(self, passport, func_name, *arg, **kwarg):
        """
        Конструктор.
        
        :type passport: C{icobject.icObjectPassport}
        :param passport: Паспорт объекта источника.
        :type func_name: C{string}
        :param func_name: Имя функции.
        """
        icSignalSrc.__init__(self, passport)
        self.func_name = func_name
        
    def generate(self, func_name=None, obj=None):
        """
        Генерация сигнала.
        
        :type func_name: C{string}
        :param func_name: Имя функции объекта.
        """
        if not func_name:
            func_name = self.func_name
            
        return icsignal.icPreFuncSignal(obj, func_name)

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'PreFunction', self.func_name


class icPostFuncSrc(icSignalSrc):
    """
    Генератор сигнала на выход из определенной функции объекта.
    """

    def __init__(self, passport, func_name, *arg, **kwarg):
        """
        Конструктор.
        
        :type passport: C{icobject.icObjectPassport}
        :param passport: Паспорт объекта источника.
        :type func_name: C{string}
        :param func_name: Имя функции.
        """
        icSignalSrc.__init__(self, passport)
        self.func_name = func_name
        
    def generate(self, func_name=None, obj=None):
        """
        Генерация сигнала.
        
        :type func_name: C{string}
        :param func_name: Имя функции объекта.
        """
        if not func_name:
            func_name = self.func_name
            
        return icsignal.icPostFuncSignal(obj, func_name)

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'PostFunction', self.func_name
