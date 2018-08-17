#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
"""

import os
import os.path
import wx

from ic.log import log

__version__ = (0, 1, 1, 1)

# Буфер картинок
USER_BITMAP_CACHE = {}


def icBitmapType(filename):
    """
    Определить тип графического файла по его расширению (.jpg, .png и т.п.)
    """

    if filename == '':
        return None

    try:
        name, ext = os.path.splitext(filename)
        ext = ext[1:].upper()
        if ext == 'BMP':
            return wx.BITMAP_TYPE_BMP
        elif ext == 'GIF':
            return wx.BITMAP_TYPE_GIF
        elif ext == 'JPG' or ext == 'JPEG':
            return wx.BITMAP_TYPE_JPEG
        elif ext == 'PCX':
            return wx.BITMAP_TYPE_PCX
        elif ext == 'PNG':
            return wx.BITMAP_TYPE_PNG
        elif ext == 'PNM':
            return wx.BITMAP_TYPE_PNM
        elif ext == 'TIF' or ext == 'TIFF':
            return wx.BITMAP_TYPE_TIF
        elif ext == 'XBM':
            return wx.BITMAP_TYPE_XBM
        elif ext == 'XPM':
            return wx.BITMAP_TYPE_XPM
        elif ext == 'ICO':
            return wx.BITMAP_TYPE_ICO
        return None
    except:
        log.fatal('Ошибка определения типа графического файла')

    return None


def GetUserBitmap(fileName, subsys, dir='images'):
    """
    Функция возвращает объект картинки из пользовательской библиотеки.
    
    @type subsys: C{string}
    @param subsys: Имя подсистемы в которой ищется картинка.
    @type fileName: C{string}
    @param fileName: Имя картинки.
    @rtype: C{wx.Bitmap}
    @return: Объект картинки.
    """
    global USER_BITMAP_CACHE
    key = str(subsys) + os.path.sep + fileName
    
    if key in USER_BITMAP_CACHE:
        return USER_BITMAP_CACHE[key]
    else:
        typ = icBitmapType(fileName)
        
        if typ:
            import ic.utils.resource as resource
            path = resource.icGetResPath().replace('\\', '/')
            if not subsys:
                path = os.path.join(path, dir, fileName)
            else:
                path = os.path.join(os.path.sep.join(path.split(os.path.sep)[:-1]), subsys, dir, fileName)
                
            img = wx.Image(path, typ)
            bmp = img.ConvertToBitmap()
            USER_BITMAP_CACHE[key] = bmp
            return bmp
