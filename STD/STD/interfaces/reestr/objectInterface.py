#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Интерфейс базового объекта реестров.
Автор(ы): Оконешников А.В.

# -----------------------------------------------------------------------------
# Name:        objectInterface.py
# Purpose:     Интерфейс базового объекта реестров.
#
# Author:      <Okoneshnikov A. V.>
#
# Created:     05.06.06
# Copyright:   (c) 2006 Infocenter
# Licence:     <your licence>
# -----------------------------------------------------------------------------
"""
import ic.kernel.icobject as icobject
# Версия
__version__ = (0, 0, 0, 1)

#class icBaseReestrObjectInterface(icobject.icObject):
class icBaseReestrObjectInterface:
    """
    """
    def __init__(self, reestr=None):
        """
        Конструктор интерфейса.
        
        @type reestr: C{icBaseReestrInterface}
        @param reestr: Ссылка на реестр, куда будет помещен объект.
        """
        self._reestr = reestr
        # Ссылка на контекс объекта
        if reestr:
            cont = reestr.GetContext()
        else:
            cont = None
    
        #icobject.icObject.__init__(self, context=cont)
        
    def Lock(self):
        """
        Блокирует объект для изменения другим пользователем.
        """
        pass

    def UnLock(self):
        """
        Снимает блокировку другим пользователем.
        """
        pass
    
    def IsLock(self):
        """
        Возвращает признак блокировки объекта.
        """
        pass
        
    def GetContext(self):
        """
        Возвращает ссылку на контекст объекта.
        """
        return self._context
    
    def GetEditPanel(self, *arg, **kwarg):
        """
        Возвращает панель редактирования.
        """
        pass

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
        
    def SetContext(self, context):
        """
        Устанавливает контекст объекта.
        """
        self._context = context