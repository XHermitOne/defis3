#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса узла управления отчетами.
"""

# Подключение библиотек
import wx
import ic.imglib.common as imglib
from . import prj_node
from ic import report

__version__ = (0, 0, 0, 3)

_ = wx.GetTranslation


class PrjReports(prj_node.PrjNode):
    """
    Отчеты.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, Parent_)
        self.img = imglib.imgEdtReports
        self.description = u'Отчеты'
        self.name = u'Отчеты'

        self.report_manager = report.REPORT_MANAGER

    def design(self):
        """
        Запуск дизайнера.
        """
        if self.report_manager:
            self.report_manager.design()

    def onNodeActivated(self, event):
        """
        Активация узла (двойной щелчок мыши на узле).
        """
        self.design()

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass
