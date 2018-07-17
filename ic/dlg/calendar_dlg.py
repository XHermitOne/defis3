#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя работы с датами.
"""

# --- Подключение пакетов ---
import wx
from ic.utils import ic_time
from ic.components import iccalendar

# --- ДИАЛОГОВЫЕ ФУНКЦИИ ----


def icCalendarDlg(Parent_=None, DateFmt_=ic_time.DEFAULT_DATETIME_FMT):
    """
    Диалоговое окно календаря.
    @param Parent_: Родительское окно.
    @param DateFmt_: Формат дыты.
    @return: Возвращает строку выбранной даты в указанном формате или 
    пустую строку, если дата не выбрана.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = iccalendar.icCalendarDialog(Parent_)
        if dlg.ShowModal() == wx.ID_OK:
            py_date = dlg.getDate()
            result = ic_time.convertDateTimeFmt(py_date,
                                                ic_time.DEFAULT_DATETIME_FMT, DateFmt_)
        else:
            result = ''
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Parent_.Destroy()
    return result


def getDateDlg(Parent_=None):
    """
    Диалоговое окно календаря.
    @param Parent_: Родительское окно.
    @return: Возвращает выбранную дату datetime.date.
        Или None, если нажата <Отмена>.
    """
    result = None
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = iccalendar.icCalendarDialog(Parent_)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getDate()
        else:
            result = None
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Parent_.Destroy()
    return result
