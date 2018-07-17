#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса контроллера ввода/редактирования даты+времени.
"""

import datetime
import wx
from . import std_controls_proto
from ic.utils import ic_time

__version__ = (0, 0, 1, 2)


DEFAULT_MIN_YEAR = datetime.MINYEAR
DEFAULT_MIN_MONTH = 1
DEFAULT_MIN_DAY = 1

DEFAULT_DATE_VALUE = ic_time.pydate2wxdate(datetime.datetime(DEFAULT_MIN_YEAR,
                                           DEFAULT_MIN_MONTH, DEFAULT_MIN_DAY))

TODAY_DATE_VALUE = ic_time.pydate2wxdate(datetime.date.today())

DEFAULT_TIME_VALUE = dict(hour=0, minute=0, second=0)


class icDateTimeControl(std_controls_proto.icDateTimeCtrlProto):
    """
    Контроллер ввода/редактирования даты+времени.
    """

    def __init__(self, parent=None, id=-1, date_time=None, *args, **kwargs):
        """
        Конструктор.
        @param parent: Родительское окно wx.Window.
        @param id: wx идентификатор объекта.
        @param date_time: Дата+время (datetime) для инициализации контрола.
            Если None, то инициализируется пустыми значениями.
        """
        # Текущее отредактированное значение
        self._dt = date_time
        self._wx_dt = None

        std_controls_proto.icDateTimeCtrlProto.__init__(self, parent=parent)

        self.h_spinBtn.SetMin(0)
        self.h_spinBtn.SetMax(23)
        self.m_spinBtn.SetMin(0)
        self.m_spinBtn.SetMax(59)
        self.s_spinBtn.SetMin(0)
        self.s_spinBtn.SetMax(59)

    def isDateValid(self):
        date_value = self.dateEdit.GetValue()
        return date_value and date_value.IsValid()

    def isTimeValid(self):
        """
        Т.к. у нас 3 контрола wx.SpinCtrl с ограничением
            ввода, то считаем что время не возможно
            ввести ошибочно.
        """
        return True

    def getWXDateTime(self):
        """
        Получить данные в виде wx.DateTime.
        @return: Данные возвращаются в виде <wx.DateTime>.
        """
        self._wx_dt = self._getCtrlWXDateTime()
        return self._wx_dt

    def _getCtrlWXDateTime(self):
        """
        Получить данные с контролов.
        @return: Данные возвращаются в виде wx.DateTime.
        """
        date_valid = self.isDateValid()
        time_valid = self.isTimeValid()

        if date_valid and time_valid:
            # И дата и время введены корректно
            lst_time = self._getCtrlTimeTuple()
            wx_datetime = self.dateEdit.GetValue()
            wx_datetime.SetHour(lst_time[0])
            wx_datetime.SetMinute(lst_time[1])
            wx_datetime.SetSecond(lst_time[2])
            return wx_datetime
        elif not date_valid and time_valid:
            # Дата не корректна а время корректно
            lst_time = self._getCtrlTimeTuple()
            return wx.DateTimeFromHMS(lst_time[0],
                                      lst_time[1],
                                      lst_time[2])
        elif date_valid and not time_valid:
            # Дата корректна а время не корректно
            return self.dateEdit.GetValue()
        else:
            # Ничего не корректно
            return None

    def isDTNone(self, dt):
        """
        Проверка на не определенной значение.
        @param dt: Дата время <datetime>ю
        @return: True/False.
        """
        # Если минимальный год, то это явно не определенный дата-время
        return self._dt.year == datetime.MINYEAR

    def getDateTime(self):
        """
        Получить данные в виде datetime.
        @return: Данные возвращаются в виде Python <datetime>.
        """
        self._dt = self._getCtrlDateTime()
        if self.isDTNone(self._dt):
            return None
        return self._dt

    getValue = getDateTime

    def _getCtrlTimeTuple(self):
        """
        Получить данные с контролов времени в формате кортежа.
        """
        hour = self.h_spinBtn.GetValue()
        minute = self.m_spinBtn.GetValue()
        second = self.s_spinBtn.GetValue()
        return hour, minute, second

    def _setCtrlTime(self, hour=0, minute=0, second=0):
        """
        Установить данные в контролы времени в формате кортежа.
        @param hour: Час.
        @param minute: Минуты.
        @param second: Секунды.
        """
        h_value = min(max(hour, 0), 23)
        self.h_spinBtn.SetValue(h_value)
        self.h_textCtrl.SetValue('%02d' % h_value)
        m_value = min(max(minute, 0), 59)
        self.m_spinBtn.SetValue(m_value)
        self.m_textCtrl.SetValue('%02d' % m_value)
        s_value = min(max(second, 0), 59)
        self.s_spinBtn.SetValue(s_value)
        self.s_textCtrl.SetValue('%02d' % s_value)

    def _getCtrlDateTime(self):
        """
        Получить данные с контролов.
        @return: Данные возвращаются в виде Python <datetime>.
        """
        dt = None
        date_valid = self.isDateValid()
        time_valid = self.isTimeValid()

        if date_valid and time_valid:
            # И дата и время введены корректно
            dt = ic_time.wxdatetime2pydatetime(self._getCtrlWXDateTime())
        elif not date_valid and time_valid:
            # Дата не корректна а время корректно
            lst_time = self._getCtrlTimeTuple()
            dt = datetime.datetime(year=DEFAULT_MIN_YEAR,
                                   month=DEFAULT_MIN_MONTH,
                                   day=DEFAULT_MIN_DAY,
                                   hour=lst_time[0],
                                   minute=lst_time[1],
                                   second=lst_time[2])
        elif date_valid and not time_valid:
            # Дата корректна а время не корректно
            dt = ic_time.wxdatetime2pydatetime(self.dateEdit.GetValue())
        return dt

    def setDateTime(self, dt):
        """
        Установить данные в виде datetime.
        @return: Данные возвращаются в виде Python <datetime>.
        """
        if dt is None:
            self._dt = None
            self.dateEdit.SetValue(DEFAULT_DATE_VALUE)
            self._setCtrlTime(**DEFAULT_TIME_VALUE)
        else:
            assert isinstance(dt, (datetime.datetime, datetime.date))
            self._dt = dt
            self._setCtrlDateTime(self._dt)

    setValue = setDateTime

    def _setCtrlDateTime(self, dt):
        """
        Установить данные в контролы.
        """
        assert isinstance(dt, (datetime.datetime, datetime.date))

        wx_date = ic_time.pydate2wxdate(dt)
        str_time = dt.strftime(ic_time.DEFAULT_TIME_FMT)
        if wx_date.IsValid():
            self.dateEdit.SetValue(wx_date)
        lst_time = str_time.split(':')
        self._setCtrlTime(hour=int(lst_time[0]),
                          minute=int(lst_time[1]),
                          second=int(lst_time[0]))

    # Блок методов-обработчиков для организации ввода времени
    def onHSpin(self, event):
        """
        Изменение значения часа.
        """
        i_value = event.GetPosition()
        value = '%02d' % i_value if i_value < 10 else str(i_value)
        self.h_textCtrl.SetValue(value)
        event.Skip()

    def onHText(self, event):
        """
        Изменение значения часа.
        """
        txt_value = event.GetString().strip()[:2]
        i_value = min(max(int(txt_value), 0), 23) if txt_value.isdigit() else self.h_spinBtn.GetValue()
        value = '%02d' % i_value
        self.h_textCtrl.SetValue(value)
        self.h_spinBtn.SetValue(i_value)
        event.Skip()

    def onMSpin(self, event):
        """
        Изменение значения минут.
        """
        i_value = event.GetPosition()
        value = '%02d' % i_value if i_value < 10 else str(i_value)
        self.m_textCtrl.SetValue(value)
        event.Skip()

    def onMText(self, event):
        """
        Изменение значения минут.
        """
        txt_value = event.GetString().strip()[:2]
        i_value = min(max(int(txt_value), 0), 59) if txt_value.isdigit() else self.m_spinBtn.GetValue()
        value = '%02d' % i_value
        self.m_textCtrl.SetValue(value)
        self.m_spinBtn.SetValue(i_value)
        event.Skip()

    def onSSpin(self, event):
        """
        Изменение значения секунд.
        """
        i_value = event.GetPosition()
        value = '%02d' % i_value if i_value < 10 else str(i_value)
        self.s_textCtrl.SetValue(value)
        event.Skip()

    def onSText(self, event):
        """
        Изменение значения секунд.
        """
        txt_value = event.GetString().strip()[:2]
        i_value = min(max(int(txt_value), 0), 59) if txt_value.isdigit() else self.s_spinBtn.GetValue()
        value = '%02d' % i_value
        self.s_textCtrl.SetValue(value)
        self.s_spinBtn.SetValue(i_value)
        event.Skip()


def test():
    """
    Тестирование контрола.
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1)

    ctrl = icDateTimeControl(parent=frame)

    btn = wx.Button(parent=frame, pos=wx.Point(100, 100), label=u'Тест')

    def on_btn(event):
        print('TEST:', ctrl.getDateTime().strftime('%Y.%m.%d %H:%M:%S'))
        event.Skip()

    btn.Bind(wx.EVT_BUTTON, on_btn)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
