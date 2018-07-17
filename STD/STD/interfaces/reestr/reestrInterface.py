#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------
# Name:        reestrInterface.py
# Purpose:     Интерфейс базового реестров.
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

import STD.interfaces.reestr.contextInterface as icnt
import ic.utils.ic_cache as ic_cache

#   Виды панелей
id_edt_panel = 1
id_view_panel = 2
id_print_panel = 3

class icBaseReestrInterface:
    """
    Базовый интерфейс реестра.
    """

    def __init__(self, context=None, *arg, **kwarg):
        """
        Конструктор.
        """
        #   Объект реестра, на который указывает курсор.
        self.curObj = None
        #   Положение текущего объекта
        self.curItem = None
        
        #   Указатель на контекст
        self.context = context
        if not context:
            self.context = icnt.icReestrContextInterface()

        #   Буфер панелей редактирования объектов
        self.objBuff = ic_cache.icCache(str(self.__class__))

    def addObject(self, *arg, **kwarg):
        """
        Добавляет объект в реестр.
        """
        pass
        
    def CreateEditPanel(self, obj=None, *arg, **kwarg):
        """
        Создает панель редактирования <Функциональность определяется в
        дочернем классе>.
        """
        pass
        
    def delObject(self, *arg, **kwarg):
        """
        Удаляет объект из системы.
        """
        pass
        
    def FindObject(self, *arg, **kwarg):
        """
        Поиск объекта в реестре.
        """
        pass
    
    def GetContext(self, *arg, **kwarg):
        """
        Возвращает контекст объекта.
        """
        return self.context

    def GetCurrentObj(self):
        """
        Возвращает объект реестра, на который указывает курсор.
        """
        return self.curObj
        
    def GetCurrentItem(self):
        """
        Возвращает положение текущего объекта.
        """
        return self.curItem
        
    def GetFromBuff(self, id_obj=None, typPanel=id_edt_panel):
        """
        Возвращает панель редактирования из буфера.
        """
        if id_obj:
            return self.objBuff.get(typPanel, id_obj)
        
    def GetEditPanel(self, obj=None, bBuff=True, *arg, **kwarg):
        """
        Возвращает объект редактирования.

        @type obj: C{icObject}
        @param obj: Объект, чью панель редактирования вызываем.
        @type bBuff: C{bool}
        @param bBuff: Признак буферизации панели редактирования.
        """
        if not obj:
            obj = self.curObj
            
        #   Ищем в буфере
        panel = None
        if bBuff:
            panel = self.GetFromBuff(obj.GetObjectUUID(), id_edt_panel)
        
        if not panel:
            panel = self.CreateEditPanel(obj)
        
    def GetPrintObject(self, *arg, **kwarg):
        """
        Возвращает указатель на объект печати объекта реестра.
        """
        pass
    
    def GetViewPanel(self, *arg, **kwarg):
        """
        Возвращает объект просмотра.
        """
        pass

    def SetContext(self, contetx, *arg, **kwarg):
        """
        Устанавливает контекст объекта.
        """
        if issubclass(context.__class__, icnt.icReestrContextInterface):
            self.context = context

    def SetCurrentItem(self, cur):
        """
        Возвращает положение текущего объекта.
        """
        self.curItem = cur
    
    def Update(self, *arg, **kwarg):
        """
        Обновить содержимое объекта.
        """
        pass

if __name__ == '__main__':
    intf = icBrowsReestrInterface()
