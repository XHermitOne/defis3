#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Иерархия уровней измерения OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEDIMENSIONHIERARCHY = {'levels': None,  # Список имен уровней измерения данной иерархии
                                 # 'label': None,  # Надпись измерения
                                 '__parent__': icwidget.SPC_IC_SIMPLE,
                                 '__attr_hlp__': {'levels': u'Список имен уровней измерения данной иерархии',
                                                  },
                                 }


class icCubeDimensionHierarchyProto(object):
    """
    Иерархия уровней измерения OLAP Куба.
    Абстрактный класс.
    """
    def getLevelNames(self):
        """
        Список имен уровней измерения данной иерархии.
        """
        return list()

    def getLevels(self):
        """
        Список уровней измерения данной иерархии.
        """
        return list()
