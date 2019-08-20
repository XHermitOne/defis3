#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса узла управления отчетами.
"""

# Подключение библиотек
import wx

from ic.imglib import common as imglib
from . import prj_node
from ic import report

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


class icPrjReports(prj_node.icPrjNode):
    """
    Отчеты.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjNode.__init__(self, parent)
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
