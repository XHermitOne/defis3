#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления просмотром структуры SpreadSheet.
Просмотр осуществляется с помощью контрола wx.Grid.
"""

from ic.log import log
from ic.utils import wxfunc

__version__ = (0, 1, 1, 1)


class icSpreadSheetViewManager(object):
    """
    Менеджер управления просмотром структуры SpreadSheet.
    Просмотр осуществляется с помощью контрола wx.Grid.
    """
    def __init__(self, grid=None):
        """
        Конструктор.
        @param grid: Управляемый объект wx.Grid.
        """
        self._spreadsheet_grid = grid

    def getSpreadSheetGrid(self):
        """
        Управляемый объект wx.Grid.
        """
        return self._spreadsheet_grid

    def setSpreadSheetGrid(self, grid=None):
        """
        Установить управляемый объект wx.Grid.
        @param grid: Управляемый объект wx.Grid.
        """
        self._spreadsheet_grid = grid

    def show_spreadsheet(self, spreadsheet_data):
        """
        Отобразить данные структуры SpreadSheet в гриде.
        @param spreadsheet_data: Данные структуры SpreadSheet.
        @return: True/False.
        """
        if self._spreadsheet_grid is None:
            log.warning(u'Не определен wx.Grid для отображения структуры SpreadSheet')
            return False
        if wxfunc.isWxDeadObject(self._spreadsheet_grid):
            log.warning(u'Объек wx.Grid для отображения структуры SpreadSheet разрушен')
            return False

        return True
