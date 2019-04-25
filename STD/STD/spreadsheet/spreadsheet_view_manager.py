#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления просмотром структуры SpreadSheet.
Просмотр осуществляется с помощью контрола wx.Grid.
"""

from ic.log import log
from ic.utils import wxfunc

from . import spreadsheet_manager

from ic.engine import panel_manager


__version__ = (0, 1, 1, 1)


class icSpreadSheetViewManager(spreadsheet_manager.icSpreadSheetManager,
                               panel_manager.icPanelManager):
    """
    Менеджер управления просмотром структуры SpreadSheet.
    Просмотр осуществляется с помощью контрола wx.Grid.
    """
    def __init__(self, grid=None, *args, **kwargs):
        """
        Конструктор.
        @param grid: Управляемый объект wx.Grid.
        """
        spreadsheet_manager.icSpreadSheetManager.__init__(self, *args, **kwargs)

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

    def view_spreadsheet(self, spreadsheet_data):
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

        try:
            return self._view_spreadsheet(spreadsheet_data)
        except:
            log.fatal(u'Ошибка отображения данных структуры SpreadSheet в гриде.')
        return False

    def _view_spreadsheet(self, spreadsheet_data, worksheet_name=None):
        """
        Отобразить данные структуры SpreadSheet в гриде.
        @param spreadsheet_data: Данные структуры SpreadSheet.
        @param worksheet_name: Имя листа.
            Если не определено, то берется первый лист.
        @return: True/False.
        """
        self.setSpreadSheetData(spreadsheet_data)
        workbook = self.getWorkbook()
        if not workbook:
            log.warning(u'SpreadSheet. Не корректная структура. Книга.')
            return False

        worksheet = workbook.getWorksheetIdx() if not worksheet_name else workbook.findWorksheet(worksheet_name)
        if not worksheet:
            log.warning(u'SpreadSheet. Не корректная структура. Лист <%s>.' % str(worksheet_name))
            return False

        table = worksheet.getTable()
        if not table:
            log.warning(u'SpreadSheet. Не корректная структура. Таблица.')
            return False

        # Устанавливаем размер грида
        column_count = table.getColumnCount()
        row_count = table.getRowCount()
        self.reCreateGrid(self._spreadsheet_grid, row_count, column_count)

        for i_row in range(row_count):
            row = table.getRow(i_row)
            for i_col in range(column_count):
                cell = row.getCellIdx(i_col)
                if cell:
                    value = cell.getValue()
                    log.debug(u'Значение <%s> [%d x %d]' % (value, i_row, i_col))
                    if value:
                        row_idx, col_idx, merge_down, merge_accross = cell.getRegion()
                        if merge_down > 1 or merge_accross > 1:
                            self._spreadsheet_grid.SetCellSize(row_idx, col_idx, merge_down+1, merge_accross+1)
                        log.debug(u'Адрес <%d x %d>' % (row_idx, col_idx))
                        self._spreadsheet_grid.SetCellValue(row_idx, col_idx, str(value))
        return True
