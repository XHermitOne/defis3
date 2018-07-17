#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.imagebrowser

import ic.components.icfont as icfont
import ic.utils.ic_exec   # Этот модуль подгружается для спецификации
import ic.bitmap.ic_bmp as ic_bmp
from ic.utils import ic_file
import time
import thread


# Класс и функции индикатора процесса
ic_proccess_dlg = None


def proccess_deco(f):
    """
    Декоратор для индикатора процесса с одной полосой индикации.
    Первым параметром обкладываемой функции, должна быть ссылка на оконный объект,
    который будет являтся родительским окном для индикатора процесса.
    """
    def func(*arg, **kwarg):
        if issubclass(arg[0].__class__, wx.Window):
            return ProccessFunc(arg[0], 'Подождите     ', f, arg, kwarg)
        else:
            return ProccessFunc(None, 'Подождите     ', f, arg, kwarg)
    return func


def proccess_noparent_deco(f):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return ProccessFunc(None, 'Подождите   ', f, arg, kwarg)
    return func


def proccess_noparent_deco_auto(f):
    """
    Декоратор для индикатора процесса с одной полосой индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return ProccessFunc(None, 'Подождите   ', f, arg, kwarg, bAutoIncr=True)
    return func


def proccess2_deco(f):
    """
    Декоратор для индикатора процесса с двумя полосами индикации.
    Первым параметром обкладываемой функции, должна быть ссылка на оконный объект,
    который будет являтся родительским окном для индикатора процесса.
    """
    def func(*arg, **kwarg):
        if issubclass(arg[0].__class__, wx.Window):
            return ProccessFunc(arg[0], 'Подождите     ', f, arg, kwarg, bDoubleLine=True)
        else:
            return ProccessFunc(None, 'Подождите     ', f, arg, kwarg, bDoubleLine=True)
    return func


def proccess2_noparent_deco(f):
    """
    Декоратор для индикатора процесса с двумя полосами индикации (без указания
    родительского оконного объекта).
    """
    def func(*arg, **kwarg):
        return ProccessFunc(None, 'Подождите   ', f, arg, kwarg, bDoubleLine=True)
    return func


def SetProccessBoxLabel(label=None, value=None, label2=None, value2=None):
    """
    Функция изменяет параметры индикатора процесса. Если значение любого из
    параметров None, то значение параметра на индикаторе не меняется.
    Примеры:
        1. SetProccessBoxLabel('Wait...', 10, 'Пересчет', 20)
        2. SetProccessBoxLabel('Wait...', 20)
        3. SetProccessBoxLabel(label2='Пересчет', value2=30)
    
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
        

def ProccessFunc(Parent_, Msg_,
                 Func_, FuncArgs_=(), FuncKW_={},
                 Frames_=None, bDoubleLine=False, bAutoIncr=False):
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
        Frames_ = [wait_dir+'Wait1.png',
                   wait_dir+'Wait2.png',
                   wait_dir+'Wait3.png',
                   wait_dir+'Wait4.png',
                   wait_dir+'Wait5.png',
                   wait_dir+'Wait6.png',
                   wait_dir+'Wait7.png',
                   wait_dir+'Wait8.png',
                   wait_dir+'Wait9.png',
                   wait_dir+'Wait10.png',
                   wait_dir+'Wait11.png',
                   wait_dir+'Wait12.png',
                   wait_dir+'Wait13.png',
                   wait_dir+'Wait14.png',
                   wait_dir+'Wait15.png']

    if bDoubleLine:
        ic_proccess_dlg = wait_box = icThreadMessageBox(Parent_, Frames_, Msg_,
                                                        Msg2_='', min2=0, max2=100, bAutoIncr=bAutoIncr)
    else:
        ic_proccess_dlg = wait_box = icThreadMessageBox(Parent_, Frames_, Msg_, bAutoIncr=bAutoIncr)
        
    wait_box.SetResultList(wait_result)
    # Запустить функцию ожидания
    thread.start_new(wait_box.Run, (Func_, FuncArgs_, FuncKW_))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_proccess_dlg = None
    return wait_result[0]


from ic.engine import ic_user


class icThreadMessageBox(wx.Dialog):
    def __init__(self, Parent_, Frames_, Msg_, min=0, max=100,
                 Msg2_=None, min2=None, max2=None, style=0, bAutoIncr=False):
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
        @type Msg2_: C{string}
        @param Msg2_: Сообщение нижнего индикатора.
        @type min2: C{int}
        @param min2: Минимальное значение нижнего индикатора.
        @type max2: C{int}
        @param max2: Максимальное значение нижнего индикатора.
        @type style: C{int}
        @param style: Стиль окна процесса.
        @type bAutoIncr: C{bool}
        @param bAutoIncr: Признак автоматического изменения состояния индикаторов.
            Используется в тех случаях, когда размерность процесса не определена,
            а показывать чего то надо.
        """
        if Msg2_ is not None:
            sy = 70
        else:
            sy = 40

        if Parent_:
            self.defBackClr = Parent_.GetBackgroundColour()
        else:
            app = ic_user.icGetRunner()
            if app:
                Parent_ = app.GetTopWindow()
                self.defBackClr = app.GetTopWindow().GetBackgroundColour()
            else:
                self.defBackClr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        if Parent_ is None:
            style = wx.STAY_ON_TOP

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(Parent_, -1, size=wx.Size(150, sy), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        self._ani = [ic_bmp.icCreateBitmap(frame_file_name) for frame_file_name in Frames_]
        self._cur_ani_state = 0     # Индекс состояния анимации
        self._max_ani_state = len(Frames_)
        self._delay = 0.3
        self._autoIncr = bAutoIncr

        if self._ani:
            self._pic_size = (self._ani[0].GetWidth(), self._ani[0].GetHeight())
        else:
            self._pic_size = (0, 0)

        self.title = ''
        self.label = Msg_
        self.label2 = Msg2_
        self.min = min
        self.max = max
        self.value = min
        self.min2 = min2
        self.max2 = max2
        self.value2 = min2
        
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

    def DrawIndicator(self, dc):
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

    def DrawPic(self,NFrame_, dc, bClear=False):
        """
        Отрисовка кадра.
        @param NFrame_: Номер кадра.
        """
        if self._ani:
            sx, sy = self.GetSize()
            bmp = self._ani[NFrame_]
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
        if not self.isParChanged():
            self.DrawPic(self.NextState(), dc, True)
            self.OnCheckClose()
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
        self.DrawLabel(dc)

        #   Отрисовываем индикатор процесса
        self.DrawIndicator(dc)
        
        #   Отрисовываем картинку
        self.DrawPic(self.NextState(), dc)
        
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

    def SetLabel2(self, label2=None):
        """
        Устанавливает текст второй полосы индикации процесса.
        """
        if label2 is not None:
            self.label2 = label2
        
    def SavePar(self):
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

    def SetValue2(self, value2):
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
        SetProccessBoxLabel('Count x:' + str(x), 10*x)
        for y in range(10):
            SetProccessBoxLabel(label2='Count y:' + str(y), value2=10*y)
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
