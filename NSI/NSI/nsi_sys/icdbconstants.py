#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Класс констант хранящихся в БД.
"""

# --- Imports ---
from . import icsprav

# Version
__version__ = (0, 1, 1, 1)

# --- Specification ---
SPC_IC_DBCONSTANTS = {'type': 'DBConstants',
                      'name': 'default',
                      'description': '',        # Описание
                      '__parent__': icsprav.SPC_IC_SPRAV,
                      }


class icDBConstantsPrototype(icsprav.icSpravPrototype):
    """
    Класс констант.
    """
    def __init__(self, SpravManager_=None, Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя в списке менеджера справочников.
        """
        icsprav.icSpravPrototype.__init__(self, SpravManager_, Name_)
