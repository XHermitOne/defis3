#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мера/Фактические данные OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEMEASURE = {'__parent__': icwidget.SPC_IC_SIMPLE,
                      '__attr_hlp__': {},
                      }


class icCubeMeasureProto(object):
    """
    Мера/Фактические данные OLAP Куб.
    Абстрактный класс.
    """
    pass
