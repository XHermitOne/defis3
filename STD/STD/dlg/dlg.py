#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции стандартных диалогов прикладного уровня.
"""

import wx
import wx.lib.calendar

from . import iccalendardlg
from . import icyeardlg
from . import icmonthdlg
from . import icmonthrangedlg
from . import icdaterangedlg


def getDateDlg(parent=None):
    """
    Выбор даты в диалоговом окне календаря.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранную дату(datetime) или None если нажата <отмена>.
    """
    selected_date = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = iccalendardlg.icCalendarDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_date = dlg.getSelectedDateAsDatetime()
    dlg.Destroy()

    return selected_date


def getYearDlg(parent=None):
    """
    Выбор года в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранный год (datetime) или None если нажата <отмена>.
    """
    selected_year = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icyeardlg.icYearDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_year = dlg.getSelectedYearAsDatetime()
    dlg.Destroy()

    return selected_year


def getMonthDlg(parent=None):
    """
    Выбор месяца в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранный месяц (datetime) или None если нажата <отмена>.
    """
    selected_month = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthdlg.icMonthDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_month = dlg.getSelectedMonthAsDatetime()
    dlg.Destroy()

    return selected_month


def getMonthRangeDlg(parent=None):
    """
    Выбор периода по месяцам в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Кортеж периода по месяцам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthrangedlg.icMonthRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedMonthRangeAsDatetime()
    dlg.Destroy()

    return selected_range


def getDateRangeDlg(parent=None):
    """
    Выбор периода по датам в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Кортеж периода по датам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icdaterangedlg.icDateRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedDateRangeAsDatetime()
    dlg.Destroy()

    return selected_range


def test():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()
    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    print(getDateDlg(frame))

    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
