#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Базовое ядро системы.
"""

from . import icobject
from . import ickernel_context
from . import icbaseuser

DEFAULT_USER = 'root'


class icBaseKernel(icobject.icObject):
    """
    Базовое ядро.
    """

    def __init__(self, context=None, *arg, **kwarg):
        # Если контекст не определен создаем его.
        if not context:
            context = ickernel_context.icKernelContext(self)
        # Объект пользователя
        self._User = None
        icobject.icObject.__init__(self, '__kernel__', -1, context, *arg, **kwarg)

    def getUser(self):
        """
        Возвращает объект залогиненного пользователя.
        """
        return self._User

    def Login(self, user=DEFAULT_USER, passw=None):
        """
        Вход в ситему.
        """
        obj = icbaseuser.icRootUser()
        self._User = None
        if obj.Login(user, passw):
            self._User = obj

    def Logout(self):
        """
        Выход из системы.
        """
        self._User = None

    def _reg_object(self, obj, name):
        """
        Регестрирует объект в контексте ядра.
        @param obj: Объект.
        @param name: Имя объекта.
        """
        self.GetContext().reg_object(obj, name)

    def getObject(self, name):
        """
        Получить зарегистрированный объект по имени.
        @param name: Имя объекта.
        @return: Искомый объект или None, если не найден.
        """
        return self.GetContext().get_object(name)
