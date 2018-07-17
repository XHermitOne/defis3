#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса меню.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import flatmenu

# Версия
__version__ = (0, 0, 1, 1)

# --- Спецификации ---
SPC_IC_FLATMENU = {'label': 'menu',    # Надпись
                   'child': list(),
                   }


class icFlatMenuPrototype(flatmenu.FlatMenu):
    """
    Класс меню.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self, *args, **kwargs)
        
    def appendItem(self, FlatMenuItem_):
        """
        Добавить пункт меню.
        @param FlatMenuItem_: Объект пункта меню. 
        """
        if FlatMenuItem_ is None:
            return None
        
        item = None
        kind = FlatMenuItem_.GetKind()
        if kind == wx.ITEM_NORMAL:
            item = self.AppendItem(FlatMenuItem_)
        elif kind == wx.ITEM_SEPARATOR:
            item = self.AppendSeparator()
        elif kind == wx.ITEM_CHECK:
            pass
        elif kind == wx.ITEM_RADIO:
            pass

        return item
    
    def appendMenu(self, FlatMenu_):
        """
        Добавить меню.
        @param FlatMenu_: Объект меню. 
        """
        if FlatMenu_ is None:
            return None
        
        id = wx.NewId()
        label = FlatMenu_.getLabel()
        menu_item = flatmenu.FlatMenuItem(self, id, label, '', wx.ITEM_NORMAL, FlatMenu_)
        self.AppendItem(menu_item)
        return menu_item
    
    def findMenuItemByName(self, MenuItemName_):
        """ 
        Поиск пункта меню по имени. 
        """
        for item in self._itemsArr:
            is_separator = item.IsSeparator()
            if not is_separator:
                # Разделители просматривать не надо
                if item.getName() == MenuItemName_:
                    return item
        return None
    
    def getMenuBar(self):
        """
        Получить горизонтальное меню.
        """
        menu_bar = self.GetMenuBar()
        if menu_bar:
            return menu_bar
        parent = self.GetParent()
        if issubclass(parent.__class__, flatmenu.FlatMenuBar):
            return parent
        elif issubclass(parent.__class__, flatmenu.FlatMenu):
            return parent.getMenuBar()        
        else:
            return None

    def popupByButton(self, button, parent=None):
        """
        Вызвать всплывающее меню по кнопке.
        @param button: Объект кнопки wx.Button.
        @param parent: Родительское окно.
        """
        if button is None:
            # Если кнопка не определена, то функция бессмыслена
            return None
        if parent is None:
            parent = button.GetParent()
        point = button.GetPosition()
        point = button.GetParent().ClientToScreen(point)
        self.SetOwnerHeight(button.GetSize().y)
        return self.Popup(wx.Point(point.x, point.y), parent)

    def getToolLeftBottomPoint(self, toolbar, tool):
        """
        Определить точку левого-нижнего края кнопки.
        Используется для вызова всплывающих меню.
        @param toolbar: Объект панели инструментов wx.ToolBar.
        @param tool: Объект инструмента панели инструментов wx.ToolBarToolBase.
        """
        if tool is None:
            # Если инструмент не определен, то функция бессмыслена
            return None

        toolbar_pos = toolbar.GetScreenPosition()
        toolbar_size = toolbar.GetSize()
        tool_index = toolbar.GetToolPos(tool.GetId())
        tool_size = toolbar.GetToolSize()
        x_offset = 0
        for i in range(tool_index):
            prev_tool = toolbar.GetToolByPos(i)
            prev_ctrl = prev_tool.GetControl() if prev_tool.IsControl() else None
            x_offset += prev_ctrl.GetSize()[0] if prev_ctrl else tool_size[0]

        return wx.Point(toolbar_pos[0] + x_offset, toolbar_pos[1] + toolbar_size[1])

    def popupByTool(self, tool, toolbar=None):
        """
        Вызвать всплывающее меню по инструменту панели инструментов.
        @param tool: Объект инструмента панели инструментов wx.ToolBarToolBase.
        @param toolbar: Объект панели инструментов wx.ToolBar.
        """
        if tool is None:
            # Если инструмент не определен, то функция бессмыслена
            return None

        if toolbar is None:
            toolbar = tool.GetToolBar()

        point = self.getToolLeftBottomPoint(toolbar, tool)
        parent = toolbar.GetParent()
        return self.Popup(wx.Point(point.x, point.y), parent)
