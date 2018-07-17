#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Дизайнер фрейма.
"""

import wx
import ic.utils.util as util
import ic.components.icwidget as icwidget
import ic.components.icwxpanel as icwxpanel
from ic.components.sizers import icboxsizer
import ic.utils.resource as resource
import ic.utils.graphicUtils as graphicUtils
from ic.interfaces import icdesignerinterface

_ = wx.GetTranslation

__version__ = (0, 0, 1, 2)

HEADER_COLOR = (78, 117, 200)


# --- Классы ---
class icFrameDesigner(icwidget.icWidget, wx.Panel, icdesignerinterface.icDesignerInterface):
    """
    Класс дизайнер фрейма.
    """
    def __init__(self, parent=None, id=-1, component={}, logType=0,
                 evalSpace = None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icFrame
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
        #   Атрибуты сайзера
        from ic.components import icframe
        self.bSizerAdd = False
        util.icSpcDefStruct(icframe.SPC_IC_FRAME, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.title = component['title']
        fgr = icwxpanel.DESIGN_BORDER_CLR
        bgr = component['backgroundColor']
        style = component['style']
        style = wx.BORDER_THEME
        wx.Panel.__init__(self, parent, id, self.position, self.size, style=style, name=self.name)
        
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))
        else:
            clr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
            self.SetBackgroundColour(clr)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #   Создаем дочерние компоненты
        self.head_h = 21
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add((20, self.head_h+1))
        # Запрещаем перемещать панель
        self.bMoveObj = False

        child = self.childCreator(bCounter, progressDlg)
        if child:
            self.sizer.Add(child, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

        from ic.imglib import newstyle_img
        self.img_min = newstyle_img.minXP
        self.img_exp = newstyle_img.expXP
        self.img_close = newstyle_img.closeXP
        
        self.border_pen = wx.Pen(wx.Colour(*icwxpanel.DESIGN_BORDER_CLR))
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            self.context.clear_spc_structs()
            if not self.context['_root_obj']:
                self.context['_root_obj'] = self
            self.GetKernel().parse_resource(self, self.child, self.sizer, context=self.context,
                                            bCounter=bCounter, progressDlg=progressDlg)
            return self.context.FindObject(self.child[0]['type'], self.child[0]['name'])

    def SetTitle(self, title):
        """
        Устанавливает заголовок окна.
        """
        self.title = title
        
    def GetTitle(self):
        """
        Возвращает заголовок окна.
        """
        return self.title
        
    def OnPaint(self, evt):
        """
        Обрабатываем событие EVT_PAINT.
        """
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        """
        Отрисовка дизайнера.
        """
        dc.BeginDrawing()

        bgr, fgr = self.GetBackgroundColour(), self.GetForegroundColour()
        d = 0
        width, height = self.GetClientSize()
        bgr_prnt = self.GetParent().GetBackgroundColour()

        if d > 0:
            backBrush = wx.Brush(bgr_prnt, wx.SOLID)
        else:
            backBrush = wx.Brush(bgr, wx.SOLID)

        dc.SetBackground(backBrush)
        dc.SetBrush(wx.Brush(bgr, wx.SOLID))
        dc.Clear()
        
        dc.SetPen(self.border_pen)
        if d != 0:
            dc.DrawRectangle(d, d, width-2*d, height-2*d)
        else:
            dc.DrawLines([wx.Point(d, d),
                          wx.Point(width-1 - d, d),
                          wx.Point(width-1 - d, height-1-d),
                          wx.Point(d, height-1-d),
                          wx.Point(d, d)])

        # Рисуем шапку (20, 79, 233), (1, 41, 107)
        H = self.head_h
        dc.SetBrush(wx.Brush(wx.Colour(*HEADER_COLOR), wx.SOLID))
        dc.DrawRectangle(d, d, width-2*d, H+2)
        # Рисуем заголовк
        if self.title:
            font = dc.GetFont()
            font.SetPointSize(10)
            font.SetWeight(wx.BOLD)
            dc.SetFont(font)
            dc.SetTextForeground(wx.WHITE)
            dc.DrawLabel(self.title, wx.Rect(5,d, width - 60 - d, H-d))
        # Рисуем кнопки
        dc.DrawBitmap(self.img_min, width - 60, d+2, True)
        dc.DrawBitmap(self.img_exp, width - 40, d+2, True)
        dc.DrawBitmap(self.img_close, width - 20, d+2, True)
        
        # Для редактора форм
        if 1:
            pen = wx.Pen('BLACK')
            dc.SetPen(pen)
            step = 10
            for y in xrange(int((height-H)/step)-1):
                for x in xrange(int(width/step)-1):
                    dc.DrawPoint((x+1)*step, (y+1)*step+H)
        # Рисуем круглые углы
        if 0:
            pen = wx.Pen(fgr)
            dc.SetPen(pen)

            graphicUtils.drawRoundCorners(dc, (width, height),
                                          fgr, bgr, bgr_prnt, d,
                                          (fgr, fgr, fgr, fgr),
                                          corners=(1, 1, 0, 0))

        dc.EndDrawing()

    def SetEditorMode(self):
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
    frame = icFrameDesigner(main_win, component={'title': 'wxFrame Test',
                                                 'keyDown': 'print(\'keyDown in icFrame\')'})
    main_win.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test2()
