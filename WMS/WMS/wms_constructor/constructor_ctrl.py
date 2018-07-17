#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Различные конструкторы WMS.
"""

import os
import os.path
import wx

from ic.log import log

from . import wms_shape
from . import rack_constructor
from . import tier_constructor
from . import layout_scheme

DEFAULT_X_OFFSET = 145
DEFAULT_Y_OFFSET = 25
DEFAULT_HEIGHT_STEP = 150

DEFAULT_BOARD_WIDTH = 48 * 13
DEFAULT_BOARD_HEIGHT = 48 * 2

DEFAULT_BG_BMP_FILENAME = os.path.join(wms_shape.DEFAULT_IMG_DIR, 'truck.png')


class icWMSSimpleTruckConstructorCtrl(wx.Panel):
    """
    Конструктор погрузки седельного тягача.
    Самый простой вариант. 1 ярус и все.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Panel.__init__(self, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Конструктор погрузки тягача
        self.truck_load_constructor = tier_constructor.icWMSTierContructorCtrl(self)

        bg_filename = DEFAULT_BG_BMP_FILENAME
        self.truck_load_constructor.setBackgroundBmp(bg_filename)
        # Основной сайзер
        sizer.Add(self.truck_load_constructor, 1, wx.GROW | wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.Layout()

    def setTierCount(self, tier_count=1, box_layout_scheme=None):
        """
        Установить количество ярусов со схемой погрузки паллет.
        @param tier_count: Количество ярусов.
        @param box_layout_scheme: Схема погрузки.
        Схема задается по позициям.
        @return: True/False.
        """
        if box_layout_scheme and tier_count > 0:
            for i in range(tier_count):
                # Сначала подготовить доски для каждого яруса
                y_offset = DEFAULT_Y_OFFSET + i * DEFAULT_HEIGHT_STEP
                scheme = layout_scheme.init_cell_points(box_layout_scheme,
                                                        DEFAULT_X_OFFSET, y_offset)
                self.truck_load_constructor.appendBoard(scheme, left=DEFAULT_X_OFFSET, top=y_offset,
                                                        width=DEFAULT_BOARD_WIDTH, height=DEFAULT_BOARD_HEIGHT)
            return True
        else:
            log.warning(u'Инициализация ярусов. Не корректные входные значения.')
        return False


class icWMSTruckConstructorCtrl(wx.Panel):
    """
    Конструктор погрузки седельного тягача.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Panel.__init__(self, *args, **kwargs)

        # Вид сбоку тягача
        self.side_view = wx.CollapsiblePane(self, label=u'Общий вид',
                                            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)
        panesizer = wx.BoxSizer(wx.VERTICAL)
        pane = self.side_view.GetPane()

        self.side_constructor = rack_constructor.icWMSRackContructorCtrl(pane)
        bmp_filename = os.path.join(wms_shape.DEFAULT_IMG_DIR, 'truck.png')
        self.side_constructor.setBackgound(bmp_filename)

        panesizer.Add(self.side_constructor, 1, wx.GROW | wx.EXPAND)
        pane.SetSizer(panesizer)
        panesizer.SetSizeHints(pane)
        self.side_view.Collapse()

        # Вид ярусов сверху
        self.tiers_view = wx.CollapsiblePane(self, label=u'Ярусы',
                                             style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)
        panesizer = wx.BoxSizer(wx.VERTICAL)
        pane = self.tiers_view.GetPane()

        self.tiers_constructor = tier_constructor.icWMSTierContructorCtrl(pane)

        panesizer.Add(self.tiers_constructor, 1, wx.GROW | wx.EXPAND)
        pane.SetSizer(panesizer)
        panesizer.SetSizeHints(pane)
        self.tiers_view.Collapse()

        # Основной сайзер
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.side_view, 0,
                       wx.GROW | wx.EXPAND, 25)
        # ВНИМАНИЕ! proportion----------+
        # устанавливает распахивание    |
        # второй панели на все окно     v
        self.sizer.Add(self.tiers_view, 1,
                       wx.GROW | wx.EXPAND, 25)
        self.SetSizer(self.sizer)
        # self.SetSizerAndFit(self.sizer)
        self.Layout()
        # self.Fit()

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onSideViewPaneChanged, self.side_view)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onTiersViewPaneChanged, self.tiers_view)

    def setTierCount(self, tier_count=1, box_layout_scheme=None):
        """
        Установить количество ярусов со схемой погрузки паллет.
        @param tier_count: Количество ярусов.
        @param box_layout_scheme: Схема погрузки.
        Схема задается по позициям.
        @return: True/False.
        """
        if box_layout_scheme and tier_count > 0:
            for i in range(tier_count):
                # Сначала подготовить доски для каждого яруса
                y_offset = DEFAULT_Y_OFFSET + i * DEFAULT_HEIGHT_STEP
                scheme = layout_scheme.init_cell_points(box_layout_scheme,
                                                        DEFAULT_X_OFFSET, y_offset)
                self.tiers_constructor.appendBoard(scheme, left=DEFAULT_X_OFFSET, top=y_offset,
                                                   width=DEFAULT_BOARD_WIDTH, height=DEFAULT_BOARD_HEIGHT)
            return True
        else:
            log.warning(u'Инициализация ярусов. Не корректные входные значения.')
        return False

    def onSideViewPaneChanged(self, event):
        """
        Обработчик изменения состояния просмотра
        панели вида загрузки тягача.
        """
        if event:
            print('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % event.Collapsed)

        # redo the layout
        self.Layout()

        # and also change the labels
        # self.collapse_pane.SetLabel(self.getPaneLabel())

        self.GetSizer().Layout()
        # self.Fit()

    def onTiersViewPaneChanged(self, event):
        """
        Обработчик изменения состояния
        панели конструктора ярусов.
        """
        if event:
            print('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % event.Collapsed)

        # redo the layout
        self.Layout()

        # and also change the labels
        # self.collapse_pane.SetLabel(self.getPaneLabel())

        self.GetSizer().Layout()
        # self.Fit()


def test():
    """
    Функция тестирования.
    """
    from ic import config
    log.init(config)

    app = wx.PySimpleApp()

    frame = wx.Frame(None, size=wx.Size(900, 500))

    panel = icWMSTruckConstructorCtrl(frame)

    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    test()
