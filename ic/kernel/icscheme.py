#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поддержка доступа к схемам БД системы через точку.
"""

# Подключение библиотек

from ic.utils import ic_cache
from . import ic_dot_use


class icDataDotUsePrototype(ic_dot_use.icMetaDotUsePrototype):
    """
    Класс поддержки доступа к объектам данных.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Консруктор.
        """
        ic_dot_use.icMetaDotUsePrototype.__init__(self, DefaultPassportList_)


class icDBSchemasDotUse(icDataDotUsePrototype):
    """
    Класс описания объектов схем. Для доступа к объектам данных через точку.
    """

    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icDataDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к БД через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            

        db_scheme = icDBSchemeDotUse(object.__getattribute__(self, '_cur_passport_list'))
        db_scheme._cur_passport_list[0] = None
        db_scheme._cur_passport_list[1] = AttrName_
        db_scheme._cur_passport_list[2] = None
        db_scheme._cur_passport_list[3] = AttrName_+'.src'
        db_scheme._cur_passport_list[-1] = None
            
        return db_scheme


class icDBSchemeDotUse(icDataDotUsePrototype):
    """
    Класс схемы БД. Для доступа к объектам данных через точку.
    """
    # Кеш таблиц в схеме БД
    DB_SCHEME_CACHE = ic_cache.icCache(name='DB_SCHEME')
    
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icDataDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к таблицам через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        tab = icTableDotUse(object.__getattribute__(self, '_cur_passport_list'))
        tab._cur_passport_list[0] = 'Table'
        tab._cur_passport_list[1] = AttrName_
        tab._cur_passport_list[2] = None
        tab._cur_passport_list[3] = AttrName_+'.tab'
        tab._cur_passport_list[-1] = None
           
        db_scheme_cache = object.__getattribute__(self, 'DB_SCHEME_CACHE')
        if db_scheme_cache.hasObject('DB_SCHEME', tab.passport()):
            return db_scheme_cache.get('DB_SCHEME', tab.passport())
        else:
            new_tab = tab.create()
            db_scheme_cache.add('DB_SCHEME', tab.passport(), new_tab)
            return new_tab
        return tab

    def create(self, parent=None, *arg, **kwarg):
        """
        Создание выбранного объекта.
        """
        db = icDataDotUsePrototype.create(self, parent, *arg, **kwarg)
        if db:
            # создать схему сразу
            return db.createScheme(reCreate=kwarg.get('reCreate', True))
        return db
        

class icTableDotUse(icDataDotUsePrototype):
    """
    Класс таблицы. Для доступа к объектам данных через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icDataDotUsePrototype.__init__(self, DefaultPassportList_)
