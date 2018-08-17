#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовое приложение.
"""

import wx
from ic.imglib import common

__version__ = (0, 1, 1, 1)


class TestApp(wx.App):
    """
    Тестовое приложение.
    """

    def OnInit(self):
        """
        Обработчик инициализации приложения.
        """
        self.locale = wx.Locale()
        self.locale.Init(wx.LANGUAGE_RUSSIAN)

        common.img_init()
        return True


if __name__ == '__main__':
    app = TestApp(0)
    frame = wx.Frame(None, -1, u'Тест')
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()
