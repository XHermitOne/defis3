#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовый класс разрешения.
"""

import wx

_ = wx.GetTranslation

# Список зарегистрированных разрешений.
__system_permissions = {}


class icPermission(object):

    def __init__(self, id, title='', description='', component_type=None, defaultState=False):
        """
        Конструктор.
        @param id: Идентификатор разрешения.
        @param title: Краткое описание.
        @parma description: Описание.
        @param component_type: Тип объекта, породившего "разрешение". Используется для 
            группировки разрешений.
        @param defaultState: Состояние по умолчанию.
        """
        self.id = id
        self.title = title
        self.description = description
        self.type = component_type
        self.state = defaultState


def registerPermission(permission):
    """
    Регистрация разрешения.
    """
    global __system_permissions
    __system_permissions[permission.id] = permission


def getPermissionDct():
    global __system_permissions
    return __system_permissions
    
view_permission = icPermission('view', _('Can view'), '', '__SYSTEM__')
edit_permission = icPermission('edit', _('Can edit'), '', '__SYSTEM__')
add_permission = icPermission('add', _('Can add'), '', '__SYSTEM__')
delete_permission = icPermission('delete', _('Can delete'), '', '__SYSTEM__')


def _gen_base_permissions():
    """
    Генерируем базовые разрешения системы.
    """
    registerPermission(view_permission)
    registerPermission(edit_permission)
    registerPermission(add_permission)
    registerPermission(delete_permission)

# Регистрируем базовые разрешения
_gen_base_permissions()
