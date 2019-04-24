#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Агрегация OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEAGGREGATE = {'function': None,   # Функция агрегации
                        'measure': None,    # Мера/Факт, которое агрегируется
                        'expression': None,     # Выражение агрегации
                        '__parent__': icwidget.SPC_IC_SIMPLE,
                        '__attr_hlp__': {'function': u'Функция агрегации',
                                         'measure': u'Мера/Факт, которое агрегируется',
                                         'expression': u'Выражение агрегации',
                                         },
                        }

# Функции агрегации
AGGREGATE_FUNCTIONS = (None, 'sum', 'count', 'min', 'max')


class icCubeAggregateProto(object):
    """
    Агрегация OLAP Куба.
    Абстрактный класс.
    """
    def getFunctionName(self):
        """
        Функция агрегации.
        """
        return None

    def getMeasureName(self):
        """
        Мера/Факт, которое агрегируется.
        """
        return None

    def getExpressionCode(self):
        """
        Выражение агрегации.
        """
        return None
