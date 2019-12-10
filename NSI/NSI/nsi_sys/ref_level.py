#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс уровня объекта-ссылки/справочника.
"""

from ic.components import icwidget

from ic.log import log

from . import icspravlevel
from . import ref_persistent

# Версия
__version__ = (0, 1, 1, 1)

# --- Спецификация ---
SPC_IC_REFLEVEL = {'type': 'RefLevel',
                   'name': 'default',
                   'description': '',      # Описание справочника

                   'len': 2,  # Длина кода уровня
                   'pic': None,  # Картинка-образ
                   'pic2': None,  # Дополнительная картинка-образ

                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   '__attr_hlp__': {'len': u'Длина кода уровня',
                                    'pic': u'Картинка-образ',
                                    'pic2': u'Дополнительная картинка-образ',
                                    },

                   }


class icRefLevelProto(ref_persistent.icRefTablePersistent,
                      icspravlevel.icSpravLevelInterface):
    """
    Класс уровня объекта-ссылки/справочника.
    """

    def __init__(self, parent, index=-1):
        """
        Конструктор.
        :param parent: Справочник-родитель.
        :param index: Индекс уровня в справочнике-родителе.
        """
        ref_persistent.icRefTablePersistent.__init__(self, parent=parent)
        icspravlevel.icSpravLevelInterface.__init__(self, parent, index)

    def getAddCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на добавление записи в справочник.
        """
        # Отключаем дополнительный контроль при добавлении записи
        return None
