#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления структурой SpreadSheet на базе библиотеки virtual_excel.
"""

from ic.log import log
from ..virtual_excel import icexcel

__version__ = (0, 1, 1, 1)

# Стили по умолчанию
DEFAULT_STYLE_COLUMN = {'ID': 'COL',
                        'name': 'Style',
                        }
DEFAULT_STYLE_ROW = {'ID': 'ROW',
                     'name': 'Style',
                     }
DEFAULT_STYLE_CELL = {'ID': 'CELL',
                      'name': 'Style',
                      }
DEFAULT_STYLE_HEADER = {'ID': 'HEADER',
                        'name': 'Style',
                        }
DEFAULT_STYLE_FOOTER = {'ID': 'FOOTER',
                        'name': 'Style',
                        }
DEFAULT_STYLE_GROUP_HEADER = {'ID': 'GRP_HEADER',
                              'name': 'Style',
                              }
DEFAULT_STYLE_GROUP_FOOTER = {'ID': 'GRP_FOOTER',
                              'name': 'Style',
                              }

DEFAULT_STYLES = (DEFAULT_STYLE_COLUMN,
                  DEFAULT_STYLE_ROW,
                  DEFAULT_STYLE_CELL,
                  DEFAULT_STYLE_HEADER,
                  DEFAULT_STYLE_FOOTER,
                  DEFAULT_STYLE_GROUP_HEADER,
                  DEFAULT_STYLE_GROUP_FOOTER)


class icSpreadSheetManager(icexcel.icVExcel):
    """
    Менеджер управления структурой SpreadSheet на базе библиотеки virtual_excel.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icexcel.icVExcel.__init__(self, *args, **kwargs)

    def setSpreadSheetData(self, spreadsheet_data):
        """
        Установить данные.
        @param spreadsheet_data: Данные структуры SpreadSheet.
        """
        self._data = spreadsheet_data

    def createDefaultColumn(self, table):
        """
        Создание колонки по умолчанию.
        @param table: Таблица.
        @return: True/False
        """
        if table is None:
            log.warning(u'Не определена таблица для создания колонки по умолчанию')
            return False

        column = table.createColumn()
        col_attrs = dict(StyleID='COL')
        column.set_attributes(col_attrs)
        return True

    def createDefaultColumns(self, table, count=1):
        """
        Создание колонок по умолчанию.
        @param table: Таблица.
        @param count: Количество создаваемых колонок.
        @return: True/False
        """
        results = [self.createDefaultColumn(table) for i in range(count)]
        return all(results)
