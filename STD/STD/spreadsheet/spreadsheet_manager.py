#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления структурой SpreadSheet на базе библиотеки virtual_excel.
"""

from ..virtual_excel import icexcel

__version__ = (0, 1, 1, 1)


class icSpreadSheetManager(icexcel.icVExcel):
    """
    Менеджер управления структурой SpreadSheet на базе библиотеки virtual_excel.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icexcel.icVExcel.__init__(self, *args, **kwargs)
