#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора месяца.
"""

import datetime
import wx
from . import std_dialogs_proto


class icMonthDialog(std_dialogs_proto.monthDialogProto):
    """
    Диалоговое окно выбора месяца.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.monthDialogProto.__init__(self, *args, **kwargs)

        self._selected_month = None

    def getSelectedMonth(self):
        return self._selected_month

    def getSelectedMonthAsDatetime(self):
        if self._selected_month:
            return datetime.datetime(year=self._selected_month[0], month=self._selected_month[1], day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_month = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_month = (self.yearChoiceControl.get_selected_year(),
                                self.monthChoiceControl.get_selected_month_num())
        self.EndModal(wx.ID_OK)
        event.Skip()


def test():
    """
    Тестирование.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)

    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    dlg = icMonthDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
