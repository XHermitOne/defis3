#!/usr/bin/env python
# embedding_in_wx.py
# 

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
import matplotlib
import wx
from matplotlib.backends.backend_wx import Toolbar, FigureCanvasWx, FigureManager

from matplotlib.figure import Figure
import matplotlib.numerix as numpy

from matplotlib.dates import HourLocator, drange, timezone
from matplotlib import pylab

matplotlib.use('WX')

__version__ = (0, 0, 1, 2)


class PlotFigure(wx.Panel):
    def __init__(self, parent, id=-1, pos=(-1, -1), size=(-1, -1), style=0):
        wx.Panel.__init__(self, parent, id, pos, size, style=style)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvasWx(self, -1, self.fig)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

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

        # --- Инициализация графика
        self.init_graph()

    def GetToolBar(self):
        """
        You will need to override GetToolBar if you are using an unmanaged toolbar in your frame.
        """
        return self.toolbar
        
    def init_graph(self):
        """
        Инициализация графика. 
        """
        self.subplot = a = self.fig.add_subplot(111)
        a.set_ylabel(u'Цена ($)\n')
        a.set_xlabel(u'Время')
        self.toolbar.update()
        
    def plot_data(self):
        a = self.subplot
        t = numpy.arange(0.0, 3.0, 0.01)
        s = numpy.sin(2*numpy.pi*t)
        c = numpy.cos(2*numpy.pi*t)
        a.plot(t, c, 'r:o')

    def add_plot_date(self, dates, values, format=None, xlabel=None, ylabel=None, bClear=True):
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
        """
        if bClear:
            self.subplot.lines = []
        
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')
        
        majorTick = HourLocator(range(0, 25, 1), tz=tz)

        line, = self.subplot.plot_date(dates, values, format, tz=tz)
        line.set_markersize(3)
        
        self.subplot.xaxis.set_major_locator(majorTick)
        if xlabel:
            self.subplot.set_xlabel(xlabel)
            
        if ylabel:
            self.subplot.set_ylabel(ylabel+'\n')
        
    def set_date_plot2(self, date1=None, date2=None):
        """
        """
        # --- Plot2
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')

        date1 = datetime.datetime(2000, 3, 2, 10, tzinfo=tz)
        date2 = datetime.datetime(2000, 3, 2, 15, tzinfo=tz)
        delta = datetime.timedelta(minutes=5)
        dates = drange(date1, date2, delta)
        
        dd = 10
        yy = pylab.arrayrange(len(dates)*1.0)
        ysq = [y*y/dd for y in yy]
        
        self.add_plot_date(dates, ysq, 'b-o', u'Время', u'Цена')
        self.add_plot_date(dates, yy, 'r-d', bClear=False)
                

if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    frame = wx.Frame(None, -1, 'Test embedded wxFigure')
    pnl = PlotFigure(frame)
    pnl.set_date_plot2()
    frame.Show()
    app.MainLoop()
