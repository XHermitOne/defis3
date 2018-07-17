#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса AUI менеджера окон. Технология AUI.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import aui

__version__ = (0, 0, 1, 1)


class icAUIManager(aui.AuiManager):
    """
    Главное окно. Технология AUI.
    """

    def __init__(self, ManagedWindow_):
        """
        Конструктор.
        @param: ManagedWindow_: Окно, управляемое AUI менеджером.
        """
        aui.AuiManager.__init__(self)
        
        # Установить управляемое окно
        if ManagedWindow_:
            self.SetManagedWindow(ManagedWindow_)

    def setGradient(self, Gradient_):
        """
        Установка градиента заполнения AUI панелей.
        """
        return self.GetArtProvider().SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, Gradient_)

    def addPane(self,Pane_):
        """
        Добавить AUI панель.
        """
        # Заполнение информации о AUI панели
        pane_info = aui.AuiPaneInfo()
        pane_info = pane_info.Name(Pane_.name)
        pane_info = pane_info.Caption(Pane_.title or '')
        
        direction = Pane_.direction.lower().strip()
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
            
        pane_info = pane_info.Layer(Pane_.layer)
        pane_info = pane_info.Position(Pane_.pos)
        pane_info = pane_info.CloseButton(Pane_.close_button)
        pane_info = pane_info.MaximizeButton(Pane_.maximize_button)
        pane_info = pane_info.BestSize(wx.Size(*Pane_.best_size))
        pane_info = pane_info.MinSize(wx.Size(*Pane_.min_size))
        pane_info = pane_info.MaxSize(wx.Size(*Pane_.max_size))

        return self.AddPane(Pane_.getControl(), pane_info)

    def SetFlags(self, flags):
        if wx.VERSION > (2, 8, 11, 0):
            self.SetAGWFlags(flags)
        else:
            aui.AuiManager.SetFlags(self, flags)
