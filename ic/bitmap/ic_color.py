#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания цветов по умолчанию, используемых при инициализации
видимых компонентов библиотеки.

@var IC_COLOR_BLACK: Черный
@var IC_COLOR_DARKGREY: Темно-серый
@var IC_COLOR_LIGHTGREY: Светло-серый
@var IC_COLOR_WHITE: Белый

@var I_RED: Индекс интенсивности красного цвета в палитре
@var I_GREEN: Индекс интенсивности зеленого цвета в палитре
@var I_BLUE: Индекс интенсивности синего цвета в палитре
"""

# Подключение библиотек
import wx

# Цветовая палитра

# Серая палитра
IC_COLOR_BLACK = wx.BLACK
IC_COLOR_DARKGREY = (128, 128, 128)
IC_COLOR_LIGHTGREY = wx.LIGHT_GREY
IC_COLOR_WHITE = wx.WHITE

# Остальные цвета
IC_COLOR_RED = wx.RED
IC_COLOR_BLUE = wx.BLUE
IC_COLOR_GREEN = wx.GREEN
IC_COLOR_CYAN = wx.CYAN

# Цветовыве константы
I_RED = 0
I_GREEN = 1
I_BLUE = 2
