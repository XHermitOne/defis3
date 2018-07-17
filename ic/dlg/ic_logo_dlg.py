#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Заставка при загрузки проекта.
"""

import wx
import wx.lib.imagebrowser

import ic.components.icfont as icfont
import ic.utils.ic_exec     # Этот модуль подгружается для спецификации
import ic.bitmap.ic_bmp as ic_bmp
from ic.utils import ic_file
import time
import thread


__version__ = (0, 0, 1, 2)


# --- Класс и функции индикатора процесса
ic_proccess_dlg = None


def load_proccess_deco(f):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """

    def func(*arg, **kwarg):
        return LoadProjectProccess(None, u'Подождите   ', f, arg, kwarg)

    return func


def SetLoadProccessBoxLabel(label=None, value=None):
    """
    Функция изменяет параметры индикатора процесса. Если значение любого из
    параметров None, то значение параметра на индикаторе не меняется.
    Примеры:
        2. SetLoadProccessBoxLabel('Wait...', 20)
    
    @type label: C{string}
    @param label: Текст сообщения на верхней полосе индикации.
    @type value: C{int}
    @param value: Значение верхней полосы индикации от 0 до 100.
    """
    if ic_proccess_dlg:
        sx, sy = ic_proccess_dlg.GetSize()
        
        ic_proccess_dlg.SetLabel(label)
        ic_proccess_dlg.SetValue(value)


def LoadProjectProccess(Parent_, Msg_,
                        Func_, FuncArgs_=(), FuncKW_={},
                        Frames_=None, bAutoIncr=False):
    """
    Окно ожидания.
    @param Parent_: Ссылка на окно.
    @param Msg_: Текст диалога.
    @param Func_: Функция, которую необходимо подождать.
    @param FuncArgs_: Аргументы функции.
    @param FuncKW_: Именованные аргументы функции.
    @param Frames_: Файлы-кадры.
    """
    global ic_proccess_dlg
    if ic_proccess_dlg:
        return Func_(*FuncArgs_, **FuncKW_)
        
    wait_result = [None]

    if not Frames_:
        # Определить кадры по умолчанию
        wait_dir = ic_file.DirName(__file__)+'/Wait/'
        Frames_ = [wait_dir+'logo.jpg']
    
    ic_proccess_dlg = wait_box = icThreadLoadProjectDlg(Parent_, Frames_, Msg_, bAutoIncr=bAutoIncr)
        
    wait_box.SetResultList(wait_result)
    # Запустить функцию ожидания
    thread.start_new(wait_box.Run, (Func_, FuncArgs_, FuncKW_))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_proccess_dlg = None
    return wait_result[0]

try:
    from ic.engine import ic_user
except ImportError:
    print('ic_user IMPORT ERROR')


