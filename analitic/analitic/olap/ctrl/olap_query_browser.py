#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Браузер результатов запросов к OLAP серверу.
"""

from . import olap_query_browse_panel_proto

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
