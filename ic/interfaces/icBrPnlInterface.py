#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс для правой панели браузера.
"""


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