class icThreadLoadProjectDlg(wx.Dialog):

    def __init__(self, Parent_, Frames_, Msg_, min=0, max=100, style=0, bAutoIncr=False):
        """
        Конструктор.
        
        @type Parent_: C{wx.Window}
        @param Parent_: Указатель на родительское окно.
        @type Msg_: C{string}
        @param Msg_: Сообщение верхнего индикатора.
        @type min: C{int}
        @param min: Минимальное значение верхнего индикатора.
        @type max: C{int}
        @param max: Максимальное значение верхнего индикатора.
        @type style: C{int}
        @param style: Стиль окна процесса.
        @type bAutoIncr: C{bool}
        @param bAutoIncr: Признак автоматического изменения состояния индикаторов.
            Используется в тех случаях, когда размерность процесса не определена,
            а показывать чего то надо.
        """
        if Parent_:
            self.defBackClr = Parent_.GetBackgroundColour()
        else:
            app = ic_user.icGetRunner()
            if app:
                Parent_ = app.GetTopWindow()
                self.defBackClr = app.GetTopWindow().GetBackgroundColour()
            else:
                self.defBackClr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        style = wx.STAY_ON_TOP
        w, h = wx.ScreenDC().GetSize()
        self._ani = [ic_bmp.icCreateBitmap(pic_name) for pic_name in Frames_]
        if self._ani:
            sx, sy = self._pic_size = (self._ani[0].GetWidth(), self._ani[0].GetHeight())
        else:
            sx, sy = self._pic_size = (250, 70)

        x = (w - sx)/2
        y = (h - sy)/2
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(Parent_, -1, pos=(x, y), size=(sx, sy), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)
        
        # Индекс состояния анимации
        self._cur_ani_state = 0
        self._max_ani_state = len(Frames_)
        self._delay = 0.3
        self._autoIncr = bAutoIncr

        self.title = ''
        self.label = Msg_
        self.min = min
        self.max = max
        self.value = min
        
        #
        self.indBgrClr = wx.Colour(230, 230, 230)
        self.indClr = wx.Colour(100, 100, 135)
        
        self.indBgrBrush = wx.Brush(self.indBgrClr, wx.SOLID)
        self.indBrush = wx.Brush(self.indClr, wx.SOLID)
            
        self.bgrBrush = wx.Brush(self.defBackClr, wx.SOLID)
        self.font = icfont.icFont({})
        
        # Высота индикатора
        self.indH = 10
        
        self._count = 0
        self._running = True    # Признак запущенной функции
        self._closed = False    # Признак закрытия окна
        self._result_list = None
        self.old_time = time.clock()
        
        self._oSize = self.GetSize()
        self._oPos = self.GetPosition()
        self._oPar = None
        
        self.timer = wx.FutureCall(1, self.OnTimer, None)
        
    def DirectRefresh(self):
        """
        """
        evt = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(evt)

    def SetResultList(self, ResultList_):
        self._result_list = ResultList_
        
    def NextState(self):
        """
        Сменить состояние.
        """
        self._cur_ani_state += 1
        if self._cur_ani_state >= self._max_ani_state:
            self._cur_ani_state = 0
        return self._cur_ani_state
    
    def DrawFrame(self, NFrame_):
        """
        Отрисовка кадра.
        @param NFrame_: Номер кадра.
        """
        frame_bmp = self._ani[NFrame_]
        
        dc = wx.WindowDC(self._picture)
        dc.BeginDrawing()
        dc.Clear()
        dc.DrawBitmap(frame_bmp, 0, 0, True)
        dc.EndDrawing()
        self._picture.Refresh()

    def DrawLabel(self, dc, label=None, label2=None):
        """
        Отрисовываем текст сообщения.
        """
        
        if label is None:
            label = self.label
        
        px = 0
        sx, sy = self.GetSize()
        w, h = self.GetTextExtent('W')
        x = 10 + px
        y = 3
        y = self._ani[0].GetHeight() - 7*self.indH - h - 3
        
        dc.SetTextForeground('#eeeeee')
        dc.SetFont(self.font)
        
        if label:
            dc.DrawText(label, x, y)

    def DrawIndicator(self, dc):
        """
        Рисует индикатор процесса.
        """
        px = 0

        sx, sy = self.GetSize()
        w, h = self.GetTextExtent('W')
        width = sx - (px+15)
        H = self.indH
        hh = self._ani[0].GetHeight() - 7*H
        
        #   Рисуем индикатор
        pen = wx.Pen(wx.Colour(50, 50, 50))
        dc.SetPen(pen)
        dc.SetBrush(self.indBgrBrush)
        
        if self.value is not None:
            dc.DrawRectangle(px+5, hh, width, H)
    
            #   Состояние индикатора
            dc.SetBrush(self.indBrush)
            dc.DrawRectangle(px+5, hh, width*(self.value-self.min)/(self.max-self.min), H)
            
    def DrawPic(self, NFrame_, dc, bClear=False):
        """
        Отрисовка кадра.
        @param NFrame_: Номер кадра.
        """
        if self._ani:
            sx, sy = self.GetSize()
            bmp = self._ani[NFrame_]
            px, py = self._pic_size
            
            memDC = wx.MemoryDC()
            memDC.SelectObject(bmp)
            dc.Blit(0, 0, px, py, memDC, 0, 0, wx.COPY, True)
        
    def isParChanged(self):
        """
        Возаращает признак изменения параметров индикатора.
        """
        
        sz = self.GetSize()
        pos = self.GetPosition()
        
        return (sz != self._oSize or pos != self._oPos or
                self._oPar != (self.min, self.max, self.value, self.label))
        
    def OnCheckClose(self, event=None):
        """
        Проверка закрытия окна.
        """
        if not self._running and not self._closed:
            try:
                self.EndModal(wx.ID_OK)
            except:
                pass
                
            self._closed = True
        else:
            self.timer.Restart(150, None)
            
        if event:
            event.Skip()

    def OnPaint(self, evt=None):
        """
        """
        t = time.clock()
        
        self.old_time = t
        dc = wx.WindowDC(self)
        dc.SetBrush(self.bgrBrush)
        
        #   Если параменты индикатора не менялись, то перерисовываем только картинку
        dc.BeginDrawing()
        pen = wx.Pen(wx.Colour(100, 100, 100))
        dc.SetPen(pen)
        sx, sy = self.GetSize()
        px, py = self._pic_size
        
        dc.SetBrush(self.bgrBrush)
        
        #   Отрисовываем картинку
        self.DrawPic(self.NextState(), dc)

        #   Отрисовываем сообщение
        self.DrawLabel(dc)

        #   Отрисовываем индикатор процесса
        self.DrawIndicator(dc)
        
        dc.EndDrawing()
        
        if evt:
            evt.Skip
        
        self.OnCheckClose()
        
    def OnTimer(self, evt):
        """
        """
        if self._autoIncr:
            self.value += 10
            if self.value > self.max:
                self.value = self.min
                    
        self.OnPaint(None)
        
        #   Сохраняем текущие параметры
        self.SavePar()

    def Run(self, Func_, Args_, KW_):
        """
        Запуск ожидания функции.
        """
        self._running = True
        result = Func_(*Args_, **KW_)
        self._running = False
        # Сбросить в результирующий список
        if isinstance(self._result_list, list):
            self._result_list[0] = result
            
    def SetLabel(self, label=None):
        """
        Устанавливает текст верхней полосы индикации процесса.
        """
        if label is not None:
            self.label = label
        
    def SavePar(self):
        """
        Сохраняет параметры индикатора.
        """
        self._oSize = self.GetSize()
        self._oPos = self.GetPosition()
        self._oPar = (self.min, self.max, self.value, self.label)

    def SetValue(self, value):
        """
        Устанавливает значение верхней полосы индикации процесса.
        """
        if value is None:
            return
        
        if value < self.min:
            self.value = self.min
        elif value > self.max:
            self.value = self.max
        else:
            self.value = value

@load_proccess_deco
def f(parent):
    """
    """
    for x in range(100):
        SetLoadProccessBoxLabel('Count x:'+str(x), x)
        time.sleep(0.5)


def test(par=0):
    """
    Тестируем класс icHeadCell.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    frame.Show(True)
    
    f(win)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
