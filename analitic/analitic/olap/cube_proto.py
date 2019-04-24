#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Куб.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBE = {'table_name': None,  # Альтернативное название таблицы куба в БД,
                                    # Если не определено, то используется имя куба
               '__parent__': icwidget.SPC_IC_SIMPLE,
               '__attr_hlp__': {'table_name': u'Альтернативное название таблицы куба в БД, Если не определено, то используется имя куба',
                                },
               }


class icCubeProto(object):
    """
    OLAP Куб.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Альтернативное название таблицы куба в БД,
        # Если не определено, то используется имя куба
        self._table_name = None

    def getDimensions(self):
        """
        Список объектов измерений
        """
        return list()

    def getMeasures(self):
        """
        Список объектов мер/фактов.
        """
        return list()

    def getAggregates(self):
        """
        Список объектов функций аггрегаций.
        """
        return list()
