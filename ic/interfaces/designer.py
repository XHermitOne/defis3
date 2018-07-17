#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Интерфейс для наших панелей редактирования в drPython.
"""

# Подключение библиотек
import wx


class icDesigner:
    """
    Интерфейс наших панелей для редактирования в drPython.
    """

    def __init__(self, Parent_=None, Node_=None, Resource_=None):
        """
        Конструтор.
        @param Parent_: Кодительское окно.
        @param Node_: Узел проекта, к которому прикреплен дизайнер.
        @param Resource_: Указание ресурса редактирования/Менеджера ресурса.
        """
        self._node = Node_
        self._parent = Parent_
        self._res = Resource_

    def design(self, Resource_=None):
        """
        Функция запуска дизайнера в drPython.
        """
        pass


class icDesignDlg(wx.Dialog):
    """
    Интерфейс наших диалоговых окон для редактирования в drPython.
    """

    def __init__(self,Parent_=None, Node_=None, Resource_=None):
        """
        Конструтор.
        @param Parent_: Родительское окно.
        @param Node_: Узел проекта, к которому прикреплен дизайнер.
        @param Resource_: Указание ресурса редактирования/Менеджера ресурса.
        """
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(Parent_, wx.NewId(), size=wx.Size(600, 400))

        self.PostCreate(pre)

        self._node = Node_

        self._parent = Parent_
        self._res = Resource_

        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def addPanel(self, Panel_):
        """
        Добавить панель в диалог/сайзер.
        """
        if Panel_:
            self.sizer.Add(Panel_, 1, wx.EXPAND | wx.GROW)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.Refresh()

    def design(self, Resource_=None):
        """
        Функция запуска дизайнера в drPython.
        """
        pass

    def getResource(self):
        """
        Ресурс.
        """
        return self._res
