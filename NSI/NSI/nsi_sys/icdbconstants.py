#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Класс констант хранящихся в БД.
Author(s): Колчанов А.В. 
"""

# Version
__version__ = (0, 0, 0, 1)

#--- Imports ---
from . import icsprav

#--- Specification ---
SPC_IC_DBCONSTANTS={
    'type': 'DBConstants',
    'name': 'default',
    'description':'',    #Описание
    '__parent__':icsprav.SPC_IC_SPRAV,
    }

#--- Functions ---
#--- Classes ---
class icDBConstantsPrototype(icsprav.icSpravPrototype):
    """
    Класс констант.
    """
    def __init__(self,SpravManager_=None,Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя в списке менеджера справочников.
        """
        icsprav.icSpravPrototype.__init__(self,SpravManager_,Name_)
