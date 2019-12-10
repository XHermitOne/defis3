#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Измерение OLAP Куба.
"""

from ic.log import log
from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_CUBEDIMENSION = {'field_name': None,  # Альтернативное название поля измерения в таблице куба,
                                             # Если не определено, то используется имя объекта
                        'detail_tabname': None,     # Имя таблицы детализации, связанной с полем таблицы куба
                        'detail_fldname': None,     # Имя поля таблицы детализации, по которому осуществляется связь
                        'attributes': None,  # Список имен полей дополнительных атрибутов
                        'label': None,  # Надпись измерения
                        'mapping': None,  # Физичекое указание поля для отображения

                        '__parent__': icwidget.SPC_IC_SIMPLE,
                        '__attr_hlp__': {'field_name': u'Альтернативное название поля измерения в таблице куба, Если не определено, то используется имя объекта',
                                         'attributes': u'Список имен полей дополнительных атрибутов',
                                         'detail_tabname': u'Имя таблицы детализации, связанной с полем таблицы куба',
                                         'detail_fldname': u'Имя поля таблицы детализации, по которому осуществляется связь',
                                         'label': u'Надпись измерения',
                                         'mapping': u'Физичекое указание поля для отображения',
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
        Список имен полей дополнительных атрибутов.
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

    def getLevels(self):
        """
        Список объектов уровней измерения.
        """
        return list()

    def getHierarchies(self):
        """
        Список объектов иерархий уровней измерения.
        """
        return list()

    def findHierarchy(self, hierarchy_name):
        """
        Наити объект иерархии по имени.
        :param hierarchy_name: Имя объекта иерархии.
        :return: Объект иерархии или None, если не найден.
        """
        finds = [obj for obj in self.getHierarchies() if obj.getName() == hierarchy_name]
        if finds:
            return finds[0]
        else:
            log.warning(u'Иерархия с именем <%s> не найдено в измерении <%s>' % (hierarchy_name, self.getName()))
        return None

    def findLevel(self, level_name):
        """
        Поиск объекта уровня измерения по его имени.
        :param level_name: Имя уровня.
        :return: Объект уровня измерения или None, если объект с таким именем не найден.
        """
        finds = [obj for obj in self.getLevels() if obj.getName() == level_name]
        if finds:
            return finds[0]
        else:
            log.warning(u'Уровень с именем <%s> не найдено в измерении <%s>' % (level_name, self.getName()))
        return None

    def getMapping(self):
        """
        Физичекое указание поля для отображения измерения.
        """
        return u''
