#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.Font. Генерирут шрифт по ресурсному описанию.

@type SPC_IC_FONT: C{Dictionary}
@var SPC_IC_FONT: Спецификация на ресурсное описание шрифта. Описание ключей:

    - B{type = 'Font'}: Тип ресурса.
    - B{name = 'defaultFont'}: Имя компонента.
    - B{family = None}: Группа шрифтов. Значение из ['default', 'serif', 'sansSerif', 'monospace']
    - B{size = 8}: Размер шрифта.
    - B{faceName = ''}: Название шрифта ('Arial', 'Tahoma', ...).
    - B{style = None}: Стиль шрифта. Значение из ['regular', 'bold', 'italic', 'boldItalic']
    - B{underline = 0}: Признак подчеркнутого шрифта.
    
@type ICFontFamily: C{List}
@var ICFontFamily: Список названий групп шрифтов ['default', 'serif', 'sansSerif', 'monospace'].
@type ICFontStyle: C{List}
@var ICFontStyle: Список названий стилей шрифтов ['regular', 'bold', 'italic', 'boldItalic'].
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.utils.util import icSpcDefStruct
from . import icwidget as icwidget

__version__ = (0, 0, 1, 1)

SPC_IC_FONT = {'type': 'Font',
               'name': 'defaultFont',
               'size': 8,
               'family': None,
               'faceName': '',
               'style': None,
               'underline': False
               }

ICFontFamily = ['default', 'serif', 'sansSerif', 'monospace']
ICFontStyle = ['regular', 'bold', 'italic', 'boldItalic']


def getICFamily(font):
    """
    Функция возвращает название группы шрифта.
    @type font: C{wx.Font}
    @param font: Указатель на нужный объект.
    @rtype: C{String}
    @return: Название группы шрифта из ['default', 'serif', 'sansSerif', 'monospace'].
    """
    wxf = font.GetFamily()
    if wxf == wx.ROMAN:
        family = 'serif'
    elif wxf == wx.SWISS:
        family = 'sansSerif'
    elif wxf == wx.MODERN:
        family = 'monospace'
    else:
        family = 'default'
    
    return family


def getICFontStyle(font):
    """
    Функция возвращает название стиля шрифта.
    @type font: C{wx.Font}
    @param font: Указатель на нужный объект.
    @rtype: C{String}
    @return: Название стиля шрифта из ['regular', 'bold', 'italic', 'boldItalic'].
    """
    style = font.GetStyle()
    weight = font.GetWeight()
    if style == wx.ITALIC and weight == wx.NORMAL:
        ret = 'italic'
    elif style == wx.NORMAL and weight == wx.BOLD:
        ret = 'bold'
    elif style == wx.ITALIC and weight == wx.BOLD:
        ret = 'boldItalic'
    else:
        ret = 'regular'
    
    return ret


class icFont(wx.Font):
    """
    Класс icFont реализует интерфейс для обработки и стадартного представления
    шрифтов в системе.
    За основы взято описание шрифтов в PythonCard:
        'size'    - Размер шрифта.
        'family'  - Вид шрифта. ('default', 'serif', 'sansSerif', 'monospace')
        'faceName'- Имя шрифта (Пример: 'Arial').
        'style'   - Стиль шрифта ('regular', 'bold', 'italic', 'boldItalic')
        'underline'- Признак подчеркивания.
    """

    def _familyId(self, name):
        """
        По названию определяет тип шрифта
        @param name: Имя типа шрифта из ресурса.
        @type name: C{string}
        @return: Определяет wxPython идентификатор типа шрифта ('wx.DEFAULT', 'wx.DECORATIVE', 'wx.ROMAN', 'wx.SCRIPT', 'wx.SWISS', 'wx.MODERN')
        @rtype: C{int}
        """
        if name in ('serif', 'Serif'):
            return wx.ROMAN
        elif name in ('sansSerif', 'Sans'):
            return wx.SWISS
        elif name in ('monospace', 'Monospace'):
            return wx.MODERN
        else:
            return wx.DEFAULT

    def _styleId(self, name):
        """ По названию определяет стиль шрифта
        @param name: Имя стиля из ресурса.
        @type name: C{string}
        @return: Определяет стиль и толщину шрифта
        @rtype: C{tuple}
        """
        if name in ('italic', 'Italic'):
            style = wx.ITALIC
            weight = wx.NORMAL
        elif name in ('bold',):
            style = wx.NORMAL
            weight = wx.BOLD
        elif name in ('boldItalic',):
            style = wx.ITALIC
            weight = wx.BOLD
        else:
            style = wx.NORMAL
            weight = wx.NORMAL

        return style, weight

    def bool_underline(self, underline):
        """
        Преобразование подчеркивания в логическую переменную.
        @param underline:
        @return:
        """
        if type(underline) in (str, unicode):
            return underline == 'Underlined'
        return bool(underline)

    def __init__(self, component):
        """
        По ресурсному описанию генерируется шрифт.
        """
        component = icSpcDefStruct(SPC_IC_FONT, component)
        size = int(component['size'])
        faceName = component['faceName']
        underline = self.bool_underline(component['underline'])
        # log.debug(u'Шрифт %s : %s' % (underline, type(underline)))

        if component['family'] is not None:
            family = self._familyId(component['family'])
        else:
            family = wx.DEFAULT

        if component['style'] is not None:
            style, weight = self._styleId(component['style'])
        else:
            style = wx.NORMAL
            weight = wx.NORMAL

        # wx.Font.__init__(self, size, family, style, weight, underline, faceName, encoding=wx.FONTENCODING_CP1251)
        wx.Font.__init__(self, size, family, style, weight, underline, faceName, encoding=wx.FONTENCODING_UTF8)


def test(par=0):
    """
    Тестируем класс icFont.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icFont Test', size=(300, 100))
    win = wx.Panel(frame, -1)
    ctrl = wx.StaticText(win, -1, u'Проверка шрифта')
    ctrl.SetFont(icFont({'style': 'boldItalic', 'size': 14}))
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test()
