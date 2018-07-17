#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит набор функций, используемых во внешних редакторах свойств.
"""

#   Функции для арботы со стилями


def getStyleDict(style, allstyles):
    """
    Возвращает стиль компонента в виде словаря.
    
    @type style: C{long}
    @param style: Стиль компонента.
    @type allstyles: C{dictionary}
    @param allstyles: Словарь всех стилей компонента.
    @rtype: C{dictionary}
    @return: Стиль компонента.
        - B{Пример}:C{'wx.DEFAULT':1, 'wx.APP':0, ...}
    """
    
    #style = component['style']
    if not allstyles:
        return {}
        
    dict = {}
    bFind = False
    
    #   В случае обобщающего стиля обрабатывать надо немного подругому
    #   Пример такого стиля wx.DEFAULT_FRAME_STYLE  = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
    #       wx.RESIZE_BORDER |  wx.SYSTEM_MENU | wx.CAPTION
    
    if style in allstyles.values():
        for k in allstyles.keys():
            dict[k] = 0
            
            if allstyles[k] == style:
                dict[k] = 1
                
        return dict
    
    #   Разбираем комбинированный стиль
    for key in allstyles.keys():
        if allstyles[key] & style & allstyles[key] == allstyles[key] and allstyles[key] > 0:
            dict[key] = 1
        else:
            dict[key] = 0

    return dict

