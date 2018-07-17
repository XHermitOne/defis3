#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Рендеры используемые в DEFIS.
"""

# --- Imports ---
import wx
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed, ControlNormal

from ic.utils.graphicUtils import GetMidColor

# --- Specifications ---
SPC_IC_RENDERERXP = dict({
    'menubar_background_start_colour': (167, 202, 240),
    'menubar_background_end_colour': (167, 202, 240),

    'toolbar_background_start_colour': (224, 238, 252),
    'toolbar_background_end_colour': (159, 193, 232),
    'toolbar_background_start_colour_tail': (117, 166, 241),
    'toolbar_background_end_colour_tail': (6, 59, 150),
    'toolbar_background_colour': (159, 193, 232),
    'toolbar_background_colour_tail': (79, 129, 210),
    'toolbar_bottom_colour': (59, 97, 156),
    'toolbar_bottom_colour_tail': (0, 53, 145),

    'separator_col_start_colour': (241, 249, 255),
    'separator_col_end_colour': (106, 140, 203),

    'enable_text_colour': (0, 0, 0),    # wx.BLACK
    })
    
# Version 2.9.1
if wx.VERSION > (2, 8, 11, 10):
    wx.Colour = wx.Colour


class icRendererXPPrototype(RendererBase):
    """
    Xp-Style renderer.
    """

    def __init__(self):
        RendererBase.__init__(self)

        self.menubar_background_start_colour = wx.Colour(167, 202, 240)
        self.menubar_background_end_colour = wx.Colour(185, 214, 244)

        self.toolbar_background_start_colour = wx.Colour(224, 238, 252)
        self.toolbar_background_end_colour = wx.Colour(159, 193, 232)
        self.toolbar_background_start_colour_tail = wx.Colour(117, 166, 241)
        self.toolbar_background_end_colour_tail = wx.Colour(6, 59, 150)
        self.toolbar_background_colour = wx.Colour(159, 193, 232)
        self.toolbar_background_colour_tail = wx.Colour(79, 129, 210)
        self.toolbar_bottom_colour = wx.Colour(59, 97, 156)
        self.toolbar_bottom_colour_tail = wx.Colour(0, 53, 145)

        self.separator_col_start_colour = wx.Colour(241, 249, 255)
        self.separator_col_end_colour = wx.Colour(106, 140, 203)

        self.enable_text_colour = wx.BLACK
        self.toolBarWidth = 350

    def DrawButton(self, dc, rect, state, input=None):
        """
        Colors rectangle according to the XP theme.
        """

        if input is None or isinstance(input, bool):
            self.DrawButtonTheme(dc, rect, state, input)
        else:
            self.DrawButtonColour(dc, rect, state, input)

    def DrawButtonTheme(self, dc, rect, state, useLightColours=None):
        """
        Colors rectangle according to the XP theme.
        """

        # switch according to the status
        if wx.VERSION >= (2, 8, 11, 0, ''):
            if state == ControlFocus:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().BackgroundColour()
            elif state == ControlPressed:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().HighlightBackgroundColour()
            else:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().BackgroundColour()
        else:
            if state == ControlFocus:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().BackgroundColor()
            elif state == ControlPressed:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().HighlightBackgroundColor()
            else:
                penColor = ArtManager.Get().FrameColour()
                brushColor = ArtManager.Get().BackgroundColor()
            
        # Draw the button borders
        self.DrawButtonBorders(dc, rect, penColor, brushColor)

    def DrawButtonColour(self, dc, rect, state, color):
        """
        Colors rectangle according to the XP theme.
        """

        # switch according to the status
        if state == ControlFocus:
            penColor = color
            brushColor = ArtManager.Get().LightColour(color, 75)
        elif state == ControlPressed:
            penColor = color
            brushColor = ArtManager.Get().LightColour(color, 60)
        else:
            penColor = color
            brushColor = ArtManager.Get().LightColour(color, 75)

        # Draw the button borders
        penColor = wx.BLACK
        self.DrawButtonBorders(dc, rect, penColor, brushColor)

    def DrawMenuBarBg(self, dc, rect):
        """
        Draws the menu bar background according to the active theme.
        """

        # For office style, we simple draw a rectangle with a gradient colouring
        artMgr = ArtManager.Get()
        vertical = artMgr.GetMBVerticalGradient()

        dcsaver = DCSaver(dc)

        # fill with gradient
        startColor = artMgr.GetMenuBarFaceColour()
        if artMgr.IsDark(startColor):
            startColor = artMgr.LightColour(startColor, 50)

        endColor = artMgr.LightColour(startColor, 90)

        startColor = self.menubar_background_start_colour
        endColor = self.menubar_background_end_colour

        artMgr.PaintStraightGradientBox(dc, rect, startColor, endColor, False)

        # Draw the border
        if artMgr.GetMenuBarBorder():
            dc.SetPen(wx.Pen(startColor))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangleRect(rect)

    def DrawToolBarBg(self, dc, rect):
        """
        Draws the toolbar background according to the active theme.
        """
        artMgr = ArtManager.Get()

        if not artMgr.GetRaiseToolbar():
            return

        # For office style, we simple draw a rectangle with a gradient colouring
        vertical = artMgr.GetMBVerticalGradient()

        dcsaver = DCSaver(dc)

        # fill with gradient
        startColor = artMgr.GetMenuBarFaceColour()
        if artMgr.IsDark(startColor):
            startColor = artMgr.LightColour(startColor, 50)

        startColor = self.toolbar_background_start_colour
        endColor = self.toolbar_background_end_colour
        startColorTail = self.toolbar_background_start_colour_tail
        endColorTail = self.toolbar_background_end_colour_tail
        brdColor = self.toolbar_background_colour
        brdColorTail = self.toolbar_background_colour_tail
        bottomColor = self.toolbar_bottom_colour
        bottomTailColor = self.toolbar_bottom_colour_tail

        tailW = 11

        rect.SetWidth(self.toolBarWidth)
        oldY = rect.GetY()
        rect.SetY(oldY+3)

        c1 = dc.GetPixel(rect.x, rect.y)
        c2 = dc.GetPixel(rect.x, rect.y + rect.height)
        c3 = dc.GetPixel(rect.x + rect.width, rect.y)
        c4 = dc.GetPixel(rect.x + rect.width, rect.y + rect.height)

        rbTailAvColor = GetMidColor(bottomTailColor, c4)
        rbTailTBColor = GetMidColor(bottomTailColor, endColor)
        rtTailAvColor = GetMidColor(startColorTail, c3)
        rtTailTBColor = GetMidColor(startColorTail, startColor)

        r = wx.Rect(rect.x-6, rect.y+1, rect.width-tailW, rect.height)
        r2 = wx.Rect(r.x + rect.width - tailW, rect.y+1, tailW, rect.height)

        artMgr.PaintStraightGradientBox(dc, r2, startColorTail, endColorTail, vertical)
        artMgr.PaintStraightGradientBox(dc, r, startColor, endColor, vertical)

        dc.SetPen(wx.Pen(c1))
        dc.DrawPoint(r.x, r.y)
        dc.DrawPoint(r.x+1, r.y)
        dc.DrawPoint(r.x+2, r.y)
        dc.DrawPoint(r.x, r.y+1)
        dc.DrawPoint(r.x, r.y+2)

        dc.SetPen(wx.Pen(c2))
        dc.DrawPoint(r.x, r.y+r.height)
        dc.DrawPoint(r.x+1, r.y+r.height)
        dc.DrawPoint(r.x+2, r.y+r.height)
        dc.DrawPoint(r.x, r.y+r.height-1)
        dc.DrawPoint(r.x, r.y+r.height-2)

        dc.SetPen(wx.Pen(startColorTail))
        dc.DrawPoint(r.x + r.width-1, r.y)
        dc.DrawPoint(r.x + r.width-2, r.y)
        dc.DrawPoint(r.x + r.width-3, r.y)
        dc.DrawPoint(r.x + r.width-1, r.y+1)
        dc.DrawPoint(r.x + r.width-1, r.y+2)

        dc.SetPen(wx.Pen(endColorTail))
        dc.DrawPoint(r.x + r.width-1, r.y+r.height)
        dc.DrawPoint(r.x + r.width-2, r.y+r.height)
        dc.DrawPoint(r.x + r.width-3, r.y+r.height)
        dc.DrawPoint(r.x + r.width-1, r.y+r.height-1)
        dc.DrawPoint(r.x + r.width-1, r.y+r.height-2)

        dc.SetPen(wx.Pen(c3))
        dc.DrawPoint(r.x + r.width-1+tailW, r.y)
        dc.DrawPoint(r.x + r.width-2+tailW, r.y)
        dc.DrawPoint(r.x + r.width-3+tailW, r.y)
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+1)
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+2)

        dc.SetPen(wx.Pen(c4))
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+r.height)
        dc.DrawPoint(r.x + r.width-2+tailW, r.y+r.height)
        dc.DrawPoint(r.x + r.width-3+tailW, r.y+r.height)
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+r.height-1)
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+r.height-2)

        # Полутона
        dc.SetPen(wx.Pen(rtTailTBColor))
        dc.DrawPoint(r.x + r.width-3, r.y)
        dc.DrawPoint(r.x + r.width-1, r.y+2)

        dc.SetPen(wx.Pen(rtTailAvColor))
        dc.DrawPoint(r.x + r.width-2, r.y+r.height-1)

        dc.SetPen(wx.Pen(rbTailTBColor))
        dc.DrawPoint(r.x + r.width-2, r.y+r.height-1)
        dc.DrawPoint(r.x + r.width-3, r.y+r.height)

        dc.SetPen(wx.Pen(rbTailAvColor))
        dc.DrawPoint(r.x + r.width-3+tailW, r.y+r.height)
        dc.DrawPoint(r.x + r.width-1+tailW, r.y+r.height-2)

        dc.SetPen(wx.Pen(endColorTail))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(brdColor))

        dc.SetPen(wx.Pen(bottomTailColor))
        dc.DrawLine(r.x+2, r.y+r.height, r.width-2+tailW, r.y+r.height)
        dc.SetPen(wx.Pen(bottomColor))
        dc.DrawLine(r.x+2, r.y+r.height, r.width-2, r.y+r.height)

    def GetTextColourEnable(self):
        """
        Returns the colour used for text colour when enabled.
        """
        return self.enable_text_colour

    def GetSeparatorCols(self):
        return self.separator_col_start_colour, self.separator_col_start_colour
