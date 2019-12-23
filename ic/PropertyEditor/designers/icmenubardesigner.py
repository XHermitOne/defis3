#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дизайнер горизонтального меню.
"""

import wx
from ic.utils import util
from ic.components import icwidget
from ic.interfaces import icdesignerinterface

_ = wx.GetTranslation


class icMenuBarDesigner(icwidget.icWidget, wx.Panel, icdesignerinterface.icDesignerInterface):
    """
    Класс дизайнер горизонтального меню.
    """
    @staticmethod
    def getToolPanelCls():
        return None
    
    def __init__(self, parent=None, id=-1, component={}, logType=0,
                 evalSpace = None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """ 
        Конструктор для создания icMenuBar.

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
        from ic.components.user import ic_menubar_wrp

        self.bSizerAdd = False
        util.icSpcDefStruct(ic_menubar_wrp.ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        # Высота горизонтального меню
        self.menubar_h = 20
        
        fgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)
        bgr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)

        style = wx.BORDER_SIMPLE
        wx.Panel.__init__(self, parent, id, self.position, self.size, style=style, name=self.name)
        
        if fgr is not None:
            self.SetForegroundColour(fgr)
        if bgr is not None:
            self.SetBackgroundColour(bgr)

        #   Создаем дочерние компоненты
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Создание дочерних дизайнеров
        children = self.childCreator(bCounter, progressDlg)
        if children:
            for child in children:
                self.sizer.Add(child, 0, wx.ALIGN_LEFT)
        # Добавить пустое место
        self.sizer.Add((50, self.menubar_h+1))
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

    def childCreator(self, bCounter, progressDlg):
        """ 
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
            return self.get_children_lst()

    def setEditorMode(self):
        """ 
        Устанавливает режим редактора.
        """
        self.is_editor_mode = True


def test2(par=0):
    """
    Тестируем класс icFrameDesigner.
    """
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
