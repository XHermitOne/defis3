#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс горизонтального меню.
"""

# --- Imports ---
import wx
from wx.lib.agw import aui
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed, ControlNormal
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, SEPARATOR_WIDTH

import wx.lib.agw.flatmenu as flatmenu

from . import icflatmenu
from . import icflatmenuitem

# --- Constants ---
_ = wx.GetTranslation


# Подменяем AUI на новый
flatmenu.AUI = aui
flatmenu.AuiPaneInfo = flatmenu.AUI.AuiPaneInfo

# --- Specifications ---
SPC_IC_FLATMENUBAR = {'renderer': None,    # Стиль отрисовки
                      'icon_size': 16,     # Размер иконок
                      'spacer_size': 7,    # Размер расстояния между элементами
                      }

# Версия
__version__ = (0, 0, 1, 2)


class icFlatMenuBarPrototype(flatmenu.FlatMenuBar):
    """
    Класс горизонтального меню.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        flatmenu.FlatMenuBar.__init__(self, *args, **kwargs)

        parent = self.GetParent()
        if hasattr(parent, 'aui_manager'):
            self.PositionAUI(parent.aui_manager)
            self.SetLCDMonitor(True)
            ArtManager.Get().DrawMenuBarBorder(False)
            ArtManager.Get().SetMBVerticalGradient(True)
            ArtManager.Get().SetRaiseToolbar(True)
            ArtManager.Get().SetMenuBarColour('Generic')
            parent.aui_manager.Update()
            self.Refresh()

    def appendTool(self, FlatMenuTool_):
        """
        Добавить инструмент на панель инструментов горизонтального меню.
        @param FlatMenuTool_: ОБъект инструмента горизонтального меню.
        """
        if FlatMenuTool_ is None:
            return None

        tool = None
        kind = FlatMenuTool_.GetKind()
        if kind == wx.ITEM_NORMAL:
            id = FlatMenuTool_.GetId()
            pic1 = FlatMenuTool_.GetNormalBmp()
            pic2 = FlatMenuTool_.GetDisabledBmp()
            helpString = FlatMenuTool_.GetHelpString()
            if not helpString:
                helpString = ''
            description = FlatMenuTool_.GetDescription()
            if not description:
                description = ''
                
            tool = self.AddTool(id, '', pic1, pic2,
                                shortHelp=helpString,
                                longHelp=description)
                
        elif kind == wx.ITEM_SEPARATOR:
            tool = self.AddSeparator()
        elif kind == wx.ITEM_CHECK:
            pass
        elif kind == wx.ITEM_RADIO:
            pass

        return tool

    def findMenuItemByName(self, MenuItemName_):
        """ 
        Поиск пункта меню по имени. 
        """
        for item in self._items:
            find_item = item.GetMenu().findMenuItemByName(MenuItemName_)
            if find_item:
                return find_item
        return None

    def GetSeparatorCols(self):
        return wx.Colour(241, 249, 255), wx.Colour(106, 140, 203)

    def DrawToolbar(self, dc, rect):
        """
        Draws the toolbar with the given dc & rect.
        """
        width = self._tbIconSize + self._spacer
        height = self._tbIconSize + self._spacer
        xx = rect.x
        yy = rect.y + (rect.height - height)/2

        artMgr = ArtManager.Get()

        # by default set all toolbar items as invisible
        for but in self._tbButtons:
            but._visible = False

        counter = 0
        # Get all the toolbar items
        for i in xrange(len(self._tbButtons)):
            tbItem = self._tbButtons[i]._tbItem
            # the button width depends on its type
            if tbItem.IsSeparator():
                width = SEPARATOR_WIDTH
            elif tbItem.IsCustomControl():
                control = tbItem.GetCustomControl()
                width = control.GetSize().x + self._spacer
            else:
                width = self._tbIconSize + self._spacer   # normal bitmap's width

            # can we keep drawing?
            if xx + width >= rect.width:
                break

            counter += 1

            # mark this item as visible
            self._tbButtons[i]._visible = True

            bmp = wx.NullBitmap

            # ------------------------------------------
            # special handling for separator
            # ------------------------------------------
            if tbItem.IsSeparator():

                # Place a separator bitmap
                h = 16
                bmp = wx.EmptyBitmap(12, h)
                mem_dc = wx.MemoryDC()
                mem_dc.SelectObject(bmp)
                mem_dc.SetPen(wx.BLACK_PEN)
                mem_dc.SetBrush(wx.BLACK_BRUSH)

                mem_dc.DrawRectangle(0, 0, bmp.GetWidth(), bmp.GetHeight())

                col = artMgr.GetMenuBarFaceColour()
                col1, col2 = self.GetSeparatorCols()

                mem_dc.SetPen(wx.Pen(col2))
                mem_dc.DrawLine(5, 0, 5, bmp.GetHeight())

                mem_dc.SetPen(wx.Pen(col1))
                mem_dc.DrawLine(6, 0, 6, bmp.GetHeight())

                mem_dc.SelectObject(wx.NullBitmap)
                bmp.SetMask(wx.Mask(bmp, wx.BLACK))

                # draw the separator
                buttonRect = wx.Rect(xx, rect.y + 5, bmp.GetWidth(), bmp.GetHeight())
                dc.DrawBitmap(bmp, xx, rect.y + 5, True)
                xx += buttonRect.width
                self._tbButtons[i]._rect = buttonRect
                continue

            elif tbItem.IsCustomControl():
                control = tbItem.GetCustomControl()
                ctrlSize = control.GetSize()
                ctrlPos = wx.Point(xx, yy + (rect.height - ctrlSize.y)/2)
                if control.GetPosition() != ctrlPos:
                    control.SetPosition(ctrlPos)

                if not control.IsShown():
                    control.Show()

                buttonRect = wx.RectPS(ctrlPos, ctrlSize)
                xx += buttonRect.width
                self._tbButtons[i]._rect = buttonRect
                continue
            else:
                if tbItem.IsEnabled():
                    bmp = tbItem.GetBitmap()
                else:
                    bmp = tbItem.GetDisabledBitmap()

            # Draw the toolbar image
            if bmp.Ok():

                x = xx
                y = yy + (height - bmp.GetHeight())/2 - 1

                buttonRect = wx.Rect(x, y, width, height)

                if len(self._tbButtons) > i >= 0:

                    if self._tbButtons[i]._tbItem.IsSelected():
                        tmpState = ControlPressed
                    else:
                        tmpState = ControlFocus

                    if self._tbButtons[i]._state == ControlFocus or self._tbButtons[i]._tbItem.IsSelected():
                        artMgr.DrawButton(dc, buttonRect, artMgr.GetMenuTheme(), tmpState, False)
                    else:
                        self._tbButtons[i]._state = ControlNormal

                imgx = buttonRect.x + (buttonRect.width - bmp.GetWidth())/2
                imgy = buttonRect.y + (buttonRect.height - bmp.GetHeight())/2

                if self._tbButtons[i]._state == ControlFocus and not self._tbButtons[i]._tbItem.IsSelected():

                    # in case we the button is in focus, place it
                    # once pixle up and left
                    # place a dark image under the original image to provide it
                    # with some shadow
                    # shadow = ConvertToMonochrome(bmp)
                    # dc.DrawBitmap(shadow, imgx, imgy, True)

                    imgx -= 1
                    imgy -= 1

                dc.DrawBitmap(bmp, imgx, imgy, True)
                xx += buttonRect.width

                self._tbButtons[i]._rect = buttonRect

                if self._showTooltip == -1:
                    self.RemoveHelp()
                else:
                    try:
                        self.DoGiveHelp(self._tbButtons[self._showTooltip]._tbItem)
                    except:
                        pass

        for j in xrange(counter, len(self._tbButtons)):
            if self._tbButtons[j]._tbItem.IsCustomControl():
                control = self._tbButtons[j]._tbItem.GetCustomControl()
                control.Hide()


def simple_test():
    """
    Тестовая функция.
    """
    from ic.imglib import common
    from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, SEPARATOR_WIDTH

    app = wx.PySimpleApp()
    common.img_init()
    frame = wx.Frame(None)

    mb = icFlatMenuBarPrototype(frame, wx.ID_ANY, 16, 7, options=FM_OPT_SHOW_TOOLBAR|FM_OPT_SHOW_CUSTOMIZE)
    fileMenu = icflatmenu.icFlatMenuPrototype()
    item_id = wx.NewId()
    item = icflatmenuitem.icFlatMenuItemPrototype(fileMenu, item_id, _('&New file'), _('New file'),
                                                  wx.ITEM_NORMAL, None, common.imgExit)
    mb.AddTool(item_id, _('Open file'), common.imgExit)
    fileMenu.AppendItem(item)
    mb.Append(fileMenu, _('&File'))
    print('ITEM: %s' % dir(item))

    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    simple_test()
