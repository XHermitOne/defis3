#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Класс перечислений хранящихся в БД.
"""

# --- Imports ---
from . import icsprav

# Version
__version__ = (0, 1, 1, 1)


# --- Specification ---
SPC_IC_DBENUM = {'type': 'DBEnum',
                 'name': 'default',
                 'description': '',     # Описание
                 '__parent__': icsprav.SPC_IC_SPRAV,
                 }


class icDBEnumPrototype(icsprav.icSpravPrototype):
    """
    Класс перечислений.
    """
    def __init__(self, SpravManager_=None, Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя в списке менеджера справочников.
        """
        icsprav.icSpravPrototype.__init__(self, SpravManager_, Name_)
