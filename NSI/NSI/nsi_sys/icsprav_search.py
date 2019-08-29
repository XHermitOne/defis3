#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль управления буфером поиска.
"""

__version__ = (0, 1, 1, 2)


class icSearchBuff(object):
    """
    Буфер поиска.
    """

    def __init__(self, find_str, search_result=None, *arg, **kwarg):
        """
        Конструктор.
        """
        # Буфер данных
#        self.find_str = find_str
#        self.search_result = search_result
#        # Курсор текущей строки
#        self.cursor = -1
#        self.bEOF = False
        self.set_data(find_str, search_result)

    def next(self):
        """
        Сдвиг курсора на следующую позицию.
        """
        self.cursor += 1
        if self.cursor >= len(self.searchResult or []):
            self.cursor = -1
        elif self.cursor:
            return self.searchResult[self.cursor]

    def set_data(self, find_str, search_result):
        """
        Устанавливает буфер поиска.
        """
        self.find_str = find_str
        self.searchResult = search_result
        self.cursor = -1
        self.bEOF = False

    def isEOF(self):
        return self.bEOF


class icSpravSearchBuff(icSearchBuff):
    """
    Буфер поиска по справочнику.
    """

    def __init__(self, find_str, search_result=None, *arg, **kwarg):
        icSearchBuff.__init__(self, find_str, search_result, *arg, **kwarg)
        self.cod_indx = kwarg.get('cod_indx', None)

    def next(self):
        """
        Сдвиг курсора на следующую позицию.
        """
        if self.searchResult:
            res = self.searchResult.fetchone()
            if res:
                self.cursor += 1
                return res

#        self.cursor = -1
        self.bEOF = True
