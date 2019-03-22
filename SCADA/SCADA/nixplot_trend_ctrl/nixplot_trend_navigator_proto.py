#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель навигации тренда на базе утилиты nixplot.
Абстрактный класс.
"""

import wx

from ic.log import log

from . import nixplot_trend_navigator_panel_proto

# --- Спецификация ---
SPC_IC_NIXPLOT_TREND_NAVIGATOR = {
                                  }

__version__ = (0, 1, 1, 1)


class icNixplotTrendNavigatorProto(nixplot_trend_navigator_panel_proto.icNixPlotTrendNavigatorPanelProto):
    """
    Панель навигации тренда на базе утилиты nixplot.
    Абстрактный класс.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        nixplot_trend_navigator_panel_proto.icNixPlotTrendNavigatorPanelProto.__init__(self, *args, **kwargs)


def test():
    """
    Тестовая функция.
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    frame = wx.Frame(None, title='My Data')
    panel = icNixplotTrendNavigatorProto(frame)
    panel.trend.draw()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
