#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол конструктора стелажа.
"""

import os
import os.path
import wx

from ic.bitmap import ic_bmp
from ic.log import log

__version__ = (0, 0, 0, 1)


class icWMSRackContructorCtrl(wx.StaticBitmap):
    """
    Контрол конструктора стелажа.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.StaticBitmap.__init__(self, *args, **kwargs)

        # self.Bind(wx.EVT_PAINT, self.onPaint)

    def setBackgound(self, bmp=None):
        """
        Установить фон.
        @param bmp: Объект wx.Bitmap фона.
            Может задаваться именем файла картинки.
        """
        if isinstance(bmp, str):
            log.debug(u'Фон задается именем файла <%s>' % bmp)
            # Картинка задается именем файла
            if os.path.exists(bmp):
                bmp = ic_bmp.createBitmap(bmp)
            else:
                # Возможно картинка задается именем файла из библиотеки
                bmp = ic_bmp.createLibraryBitmap(bmp)
        self.SetBitmap(bmp)

    # def draw(self, dc):
    #     """
    #     Отрисовка состояния стелажа.
    #     @param dc: Контекст устройства контрола.
    #     """
    #     if self.bg_bmp:
    #         dc.DrawBitmap(self.bg_bmp, 0, 0)
    #
    # def onPaint(self, event):
    #     """
    #     Обработчик отрисовки контрола.
    #     """
    #     dc = wx.ClientDC(self)
    #     self.draw(dc)
    #
    #     #event.Skip()
