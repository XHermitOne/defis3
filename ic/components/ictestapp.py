#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Тестовое приложение.
"""

import wx
import ic.imglib.common as common


class TestApp(wx.App):
    
    def OnInit(self):
        self.locale = wx.Locale()
        self.locale.Init(wx.LANGUAGE_RUSSIAN)

        common.img_init()
        return True


if __name__ == '__main__':
    app = TestApp(0)
    frame = wx.Frame(None, -1, 'This is a test')
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()
