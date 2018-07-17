#!/usr/bin/env python

"""
Show how to have wx draw a cursor over an axes that moves with the
mouse and reports the data coords
"""

import datetime
import wx
import matplotlib.numerix as numerix
from matplotlib.numerix import arange, sin, pi
from matplotlib import pylab

import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.backends.backend_wx import Toolbar, FigureManager

from matplotlib.figure import Figure

from matplotlib.dates import HourLocator, drange, timezone


matplotlib.use('WXAgg')

__version__ = (0, 0, 1, 2)


class icCanvasPanel(wx.Panel):
    
    def __init__(self, parent, id=-1, pos=(-1, -1), size=(-1, -1)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.count = 0
        
        self.SetBackgroundColour(wx.NamedColor('WHITE'))
        self.figure = Figure()

        # ---
        dd = 10

        # --- Plot2
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')

        date1 = datetime.datetime(2000, 3, 2, 10, tzinfo=tz)
        date2 = datetime.datetime(2000, 3, 2, 15, tzinfo=tz)
        delta = datetime.timedelta(minutes=5)
        dates = drange(date1, date2, delta)
        
        self.axes1 = self.figure.add_subplot(111)

        yy = pylab.arrayrange( len(dates)*1.0)
        majorTick = HourLocator(range(0, 25, 1), tz=tz)
        
        ysq = [y*y/dd for y in yy]
        line = self.axes1.plot_date(dates, ysq, tz=tz)
        
        self.axes1.xaxis.set_major_locator(majorTick)
        self.axes1.set_xlabel('Time (s)')
        self.axes1.set_ylabel('Price 2 ($)') 

        #
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)

        # --- Add Toolbar
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()       
        
        # On Windows, default frame size behaviour is incorrect
        # you don't need this under Linux
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))

        # Create a figure manager to manage things
        self.figmgr = FigureManager(self.canvas, 1, self)

        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        self.toolbar.update()
        self.statusBar = wx.StatusBar(self, -1)
        self.statusBar.SetFieldsCount(1)
        self.sizer.Add(self.statusBar, 0, wx.EXPAND)

        self.Fit()
        
        # --- Обработчики событий
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def GetToolBar(self):
        """
        You will need to override GetToolBar if you are using an unmanaged toolbar in your frame.
        """
        return self.toolbar

    def mouse_move(self, event):
        self.draw_cursor(event)

    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()

    def OnButton(self, evt):
        """
        """
        dd = 20
        t = arange(0.0, 3.0, 1.0/dd)
        s = [10+y*y/dd+self.count for y in xrange(0, 3*dd)]
        self.count += 5
        self.axes.lines.pop(0)
        
        line, = self.axes.plot(t, s, 'r:d')
        line.set_markersize(5)
        self.Refresh()
        evt.Skip()
        
    def OnPaint(self, event):
        self.erase_cursor()
        try:
            del self.lastInfo
        except AttributeError:
            pass
        self.canvas.draw()
        event.Skip()
        
    def draw_cursor(self, event):
        """
        event is a MplEvent.  Draw a cursor over the axes.
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
        self.statusBar.SetStatusText('Time=%f  Price=%f' % (time, price), 0)

    def erase_cursor(self):
        try:
            lastline1, lastline2, lastax, lastdc = self.lastInfo
        except AttributeError:
            pass
        else:
            lastdc.DrawLine(*lastline1)     # erase old
            lastdc.DrawLine(*lastline2)     # erase old


def test(par=0):
    """
    Тестируем класс icCanvasPanel
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'icButton Test')
    panel = icCanvasPanel(frame, -1, (0, 0), (200, 200))
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
