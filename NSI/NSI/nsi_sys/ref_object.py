#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс объекта-ссылки/справочника.
"""

from ic.components import icwidget

from ic.log import log
from ic.utils import system_cache

from . import icsprav

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_REFOBJECT = {'type': 'RefObject',
                    'name': 'default',
                    'description': '',      # Описание справочника

                    'db': None,             # Паспорт БД хранения данных
                    'cache': True,          # Автоматически кэшировать?
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    '__attr_hlp__': {'db': u'Паспорт БД хранения данных',
                                     'cache': u'Автоматически кэшировать?',
                                     },
                    }


class icRefObjectProto(icsprav.icSpravInterface):
    """
    Класс объекта-ссылки/справочника.
    """

    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.
        @param sprav_manager: Объект менеджера справочника.
        @param name: Имя справочника в списке менеджера справочников.
        """
        icsprav.icSpravInterface.__init__(self, sprav_manager, name)

        # Кэш
        self._cache = system_cache.icCache()
