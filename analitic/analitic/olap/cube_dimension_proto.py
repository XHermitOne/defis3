#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Измерение OLAP Куба.
"""

from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEDIMENSION = {'__parent__': icwidget.SPC_IC_SIMPLE,
                        '__attr_hlp__': {},
                        }


class icCubeDimensionProto(object):
    """
    Измерение OLAP Куба.
    Абстрактный класс.
    """
    pass
