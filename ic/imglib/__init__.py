#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Библиотека управления образами.
"""

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# ВНИМАНИЕ! Эти импорты необходимы для корректного выполнения выражений
import ic
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

__version__ = (0, 1, 1, 1)


def get_image_by_expr(expr):
    """
    Возвращет изображение по выражению.
    Пример: '@ic.imglib.newstyle_img.foler'.
    @param expr: Выражение.
    """
    import wx
    from . import common
    from ic.bitmap import icbitmap

    img = expr
    
    if isinstance(expr, str) and expr not in ('', 'None') and expr.startswith('@'):
        expr = expr[1:]
        
        try:
            img = eval(expr)
        except AttributeError:
            mod = '.'.join(expr.split('.')[:-1])
            exec('import %s' % mod)
            img = eval(expr)
            
        expr = img

    if isinstance(expr, str) and expr not in ('', 'None'):
        bmptype = icbitmap.icBitmapType(expr)
        img = wx.Image(expr, bmptype).ConvertToBitmap()
    elif not img:
        img = common.imgEdtImage
        
    return img
