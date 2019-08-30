#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговые окна прогресс бара.
"""

import os
import os.path
import time
import _thread
import wx
import wx.lib.imagebrowser

from ic.components import icfont
import ic.utils.execfunc   # Этот модуль подгружается для спецификации
from ic.bitmap import bmpfunc
from ic.utils import filefunc

__version__ = (0, 1, 1, 1)

# Класс и функции индикатора процесса
ic_proccess_dlg = None


def proccess_deco(function):
    """
    Декоратор для индикатора процесса с одной полосой индикации.
    Первым параметром обкладываемой функции, должна быть ссылка на оконный объект,
    который будет являтся родительским окном для индикатора процесса.
    """
    def func(*arg, **kwarg):
        if issubclass(arg[0].__class__, wx.Window):
            return proccess_function(arg[0], u'Подождите     ', function, arg, kwarg)
        else:
            return proccess_function(None, u'Подождите     ', function, arg, kwarg)
    return func


def proccess_noparent_deco(function):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return proccess_function(None, u'Подождите   ', function, arg, kwarg)
    return func


def proccess_noparent_deco_auto(function):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return proccess_function(None, u'Подождите   ', function, arg, kwarg, bAutoIncr=True)
    return func


def proccess2_deco(function):
    """
    Декоратор для индикатора процесса с двумя полосами индикации.
    Первым параметром обкладываемой функции, должна быть ссылка на оконный объект,
    который будет являтся родительским окном для индикатора процесса.
    """
    def func(*arg, **kwarg):
        if issubclass(arg[0].__class__, wx.Window):
            return proccess_function(arg[0], u'Подождите     ', function, arg, kwarg, bDoubleLine=True)
        else:
            return proccess_function(None, u'Подождите     ', function, arg, kwarg, bDoubleLine=True)
    return func


def proccess2_noparent_deco(function):
    """
    Декоратор для индикатора процесса с двумя полосами индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return proccess_function(None, u'Подождите   ', function, arg, kwarg, bDoubleLine=True)
    return func


def setProccessBoxLabel(label=None, value=None, label2=None, value2=None):
    """
    Функция изменяет параметры индикатора процесса. Если значение любого из
    параметров None, то значение параметра на индикаторе не меняется.
    Примеры:
        1. setProccessBoxLabel('Wait...', 10, 'Пересчет', 20)
        2. setProccessBoxLabel('Wait...', 20)
        3. setProccessBoxLabel(label2='Пересчет', value2=30)
    
    @type label: C{string}
    @param label: Текст сообщения на верхней полосе индикации.
    @type value: C{int}
    @param value: Значение верхней полосы индикации от 0 до 100.
    @type label2: C{string}
    @param label2: Текст сообщения на второй полосе индикации (если она есть).
    @type value2: C{int}
    @param value2: Значение второй полосы индикации от 0 до 100 (если она есть).
    """
    if ic_proccess_dlg:
        sx, sy = ic_proccess_dlg.GetSize()
        
        if label or label2:
            if label and label2 and len(label) >= len(label2):
                Lbl = label
            elif label and label2 and len(label) < len(label2):
                Lbl = label2
            elif label is not None:
                Lbl = label
            else:
                Lbl = label2

            cx = (len(Lbl)*7) + 20

            if cx > sx:
                ic_proccess_dlg.SetSize((cx, sy))
                ic_proccess_dlg.Centre()
            
        ic_proccess_dlg.SetLabel(label)
        ic_proccess_dlg.SetValue(value)
        ic_proccess_dlg.SetLabel2(label2)
        ic_proccess_dlg.SetValue2(value2)
        

def proccess_function(parent, message,
                      function, function_args=(), function_kwargs={},
                      frames=None, bDoubleLine=False, bAutoIncr=False):
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
        frames = [wait_dir + 'Wait1.png',
                  wait_dir +'Wait2.png',
                  wait_dir +'Wait3.png',
                  wait_dir +'Wait4.png',
                  wait_dir +'Wait5.png',
                  wait_dir +'Wait6.png',
                  wait_dir +'Wait7.png',
                  wait_dir +'Wait8.png',
                  wait_dir +'Wait9.png',
                  wait_dir +'Wait10.png',
                  wait_dir +'Wait11.png',
                  wait_dir +'Wait12.png',
                  wait_dir +'Wait13.png',
                  wait_dir +'Wait14.png',
                  wait_dir +'Wait15.png']

    if bDoubleLine:
        ic_proccess_dlg = wait_box = icThreadMessageBox(parent, frames, message,
                                                        message2='', min_value2=0, max_value2=100, bAutoIncr=bAutoIncr)
    else:
        ic_proccess_dlg = wait_box = icThreadMessageBox(parent, frames, message, bAutoIncr=bAutoIncr)
        
    wait_box.setResultList(wait_result)
    # Запустить функцию ожидания
    _thread.start_new(wait_box.run, (function, function_args, function_kwargs))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_proccess_dlg = None
    return wait_result[0]


