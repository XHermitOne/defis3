#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол конструктора WMS объекта.
"""

import wx

from ic.bitmap import bmpfunc

__version__ = (0, 0, 0, 1)


class icWMSWarehouseContructorCtrl(wx.ScrolledWindow):
    """
    Контрол конструктора склада.
    """

    def __init__(self, parent, ID=-1):
        """
        Конструктор.
        :param parent: Родительское wx.Window окно.
        :param ID: Идентификатор wx.ID.
        """
        wx.ScrolledWindow.__init__(self, parent, ID)
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        # self.bg_bmp = images.Background.GetBitmap()
        self.bg_bmp = None
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)

        # Make a shape from an image and mask.  This one will demo
        # dragging outside the window
        bmp = bmpfunc.createLibraryBitmap('A4album.png')

        # bmp = images.TestStar.GetBitmap()
        # bmp = wx.Bitmap('bitmaps/toucan.png')
        shape = icWMSBoxShape(bmp)
        shape.pos = (5, 5)
        shape.fullscreen = True
        self.shapes.append(shape)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def OnLeaveWindow(self, event):
        """
        We're not doing anything here, but you might have reason to.
        for example, if you were dragging something, you might elect to
        'drop it' when the cursor left the window.
        """
        pass

    def TileBackground(self, dc):
        """
        tile the background bitmap.
        """
        if self.bg_bmp is None:
            return
        sz = self.GetClientSize()
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()

        x = 0

        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h

            x = x + w

    def DrawShapes(self, dc):
        """
        Go through our list of shapes and draw them in whatever place they are.
        """
        for shape in self.shapes:
            if shape.shown:
                shape.draw(dc)

    def FindShape(self, pt):
        """
        This is actually a sophisticated 'hit test', but in this
        case we're also determining which shape, if any, was 'hit'.
        """
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
        return None

    def OnEraseBackground(self, event):
        """
        Clears the background, then redraws it. If the DC is passed, then
        we only do so in the area so designated. Otherwise, it's the whole thing.
        """
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, event):
        """
        Fired whenever a paint event occurs
        """
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self.DrawShapes(dc)

    def OnLeftDown(self, event):
        """
        Left mouse button is down.
        """
        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(event.GetPosition())

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            self.dragShape = shape
            self.dragStartPos = event.GetPosition()

    def OnLeftUp(self, event):
        """
        Left mouse button up.
        """
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        if self.hiliteShape:
            self.RefreshRect(self.hiliteShape.GetRect())
            self.hiliteShape = None

        # reposition and draw the shape

        # Note by jmg 11/28/03
        # Here's the original:
        #
        # self.dragShape.pos = self.dragShape.pos + event.GetPosition() - self.dragStartPos
        #
        # So if there are any problems associated with this, use that as
        # a starting place in your investigation. I've tried to simulate the
        # wx.Point __add__ method here -- it won't work for tuples as we
        # have now from the various methods
        #
        # There must be a better way to do this :-)
        #

        self.dragShape.pos = (
            self.dragShape.pos[0] + event.GetPosition()[0] - self.dragStartPos[0],
            self.dragShape.pos[1] + event.GetPosition()[1] - self.dragStartPos[1]
            )

        self.dragShape.shown = True
        self.RefreshRect(self.dragShape.GetRect())
        self.dragShape = None

    def OnMotion(self, event):
        """
        The mouse is moving
        """
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not event.Dragging() or not event.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = event.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.dragShape.GetRect(), True)
            self.Update()

            if self.dragShape.text:
                self.dragImage = wx.DragString(self.dragShape.text,
                                              wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.dragImage = wx.DragImage(self.dragShape.bmp,
                                             wx.StockCursor(wx.CURSOR_HAND))

            hotspot = self.dragStartPos - self.dragShape.pos
            self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

            self.dragImage.Move(pt)
            self.dragImage.Show()


        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.dragShape and self.dragImage:
            onShape = self.FindShape(event.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hiliteShape:
                if onShape is None or self.hiliteShape is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hiliteShape and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.dragImage.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hiliteShape.Draw(dc)
                self.hiliteShape = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hiliteShape = onShape
                self.hiliteShape.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.dragImage.Move(event.GetPosition())
            if unhiliteOld or hiliteNew:
                self.dragImage.Show()


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    frame = wx.Frame(None)

    panel = icWMSWarehouseContructorCtrl(frame)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
