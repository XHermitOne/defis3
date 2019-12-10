#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Интерфейс для правой панели браузера.
"""

__version__ = (0, 1, 1, 1)


class icBrowsPanelInterface:
    """
    Интерфейс для правой панели браузера.
    """
    def __init__(self, metaObj=None):
        """
        """
        self.metaObj = metaObj
        
    def LoadData(self, *arg, **kwarg):
        """
        Функция загрузки данных на панель.
        """
        
    def SaveData(self, *arg, **kwarg):
        """
        Функция сохранения данных на панели.
        """
