#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль прикладной системы.
Автор(ы):
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Функции
import wx
from ic.dlg import dlgfunc

def getSQLTest():
    """
    Определение SQL запроса для тестового отчета.
    """
    print('getSQLTest')
    if dlgfunc.getAskDlg('ЛаЛаЛа', '?')==wx.YES:
        return 'SQL SELECT * FROM nsi_list'
    else:
        return 'SQL SELECT * FROM nsi_std'
