#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Класс констант хранящихся в БД.
"""

# --- Imports ---
from . import icsprav

# Version
__version__ = (0, 1, 1, 2)

# --- Specification ---
SPC_IC_DBCONSTANTS = {'type': 'DBConstants',
                      'name': 'default',
                      'description': '',        # Описание
                      '__parent__': icsprav.SPC_IC_SPRAV,
                      }


class icDBConstantsProto(icsprav.icSpravProto):
    """
    Класс констант.
    """
    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.
        @param sprav_manager: Объект менеджера справочника.
        @param name: Имя в списке менеджера справочников.
        """
        icsprav.icSpravProto.__init__(self, sprav_manager, name)
