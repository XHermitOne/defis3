#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления сводной таблицей.
Реализация таблицы производится через библиотеку pandas.
"""

import numpy
import pandas

from ic.log import log

__version__ = (0, 1, 1, 1)

AGGREGATE_FUNCTION_NAMES = ('sum', 'min', 'max', 'mean')


class icPivotDataFrameManager(object):
    """
    Менеджер управления сводной таблицей.
    """
    def __init__(self):
        """
        Конструктор.
        """
        # Текущая сводная таблица
        self._cur_pivot_dataframe = None

    def getPivotDataFrame(self):
        """
        Текущая сводная таблица.
        """
        return self._cur_pivot_dataframe

    def create_dataframe(self, rows, column_names):
        """
        Создать простую таблицу.
        @param rows: Список строк.
            Список строк - список списков в соответствии со списком имен колонок.
        @param column_names: Имена колонок.
        @return: Созданный объект pandas.DataFrame.
        """
        self._cur_pivot_dataframe = None

        try:
            data_rows = [pandas.Series(row) for row in rows]
            self._cur_pivot_dataframe = pandas.DataFrame(data_rows)
            # Устанавливаем имена колонок
            self._cur_pivot_dataframe.columns = column_names
        except:
            log.fatal(u'Ошибка создания сводной таблицы. Колонки: %s' % str(column_names))

        return self._cur_pivot_dataframe

    def set_pivot_dimensions(self, row_dimension, col_dimension):
        """
        Установить измерения строк и колонок в сводной таблице.
        @param row_dimension: Измерение/измерения, которые будут отображаться по строкам.
            Задается списком имен колонок.
        @param col_dimension: Измерение/измерения, которые будут отображаться по колонкам.
            Задается списком имен колонок.
        @return: Текущий объект pandas.DataFrame.
        """
        if not row_dimension:
            row_dimension = list()
        if not col_dimension:
            col_dimension = list()

        dimensions = list(row_dimension) + list(col_dimension)
        # Устанавливаем индексы измерений
        self._cur_pivot_dataframe = self._cur_pivot_dataframe.set_index(dimensions)
        if col_dimension:
            # Переносим измерения колонок
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.unstack(col_dimension)
        return self._cur_pivot_dataframe

    def fillna_value(self, value=0):
        """
        Заменить не определенные значения NaN в сводной таблице
        на указанное значение.
        @param value: Значение для замены.
        @return: Текущий объект pandas.DataFrame.
        """
        self._cur_pivot_dataframe = self._cur_pivot_dataframe.fillna(value=value)
        return self._cur_pivot_dataframe

    def groupby_dimensions(self, row_dimension):
        """
        Группировка строк по измерениям.
        @param row_dimension: Измерение/измерения, которые будут отображаться по строкам.
            Задается списком имен колонок.
        @return: Текущий объект pandas.DataFrame.
        """
        if (isinstance(row_dimension, tuple) or isinstance(row_dimension, list)) and len(row_dimension) == 1:
            row_dimension = row_dimension[0]

        self._cur_pivot_dataframe = self._cur_pivot_dataframe.groupby(row_dimension)
        return self._cur_pivot_dataframe

    def aggregate_dimensions(self, aggregate_function_name='sum'):
        """
        Выполнить агрегирование по группам.
        @param aggregate_function_name: Имя аггрегирующей функции.
        @return: Текущий объект pandas.DataFrame.
        """
        if aggregate_function_name == 'sum':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.sum)
        elif aggregate_function_name == 'min':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.min)
        elif aggregate_function_name == 'max':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.max)
        elif aggregate_function_name == 'mean':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.mean)
        return self._cur_pivot_dataframe

    def get_pivot_shape(self, dataframe=None):
        """
        Размер данных сводной таблицы.
        @param dataframe: Объект сводной таблицы.
            Если не определена, то берется внутренняя.
        @return: Количество строк, количество колонок.
        """
        if dataframe is None:
            dataframe = self._cur_pivot_dataframe
        return dataframe.shape

    def get_pivot_tab_size(self, dataframe=None):
        """
        Размер сводной таблицы.
        @param dataframe: Объект сводной таблицы.
            Если не определена, то берется внутренняя.
        @return: Количество строк, количество колонок.
        """
        if dataframe is None:
            dataframe = self._cur_pivot_dataframe

        row_count, col_count = self.get_pivot_shape(dataframe)
        # Учет строки надписей колонок уовней строк---V
        row_level_count = 1 if any(dataframe.index.names) else 0

        row_count = row_count + dataframe.columns.nlevels + row_level_count
        col_count = col_count + dataframe.index.nlevels
        return row_count, col_count

    def total_pivot_table(self, dataframe):
        """
        Расчет общих итогов сводной таблицы по строкам.
        @param dataframe: Объект pandas.DataFrame сводной таблицы.
        @return: Объект pandas.DataFrame, соответствующей сводной таблице.
        """
        total = dataframe.agg(numpy.sum)
        total_row = pandas.DataFrame([total])
        log.debug(u'Расчет общих итогов по значениям:\n%s' % str(total))
        result = pandas.concat([dataframe, total_row],
                               keys=[u'', u'ИТОГО'])
        return result

    def total_group_pivot_table(self, dataframe):
        """
        Расчет итогов по группам сводной таблицы по строкам.
        @param dataframe: Объект pandas.DataFrame сводной таблицы.
        @return: Объект pandas.DataFrame, соответствующей сводной таблице.
        """
        total = dataframe.groupby(dataframe.index).agg(numpy.sum)
        # total_row = pandas.DataFrame([total])
        log.debug(u'Расчет групповых итогов по значениям:\n%s' % str(total))
        # result = pandas.concat([dataframe, total_row],
        #                        keys=[u'', u'ИТОГО'])
        result = total
        return result
