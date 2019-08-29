#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Класс перечислений хранящихся в БД.
"""

# --- Imports ---
from . import icsprav

# Version
__version__ = (0, 1, 1, 2)


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
    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.
        @param sprav_manager: Объект менеджера справочника.
        @param name: Имя в списке менеджера справочников.
        """
        icsprav.icSpravPrototype.__init__(self, sprav_manager, name)