from ic.engine import glob_functions


class icThreadMessageBox(wx.Dialog):
    def __init__(self, parent, frames, message, min_value=0, max_value=100,
                 message2=None, min_value2=None, max_value2=None, style=0, bAutoIncr=False):
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
        @type message2: C{string}
        @param message2: Сообщение нижнего индикатора.
        @type min_value2: C{int}
        @param min_value2: Минимальное значение нижнего индикатора.
        @type max_value2: C{int}
        @param max_value2: Максимальное значение нижнего индикатора.
        @type style: C{int}
        @param style: Стиль окна процесса.
        @type bAutoIncr: C{bool}
        @param bAutoIncr: Признак автоматического изменения состояния индикаторов.
            Используется в тех случаях, когда размерность процесса не определена,
            а показывать чего то надо.
        """
        if message2 is not None:
            sy = 70
        else:
            sy = 40

        if parent:
            self.defBackClr = parent.GetBackgroundColour()
        else:
            app = glob_functions.getEngine()
            if app:
                parent = app.GetTopWindow()
                self.defBackClr = app.GetTopWindow().GetBackgroundColour()
            else:
                self.defBackClr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        if parent is None:
            style = wx.STAY_ON_TOP

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, size=wx.Size(150, sy), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        self._ani = [bmpfunc.icCreateBitmap(frame_file_name) for frame_file_name in frames]
        self._cur_ani_state = 0     # Индекс состояния анимации
        self._max_ani_state = len(frames)
        self._delay = 0.3
        self._autoIncr = bAutoIncr

        if self._ani:
            self._pic_size = (self._ani[0].GetWidth(), self._ani[0].GetHeight())
        else:
            self._pic_size = (0, 0)

        self.title = ''
        self.label = message
        self.label2 = message2
        self.min = min_value
        self.max = max_value
        self.value = min_value
        self.min2 = min_value2
        self.max2 = max_value2
        self.value2 = min_value2
        
        #
        self.indBgrClr = wx.Colour(230, 230, 230)
        self.indClr = wx.Colour(100, 100, 135)
        
        self.indBgrBrush = wx.Brush(self.indBgrClr, wx.SOLID)
        self.indBrush = wx.Brush(self.indClr, wx.SOLID)
            
        self.bgrBrush = wx.Brush(self.defBackClr, wx.SOLID)
        self.font = icfont.icFont({})
        
        # Высота индикатора
        self.indH = 15
        
        self.CenterOnScreen()
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
        event = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(event)

    def setResultList(self, result_list):
        self._result_list = result_list
        
    def setNextState(self):
        """
        Сменить состояние.
        """
        self._cur_ani_state += 1
        if self._cur_ani_state >= self._max_ani_state:
            self._cur_ani_state = 0
        return self._cur_ani_state

    def drawFrame(self, n_frame):
        """
        Отрисовка кадра.
        @param n_frame: Номер кадра.
        """
        frame_bmp = self._ani[n_frame]
        
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
        if label2 is None:
            label2 = self.label2
        
        if self._ani:
            px = self._ani[0].GetWidth()
        else:
            px = 0
        
        sx, sy = self.GetSize()
        w, h = self.GetTextExtent('W')
        x = 10 + px
        y = 3
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetFont(self.font)
        
        if label:
            dc.DrawText(label, x, y)
        
        if label2:
            y = y + h + 3 + self.indH
            dc.DrawText(label2, x, y)

    def drawIndicator(self, dc):
        """
        Рисует индикатор процесса.
        """
        if self._ani:
            px = self._ani[0].GetWidth()
        else:
            px = 0

        sx, sy = self.GetSize()
        w, h = self.GetTextExtent('W')
        width = sx - (px+15)
        H = self.indH
        hh = h+5
        
        #   Рисуем первый индикатор
        pen = wx.Pen(wx.Colour(50, 50, 50))
        dc.SetPen(pen)
        dc.SetBrush(self.indBgrBrush)
        
        if self.value is not None:
            dc.DrawRectangle(px+5, hh, width, H)
    
            #   Состояние индикатора
            dc.SetBrush(self.indBrush)
            dc.DrawRectangle(px+5, hh, width*(self.value-self.min)/(self.max-self.min), H)
            
            #   Проценты
            if (self.value - self.min) < (self.max - self.value):
                dc.SetTextForeground(self.indClr)
                xx = px+5 + width*3/4
                dc.DrawText('%d%%' % int(100*(self.value-self.min)/(self.max-self.min)), xx, hh+1)
            else:
                dc.SetTextForeground(self.indBgrClr)
                xx = px+5 + width/4
                dc.DrawText('%d%%' % int(100*(self.value-self.min)/(self.max-self.min)), xx, hh+1)

        #   Рисуем второй индикатор
        if self.value2 is not None:
            if self.label2:
                hh = hh + H + w + 5
            else:
                hh = hh + H + 5
            
            if self.max2 is not None:
                dc.SetBrush(self.indBgrBrush)
                dc.DrawRectangle(px+5, hh, width, H)
        
                #   Состояние индикатора
                dc.SetBrush(self.indBrush)
                dc.DrawRectangle(px+5, hh, width*(self.value2-self.min2)/(self.max2-self.min2), H)
                
                #   Проценты
                if (self.value2 - self.min2) < (self.max2 - self.value2):
                    dc.SetTextForeground(self.indClr)
                    xx = px+5 + width*3/4
                    dc.DrawText('%d%%' % int(100*(self.value2-self.min2)/(self.max2-self.min2)), xx, hh+1)
                else:
                    dc.SetTextForeground(self.indBgrClr)
                    xx = px+5 + width/4
                    dc.DrawText('%d%%' % int(100*(self.value2-self.min2)/(self.max2-self.min2)), xx, hh+1)

    def drawPic(self, n_frame, dc, bClear=False):
        """
        Отрисовка кадра.
        @param n_frame: Номер кадра.
        """
        if self._ani:
            sx, sy = self.GetSize()
            bmp = self._ani[n_frame]
            px, py = self._pic_size
            y = (sy - py)/2
            x = 0
            
            if bClear:
                pen = wx.Pen(self.defBackClr)
                dc.SetPen(pen)
                dc.DrawRectangle(x+1, y, px, py)

            memDC = wx.MemoryDC()
            memDC.SelectObject(bmp)
            dc.Blit(x, y, px, py, memDC, 0, 0, wx.COPY, True)
        
    def isParChanged(self):
        """
        Возаращает признак изменения параметров индикатора.
        """
        sz = self.GetSize()
        pos = self.GetPosition()
        
        return (sz != self._oSize or pos != self._oPos or
                self._oPar != (self.min, self.max, self.value, self.min2, self.max2, self.value2, self.label))
        
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

    def OnPaint(self, event=None):
        """
        """
        t = time.clock()
        
        self.old_time = t
        dc = wx.WindowDC(self)
        dc.SetBrush(self.bgrBrush)
        
        #   Если параменты индикатора не менялись, то перерисовываем только картинку
        if not self.isParChanged():
            self.drawPic(self.setNextState(), dc, True)
            self.onCheckClose()
            return
            
        dc.BeginDrawing()
        pen = wx.Pen(wx.Colour(100, 100, 100))
        dc.SetPen(pen)
        sx, sy = self.GetSize()
        px, py = self._pic_size
        
        dc.SetBrush(self.bgrBrush)
        
        #   Чистим
        dc.DrawRectangle(0, 0, sx, sy)

        #   Отрисовываем сообщение
        self.drawLabel(dc)

        #   Отрисовываем индикатор процесса
        self.drawIndicator(dc)
        
        #   Отрисовываем картинку
        self.drawPic(self.setNextState(), dc)
        
        dc.EndDrawing()
        
        if event:
            event.Skip
        
        self.onCheckClose()
        
    def onTimer(self, event):
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

    def setLabel2(self, label2=None):
        """
        Устанавливает текст второй полосы индикации процесса.
        """
        if label2 is not None:
            self.label2 = label2
        
    def saveParameter(self):
        """
        Сохраняет параметры индикатора.
        """
        self._oSize = self.GetSize()
        self._oPos = self.GetPosition()
        self._oPar = (self.min, self.max, self.value,
                      self.min2, self.max2, self.value2, self.label)

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

    def setValue2(self, value2):
        """
        Устанавливает значение второй полосы индикации процесса.
        """
        if value2 is None:
            return
        
        if value2 < self.min2:
            self.value2 = self.min2
        elif value2 > self.max2:
            self.value2 = self.max2
        else:
            self.value2 = value2


@proccess2_noparent_deco
def f(parent):
    """
    """
    for x in range(10):
        setProccessBoxLabel('Count x:' + str(x), 10 * x)
        for y in range(10):
            setProccessBoxLabel(label2='Count y:' + str(y), value2=10 * y)
            time.sleep(0.05)


def test(par=0):
    """
    Тестируем класс icHeadCell.
    """

    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    frame.Show(True)
    
    load_component_proccess()

    app.MainLoop()


if __name__ == '__main__':
    test(0)
