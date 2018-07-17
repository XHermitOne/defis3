#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Панель управления разрешениями на действие."""
import wx
from ic.kernel import io_prnt

class pe_Panel(wx.Panel):
    pass

def test(par=0):
    """Тестируем класс icButton."""
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, u'Test')
    #win = wx.Panel(frame, -1)
    win = pe_Panel(frame, -1)
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    """ Тестируем."""
    test(0)
