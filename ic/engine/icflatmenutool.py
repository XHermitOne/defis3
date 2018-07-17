#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса инструмента горизонтального меню.
"""

# --- Подключение библиотек ---
import wx
import wx.lib.agw.flatmenu as flatmenu

# --- Спецификации ---
SPC_IC_FLATMENUTOOL = {'short_help': None,  # Всплывающая подсказка
                       'pic1': None,        # Образ пункта
                       'pic2': None,        # Образ выключенного пункта
                       'item': None,        # Пункт, связанный с инструментом
                       'kind': 'normal',    # Вид инструмента меню
                       'onSelected': None,  # Блок кода на выбор инструмента
                       }

__version__ = (0, 0, 0, 2)


class icFlatMenuToolPrototype(object):
    """
    Класс инструмента горизонтального меню.
    """

    def __init__(self, parent, id, helpString='', kind=wx.ITEM_NORMAL,
                 normalBmp=wx.NullBitmap, disabledBmp=wx.NullBitmap, description=''):
        """
        Конструктор.
        """
        self._parent = parent
        self._id = id
        self._helpString = helpString
        self._kind = kind
        self._normalBmp = normalBmp
        self._disabledBmp = disabledBmp
        self._description = description
        
    def GetParent(self):
        """
        Родительское горизонтальное меню.
        """
        return self._parent
    
    def GetId(self):
        """
        Идентификатор.
        """
        return self._id
    
    def GetKind(self):
        """
        Вид инструмента.
        """
        return self._kind
    
    def GetHelpString(self):
        """
        Всплывающая подсказка.
        """
        return self._helpString
    
    def GetDescription(self):
        """
        Дополнительное описание.
        """
        return self._description
    
    def GetNormalBmp(self):
        """
        Картинка инструмента в нормальном состоянии.
        """
        return self._normalBmp
    
    def GetDisabledBmp(self):
        """
        Картинка инструмента в выключенном состоянии.
        """
        return self._disabledBmp
