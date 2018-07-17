#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Описание пользователя системы.
"""

from . import icrole
from . import icexceptions
from . import icpermission
from ic.utils import coderror
from ic.utils import icprotector


class icBaseUser(object):
    """
    Базовый класс пользователя системы.
    """
    roles = icprotector.readonly([])

    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        # Списоск ролей пользователя
        self.username = None
        
    def Login(self, user, passw=None, *arg, **kwarg):
        """
        Вход в систему.
        """
        pass
    
    def Logout(self):
        """
        Выход из системы.
        """
        pass
        
    def getRoles(self):
        """
        Возвращает список ролей.
        """
        return self.roles
        
    def getPermissions(self):
        """
        Возвращает список разрешений для данной роли.
        """
        lst = []
        for role in self.roles:
            lst = lst + list(role.getPermissions())
        return lst


class icRootUser(icBaseUser):
    """
    Root системы.
    """
    roles = icprotector.readonly((icrole.icAdminRole(),))
    
    def __init__(self, user=None, passw=None, *arg, **kwarg):
        """
        Конструктор.
        """
        # Списоск ролей пользователя
        icBaseUser.__init__(self)
        if user:
            self.Login(user, passw)
                
    def __is_valid(self, user, passw):
        """
        Проверка соответствия пароля.
        """
        return user == 'root'
            
    def Login(self, user, passw=None, *arg, **kwarg):
        """
        Вход в систему.
        """
        if not self.__is_valid(user, passw):
            raise icexceptions.LoginInvalidException((coderror.IC_LOGIN_ERROR, 'root login error'))
        
        self.username = user
        return True
