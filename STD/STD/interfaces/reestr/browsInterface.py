#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------
# Name:        browsInterface.py
# Purpose:     Интерфейс базового реестра.
#
# Author:      <Okoneshnikov A. V.>
#
# Created:     05.06.06
# Copyright:   (c) 2006 Infocenter
# Licence:     <your licence>
# -----------------------------------------------------------------------------
"""
# Версия
__version__ = (0, 0, 0, 1)

class icBrowsReestrInterface:
    """
    Интерфейс базового реестра.
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        #   Указатель на текущий реестр
        self._reestr = None
        #   Указатель на текущий элемент реестра
        self.item = None
        
    def GetContext(self):
        """
        Возвращает контекст объекта.
        """
        pass

    def GetReestr(self, reestr):
        """
        Возвращает указатель на текущий реестра.
        """
        return self._reestr
        
    def SetContext(self, context):
        """
        Устанавливает контекст реестра
        """
        pass
        
    def SetReestr(self, reestr):
        """
        Устанавливает реестр в качестве текущего.
        """
        self._reestr = reestr