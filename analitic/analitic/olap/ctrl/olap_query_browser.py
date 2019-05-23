#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Браузер результатов запросов к OLAP серверу.
"""

import wx

from . import olap_query_browse_panel_proto

from ic.log import log
from ic.engine import ic_user

from ic.engine import panel_manager
from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_OLAPQUERYBROWSER = {'__parent__': icwidget.SPC_IC_WIDGET,
                           '__attr_hlp__': {
                                            },
                           }


class icOLAPQueryBrowserProto(olap_query_browse_panel_proto.icOLAPQueryBrowsePanelProto,
                              panel_manager.icPanelManager):
    """
    Браузер результатов запросов к OLAP серверу.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        olap_query_browse_panel_proto.icOLAPQueryBrowsePanelProto.__init__(self, *args, **kwargs)

    def onCollapseToolClicked(self, event):
        """
        Обработчик кнопки СВЕРНУТЬ.
        """
        self.collapseSplitterPanel(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Обработчик кнопки РАЗВЕРНУТЬ.
        """
        self.expandSplitterPanel(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()


def show_olap_query_browser(parent=None, title=u'Аналитические отчеты', olap_server=None):
    """
    Функция просмотра браузера результатов запросов к OLAP серверу.
    @param parent: Родительское окно.
    @param title: Заголовок страницы браузера.
    @param olap_server: Объект OLAP сервера, отображаемого в браузере.
    @return: True/False.
    """
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        browser_panel = icOLAPQueryBrowserProto(parent=parent)
        browser_panel.query_treectrl.setOLAPServer(olap_server)

        ic_user.addMainNotebookPage(browser_panel, title)
        return True
    except:
        log.fatal(u'Ошибка просмотра браузера результатов запросов к OLAP серверу')
    return False
