#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Заставка при загрузки проекта.
"""

import os
import os.path
import time
import _thread
import wx
import wx.lib.imagebrowser

from ic.components import icfont
import ic.utils.execfunc     # Этот модуль подгружается для спецификации
from ic.bitmap import bmpfunc


__version__ = (0, 1, 1, 1)


# --- Класс и функции индикатора процесса
ic_proccess_dlg = None


def load_proccess_deco(f):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """

    def func(*arg, **kwarg):
        return loadProjectProccess(None, u'Подождите   ', f, arg, kwarg)

    return func


def setLoadProccessBoxLabel(label=None, value=None):
    """
    Функция изменяет параметры индикатора процесса. Если значение любого из
    параметров None, то значение параметра на индикаторе не меняется.
    Примеры:
        2. setLoadProccessBoxLabel('Wait...', 20)
    
    @type label: C{string}
    @param label: Текст сообщения на верхней полосе индикации.
    @type value: C{int}
    @param value: Значение верхней полосы индикации от 0 до 100.
    """
    if ic_proccess_dlg:
        sx, sy = ic_proccess_dlg.GetSize()
        
        ic_proccess_dlg.SetLabel(label)
        ic_proccess_dlg.SetValue(value)


def loadProjectProccess(parent, message,
                        function, function_args=(), function_kwargs={},
                        frames=None, bAutoIncr=False):
    """
    Окно ожидания.
    @param parent: Ссылка на окно.
    @param message: Текст диалога.
    @param function: Функция, которую необходимо подождать.
    @param function_args: Аргументы функции.
    @param function_kwargs: Именованные аргументы функции.
    @param frames: Файлы-кадры.
    """
    global ic_proccess_dlg
    if ic_proccess_dlg:
        return function(*function_args, **function_kwargs)
        
    wait_result = [None]

    if not frames:
        # Определить кадры по умолчанию
        wait_dir = os.path.join(os.path.dirname(__file__), 'Wait')
        frames = [wait_dir + 'logo.jpg']
    
    ic_proccess_dlg = wait_box = icThreadLoadProjectDlg(parent, frames, message, bAutoIncr=bAutoIncr)
        
    wait_box.setResultList(wait_result)
    # Запустить функцию ожидания
    _thread.start_new(wait_box.run, (function, function_args, function_kwargs))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_proccess_dlg = None
    return wait_result[0]


try:
    from ic.engine import glob_functions
except ImportError:
    print('ic_user IMPORT ERROR')


class icThreadLoadProjectDlg(wx.Dialog):

    def __init__(self, parent, frames, message, min_value=0, max_value=100, style=0, bAutoIncr=False):
        """
        Конструктор.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type message: C{string}
        @param message: Сообщение верхнего индикатора.
        @type min_value: C{int}
        @param min_value: Минимальное значение верхнего индикатора.
        @type max_value: C{int}
        @param max_value: Максимальное значение верхнего индикатора.
        @type style: C{int}
        @param style: Стиль окна процесса.
        @type bAutoIncr: C{bool}
        @param bAutoIncr: Признак автоматического изменения состояния индикаторов.
            Используется в тех случаях, когда размерность процесса не определена,
            а показывать чего то надо.
        """
        if parent:
            self.defBackClr = parent.GetBackgroundColour()
        else:
            app = glob_functions.getEngine()
            if app:
                parent = app.GetTopWindow()
                self.defBackClr = app.GetTopWindow().GetBackgroundColour()
            else:
                self.defBackClr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        style = wx.STAY_ON_TOP
        w, h = wx.ScreenDC().GetSize()
        self._ani = [bmpfunc.icCreateBitmap(pic_name) for pic_name in frames]
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
        pre.Create(parent, -1, pos=(x, y), size=(sx, sy), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)
        
        # Индекс состояния анимации
        self._cur_ani_state = 0
        self._max_ani_state = len(frames)
        self._delay = 0.3
        self._autoIncr = bAutoIncr

        self.title = ''
        self.label = message
        self.min = min_value
        self.max = max_value
        self.value = min_value
        
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
        
        self.timer = wx.FutureCall(1, self.onTimer, None)
        
    def DirectRefresh(self):
        """
        """
        evt = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(evt)

    def setResultList(self, ResultList_):
        self._result_list = ResultList_
        
    def setNextState(self):
        """
        Сменить состояние.
        """
        self._cur_ani_state += 1
        if self._cur_ani_state >= self._max_ani_state:
            self._cur_ani_state = 0
        return self._cur_ani_state
    
    def drawFrame(self, NFrame_):
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

    def drawLabel(self, dc, label=None, label2=None):
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

    def drawIndicator(self, dc):
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
            
    def drawPic(self, n_frame, dc, bClear=False):
        """
        Отрисовка кадра.
        @param n_frame: Номер кадра.
        """
        if self._ani:
            sx, sy = self.GetSize()
            bmp = self._ani[n_frame]
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
        
    def onCheckClose(self, event=None):
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
        self.drawPic(self.setNextState(), dc)

        #   Отрисовываем сообщение
        self.drawLabel(dc)

        #   Отрисовываем индикатор процесса
        self.drawIndicator(dc)
        
        dc.EndDrawing()
        
        if evt:
            evt.Skip
        
        self.onCheckClose()
        
    def onTimer(self, evt):
        """
        """
        if self._autoIncr:
            self.value += 10
            if self.value > self.max:
                self.value = self.min
                    
        self.OnPaint(None)
        
        #   Сохраняем текущие параметры
        self.saveParameter()

    def run(self, function, function_args, function_kwargs):
        """
        Запуск ожидания функции.
        """
        self._running = True
        result = function(*function_args, **function_kwargs)
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
        
    def saveParameter(self):
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
        setLoadProccessBoxLabel('Count x:' + str(x), x)
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
