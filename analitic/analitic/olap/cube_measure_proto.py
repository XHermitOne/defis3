#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мера/Фактические данные OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEMEASURE = {'field_name': None,  # Альтернативное название поля факта в таблице куба,
                                           # Если не определено, то используется имя объекта

                      '__parent__': icwidget.SPC_IC_SIMPLE,
                      '__attr_hlp__': {'field_name': u'Альтернативное название поля факта в таблице куба, Если не определено, то используется имя объекта',
                                       },
                      }


class icCubeMeasureProto(object):
    """
    Мера/Фактические данные OLAP Куб.
    Абстрактный класс.
    """
    pass
