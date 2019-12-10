#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания класса AUI менеджера окон. Технология AUI.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import aui

__version__ = (0, 1, 1, 1)


class icAUIManager(aui.AuiManager):
    """
    Главное окно. Технология AUI.
    """

    def __init__(self, managed_window):
        """
        Конструктор.

        :param: managed_window: Окно, управляемое AUI менеджером.
        """
        aui.AuiManager.__init__(self)
        
        # Установить управляемое окно
        if managed_window:
            self.SetManagedWindow(managed_window)

    def setGradient(self, gradient):
        """
        Установка градиента заполнения AUI панелей.
        """
        return self.GetArtProvider().SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, gradient)

    def addPane(self, pane):
        """
        Добавить AUI панель.
        """
        # Заполнение информации о AUI панели
        pane_info = aui.AuiPaneInfo()
        pane_info = pane_info.Name(pane.name)
        pane_info = pane_info.Caption(pane.title or '')
        
        direction = pane.direction.lower().strip()
        if direction == 'left':
            pane_info = pane_info.Left()
        elif direction == 'right':
            pane_info = pane_info.Right()
        elif direction == 'top':
            pane_info = pane_info.Top()
        elif direction == 'bottom':
            pane_info = pane_info.Bottom()
        elif direction == 'center':
            pane_info = pane_info.Center()
            
        pane_info = pane_info.Layer(pane.layer)
        pane_info = pane_info.Position(pane.pos)
        pane_info = pane_info.CloseButton(pane.close_button)
        pane_info = pane_info.MaximizeButton(pane.maximize_button)
        pane_info = pane_info.BestSize(wx.Size(*pane.best_size))
        pane_info = pane_info.MinSize(wx.Size(*pane.min_size))
        pane_info = pane_info.MaxSize(wx.Size(*pane.max_size))

        return self.AddPane(pane.getControl(), pane_info)

    def SetFlags(self, flags):
        if wx.VERSION > (2, 8, 11, 0):
            self.SetAGWFlags(flags)
        else:
            aui.AuiManager.SetFlags(self, flags)
