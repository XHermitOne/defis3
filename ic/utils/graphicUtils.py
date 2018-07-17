#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Функции для работы с графикой.
@type BGR_SOLID: C{int}
@param BGR_SOLID: Идентификатор сплошной одноцветной заливки.
@type BGR_GRAD_TOP: C{int}
@param BGR_GRAD_TOP: Идентификатор градиентной заливки в вертикальном направлении
    от светлого к темному.
@type BGR_GRAD_BOTTOM: C{int}
@param BGR_GRAD_BOTTOM: Идентификатор градиентной заливки в вертикальном направлении
    от темного к светлому.
@type BGR_GRAD_LEFT: C{int}
@param BGR_GRAD_LEFT: Идентификатор градиентной заливки в горизонтальном направлении
    от светлого к темному.
@type BGR_GRAD_RIGHT: C{int}
@param BGR_GRAD_RIGHT: Идентификатор градиентной заливки в горизотнальном направлении
    от темного к светлому.
"""

import wx

__version__ = (0, 0, 1, 2)

#   Идентификаторы типов заливки ячейки
BGR_SOLID = 0
BGR_GRAD_TOP = 1
BGR_GRAD_BOTTOM = 2
BGR_GRAD_LEFT = 3
BGR_GRAD_RIGHT = 4

# Version 2.9.1
if wx.VERSION > (2, 8, 11, 10):
    wx.Colour = wx.Colour

# --- Функции для работы с градиентами


def GetMidColor(clr1, clr2, part=0.5):
    """ 
    Функция возвращает промежуточный цвет между двумя.
    @type clr1: C{wx.Colour}
    @param clr1: Первый цвет.
    @type clr2: C{wx.Colour}
    @param clr2: Второй цвет.
    """
    r1, g1, b1 = clr1.Red(), clr1.Green(), clr1.Blue()
    r2, g2, b2 = clr2.Red(), clr2.Green(), clr2.Blue()
    r = int(r1 + (r2-r1)*part)
    g = int(g1 + (g2-g1)*part)
    b = int(b1 + (b2-b1)*part)
    return wx.Colour(r, g, b)


def DrawGradient(dc, width, height, clr, gradType=BGR_GRAD_TOP, x0=0, y0=0, delta=None):
    """ 
    Рисует прямоугольник с градиентной заливкой.
    type dc: C{wx.DC}
    param dc: Контекст устройства.
    type width: C{int}
    param width: Ширина прямоугольника.
    type height: C{int}
    param height: Высота прямоугольника.
    type clr: C{wx.Colour}
    param clr: Основной цвет.
    type gradType: C{int}
    param gradType: Тип заливки:
        BGR_SOLID - сплошная заливка без градиента.
        BGR_GRAD_TOP - верх-низ
        BGR_GRAD_BOTTOM - низ-верх
        BGR_GRAD_LEFT - лево-право
        BGR_GRAD_RIGHT - право-лево.
    type x0: C{int}
    param x0: Левый угол.
    type y0: C{int}
    param y0: Верх угла.
    type delta: C{int}
    param delta: Глубина градиента
    """
    if not delta:
        if clr.Red() == clr.Green() and clr.Red() ==  clr.Blue():
            delta = 4
        else:
            delta = 3

    if gradType in [BGR_GRAD_TOP, BGR_GRAD_BOTTOM]:
        for h in xrange(height):
            if gradType == BGR_GRAD_BOTTOM:
                y = height - h
            else:
                y = h
                
            if clr.Red() > clr.Green() and clr.Red() > clr.Blue():
                clrR = (clr.Red()*height - clr.Red()*y/(delta+1))/height
            else:
                clrR = (clr.Red()*height - clr.Red()*y/delta)/height

            if clr.Green() > clr.Red() and clr.Green() > clr.Blue():
                clrG = (clr.Green()*height - clr.Green()*y/(delta+1))/height
            else:
                clrG = (clr.Green()*height - clr.Green()*y/delta)/height

            if clr.Blue() > clr.Green() and clr.Blue() > clr.Red():
                clrB = (clr.Blue()*height - clr.Blue()*y/(delta+1))/height
            else:
                clrB = (clr.Blue()*height - clr.Blue()*y/delta)/height
                    
            pen = wx.Pen((clrR, clrG, clrB))
            dc.SetPen(pen)
            dc.DrawLine(x0, y0+h, x0+width, y0+h)
    else:
        for w in xrange(width):

            if gradType == BGR_GRAD_RIGHT:
                x = width - w
            else:
                x = w
                
            if clr.Red() > clr.Green() and clr.Red() > clr.Blue():
                clrR = (clr.Red()*width - clr.Red()*x/(delta+1))/width
            else:
                clrR = (clr.Red()*width - clr.Red()*x/(delta+1))/width

            if clr.Green() > clr.Red() and clr.Green() > clr.Blue():
                clrG = (clr.Green()*width - clr.Green()*x/(delta+1))/width
            else:
                clrG = (clr.Green()*width - clr.Green()*x/(delta+1))/width

            if clr.Blue() > clr.Green() and clr.Blue() > clr.Red():
                clrB = (clr.Blue()*width - clr.Blue()*x/(delta+1))/width
            else:
                clrB = (clr.Blue()*width - clr.Blue()*x/(delta+1))/width
                    
            pen = wx.Pen((clrR, clrG, clrB))
            
            dc.SetPen(pen)
            dc.DrawLine(x0+w, y0+0, x0+w, y0+height)


def DrawLineGradient(dc, x0, y0, x1, y1, clr1, clr2, gradType=BGR_GRAD_TOP, clr_bord=None):
    """ 
    Рисует прямоугольник с градиентной заливкой.
    """
    gc = wx.GraphicsContext.Create(dc)
    if gradType == BGR_GRAD_TOP:
        grad = gc.CreateLinearGradientBrush(x0, y1, x0, y0, clr1, clr2)
    elif gradType == BGR_GRAD_BOTTOM:
        grad = gc.CreateLinearGradientBrush(x0, y0, x0, y1, clr1, clr2)
    elif gradType == BGR_GRAD_RIGHT:
        grad = gc.CreateLinearGradientBrush(x0, y0, x1, y0, clr1, clr2)
    else:
        grad = gc.CreateLinearGradientBrush(x1, y0, x0, y0, clr1, clr2)
    
    rect = wx.Rect(x0, y0, x1-x0+1, y1-y0)

    if clr_bord is None:
        gc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
    else:
        gc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))

    gc.SetBrush(grad)
    gc.DrawRectangle(x0, y0, rect.width, rect.height)

    
def DrawGradientRect(dc, width, height, clr1, clr2=wx.Colour(128, 128, 128),
                     gradType=BGR_GRAD_TOP, x0=0, y0=0):
    """ 
    Рисует прямоугольник с градиентной заливкой.
    type dc: C{wx.DC}
    param dc: Контекст устройства.
    type width: C{int}
    param width: Ширина прямоугольника.
    type height: C{int}
    param height: Высота прямоугольника.
    type clr1: C{wx.Colour}
    param clr1: цвет 1.
    type clr2: C{wx.Colour}
    param clr2: цвет 2.
    type gradType: C{int}
    param gradType: Тип заливки:
        BGR_SOLID - сплошная заливка без градиента.
        BGR_GRAD_TOP - верх-низ
        BGR_GRAD_BOTTOM - низ-верх
        BGR_GRAD_LEFT - лево-право
        BGR_GRAD_RIGHT - право-лево.
    type x0: C{int}
    param x0: Левый угол.
    type y0: C{int}
    param y0: Верх угла.
    """
    if gradType in [BGR_GRAD_TOP, BGR_GRAD_BOTTOM]:
        for h in xrange(height):
            if gradType == BGR_GRAD_BOTTOM:
                clr = GetMidColor(clr1, clr2, float(h/(height-1.0)))
            else:
                clr = GetMidColor(clr2, clr1, float(h/(height-1.0)))
            pen = wx.Pen(clr)
            dc.SetPen(pen)
            dc.DrawLine(x0, y0+h, x0+width, y0+h)
    else:
        for w in xrange(width):
            if gradType == BGR_GRAD_RIGHT:
                clr = GetMidColor(clr1, clr2, float(w/(width-1)))
            else:
                clr = GetMidColor(clr2, clr1, float(w/(width-1)))
                    
            pen = wx.Pen(clr)
            dc.SetPen(pen)
            dc.DrawLine(x0+w, y0+0, x0+w, y0+height)


pLeft = [[0,    0.4,   0.7,  0.9],
         [0.4, -0.75, -0.3, -0.1],
         [0.7, -0.3,  -0.01,   -0.01],
         [0.9, -0.1,  -0.01,   -0.01]]


def drawRoundCorners(dc, size, fgr, bgr, bgr_prnt,
                    st=0, clrLst=None, corners=(1, 1, 1, 1), backgroundType=0):
    """
    """
    return drawRoundCornersRect(dc, (0,0), size, fgr, bgr, bgr_prnt,
                                st, clrLst, corners, backgroundType)

    
def drawRoundCornersRect(dc, pos, size, fgr, bgr, bgr_prnt,
                         st=0, clrLst=None, corners=(1, 1, 1, 1), backgroundType=0):
    """ 
    Рисует скругленные углы (радиус=4).
    @type dc: C{wx.DC}
    @param dc: Контекст устройства.
    @type pos: C{tuple/list}
    @param pos: Начальная позиция прямоугольника.
    @type size: C{tuple/list}
    @param size: Размеры прямоугольника, у которого рисуем скругленные углы.
    @type fgr: C{wx.Colour}
    @param fgr: Цвет надписей.
    @type bgr: C{wx.Colour}
    @param bgr: Цвет фона.
    @type bgr_prnt: C{C{wx.Colour}}
    @param bgr_prnt: Цвет фона родительского компонента.
    @type st: C{int}
    @param st: Отступ от границы.
    @type clrLst: C{tuple}
    @param clrLst: Список цветов границ (T, R, B, L).
    @type corners: C{tuple}
    @param corners: Признаки углов (LT, RT, RB, LB).
    @type backgroundType: C{int}
    @param backgroundType: Идентификаторы типа заливки (см. выше описание
        идентификаторов).
    """
    r = 4
    x0, y0 = pos
    width, height = size
    
    if clrLst:
        clrT, clrR, clrB, clrL = clrLst
    else:
        clrT, clrR, clrB, clrL = fgr, fgr, fgr, fgr
    
    if isinstance(bgr_prnt, tuple):
        clr_prnt = wx.Colour(*bgr_prnt)
    else:
        clr_prnt = bgr_prnt
        
    if isinstance(clrT, tuple):
        clrT = wx.Colour(*clrT)
    if isinstance(clrR, tuple):
        clrR = wx.Colour(*clrR)
    if isinstance(clrB, tuple):
        clrB = wx.Colour(*clrB)
    if isinstance(clrL, tuple):
        clrL = wx.Colour(*clrL)
    
    if height >= r*2:
        d = r
        bLT, bRT, bRB, bLB = corners
        # --- Рисуем углы
        for y, r in enumerate(pLeft):
            for x, p in enumerate(r):
                if p >= 0:
                    clr = GetMidColor(clr_prnt, clrT, p)
                else:
                    clr = GetMidColor(dc.GetPixel(x0+x+st, y0+y+st), clrT, -p)
                        
                pen = wx.Pen(clr)
                dc.SetPen(pen)
                if bLT and clrT:
                    dc.DrawPoint(x0+x+st, y0+y+st)
                    
                # RT
                if bRT and clrR:
                    if backgroundType:
                        if p >= 0:
                            clr = GetMidColor(clr_prnt, clrR, p)
                        else:
                            clr = GetMidColor(dc.GetPixel(x0+width-x-st-1, y0+y+st), clrR, -p)
                        pen = wx.Pen(clr)
                        dc.SetPen(pen)

                    dc.DrawPoint(x0+width-x-st-1, y0+y+st)
                # RB
                if bRB and clrB:
                    if backgroundType:
                        if p >= 0:
                            clr = GetMidColor(clr_prnt, clrB, p)
                        else:
                            clr = GetMidColor(dc.GetPixel(x0+width-x-st-1, y0+height-y-st-1), clrB, -p)
                        pen = wx.Pen(clr)
                        dc.SetPen(pen)

                    dc.DrawPoint(x0+width-x-st-1, y0+height-y-st-1)
                # LB
                if bLB and clrL:
                    if backgroundType:
                        if p >= 0:
                            clr = GetMidColor(clr_prnt, clrL, p)
                        else:
                            clr = GetMidColor(dc.GetPixel(x0+x+st, y0+height-y-st-1), clrL, -p)
                            
                        pen = wx.Pen(clr)
                        dc.SetPen(pen)
                    dc.DrawPoint(x0+x+st, y0+height-y-st-1)

# ------ new


def AdjustColour(color, percent, alpha=wx.ALPHA_OPAQUE):
    """ 
    Brighten/Darken input colour by percent and adjust alpha
    channel if needed. Returns the modified color.
    @param color: color object to adjust
    @type color: wx.Colour
    @param percent: percent to adjust +(brighten) or -(darken)
    @type percent: int
    @keyword alpha: amount to adjust alpha channel
    """ 
    end_color = wx.WHITE
    if color == end_color and percent < 0:
        end_color = wx.LIGHT_GREY
        percent = -percent
        
    rdif = end_color.Red() - color.Red()
    gdif = end_color.Green() - color.Green()
    bdif = end_color.Blue() - color.Blue()
    high = 100

    # We take the percent way of the color from color -. white
    red = color.Red() + ((percent * rdif) / high)
    green = color.Green() + ((percent * gdif) / high)
    blue = color.Blue() + ((percent * bdif) / high)
    return wx.Colour(max(red, 0), max(green, 0), max(blue, 0), alpha)


def AdjustColour2(color, shift, alpha=wx.ALPHA_OPAQUE):
    """ 
    Brighten/Darken input colour by percent and adjust alpha
    channel if needed. Returns the modified color.
    @param color: color object to adjust
    @type color: wx.Colour
    @param percent: percent to adjust +(brighten) or -(darken)
    @type percent: int
    @keyword alpha: amount to adjust alpha channel
    """ 
    I = float(color.Red() + color.Green() + color.Blue())/(3.0*255)
    if I > 0.5:
        end_color = wx.WHITE
        rdif = color.Red()
        gdif = color.Green()
        bdif = color.Blue()
        percent = -abs(shift)
    else:
        end_color = wx.WHITE
        rdif = end_color.Red() - color.Red()
        gdif = end_color.Green() - color.Green()
        bdif = end_color.Blue() - color.Blue()
        percent = abs(shift)
        
    high = 100

    # We take the percent way of the color from color -. white
    red = color.Red() + ((percent * rdif) / high)
    green = color.Green() + ((percent * gdif) / high)
    blue = color.Blue() + ((percent * bdif) / high)
    return wx.Colour(max(red, 0), max(green, 0), max(blue, 0), alpha)
