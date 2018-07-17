#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса пунта меню.
"""

# --- Подключение библиотек ---
import wx
import wx.lib.agw.flatmenu as flatmenu

# --- Константы ---
# Виды пунктов меню
IC_ITEM_KIND = ('normal', 'separator', 'check', 'radio')

# --- Спецификации ---
SPC_IC_FLATMENUITEM = {'label': 'item',        # Надпись
                       'hot_key': None,        # Горячая клавиша
                       'short_help': None,     # Всплывающая подсказка
                       'pic1': None,           # Образ пункта
                       'pic2': None,           # Образ выключенного пункта
                       'onSelected': None,     # Блок кода на выбор пункта
                       'kind': 'normal',       # Вид пункта меню
                       }

__version__ = (0, 0, 0, 2)


class icFlatMenuItemPrototype(flatmenu.FlatMenuItem):
    """
    Класс пункта меню.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        flatmenu.FlatMenuItem.__init__(self, *args, **kwargs)

        if not hasattr(self, 'name'):
            # Если имя не определено, то имя пункта меню - идентификатор
            self.name = str(self.GetId())
        
    def getName(self):
        """
        Имя пункта меню.
        """
        return self.name
    
    def getMenuBar(self):
        """
        Получить горизонтальное меню.
        """
        menu_bar = self.GetMenu().GetMenuBar()
        if menu_bar:
            return menu_bar
        else:
            return self.GetMenu().getMenuBar()
