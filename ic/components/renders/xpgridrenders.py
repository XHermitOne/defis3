#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Рендереры для грида в стиле XP.
"""

import wx.lib.mixins.gridlabelrenderer as glr
import wx
import wx.grid
from ic.utils import graphicUtils

TOP_LAB_CLR = wx.Colour(133, 168, 227)
BOT_LAB_CLR = wx.Colour(181, 211, 241)
TEXT_LAB_CLR = wx.Colour(62, 87, 160)
TOP_LINE_CLR = wx.Colour(180, 208, 239)
BOT_LINE_CLR = wx.Colour(133, 168, 227)
RIGHT_LINE_CLR = wx.Colour(83, 107, 136)
LEFT_LINE_CLR = wx.Colour(133, 168, 227)
GRID_LINE_CLR = wx.Colour(180, 199, 239)
DEFAULT_EMPTY_BGR_CLR = wx.Colour(225, 235, 250)
DEFAULT_CELL_BGR_CLR = wx.Colour(255, 255, 255)
DEFAULT_SEL_CELL_BGR_CLR = wx.Colour(221, 236, 254)
CELL_TEXT_CLR = wx.Colour(220, 220, 220)
SORT_P_CLR = wx.Colour(91, 118, 183)
SORT_UP_CLR = wx.Colour(150, 189, 235)
SORT_BORDER_CLR = wx.Colour(105, 134, 195)
SEL_CELL_CLR = wx.Colour(35, 100, 200)
SEL_BGR_CLR = wx.Colour(122, 150, 223)

# Кнопка сортировки по убыванию
SortMarkPointsDark = [(0, 0), (8, 0), (4, 4), (0, 0)]
SortMarkPointsLight = [(9, 0), (4, 5), (-1, 0), (0, 0), (9, 0)]
# Кнопка сортировки по возрастанию
SortMarkPointsDarkUp = [(0, 4), (8, 4), (4, 0), (0, 4)]
SortMarkPointsLightUp = [(-1, 4), (4, -1), (9, 4), (8, 4), (-1, 4)]
# Курсор
CursorMarkDark = [(0, 0), (0, 8), (4, 4), (0, 0)]
CursorMarkLight = [(4, -4), (4, 4), (0, 8), (4, -4)]

mark_shith_x = 4
mark_shith_y = 5


class XPCornerLabelRenderer(glr.GridLabelRenderer):

    def __init__(self, start_color=BOT_LAB_CLR, end_color=TOP_LAB_CLR, 
                 top_clr=TOP_LINE_CLR,
                 bot_clr=BOT_LINE_CLR,
                 left_clr=LEFT_LINE_CLR,
                 right_clr=RIGHT_LINE_CLR
                 ):
                
        self._start_color = start_color
        self._end_color = end_color
        self._top_clr = top_clr
        self._bot_clr = bot_clr
        self._left_clr = left_clr
        self._right_clr = right_clr
        self._top_pen = wx.Pen(top_clr)
        self._bot_pen = wx.Pen(bot_clr)
        self._left_pen = wx.Pen(left_clr)
        self._right_pen = wx.Pen(right_clr)

    def Draw(self, grid, dc, rect, rc):
        graphicUtils.DrawLineGradient(dc, rect.GetX(), rect.GetY(), rect.GetX()+rect.GetWidth()-2, rect.GetY()+rect.GetHeight(),
                                      self._start_color, self._end_color)
        r = wx.Rect(rect.GetX(), rect.GetY(), rect.GetWidth(), rect.GetHeight())
        # Top Line
        dc.SetPen(self._top_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX() + r.GetWidth(), r.GetY())
        dc.DrawLine(r.GetX(), r.GetY() + 1, r.GetX() + r.GetWidth(), r.GetY() + 1)
        # Right Line
        dc.SetPen(self._right_pen)
        dc.DrawLine(r.GetX() + r.GetWidth() - 1, r.GetY(), r.GetX() + r.GetWidth() - 1, r.GetY() + r.GetHeight())
        # Left Line
        dc.SetPen(self._left_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX(), r.GetY() + r.GetHeight())
        # Bottom
        dc.SetPen(self._bot_pen)
        dc.DrawLine(r.GetX(), r.GetY() + r.GetHeight() - 1, r.GetX() + r.GetWidth(), r.GetY() + r.GetHeight() - 1)


class XPRowLabelRenderer(glr.GridLabelRenderer):

    def __init__(self, start_color=BOT_LAB_CLR, end_color=TOP_LAB_CLR, 
                 top_clr=TOP_LINE_CLR,
                 bot_clr=BOT_LINE_CLR,
                 left_clr=LEFT_LINE_CLR,
                 right_clr=RIGHT_LINE_CLR,
                 bcur=False,
                 draw_num=True,
                 ):
                
        self._start_color = start_color
        self._end_color = end_color
        self._top_clr = top_clr
        self._bot_clr = bot_clr
        self._left_clr = left_clr
        self._right_clr = right_clr
        self._top_pen = wx.Pen(top_clr)
        self._bot_pen = wx.Pen(bot_clr)
        self._left_pen = wx.Pen(left_clr)
        self._right_pen = wx.Pen(right_clr)
        # Признак отрисовки номера строки
        self._drawNumRow = draw_num
        self._drawCursor = bcur
        
    def IsDrawCursor(self):
        """
        Признак отрисовки курсора.
        """
        return self._drawCursor
        
    def SetCursorFlag(self, flag=True):
        """
        Признак отрисовки курсора.
        """
        self._drawCursor = flag
        
    def SetVisibleNumRow(self, flag=True):
        """
        Устанавливает признак отрисовки номера строки.
        """
        self._drawNumRow = flag

    def SetVisibleRowCursor(self, flag=True):
        """
        Устанавливает признак отрисовки номера строки.
        """
        self._drawCursor = flag
        
    def Draw(self, grid, dc, rect, row):
        graphicUtils.DrawLineGradient(dc, rect.GetX(), rect.GetY(), rect.GetX()+rect.GetWidth()-2, rect.GetY()+rect.GetHeight()-1,
                                      self._start_color, self._end_color)
        r = wx.Rect(rect.GetX(), rect.GetY(), rect.GetWidth(), rect.GetHeight())
        if self._drawNumRow:
            hAlign, vAlign = grid.GetRowLabelAlignment()
            text = grid.GetRowLabelValue(row)
            dc.SetPen(wx.TRANSPARENT_PEN)
            self.DrawText(grid, dc, rect, text, hAlign, vAlign)
        
        # Top Line
        dc.SetPen(self._top_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX() + r.GetWidth(), r.GetY())
        dc.DrawLine(r.GetX(), r.GetY() + 1, r.GetX() + r.GetWidth(), r.GetY() + 1)
        # Right Line
        dc.SetPen(self._right_pen)
        dc.DrawLine(r.GetX() + r.GetWidth() - 1, r.GetY(), r.GetX() + r.GetWidth() - 1, r.GetY() + r.GetHeight())
        # Left Line
        dc.SetPen(self._left_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX(), r.GetY() + r.GetHeight())
        # Bottom
        dc.SetPen(self._bot_pen)
        dc.DrawLine(r.GetX(), r.GetY() + r.GetHeight() - 1, r.GetX() + r.GetWidth(), r.GetY() + r.GetHeight() - 1)
        
        if self.IsDrawCursor() and grid.GetGridCursorRow() == row:
            st = 0
            sty = r.GetY()
            penBound = wx.Pen(SORT_BORDER_CLR)
            dc.SetPen(penBound)
            brush = wx.Brush(SORT_P_CLR, wx.SOLID)
            dc.SetBrush(brush)
            dc.DrawPolygon(CursorMarkDark, mark_shith_x+st, mark_shith_y+sty)

        
class XPColLabelRenderer(glr.GridLabelRenderer):

    def __init__(self, start_color=BOT_LAB_CLR, end_color=TOP_LAB_CLR, 
                 top_clr=TOP_LINE_CLR,
                 bot_clr=BOT_LINE_CLR,
                 left_clr=LEFT_LINE_CLR,
                 right_clr=RIGHT_LINE_CLR
                 ):
                
        self._start_color = start_color
        self._end_color = end_color
        self._top_clr = top_clr
        self._bot_clr = bot_clr
        self._left_clr = left_clr
        self._right_clr = right_clr
        self._top_pen = wx.Pen(top_clr)
        self._bot_pen = wx.Pen(bot_clr)
        self._left_pen = wx.Pen(left_clr)
        self._right_pen = wx.Pen(right_clr)
        # Признак сортировки
        self._isSort = False
        # Направление сортировки
        self.sortDirection = 0

    def SetSortFlag(self, flag=True):
        """
        Устанавливаем признак сортируемой колонки.
        """
        self._isSort = flag
        
    def CanSort(self):
        """
        Возвращает признак сортировки колонки.
        """
        return self._isSort
        
    def Draw(self, grid, dc, rect, col):
        graphicUtils.DrawLineGradient(dc, rect.GetX(), rect.GetY(), rect.GetX()+rect.GetWidth()-2, rect.GetY()+rect.GetHeight(),
                                      self._start_color, self._end_color)
        r = wx.Rect(rect.GetX(), rect.GetY(), rect.GetWidth(), rect.GetHeight())
        hAlign, vAlign = grid.GetColLabelAlignment()
        text = grid.GetColLabelValue(col)
        
        dc.SetPen(wx.TRANSPARENT_PEN)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)
        
        # Top Line
        dc.SetPen(self._top_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX() + r.GetWidth(), r.GetY())
        dc.DrawLine(r.GetX(), r.GetY() + 1, r.GetX() + r.GetWidth(), r.GetY() + 1)
        # Right Line
        dc.SetPen(self._right_pen)
        dc.DrawLine(r.GetX() + r.GetWidth() - 2, r.GetY(), r.GetX() + r.GetWidth() - 2, r.GetY() + r.GetHeight())
        # Left Line
        dc.SetPen(self._left_pen)
        dc.DrawLine(r.GetX(), r.GetY(), r.GetX(), r.GetY() + r.GetHeight())
        dc.DrawLine(r.GetX() + r.GetWidth() - 1, r.GetY(), r.GetX() + r.GetWidth() - 1, r.GetY() + r.GetHeight())        
        # Bottom
        dc.SetPen(self._bot_pen)
        dc.DrawLine(r.GetX(), r.GetY() + r.GetHeight() - 1, r.GetX() + r.GetWidth(), r.GetY() + r.GetHeight() - 1)
        
        #   Рисуем признак сортируемой ячейки
        if self.CanSort() and r.GetWidth() > 5:
            penBound = wx.Pen(SORT_BORDER_CLR)
            dc.SetPen(penBound)
            clr = BOT_LAB_CLR
            stx = r.GetX()
            st = 0
            # Колока не сортирована
            if self.sortDirection == 0:
                brush = wx.Brush(SORT_UP_CLR, wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDark, mark_shith_x+stx, mark_shith_y+st)
            # Колонка отсортирована по убыванию
            elif self.sortDirection < 0:
                brush = wx.Brush(SORT_P_CLR, wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDark, mark_shith_x+stx, mark_shith_y+st)
            # Колонка отсортирована по возрастанию
            else:
                brush = wx.Brush(SORT_P_CLR, wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDarkUp, mark_shith_x+stx, mark_shith_y+st)


class cellImageRenderer(wx.grid.PyGridCellRenderer):
    """
    Рендерер для отображений образов.
    """
    def __init__(self, *Images_):
        """
        Конструктор.
        """
        wx.grid.PyGridCellRenderer.__init__(self)
        self._images = Images_

    def Draw(self, Grid_, Attr_, DC_, Rect_, Row_, Col_, isSelected_):
        """
        Отрисовка.
        """
        img = self._images[0]
        img_dc = wx.MemoryDC()
        img_dc.SelectObject(img)

        # Очистка фона
        DC_.SetBackgroundMode(wx.SOLID)

        if isSelected_:
            DC_.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            DC_.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            DC_.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            DC_.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        DC_.DrawRectangleRect(Rect_)

        # copy the image but only to the size of the grid cell
        width, height = img.GetWidth(), img.GetHeight()

        if width > Rect_.GetWidth() - 2:
            width = Rect_.GetWidth() - 2

        if height > Rect_.GetHeight() - 2:
            height = Rect_.GetHeight() - 2

        DC_.Blit(Rect_.GetX() + 1, Rect_.GetY() + 1, width, height,
                 img_dc, 0, 0, wx.COPY, True)


class stateImageRenderer(wx.grid.PyGridCellRenderer):
    """
    Рендерер для отображений образов.
    """
    def __init__(self, *images):
        """
        Конструктор.
        """
        wx.grid.PyGridCellRenderer.__init__(self)
        
        self._images = images
        self._sx = 0
        self._sy = 0

    def DrawText(self, grid, dc, rect, text, hAlign, vAlign):
        """
        Draw the label's text in the rectangle, using the alignment
        flags, and the grid's specified label font and color.
        """
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetTextForeground(grid.GetDefaultCellTextColour())
        dc.SetFont(grid.GetLabelFont())
        rect = wx.Rect(*rect)
        rect.Deflate(2, 1)
        grid.DrawTextRectangle(dc, text, rect, hAlign, vAlign)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        Отрисовка.
        """
        sx, st = grid.GetRowState(row)
        img = None
        if st is not None and st < len(self._images):
            img = self._images[st]
        
        if img:
            img_dc = wx.MemoryDC()
            img_dc.SelectObject(img)

        # Очистка фона
        dc.SetBackgroundMode(wx.SOLID)

        if isSelected:
            dc.SetBrush(wx.Brush(SEL_BGR_CLR, wx.SOLID))
            dc.SetPen(wx.Pen(SEL_BGR_CLR, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)

        # copy the image but only to the size of the grid cell
        if img:
            width, height = img.GetWidth(), img.GetHeight()
            if width > rect.GetWidth()-2:
                width = rect.GetWidth()-2
            if height > rect.GetHeight()-2:
                height = rect.GetHeight()-2
            dc.Blit(rect.GetX()+1+sx*img.GetWidth(), rect.GetY()+1, width, height,
                    img_dc, self._sx, self._sy, wx.COPY, True)
        else:
            width, height = 0, 0
            
        hAlign, vAlign = grid.GetCellAlignment(row, col)
        text = grid.GetCellValue(row, col)
        if text:
            dc.SetPen(wx.TRANSPARENT_PEN)
            if hAlign < width:
                rect.SetX(rect.GetX() + width)
                rect.SetWidth(rect.GetWidth() - width)
            if sx:    
                rect.SetX(rect.GetX() + sx*width)
                rect.SetWidth(rect.GetWidth() - sx * width)

            self.DrawText(grid, dc, rect, text, hAlign, vAlign)


class DefaultCellRenderer(wx.grid.PyGridCellRenderer):
    """
    Рендерер для отображений образов.
    """
    def __init__(self, color=DEFAULT_CELL_BGR_CLR, sel_color=DEFAULT_SEL_CELL_BGR_CLR, *arg, **kwarg):
        """
        Конструктор.
        """
        wx.grid.PyGridCellRenderer.__init__(self)
        self.color = color
        self.sel_color = sel_color

    def DrawText(self, grid, dc, rect, text, hAlign, vAlign):
        """
        Draw the label's text in the rectangle, using the alignment
        flags, and the grid's specified label font and color.
        """
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetTextForeground(grid.GetDefaultCellTextColour())
        dc.SetFont(grid.GetLabelFont())
        rect = wx.Rect(*rect)
        rect.Deflate(2, 2)
        grid.DrawTextRectangle(dc, text, rect, hAlign, vAlign)

    def Draw(self, grid, attr, dc, rect, row, col, is_selected):
        """
        Отрисовка.
        """
        # Очистка фона
        dc.SetBackgroundMode(wx.SOLID)

        if is_selected:
            dc.SetBrush(wx.Brush(self.sel_color, wx.SOLID))
            dc.SetPen(wx.Pen(self.sel_color, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(self.color, wx.SOLID))
            dc.SetPen(wx.Pen(self.color, 1, wx.SOLID))
            
        dc.DrawRectangleRect(rect)
        hAlign, vAlign = grid.GetCellAlignment(row, col)
        text = grid.GetCellValue(row, col)
        dc.SetPen(wx.TRANSPARENT_PEN)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)


class XPColAttr(wx.grid.GridCellAttr):

    def __init__(self, *arg, **kwarg):
        wx.grid.GridCellAttr.__init__(self, *arg, **kwarg)
        self.SetBackgroundColour(DEFAULT_CELL_BGR_CLR)
