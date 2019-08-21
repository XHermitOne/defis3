#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Библиотека управления образами.
"""

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# ВНИМАНИЕ! Эти импорты необходимы для корректного выполнения выражений
import ic
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

__version__ = (0, 1, 1, 1)


def import_image_by_expr(expr):
    """
    Импорт изображения из модуля по выражению
    @param expr:
    @param expr: Выражение.
    @return: Образ или None в случае ошибки.
    """
    img = None
    try:
        mod = '.'.join(expr.split('.')[:-1])
        exec('import %s' % mod)
        img = eval(expr)
    except:
        print(u'Ошибка выполнения выражения <%s>' % str(expr))
    return img


def get_image_by_expr(expr):
    """
    Возвращет изображение по выражению.
    Пример: '@ic.imglib.newstyle_img.folder'.
    @param expr: Выражение.
    """
    import wx
    from . import common
    from ic.bitmap import bmpfunc

    img = expr
    
    if isinstance(expr, str) and expr not in ('', 'None') and expr.startswith('@'):
        expr = expr[1:]
        
        try:
            img = eval(expr)
        except AttributeError:
            img = import_image_by_expr(expr)
            
        expr = img

    if isinstance(expr, str) and expr not in ('', 'None'):
        bmptype = bmpfunc.getBitmapType(expr)
        img = wx.Image(expr, bmptype).ConvertToBitmap()
    elif not img:
        img = common.imgEdtImage
        
    return img
