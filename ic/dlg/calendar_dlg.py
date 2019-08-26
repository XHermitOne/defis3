#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя работы с датами.
"""

# --- Подключение пакетов ---
import wx
from ic.utils import datetimefunc
from ic.components import iccalendar

__version__ = (0, 1, 1, 1)


def openCalendarDlg(parent=None, date_fmt=datetimefunc.DEFAULT_DATETIME_FMT):
    """
    Диалоговое окно календаря.
    @param parent: Родительское окно.
    @param date_fmt: Формат дыты.
    @return: Возвращает строку выбранной даты в указанном формате или 
        пустую строку, если дата не выбрана.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = iccalendar.icCalendarDialog(parent)
        if dlg.ShowModal() == wx.ID_OK:
            py_date = dlg.getDate()
            result = datetimefunc.convertDateTimeFmt(py_date, datetimefunc.DEFAULT_DATETIME_FMT, date_fmt)
        else:
            result = ''
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()
    return result


def getDateDlg(parent=None):
    """
    Диалоговое окно календаря.
    @param parent: Родительское окно.
    @return: Возвращает выбранную дату datetime.date.
        Или None, если нажата <Отмена>.
    """
    result = None
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = iccalendar.icCalendarDialog(parent)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getDate()
        else:
            result = None
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()
    return result
