#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Интерфейс визуального дизайнера компонентов.
"""

import wx


class icDesignerInterface(object):
    """
    Интерфейс визуального дизайнера компонентов.
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструтор.
        """
        pass

    @staticmethod
    def GetToolPanelCls():
        """
        Возвращает класс панели инструментов.
        """
        from ic.PropertyEditor import icstylepanel
        return icstylepanel.icStyleToolPanel
    
    def GetToolPanel(self, parent, *arg, **kwarg):
        """
        Возвращает панель инструментов.
        """
        cls = self.GetToolPanelCls()
        if cls:
            return cls(parent)
