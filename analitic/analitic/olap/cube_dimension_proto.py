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
                        'detail_tabname': None,     # Имя таблицы детализации, связанной с полем таблицы куба
                        'detail_fldname': None,     # Имя поля таблицы детализации, по которому осуществляется связь
                        'attributes': None,  # Список имен полей дополнительных атрибутов
                        'label': None,  # Надпись измерения
                        '__parent__': icwidget.SPC_IC_SIMPLE,
                        '__attr_hlp__': {'field_name': u'Альтернативное название поля измерения в таблице куба, Если не определено, то используется имя объекта',
                                         'attributes': u'Список имен полей дополнительных атрибутов',
                                         'detail_tabname': u'Имя таблицы детализации, связанной с полем таблицы куба',
                                         'detail_fldname': u'Имя поля таблицы детализации, по которому осуществляется связь',
                                         'label': u'Надпись измерения',
                                         },
                        }


class icCubeDimensionProto(object):
    """
    Измерение OLAP Куба.
    Абстрактный класс.
    """
    def getFieldName(self):
        """
        Имя поля измерения в таблице куба.
        """
        return u''

    def getAttributes(self):
        """
        Список имен полей дополнительных атрибутов
        """
        return list()

    def getDetailTableName(self):
        """
        Имя таблицы детализации, связанной с полем таблицы куба.
        """
        return None

    def getDetailFieldName(self):
        """
        Имя поля таблицы детализации, по которому осуществляется связь.
        """
        return None

    def getLabel(self):
        """
        Надпись измерения.
        """
        return u''
