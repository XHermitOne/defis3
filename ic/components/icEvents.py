#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обработчики событий используемые библиотекой ic.
"""

import wx

__version__ = (0, 0, 0, 4)

#   *** Идентификаторы для события icKeyDownEvent ***
icEVT_KEY_DOWN_IC = wx.NewEventType()
EVT_KEY_DOWN_IC = wx.PyEventBinder(icEVT_KEY_DOWN_IC, 1)


class icKeyDownEvent(wx.PyCommandEvent):
    """ 
    Класс события нажатия кнопки. Используется для передачи сообщения главному окну
    формы.
    """
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        #   Пользовательские данные
        self.data = None
        #   Указатель на объект возбудивший событие
        self._icobject = None
        #   Указатель на сообщение, по которому было инициировано текущее
        self._key_event = None
        
    def SetKeyEvt(self, evt):
        self._key_event = evt

    def GetKeyEvt(self):
        return self._key_event
        
    def SetICObject(self, obj):
        self._icobject = obj

    def GetICObject(self):
        return self._icobject
        
    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

#   *** Идентификаторы для события icGridDestroyEvent ***
icEVT_GRID_DESTROY = wx.NewEventType()
EVT_GRID_DESTROY = wx.PyEventBinder(icEVT_GRID_DESTROY)


class icGridDestroyEvent(wx.PyEvent):
    """ 
    Используется для передачи сообщения гриду о том, что ему пора разрушаться.
    """

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

#   *** Идентификаторы для события icDestroyEvent ***
icEVT_DLG_PREDESTROY = wx.NewEventType()
EVT_DLG_PREDESTROY = wx.PyEventBinder(icEVT_DLG_PREDESTROY)


class icDlgPreDestroyEvent(wx.PyEvent):
    """ 
    Используется для разрушения диалогов.
    """

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

#   *** Идентификаторы для события icDestroyEvent ***
icEVT_TEXT_TEMPL = wx.NewEventType()
EVT_TEXT_TEMPL = wx.PyEventBinder(icEVT_TEXT_TEMPL)


class icTextTemplEvent(wx.PyEvent):
    """
    """
    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

#   Сообщение для автоматического заполнения текста
icEVT_AUTO_TEXT_FILL = wx.NewEventType()
EVT_AUTO_TEXT_FILL = wx.PyEventBinder(icEVT_AUTO_TEXT_FILL)


class icAutoTextFillEvent(wx.PyEvent):

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

#   Сообщение post_select для грида
icEVT_GRID_POST_SELECT = wx.NewEventType()
EVT_GRID_POST_SELECT = wx.PyEventBinder(icEVT_GRID_POST_SELECT)


class icGridPostSelectEvent(wx.PyEvent):
    """
    """

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

#   Сообщение, которое приходит после инициализации визуального компонента
icEVT_POST_INIT = wx.NewEventType()
EVT_POST_INIT = wx.PyEventBinder(icEVT_POST_INIT)


class icPostInitEvent(wx.PyEvent):
    """
    """

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None

    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

#   Сообщение, на изменение надписи визуального компонента
icEVT_LABEL_CHANGE = wx.NewEventType()
EVT_LABEL_CHANGE = wx.PyEventBinder(icEVT_LABEL_CHANGE)


class icLabelChangeEvent(wx.PyEvent):
    """
    Сообщение, на изменение надписи визуального компонента.
    """

    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, id, evtType)
        #   Пользовательские данные
        self.id = id
        self.data = None
        
        #   Указатель на объект возбудивший событие
        self._icobject = None

    def SetData(self, val):
        self.data = val

    def GetData(self):
        return self.data

    def SetICObject(self, obj):
        self._icobject = obj

    def GetICObject(self):
        return self._icobject
