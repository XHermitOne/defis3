#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дизайнер выпадающего меню.
"""

import wx
from ic.utils import util
from ic.components import icwidget
from ic.interfaces import icdesignerinterface

_ = wx.GetTranslation


class icMenuDesigner(icwidget.icWidget, wx.Panel, icdesignerinterface.icDesignerInterface):
    """
    Класс дизайнер выпадающего меню.
    """
    @staticmethod
    def getToolPanelCls():
        return None

    def __init__(self, parent=None, id=-1, component={}, logType=0,
                 evalSpace = None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """ 
        Конструктор для создания icMenu

        :type parent: C{wxWindow}
        :param parent: Указатель на родительское окно
        :type id: C{int}
        :param id: Идентификатор окна
        :type component: C{dictionary}
        :param component: Словарь описания компонента
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        :type evalSpace: C{dictionary}
        """
        from ic.components.user import ic_menu_wrp
        
        self.bSizerAdd = False
        util.icSpcDefStruct(ic_menu_wrp.ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.caption = component['caption']
        
        self.menu_label_h = 20
        
        self._fgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)
        self._bgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)

        style = wx.BORDER_NONE
        wx.Panel.__init__(self, parent, id, self.position, self.size, style=style, name=self.name)
        
        if self._fgr is not None:
            self.SetForegroundColour(self._fgr)
        if self._bgr is not None:
            self.SetBackgroundColour(self._bgr)

        #   Создаем дочерние компоненты
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add((5, self.menu_label_h+1))
        self.label = wx.StaticText(self, -1, self.caption)
        self.sizer.Add(self.label, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.label.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)        
        self.sizer.Add((5, self.menu_label_h+1))
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Fit()

    def createMenu(self, MenuName_, MenuResource_):
        """
        Создание меню по ресурсу.
        """
        from ic.engine import ext_func_menu
        menu=ext_func_menu.icMenu(None, MenuName_, MenuResource_, Window_=self)
        return menu
        
    def OnMouseClick(self,event):
        """
        Обработчик клика на ярлыке выпадающего меню.
        """
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.label.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.Refresh()
        
        menu = self.createMenu(self.name, self.resource)
        if menu:
            menu_point = wx.Point(self.label.GetPosition().x-5, self.GetSize().GetHeight())
            self.PopupMenu(menu, menu_point)
            menu.Destroy()
            
        self.SetBackgroundColour(self._bgr)
        self.label.SetForegroundColour(self._fgr)
        self.Refresh()
            
        event.Skip()
        
    def setEditorMode(self):
        """ 
        Устанавливает режим редактора.
        """
        self.is_editor_mode = True


def test2(par=0):
    """ Тестируем класс icFrameDesigner."""
    from ic.components.ictestapp import TestApp
    from ic.components import icframe
    app = TestApp(par)
    main_win = icframe.icFrame()
    frame = icMenuBarDesigner(main_win, component={'title': 'wxFrame Test',
                                                   'keyDown': 'print \'keyDown in icFrame\''})
    main_win.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test2()
