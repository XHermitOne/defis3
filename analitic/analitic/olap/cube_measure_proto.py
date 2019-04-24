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
                      'label': None,    # Надпись, если не определена, то берется description

                      '__parent__': icwidget.SPC_IC_SIMPLE,
                      '__attr_hlp__': {'field_name': u'Альтернативное название поля факта в таблице куба, Если не определено, то используется имя объекта',
                                       'label': u'Надпись, если не определена, то берется description',
                                       },
                      }


class icCubeMeasureProto(object):
    """
    Мера/Фактические данные OLAP Куб.
    Абстрактный класс.
    """
    def getFieldName(self):
        """
        Альтернативное название поля факта в таблице куба,
        Если не определено, то используется имя объекта
        """
        return None

    def getLabel(self):
        """
        Надпись, если не определена, то берется description.
        """
        return None


