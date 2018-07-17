#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора календаря.
"""

import datetime
import wx
import wx.calendar

from ic.dlg.msgbox import MsgBox
from .icwidget import icWidget
from ic.utils import ic_time
from ic.log import log

from ic.dlg import calendar_dlg_proto


__version__ = (0, 0, 0, 2)

# Строковый формат даты по умолчанию
DEFAULT_DATE_FORMAT = '%Y.%m.%d'


class icCalendarDialog(icWidget, calendar_dlg_proto.icCalendarDialogProto):
    """
    Диалог для ввода дат. В качестве параметров передается дата, на которую будет установлен
        календарь. Если параметры даты не передаются, то установится текущая дата.
    """

    def __init__(self, parent, day=None, month=None, year=None):
        """
        Конструктор.
        @type parent: C{wxWindows}
        @param parent: Родительское окно.
        @type day: C{integer}
        @param day: День недели.
        @type month: C{integer}
        @param month: Месяц.
        @type year: C{integer}
        @param year: Год.
        """
        #
        icWidget.__init__(self, parent)
        calendar_dlg_proto.icCalendarDialogProto.__init__(self, parent)

        wx_date = wx.DateTime.Today()
        if day is not None:
            wx_date.SetDay(day)
        if month is not None:
            wx_date.SetMonth(month)
        if year is not None:
            wx_date.SetYear(year)

        self.calendar_control.SetDate(wx_date)

        self.result = None

    def onOkButtonClick(self, event):
        """
        Ок.
        """
        wx_date = self.calendar_control.GetDate()
        py_date = ic_time.wxdate2pydate(wx_date)
        self.result = py_date
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Отмена.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def getStrDate(self, date_format=DEFAULT_DATE_FORMAT):
        """
        Выбранная дата в строковом представлении.
        @param date_format: Формат даты.
        """
        return self.result.strftime(date_format)

    def getDateTime(self):
        """
        Выбранная дата.
        @return: Дата в формате datetime.datetime.
        """
        return datetime.datetime.combine(self.result,
                                         datetime.datetime.min.time())

    def getDate(self):
        """
        Выбранная дата.
        @return: Дата в формате datetime.date.
        """
        return self.result


def icInputDate(parent, day=None, month=None, year=None):
    """
    Функция позволяет вводить дату. В качестве параметров передается дата, на которую будет установлен
    календарь. Если параметры даты не передаются, то установится текщая дата.

    @type parent: C{wx.Windows}
    @param parent: Родительское окно.
    @type day: C{integer}
    @param day: День недели.
    @type month: C{integer}
    @param month: Месяц.
    @type year: C{integer}
    @param year: Год.
    @rtype: C{List}
    @return: Возвращает выбранную дату либо None.
    """
    if parent is None:
        MsgBox(None, u'Для данного отображения календаря необходимо родительское окно !')
        return None

    dlg = icCalendarDialog(parent, day, month, year)
    dlg.result = [day, month, year]

    dlg.CenterOnScreen()

    if dlg.ShowModal() == wx.ID_OK:
        str_date = dlg.getStrDate()
        return str_date
    else:
        log.warning(u'No Date Selected')

    return None


def test():
    """
    Тестовая функция.
    """
    app = wx.PySimpleApp()

    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1, u'Тестируем календарь')
    new_date = icInputDate(frame, 5, 11, 2017)

    log.debug(u'new_date = <%s>' % new_date)

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
