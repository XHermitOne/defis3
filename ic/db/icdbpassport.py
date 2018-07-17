#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Индентификация объектов в пространстве данных.
"""

from ic.kernel import icobject
import ic

__version__ = (0, 0, 1, 2)


def to_db_passport(func):
    """ 
    Приводит пасспорт к базовому виду.
    """
    def wrapper(self, passport, *args, **kwargs):
        if type(passport) in (type([]), type((0,))):
            passport = icDBPassport(*passport)
        return func(self, passport, *args, **kwargs)
    return wrapper


def get_object(psp):
    """ 
    По паспорту возвращает объект замапированного к таблице класса.
    @type psp: C{icDBPassport}
    @param psp: Паспорт объекта данных.
    """
    if psp.subsys:
        sub = getattr(ic.metadata, psp.subsys)
    else:
        sub = getattr(ic.metadata, 'THIS')
    tab = getattr(sub.tab, psp.table).create()
    cls = tab.getMapperClass()
    session = tab.db.getSession()
    obj = session.get(cls, psp.id)
    return obj

        
class icDBPassport(icobject.icBasePassport):
    """ 
    Индентификация объектов в пространстве данных (таблиц). Паспорт задается списком 
    идентифицирующих кортежей, первый картеж задает объект по имени таблицы,
    его идентификатору и имени подсистемы, второой картеж содержит UUID объекта 
    (Второй картеж не обязательный). 
    
    Пример:  icDBPassport([('people', 1841, 'STD'), ('asdf12233566af00',)])
    Доступ к объект таблицы можно получить следующим образом:
    >>>import ic
    >>>ic.Login('admin', None, '../myPrj/myPrj/')
    >>>p1 = icDBPassport(('people', 1840, 'myPrj'), ('asdf12233566af00',)) # С точным указанием подсистемы
    >>>p2 = icDBPassport(('people', 1840, None))  # С указанием на текущую подсистему
    >>>p1 == p2
    True
    >>>tab = ic.metadata.STD.tab.people.create()
    >>>obj = tab.get(1840)
    >>>obj = get_object(p1) # альтернативный способ 
    >>>ic.Logout()
    """

    def __init__(self, *arg):
        icobject.icBasePassport.__init__(self, *arg)
        
    def get_table(self):
        """ 
        Возвращает имя объекта таблицы.
        """
        return self[0][0]
        
    def get_id(self):
        """ 
        Возвращает идентификатор объекта.
        """
        return self[0][1]
    
    def get_subsys(self):
        """ 
        Возвращает имя подсистемы.
        """
        if len(self[0]) > 2: 
            return self[0][2]
            
    table = property(get_table)
    id = property(get_id)
    subsys = property(get_subsys)
