#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Базовый класс управления ресурсом в редакторе.
"""

__version__ = (0, 1, 1, 1)


class IEditorResourceManager(object):
    """
    Класс управления ресурсом в редакторе.
    """
    component_class = None
        
    @staticmethod
    def InitResource(res, *arg, **kwarg):
        pass
    
    @staticmethod
    def DeleteResource(res, *arg, **kwarg):
        pass
    
    @staticmethod
    def DeleteChild(res, child, *arg, **kwarg):
        pass
        
    @staticmethod
    def SetObjProperty(obj, attr, value, *arg, **kwarg):
        """
        Изменяет свойство объекта при редактировании в редакторе форм.
        """
        pass
