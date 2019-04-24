#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Измерение OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEDIMENSION = {'field_name': None,  # Альтернативное название поля измерения в таблице куба,
                                             # Если не определено, то используется имя объекта
                        '__parent__': icwidget.SPC_IC_SIMPLE,
                        '__attr_hlp__': {'field_name': u'Альтернативное название поля измерения в таблице куба, Если не определено, то используется имя объекта',
                                         },
                        }


class icCubeDimensionProto(object):
    """
    Измерение OLAP Куба.
    Абстрактный класс.
    """
    pass
