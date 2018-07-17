#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------
# Name:        browsPanelInterface.py
# Purpose:     Интерфейс базовой панели редактирования и просмотра реестров.
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

class icBrowsPanelReestrInterface:
    """
    """
    def __init__(self, edit_mode=True, *arg, **kwarg):
        """
        """
        self._bEditMode = edit_mode
        self._object = None

    def get_object(self):
        """
        Возвращает указатель на редактируемый объект.
        """
        return  self._object

    def IsEditMode(self):
        """
        Возвращает признак режима редактирования.
        """
        return self._bEditMode

    def LoadData(self, *arg, **kwarg):
        """
        Загрузить данные на панель редактирования.
        """
        pass
    
    def SaveData(self, *arg, **kwarg):
        """
        Соохранить данные, которые были изменены на панеле редактирования.
        """
        pass
        
    def SetEditMode(self, edit_mode=True):
        """
        Устанавливае режим редакирования.
        """
        self._bEditMode = edit_mode
        
    def set_object(self, obj):
        """
        Устанавливает редактируемый объект.
        """
        self._object = obj