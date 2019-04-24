#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол просмотра структуры SpreadSheet.
Контрол реализован на базе wx.Grid.
"""

import wx
import wx.grid

from ic.log import log

from ic.components import icwidget

from . import spreadsheet_proto

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_SPREADSHEETVIEWERCTRL = {'__parent__': icwidget.SPC_IC_WIDGET,
                                '__attr_hlp__': {},
                                }


class icSpreadSheetViewerCtrlProto(wx.grid.Grid,
                                   spreadsheet_proto.icSpreadSheetProto):
    """
    Контрол просмотра структуры SpreadSheet.
    Контрол реализован на базе wx.Grid.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.grid.Grid.__init__(self, *args, **kwargs)

        spreadsheet_proto.icSpreadSheetProto.__init__(self, grid=self)

