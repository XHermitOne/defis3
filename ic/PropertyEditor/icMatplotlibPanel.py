#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Jeremy O'Donoghue, 2003.
 
License: This work is licensed under the PSF. A copy should be included
with this source code, and is also available at
http://www.python.org/psf/license.html

This is a sample showing how to embed a matplotlib figure in a wxPanel.

The example implements the full navigation toolbar, so you can automatically
inherit standard matplotlib features such as the ability to zoom, pan and
save figures in the supported formats.

There are a few small complexities worth noting in the example:
    
1) By default, a wxFrame can contain a toolbar (added with SetToolBar())
   but this is at the top of the frame. Matplotlib default is to put the
   controls at the bottom of the frame, so you have to manage the toolbar
   yourself. I have done this by putting the figure and toolbar into a
   sizer, but this means that you need to override GetToolBar for your
   wxFrame so that the figure manager can find the toolbar.
   
2) I have implemented a figure manager to look after the plots and axes.
   If you don't want a toolbar, it is simpler to add the figure directly
   and not worry. However, the figure manager looks after clipping of the
   figure contents, so you will need it if you want to navigate
   
3) There is a bug in the way in which my copy of wxPython calculates
   toolbar width on Win32, so there is a tricky line to ensure that the
   width of the toolbat is the same as the width of the figure.
   
4) Depending on the parameters you pass to the sizer, you can make the
   figure resizable or not.
