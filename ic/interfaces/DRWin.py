#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс для наших панелей редактирования в drPython.
"""


class DRWin:
    """
    Интерфейс наших панелей для редактирования в drPython.
    """

    def __init__(self, Parent_=None, DrFrame_=None, Position_=1, Index_=1):
        """
        Конструтор.
        @param Parent_: Родительское окно.
        @param DrFrame_: Главное окно drPython.
        """
        self._Parent = Parent_
        self._DrFrame = DrFrame_
        self.Position = Position_
        self.Index = Index_

        self.parent = Parent_.GetGrandParent().GetGrandParent()
        self.parent.PBind(self.parent.EVT_DRPY_DOCUMENT_CHANGED,
                          self.OnRefresh, None)

    def OnRefresh(self, event):
        """
        Обновление объекта.
        """
        self.Refresh()
        if event is not None:
            event.Skip()
