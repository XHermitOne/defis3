#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Уровень измерения OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEDIMENSIONLEVEL = {'attributes': None,  # Список имен полей дополнительных атрибутов
                             # 'label': None,  # Надпись измерения
                             '__parent__': icwidget.SPC_IC_SIMPLE,
                             '__attr_hlp__': {'attributes': u'Список имен полей дополнительных атрибутов',
                                              },
                             }


class icCubeDimensionLevelProto(object):
    """
    Уровень измерения OLAP Куба.
    Абстрактный класс.
    """
    def getAttributes(self):
        """
        Список имен полей дополнительных атрибутов.
        """
        return list()