"""

import datetime
import wx
import matplotlib
from matplotlib.backends.backend_wx import Toolbar, FigureManager
from matplotlib.backends.backend_wx import FigureCanvasWx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvasWxAgg
from matplotlib.figure import Figure
import matplotlib.numerix as numpy
from matplotlib.dates import HourLocator, drange, timezone, num2date
from matplotlib import pylab

matplotlib.use('WX')
matplotlib.use('WXAgg')

__version__ = (0, 0, 1, 2)


class icPloterToolbar(Toolbar):
    def __init__(self, *arg, **kwarg):
        Toolbar.__init__(self, *arg, **kwarg)
        
    def set_active(self, ind):
        """
        ind is a list of index numbers for the axes which are to be made active
        """
        self._ind = ind
        if ind is not None and len(self._axes) == len(self._ind):
            self._active = []
            for i in self._ind:
                if i+1 <= len(self._axes):
                    self._active.append(self._axes[i])
        else:
            self._active = []
        # Now update button text wit active axes
        self._menu.updateButtonText(ind)


class icPlotPanel(wx.Panel):
    """
    """
    def __init__(self, parent, id=-1, pos=(-1, -1), size=(-1, -1), style=0, bWxAgg=False):
        wx.Panel.__init__(self, parent, id, pos, size, style=style)

        self.fig = Figure((5, 4), 75)

        if bWxAgg:
            self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        else:
            self.canvas = FigureCanvasWx(self, -1, self.fig)
            
        self.canvas.mpl_connect('motion_notify_event', self.OnMouseMove)
        self.canvas.mpl_connect('button_press_event', self.OnMouseLeftDown)
        
        self.toolbar = icPloterToolbar(self.canvas)
        self.toolbar.Realize()
        self.parent = parent
        self.legendLst = []

        # --- Атрибуты курсора
        #   Положение курсора
        self._cursor = None
        #   Значение курсора
        self._cursorVal = None
        #   Статический курсор - значение обновляется только при нажантии
        #   левой кнопки мыши
        self._statCursor = None
        
        # On Windows, default frame size behaviour is incorrect
        # you don't need this under Linux
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))

        # Create a figure manager to manage things
        self.figmgr = FigureManager(self.canvas, 1, self)
        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        # Best to allow the toolbar to resize!
        sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(sizer)
        self.Fit()
        
        # --- Описание обработчиков
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        # --- Инициализация графика
        self.init_graph()

    def draw_cursor(self, event):
        """
        event is a MplEvent.  Draw a cursor over the axes
        """
        if event.inaxes is None:
            self.erase_cursor()
            try:
                del self.lastInfo
            except AttributeError:
                pass
            return
            
        canvas = self.canvas
        figheight = canvas.figure.bbox.height()
        ax = event.inaxes
        left, bottom, width, height = ax.bbox.get_bounds()
        bottom = figheight-bottom
        top = bottom - height
        right = left + width
        x, y = event.x, event.y
        y = figheight-y

        dc = wx.ClientDC(canvas)
        dc.SetLogicalFunction(wx.XOR)
        wbrush = wx.Brush(wx.Colour(255, 255, 255), wx.TRANSPARENT)
        wpen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.SOLID)
        dc.SetBrush(wbrush)
        dc.SetPen(wpen)
            
        dc.ResetBoundingBox()
        dc.BeginDrawing()

        x, y, left, right, bottom, top = [int(val) for val in x, y, left, right, bottom, top]

        self.erase_cursor()
        line1 = (x, bottom, x, top)
        line2 = (left, y, right, y)
        self.lastInfo = line1, line2, ax, dc
        dc.DrawLine(*line1)     # draw new
        dc.DrawLine(*line2)     # draw new
        dc.EndDrawing()

        time, price = event.xdata, event.ydata
        
        try:
            tm = str(num2date(time))[:16]
        except:
            tm = time
        
        self._cursor = (time, price)
        self._cursorVal = (tm, price)

    def erase_cursor(self):
        try:
            lastline1, lastline2, lastax, lastdc = self.lastInfo
        except AttributeError:
            pass
        else:
            lastdc.DrawLine(*lastline1)     # erase old
            lastdc.DrawLine(*lastline2)     # erase old

    def GetToolBar(self):
        """
        You will need to override GetToolBar if you are using an unmanaged toolbar in your frame.
        """
        return self.toolbar
    
    def GetCursorPos(self):
        """
        Возвращает положение курсора.
        """
        return self._cursor

    def GetCursorVal(self):
        """
        Возвращает значение курсора - временная координата приведена в
        читаемый вид - YYYY-MM-DD HH:MM:SS.
        """
        return self._cursorVal
        
    def GetStaticCursor(self):
        """
        Возвращает значение статического курсора - значение которого обновляется
        только при нажантии левой кнопки мыши.
        """
        return self._statCursor
        
    def init_graph(self):
        """
        Инициализация графика.
        """
        self.canvas.figure.set_facecolor('#f5f5f5')
        self.subplot = a = self.fig.add_subplot(111)
        
        a.grid(True)
        self.toolbar.update()
        
    def OnMouseMove(self, evt):
        """
        """
        self.draw_cursor(evt)
        
    def OnMouseLeftDown(self, evt):
        """
        """
        self._statCursor = self.GetCursorPos()
        
    def OnPaint(self, evt):
        """
        """
        self.erase_cursor()
        try:
            del self.lastInfo
        except AttributeError:
            pass
            
        self.canvas.draw()
        evt.Skip()

    def plot_data(self):
        a = self.subplot
        t = numpy.arange(0.0, 3.0, 0.01)
        s = numpy.sin(2*numpy.pi*t)
        c = numpy.cos(2*numpy.pi*t)
        a.plot(t, c, 'r:o')

    def add_plot_date(self, dates, values, format=None, xlabel=None, ylabel=None,
                      bClear=True, titlePlot='Title', legend='Legend'):
        """
        Наполняет график точками.
        
        @type dates: C{list | tuple}
        @param dates: Список дат в формате datetime.
        @type values: C{list | tuple}
        @param values: Список значений.
        @type dates: C{list | tuple}
        @param dates: Список дат в формате datetime.
        @type xlabel: C{string}
        @param xlabel: Подпись оси X.
        @type ylabel: C{string}
        @param ylabel: Подпись оси Y.
        @type bClear: C{bool}
        @param bClear: Признак того, что необходимо все предыдущие точки удалить
            из графика.
        @type titlePlot: C{string}
        @param titlePlot: Заголовок.
        @type legend: C{string}
        @param legend: Легенда.
        """
        if bClear:
            self.subplot.lines = []
            self.legendLst = []
            
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')
        
        majorTick = HourLocator(range(0, 25, 3), tz=tz)

        line = self.subplot.plot_date(dates, values, format, tz=tz)

        self.subplot.xaxis.set_major_locator(majorTick)

        #   Устанавливаем легенду
        self.legendLst.append(legend)
        self.subplot.legend(self.subplot.lines, self.legendLst, 'upper right',
                            shadow=True)
        
    def set_date_plot2(self, date1=None, date2=None):
        """
        """
        # --- Plot2
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')
        
        if not date1:
            date1 = datetime.datetime(2000, 3, 2, 0, tzinfo=tz)
        else:
            date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], tzinfo=tz)
            
        if not date2:
            date2 = datetime.datetime(2000, 3, 2, 23, tzinfo=tz)
        else:
            date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], tzinfo=tz)

        delta = datetime.timedelta(minutes=20)
        dates = drange(date1, date2, delta)
        
        dd=10
        yy = pylab.arrayrange( len(dates)*1.0)
        ysq = [y*y/dd for y in yy]
        
        self.add_plot_date(dates, ysq, 'bo', 'Время', 'Цена', legend='Скорость')
        self.add_plot_date(dates, yy, 'r-d', bClear=False)

        labels = self.subplot.get_xticklabels()
        pylab.set(labels, 'rotation', 45, size=10)

        
if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    frame = wx.Frame(None, -1, 'Test embedded wxFigure')
    pnl = icPlotPanel(frame, bWxAgg=True)
    pnl.set_date_plot2()

    frame.Show()
    app.MainLoop()
