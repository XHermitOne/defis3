#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Библиотека управления образами.
"""

__version__ = '0.3'

def get_image_by_expr(expr):
    """
    Возвращет изображение по выражению.
    Пример: '@ic.imglib.newstyle_img.foler'.
    @param expr: Выражение.
    """
    import wx
    import ic
    from . import common
    from ic.bitmap import icbitmap
    img = expr
    
    if type(expr) in (str, unicode) and expr not in ('', 'None') and expr.startswith('@'):
        expr = expr[1:]
        
        try:
            img = eval(expr)
        except AttributeError:
            mod = '.'.join(expr.split('.')[:-1])
            exec('import %s' % mod)
            img = eval(expr)
            
        expr = img

    if type(expr) in (str, unicode) and expr not in ('', 'None'):
        bmptype = icbitmap.icBitmapType(expr)
        img = wx.Image(expr, bmptype).ConvertToBitmap()
    elif not img:
        img = common.imgEdtImage
        
    return img