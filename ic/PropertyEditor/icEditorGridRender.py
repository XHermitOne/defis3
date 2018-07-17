#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Отрисовка значений атрибутов в редакторе свойств.
"""

import wx
import string
import wx.grid as Grid
from . import icDefInf


class PropValueRenderer(Grid.PyGridCellRenderer):
    """
    """
    def __init__(self, table, color='blue', font='ARIAL', fontsize=8, **kwarg):
        """
        """
        Grid.PyGridCellRenderer.__init__(self)
        self.table = table
        self.color = color
        self.backgroundColor = wx.Colour(248, 248, 248)
        self.font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, font)
        self.selectedBrush = wx.Brush('blue', wx.SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.SOLID)
        self.colSize = None
        self.rowSize = 50
        self._colAttrTypes = {}
        # Дополнительные параметры
        self.kwarg = kwarg
        
    def SetColAttrTypes(self, dict):
        """
        Устанавливает типы значений аттрибутов.
        
        @type dict: C{dictionary}
        @param dict: Словарь типов атрибутов. Ключи идентификаторы типов, значения списки
            атрибутов. Пример: {1:['attr1','a2'], 2:['n']}.
        """
        
        # Преобразуем к более практичному виду - {имя атрибута: идентификатор типа}.
        self._colAttrTypes = {}
        
        for key in dict:
            for attr in dict[key]:
                self._colAttrTypes[attr] = key

    def GetColAttrType(self, attr):
        """
        Возвращает тип значения заданного аттрибута.
        """
        attr = attr.strip()
        if attr and attr in self._colAttrTypes:
            return self._colAttrTypes[attr]
        
        return None
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        В зависимости от типа ячейки отрисовываем значение.
        """
        attr = grid.GetTable().GetValue(row, 0)
        attr = attr.strip()
        attr_type = self.GetColAttrType(attr)

        cls = icDefInf.GetEditorClass(attr_type)
        if cls:
            cls.Draw(self, grid, attr, dc, rect, row, col, isSelected)
