#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль приложения браузера отчетов.
"""

# Подключение библиотек

from ic import report
import ic.interfaces.designer as designer


class ReportBrowserDlg(icreportbrowser.icReportBrowserDialog, designer.icDesignDlg):
    """
    Браузер отчетов.
    """

    def __init__(self, Parent_, Node_=None):
        """
        Конструктор.
        @param Parent_: Родительское окно.
        """
        designer.icDesignDlg.__init__(self, Parent_, Node_)
        icreportbrowser.icReportBrowserDialog.__init__(self, Parent_,
                                                       icreportbrowser.IC_REPORT_EDITOR)

    def design(self):
        """
        Вызов браузера отчетов.
        """
        self.CenterOnScreen()
        self.ShowModal()
