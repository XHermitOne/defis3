#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дизайнер диалога.
"""

import wx
from ic.utils import util
from ic.components import icwidget
import ic.components.icwxpanel as icwxpanel
import ic.utils.resource as resource
import ic.utils.graphicUtils as graphicUtils
from ic.interfaces import icdesignerinterface
from ic.bitmap import bmpfunc

_ = wx.GetTranslation

HEADER_COLOR = (78, 117, 200)

DEFAULT_MIN_BUTTON_IMG = 'navigation-270-button.png'
DEFAULT_EXP_BUTTON_IMG = 'navigation-090-button.png'
DEFAULT_CLOSE_BUTTON_IMG = 'cross-button.png'


class icDialogDesigner(icwidget.icWidget, wx.Panel, icdesignerinterface.icDesignerInterface):
    """
    Класс дизайнер фрейма.
    """
    def __init__(self, parent=None, id=-1, component={}, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icFrame

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
        #   Атрибуты сайзера
        from ic.components import icdialog
        self.bSizerAdd = False
        util.icSpcDefStruct(icdialog.SPC_IC_DIALOG, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.title = component['title']
        fgr = icwxpanel.DESIGN_BORDER_CLR
        bgr = component['backgroundColor']
        style = wx.BORDER_THEME
        wx.Panel.__init__(self, parent, id, self.position, self.size, style=style, name=self.name)
        clr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))
        else:
            self.SetBackgroundColour(clr)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        #   Создаем дочерние компоненты
        self.head_h = 21
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add((20, self.head_h+1))
        
        self.panel = icwxpanel.icWXPanel(self, -1, {'backgroundColor': bgr})
        self.panel.setEditorMode()
        self.panel.SetForegroundColour(clr)
        self.panel.resource['__item_id'] = self.resource.get('__item_id', None)
        # Запрещаем перемещать панель
        self.panel.bMoveObj = False
        self.bMoveObj = False
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        # Регистрируем панель в подложке редактора
        try:
            self.parent.AddObject(self.panel)
        except:
            pass
            
        child = self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

        self.img_min = bmpfunc.createLibraryBitmap(DEFAULT_MIN_BUTTON_IMG)
        self.img_exp = bmpfunc.createLibraryBitmap(DEFAULT_EXP_BUTTON_IMG)
        self.img_close = bmpfunc.createLibraryBitmap(DEFAULT_CLOSE_BUTTON_IMG)
        
        # 
        self.border_pen = wx.Pen(wx.Colour(*icwxpanel.DESIGN_BORDER_CLR))
        
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
        
    def OnPaint(self, event):
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
            dc.drawLabel(self.title, wx.Rect(5, d, width - 60 - d, H - d))
        # Рисуем кнопки
        dc.DrawBitmap(self.img_min, width - 60, d+2, True)
        dc.DrawBitmap(self.img_exp, width - 40, d+2, True)
        dc.DrawBitmap(self.img_close, width - 20, d+2, True)
        
        pen = wx.Pen(fgr)
        dc.SetPen(pen)
        # Для редактора форм
        if 0:
            step = 10
            for y in xrange(int((height-H)/step)-1):
                for x in xrange(int(width/step)-1):
                    dc.DrawPoint((x+1)*step, (y+1)*step+H)
        # Рисуем круглые углы
        if 0:
            graphicUtils.drawRoundCorners(dc, (width, height),
                                          fgr, bgr, bgr_prnt, d,
                                          (fgr, fgr, fgr, fgr),
                                          corners=(1, 1, 0, 0))

        dc.EndDrawing()

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
    frame = icDialogDesigner(main_win, component={'title': 'wxDialog Test',
                                                  'backgroundColor': (255, 255, 255),
                                                  'keyDown': 'print \'keyDown in icFrame\''})
    main_win.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test2()
