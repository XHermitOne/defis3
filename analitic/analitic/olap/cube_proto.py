#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Куб.
"""

from ic.log import log

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

    def findDimension(self, dimension_name):
        """
        Поиск объекта измерения по его имени.
        @return: Объект измерения или None, если объект с таким именем не найден.
        """
        finds = [obj for obj in self.getDimensions() if obj.getName() == dimension_name]
        if finds:
            return finds[0]
        else:
            log.warning(u'Измерение с именем <%s> не найдено в кубе <%s>' % (dimension_name, self.getName()))
        return None

    def findMeasure(self, measure_name):
        """
        Поиск объекта меры/факта по его имени.
        @return: Объект измерения или None, если объект с таким именем не найден.
        """
        finds = [obj for obj in self.getMeasures() if obj.getName() == measure_name]
        if finds:
            return finds[0]
        else:
            log.warning(u'Мера/факт с именем <%s> не найдено в кубе <%s>' % (measure_name, self.getName()))
        return None

    def findAggregate(self, aggregate_name):
        """
        Поиск объекта функции агрегации по его имени.
        @return: Объект функции агрегации или None, если объект с таким именем не найден.
        """
        finds = [obj for obj in self.getDimensions() if obj.getName() == aggregate_name]
        if finds:
            return finds[0]
        else:
            log.warning(u'Функции агрегации с именем <%s> не найдено в кубе <%s>' % (aggregate_name, self.getName()))
        return None
