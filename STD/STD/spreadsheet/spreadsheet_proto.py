#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Общий менеджер управления структурой SpreadSheet.
"""

from ic.log import log

from ic.components import icwidget

from . import spreadsheet_view_manager

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_SPREADSHEET = {'viewer': None,   # wx.Grid для отображения
                      '__parent__': icwidget.SPC_IC_SIMPLE,
                      '__attr_hlp__': {'viewer': u'wx.Grid для отображения',
                                       },
                      }


class icSpreadSheetProto(spreadsheet_view_manager.icSpreadSheetViewManager):
    """
    Общий менеджер управления структурой SpreadSheet.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        spreadsheet_view_manager.icSpreadSheetViewManager.__init__(self, *args, **kwargs)
