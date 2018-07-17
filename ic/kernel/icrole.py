#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовый класс роли.
"""

from ic.utils import icprotector
from . import icpermission


class icRole(object):
    """
    Базовый класс роли.
    """
    id = 'role'
    permissions = []
    
    def __init__(self, title='', description='', *arg, **kwarg):
        """
        Конструктор.
        @param title: Краткое описание.
        @parma description: Описание роли.
        """
        self.title = title
        self.description = description
        
    def getPermissions(self):
        """
        Возвращает список разрешений данной роли.
        """
        return self.permissions


class icAdminRole(icRole):
    """
    Администратор системы.
    """
    id = 'Admin'
    permissions = icprotector.readonly((icpermission.view_permission,
                                        icpermission.edit_permission,
                                        icpermission.add_permission,
                                        icpermission.delete_permission,
                                        ))


class icManagerRole(icAdminRole):
    """
    Пользователь с правами администратора.
    """
    id = 'Manager'


class icEditorRole(icRole):
    """
    Редактор.
    """
    id = 'Editor'
    permissions = icprotector.readonly((icpermission.view_permission,
                                        icpermission.edit_permission,
                                        ))


class icMemberRole(icRole):
    """
    Пользователь.
    """
    id = 'Member'
    permissions = icprotector.readonly((icpermission.view_permission,
                                        ))


class icContributorRole(icRole):
    """
    Пользователь с правами расширения системы.
    """
    id = 'Contributor'
    permissions = icprotector.readonly((icpermission.view_permission,
                                        icpermission.add_permission,
                                        icpermission.delete_permission
                                        ))
