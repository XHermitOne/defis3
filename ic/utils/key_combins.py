#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль используемых комбинаций клавиш.
Используется для определения Акселераторных таблиц (wx.AcceleratorTable).
По мнемоническому правилу в имени комбинации клашиш дожен присутствовать
символ <_>. Например CTRL_F1. В имени одиночных клавиш этот символ отсутствует.
Описание одиночной клавиши/комбинации клавиш можно получить по функции 
get_key_combine().
Структура описания одиночной клавиши/комбинации клавиш представляет собой словарь
{
    'mode': режим комбинации клавиш
            м.б. wx.ACCEL_NORMAL - одиночные клавиши
                 wx.ACCEL_CTRL - комбинация клавиш с нажатой <Control>
                 wx.ACCEL_ALT - комбинация клавиш с нажатой <Alt>
                 wx.ACCEL_SHIFT - комбинация клавиш с нажатой <Shift>
    'key': сама клавиша.
            м.б. константой wx.WXK_... 
            Например wx.WXK_F1
            Либо непосредственным кодом. Например ord('Q').
    'label': отображение комбинации клавиш в помоши.
}
"""

import wx
from ic.log import log

# Список одиночных клавиш
F1 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F1, label='F1')
F2 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F2, label='F2')
F3 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F3, label='F1')
F4 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F4, label='F1')
F5 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F5, label='F1')
F6 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F6, label='F1')
F7 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F7, label='F1')
F8 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F8, label='F1')
F9 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F9, label='F1')
F10 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F10, label='F1')
F11 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F11, label='F1')
F12 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F12, label='F1')

ESC = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_ESCAPE, label='ESC')
SPACE = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_SPACE, label='SPACE')
# ВНИМАНИЕ! Основной ENTER задействоваться не может, т.к. завязан на
# обработку wx виджетов ------------------------v
ENTER = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_NUMPAD_ENTER, label='ENTER')
INS = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_INSERT, label='INS')
DEL = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_DELETE, label='DEL')
HOME = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_HOME, label='HOME')
END = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_END, label='END')
BACKSPACE = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_BACK, label='BACKSPACE')
PAGEUP = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_PAGEUP, label='PAGEUP')
PAGEDOWN = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_PAGEDOWN, label='PAGEDOWN')
SHIFT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_SHIFT, label='SHIFT')
ALT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_ALT, label='ALT')
LEFT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_LEFT, label='LEFT')
RIGHT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_RIGHT, label='RIGHT')
UP = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_UP, label='UP')
DOWN = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_DOWN, label='DOWN')

# Список используемых комбинаций клавиш
CTRL_UP = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_UP, label='CTRL+UP')
CTRL_DOWN = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_DOWN, label='CTRL+DOWN')
CTRL_LEFT = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_LEFT, label='CTRL+LEFT')
CTRL_RIGHT = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_RIGHT, label='CTRL+RIGHT')

# Разделитель наименования комбинации клавиш
KEY_COMBUNE_NAME_SEPARATOR = '_'


def get_key_combine(key_combin_name):
    """
    Получить описание комбинации клавиш.
    @param key_combin_name: Имя комбинации клавиш.
        По мнемоническому правилу в имени комбинации клашиш дожен присутствовать
        символ <_>. Например CTRL_F1. В имени одиночных клавиш этот символ отсутствует.
    @return: Словарь описания комбинации клавиш или None если комбинация не определена. 
        Структура описания одиночной клавиши/комбинации клавиш представляет собой словарь
        {
            'mode': режим комбинации клавиш
                    м.б. wx.ACCEL_NORMAL - одиночные клавиши
                    wx.ACCEL_CTRL - комбинация клавиш с нажатой <Control>
                    wx.ACCEL_ALT - комбинация клавиш с нажатой <Alt>
                    wx.ACCEL_SHIFT - комбинация клавиш с нажатой <Shift>
            'key': сама клавиша.
                    м.б. константой wx.WXK_... 
                    Например wx.WXK_F1
                    Либо непосредственным кодом. Например ord('Q').
            'label': отображение комбинации клавиш в помоши.
        }
    """
    key_combin = globals().get(key_combin_name, None)
    if key_combin is None:
        # Такая комбинация не определена в модуле
        # необходимо произвести разбор по имени
        key_combin_list = key_combin_name.split(KEY_COMBUNE_NAME_SEPARATOR)
        # Последний элемент контрольная клавиша:
        ctrl_key = key_combin_list[-1]
        wx_key = 'WXK_' + ctrl_key
        combin_key = getattr(wx, wx_key) if hasattr(wx, wx_key) else globals().get(ctrl_key, ord(ctrl_key))
        # Остальные элементы комбинации:
        if key_combin_list[:-1]:
            combin_mode = 0
            for ctrl_key in key_combin_list[:-1]:
                if ctrl_key == 'CTRL':
                    combin_mode |= wx.ACCEL_CTRL
                elif ctrl_key == 'ALT':
                    combin_mode |= wx.ACCEL_ALT
                elif ctrl_key == 'SHIFT':
                    combin_mode |= wx.ACCEL_SHIFT
                else:
                    log.warning(u'Не поддерживается клавиша <%s> в комбинации клавиши' % ctrl_key)
        else:
            # Одиночная клавиша
            combin_mode = wx.ACCEL_NORMAL
        key_combin = dict(mode=combin_mode, key=combin_key,
                          label=key_combin_name.replace(KEY_COMBUNE_NAME_SEPARATOR, '+'))

    return key_combin
