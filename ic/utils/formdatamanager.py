#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер заполнения/чтения данных формы.
ВНИМАНИЕ! Данные заполняются ассоциативно,
поэтому могут заполняться не полностью.
Отлаживаться необходимо по логу.
В логе отображается с объектом какого типа выполняются действия
и какой функцией устанавливаются/читаются данные.
"""

import wx
import datetime

from ic.components import icwidget
from ic.kernel import io_prnt
from ic.utils import ic_str
from ic.utils import ic_time
from . import frequencydict


__version__ = (1, 0, 1, 2)


class icFormDataManager(object):
    """
    Менеджер заполнения/чтения данных формы.
    """
    def __init__(self, form=None):
        """
        Конструктор.
        @param form: Форма с контролами, отражающими данные.
            Если None то считается что форма наследуется от
            icFormDataManager и в данном случае берется self.
        """
        self.__form = form
        if self.__form is None:
            self.__form = self

        # Частотный словарь автоматического заполнения вводимого текста
        frequencydict_name = str(self.__form.name) if hasattr(self.__form, 'name') else frequencydict.DEFAULT_FREQUENCYDICT_NAME
        self.autocomplit = frequencydict.icFrequencyDict(frequencydict_name)

    def findControlByName(self, name):
        """
        Определить контрол по его имени.
        @param name: Имя контрола.
        @return: Объект контрола формы или None в случае
            когда контрол не найден.
        """
        if self.__form is None:
            io_prnt.outWarning(u'Не определена форма заполнения/чтения данных')
            return None

        ctrl = None

        if hasattr(self.__form, name):
            ctrl = getattr(self.__form, name)
        if ctrl is None and isinstance(self.__form, icwidget.icWidget):
            ctrl = self.__form.FindObjectByName(name)
        if ctrl is None:
            ctrl = self.__form.FindWindowByName(name)

        if ctrl is None:
            io_prnt.outWarning(u'Контрол <%s> в форме данных не найден' % name)
        return ctrl

    def setControlValue(self, ctrl, value):
        """
        Установить значение в найденный контрол.
        @param ctrl: Контрол.
        @param value: Значение кoнтрола.
        @return: True/False.
        """
        result = False
        if hasattr(ctrl, 'setData'):
            # Обработка методом setData
            try:
                io_prnt.outLog(u'Заполнение данных объекта <%s> методом setData.' % ctrl.__class__.__name__)
                ctrl.setData(value)
                result = True
            except:
                io_prnt.outErr(u'Ошибка заполнения данных объекта <%s> методом setData. Значение <%s : %s>' % (ctrl.__class__.__name__, type(value), value))
                result = False
        elif hasattr(ctrl, 'setValue'):
            # Обработка методом setValue
            try:
                io_prnt.outLog(u'Заполнение данных объекта <%s> методом setValue.' % ctrl.__class__.__name__)
                ctrl.setValue(value)
                result = True
            except:
                io_prnt.outErr(u'Ошибка заполнения данных объекта <%s> методом setValue. Значение <%s : %s>' % (ctrl.__class__.__name__, type(value), value))
                result = False
        elif hasattr(ctrl, 'SetValue'):
            # Обработка методом SetValue
            try:
                if isinstance(ctrl, wx.DatePickerCtrl):
                    # Преобразование типа для wxDatePickerCtrl
                    if isinstance(value, datetime.date):
                        value = ic_time.pydate2wxdate(value)
                    elif isinstance(value, datetime.datetime):
                        value = ic_time.pydatetime2wxdatetime(value)
                io_prnt.outLog(u'Заполнение данных объекта <%s> методом SetValue.' % ctrl.__class__.__name__)
                ctrl.SetValue(value)
                result = True
            except:
                io_prnt.outErr(u'Ошибка заполнения данных объекта <%s> методом SetValue. Значение <%s : %s>' % (ctrl.__class__.__name__, type(value), value))
                result = False
        elif hasattr(ctrl, 'SetLabel'):
            # Обработка методом SetValue (Только для объектов wxStaticText)
            try:
                io_prnt.outLog(u'Заполнение данных объекта <%s> методом SetLabel.' % ctrl.__class__.__name__)
                value = ic_str.toUnicode(value)
                ctrl.SetLabel(value)
                result = True
            except:
                io_prnt.outErr(u'Ошибка заполнения данных объекта <%s> методом SetLabel. Значение <%s : %s>' % (ctrl.__class__.__name__, type(value), value))
                result = False
        else:
            io_prnt.outWarning(u'Не определен метод заполнения данных объекта <%s>' % ctrl.__class__.__name__)
        return result

    def setData(self, data):
        """
        Установить данные в форму.
        @param data: Словарь данных формы.
        @return: True/False.
        """
        if data is None:
            io_prnt.outWarning(u'Не определен словарь данных формы')
            return False

        # Контроль типа входного значения
        # д.б. словарь обязательно
        assert isinstance(data, (dict,))

        result = True
        for ctrl_name, value in data.items():
            ctrl = self.findControlByName(ctrl_name)
            if ctrl is not None:
                result = result and self.setControlValue(ctrl, value)
        return result

    def getAllChildren(self, form=None):
        """
        Получить список всех контролов формы.
        @param form: Форма. Если не определен, то берется self.__form
        @return: Словарь контролов. { 'имя контрола': объект контрола}.
        """
        if form is None:
            form = self.__form

        children = dict()
        children_names = dir(form)
        for child_name in children_names:
            child = getattr(form, child_name)
            if isinstance(child, wx.Window):
                children[child_name] = child
        return children

    def getControlValue(self, ctrl):
        """
        Прочитать значение контрола.
        @param ctrl: Контрол.
        @return: Значение в любом виде.
        """
        value = None

        if ctrl == self:
            # ВНИМАНИЕ! компонент может ссылаться сам на себя
            # Без этой проверки может быть постоянная реккурсия
            return None

        if hasattr(ctrl, 'getData'):
            # Обработка методом getData
            try:
                value = ctrl.getData()
                io_prnt.outLog(u'Получение данных объекта <%s> методом getData.' % ctrl.__class__.__name__)
            except:
                io_prnt.outErr(u'Ошибка получения данных объекта <%s> методом getData.' % ctrl.__class__.__name__)
                value = None
        elif hasattr(ctrl, 'getValue'):
            # Обработка методом getValue
            try:
                value = ctrl.getValue()
                io_prnt.outLog(u'Получение данных объекта <%s> методом getValue.' % ctrl.__class__.__name__)
            except:
                io_prnt.outErr(u'Ошибка получения данных объекта <%s> методом getValue.' % ctrl.__class__.__name__)
                value = None
        elif hasattr(ctrl, 'GetValue'):
            # Обработка методом GetValue
            try:
                value = ctrl.GetValue()
                io_prnt.outLog(u'Получение данных объекта <%s> методом GetValue.' % ctrl.__class__.__name__)
            except:
                io_prnt.outErr(u'Ошибка получения данных объекта <%s> методом GetValue.' % ctrl.__class__.__name__)
                value = None
        elif hasattr(ctrl, 'GetLabel'):
            # Обработка методом SetValue (Только для объектов wxStaticText)
            try:
                value = ctrl.GetLabel()
                io_prnt.outLog(u'Получение данных объекта <%s> методом GetLabel.' % ctrl.__class__.__name__)
            except:
                io_prnt.outErr(u'Ошибка получения данных объекта <%s> методом GetLabel.' % ctrl.__class__.__name__)
                value = None
        else:
            io_prnt.outWarning(u'Не определен метод получения данных объекта <%s>' % ctrl.__class__.__name__)
        return value

    def getData(self, *name_filter):
        """
        Прочитать данные из формы.
        @param name_filter: Список имен контролов,
            значения которых надо прочитать.
            Если не определен, то берется весь список имен формы.
        @return: Словарь данных формы {'имя контрола': значение}.
            Или None в случае ошибки.
        """
        data = dict()

        children_dict = self.getAllChildren()
        for ctrl_name, ctrl in children_dict.items():
            if (not name_filter) or (name_filter and ctrl_name in name_filter):
                if ctrl is not None:
                    value = self.getControlValue(ctrl)
                    data[ctrl_name] = value
        return data
