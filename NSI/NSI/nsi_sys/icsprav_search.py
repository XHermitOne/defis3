#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль управления буфером поиска.
"""


class search_buff(object):
    """
    Буфер поиска.
    """

    def __init__(self, find_str, searchResult=None, *arg, **kwarg):
        """
        Конструктор.
        """
        # Буфер данных
#        self.find_str = find_str
#        self.searchResult = searchResult
#        # Курсор текущей строки
#        self.cursor = -1
#        self.bEOF = False
        self.set_data(find_str, searchResult)

    def next(self):
        """
        Сдвиг курсора на следующую позицию.
        """
        self.cursor += 1
        if self.cursor >= len(self.searchResult or []):
            self.cursor = -1
        elif self.cursor:
            return self.searchResult[self.cursor]

    def set_data(self, find_str, searchResult):
        """
        Устанавливает буфер поиска.
        """
        self.find_str = find_str
        self.searchResult = searchResult
        self.cursor = -1
        self.bEOF = False

    def isEOF(self):
        return self.bEOF


class sparv_search(search_buff):
    """
    Буфер поиска по справочнику.
    """

    def __init__(self, find_str, searchResult=None, *arg, **kwarg):
        search_buff.__init__(self, find_str, searchResult, *arg, **kwarg)
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
