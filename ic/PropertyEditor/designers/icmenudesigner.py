#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Name:        icmenudesigner.py
# Purpose:     Дизайнер выпадающего меню.
#
# Author:      <Kolchanov A. V.>
#
# Created:     11.02.2008
# RCS-ID:      $Id: icmenudesigner.py $
# Copyright:   (c) 2008
# Licence:     <your licence>
# -----------------------------------------------------------------------------

import wx
import ic.utils.util as util
import ic.components.icwidget as icwidget
import ic.utils.resource as resource
import ic.utils.graphicUtils as graphicUtils
from ic.interfaces import icdesignerinterface
_ = wx.GetTranslation

#---------- Классы --------------
class icMenuDesigner(icwidget.icWidget, wx.Panel, icdesignerinterface.icDesignerInterface):
    """ Класс дизайнер выпадающего меню."""
    @staticmethod
    def GetToolPanelCls():
        return None

    def __init__(self, parent = None, id = -1, component = {}, logType = 0,
            evalSpace = None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """ 
        Конструктор для создания icMenu
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        from ic.components.user import ic_menu_wrp
        
        self.bSizerAdd = False
        util.icSpcDefStruct(ic_menu_wrp.ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.caption=component['caption']
        
        self.menu_label_h=20
        
        self._fgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT) #component['foregroundColor']
        self._bgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU) #component['backgroundColor']

        style = wx.BORDER_NONE
        wx.Panel.__init__(self, parent, id, self.position, self.size, style = style, name = self.name)
        
        if self._fgr != None:
            self.SetForegroundColour(self._fgr)
        if self._bgr != None:
            self.SetBackgroundColour(self._bgr)

        #   Создаем дочерние компоненты
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add((5, self.menu_label_h+1))
        self.label=wx.StaticText(self,-1,self.caption)
        self.sizer.Add(self.label, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.label.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)        
        self.sizer.Add((5, self.menu_label_h+1))
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Fit()

    def createMenu(self,MenuName_,MenuResource_):
        """
        Создание меню по ресурсу.
        """
        from ic.engine import ic_menu
        menu=ic_menu.icMenu(None,MenuName_,MenuResource_,Window_=self)
        return menu
        
    def OnMouseClick(self,event):
        """
        Обработчик клика на ярлыке выпадающего меню.
        """
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.label.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.Refresh()
        
        menu=self.createMenu(self.name,self.resource)
        if menu:
            menu_point=wx.Point(self.label.GetPosition().x-5,self.GetSize().GetHeight())
            self.PopupMenu(menu,menu_point)
            menu.Destroy()
            
        self.SetBackgroundColour(self._bgr)
        self.label.SetForegroundColour(self._fgr)
        self.Refresh()
            
        event.Skip()
        
    def SetEditorMode(self):
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
    frame = icMenuBarDesigner(main_win, component = {'title':'wxFrame Test',
                                #'backgroundColor':(255,255,255),
                                'keyDown':'print \'keyDown in icFrame\''})
    #MsgBox(frame, 'Проверка')
    main_win.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test2()
