#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительные функции работы с wx объектами.
"""

import wx

from ic.log import log

__version__ = (0, 1, 1, 1)


def is_same_wx_object(wx_obj1, wx_obj2):
    """
    Проверка на тот же самый объект wx.
    @param wx_obj1: Первый сравниваемый wx объект.
    @param wx_obj2: Второй сравниваемый wx объект.
    @return: Если это тот же самый объект, то возвращается True иначе False.
    """
    if issubclass(wx_obj1.__class__, wx.Object) and issubclass(wx_obj2.__class__, wx.Object):
        # Сравнение наследников wx.Object
        return wx_obj1.IsSameAs(wx_obj2)
    elif 'Swig' in wx_obj1.__str__() and 'Swig' in wx_obj2.__str__():
        # Не все классы wxPython наследуются от wx.Object
        # Поэтому просто проверяем строковое представление объектов
        return wx_obj1.__str__() == wx_obj2.__str__()
    # Ничего не получилось
    # просто проверяем объекты как питоновские
    return wx_obj1 == wx_obj2


def is_wx_object_in_list(wx_obj, wx_obj_list):
    """
    Проверка есть ли wx объект в списке.
    @param wx_obj: wx Объект.
    @param wx_obj_list: Список каких либо объектов.
    @return: True/False.
    """
    return bool([obj for obj in wx_obj_list if is_same_wx_object(wx_obj, obj)])


def get_index_wx_object_in_list(wx_obj, wx_obj_list):
    """
    Получить индекс wx объекта в списке.
    @param wx_obj: wx Объект.
    @param wx_obj_list: Список каких либо объектов.
    @return: Индекс объекта в списке, если он в нем присутствует
        или -1 если он не присутствует.
    """
    for i, obj in enumerate(wx_obj_list):
        if is_same_wx_object(wx_obj, obj):
            return i
    return -1


def isWxDeadObject(wx_object):
    """
    Проверка является ли объект WX удаленным/разрушенным методом Destroy.
    @param wx_object: WX объект.
    @return: True/False.
    """
    return not wx_object  # avoid a PyDeadObject error


def wxColour2StrHex(colour):
    """
    Цвет wxColour в виде строки #RRGGBB.
    @param colour: Цвет wx.Colour.
    @return: Строка #RRGGBB соответствующая цвету.    
    """
    return colour.GetAsString(wx.C2S_HTML_SYNTAX)


def getWxPythonMajorVersion():
    """
    Мажорная версия wxPython.
    """
    return wx.MAJOR_VERSION


def getWxPythonMinorVersion():
    """
    Минорная версия wxPython.
    """
    return wx.MINOR_VERSION


def isWxPython4():
    """
    Проверка на wxPython версии 4 и выше.
    @return: True - wxPython версии 4 и выше / False - другая версия wxPython.
    """
    return wx.MAJOR_VERSION >= 4


def showInfoWindow(parent=None, ctrl=None, x=-1, y=-1, info_text=u'',
                   backgroundColour=None):
    """
    Отобразить текст информации в всплывающем окне.
    @param parent: Родительское окно для отображения всплыващего окна.
    @param ctrl: Контрол, к которому приклеплено всплывающее окно.
    @param x: Координата X вывода всплывающего окна.
        Если не определено, то берется левая граница контрола.
    @param y: Координата Y вывода всплывающего окна.
        Если не определено, то берется нижняя граница контрола.
    @param info_text: Текст информационного сообщения.
    @param backgroundColour: Цвет фона окна.
        Если не определен, то берется 'CADET BLUE'.
    @return: Функция возвращает созданное всплывающее окно
        или None в случае ошибки.
    """
    try:
        if ctrl:
            x_offset, y_offset = ctrl.ClientToScreen((0, 0))
            if x <= 0:
                x = x_offset
            if y <= 0:
                y = y_offset

        if x <= 0:
            x = 0
        if y <= 0:
            y = 0

        if parent is None:
            parent = wx.GetApp().GetTopWindow()

        popup_win = wx.PopupWindow(parent, wx.SIMPLE_BORDER)
        panel = wx.Panel(popup_win)
        panel.SetBackgroundColour('CADET BLUE')

        static_txt = wx.StaticText(panel, -1, info_text, pos=(10, 10))

        size = static_txt.GetBestSize()
        popup_win.SetSize((size.width + 20, size.height + 20))
        panel.SetSize((size.width + 20, size.height + 20))

        height = ctrl.GetSize().height if ctrl else 0
        popup_win.Position(wx.Point(x, y), (0, height))
        popup_win.Show()
        return popup_win
    except:
        log.fatal(u'Ошибка отображения информационного всплывающего окна')
    return None


def isCreateApp():
    """
    Проверка создали объект приложения WX.
    @return: True - Да объект приложения создан / False - Нет.
    """
    app = wx.GetApp()
    return app is not None
