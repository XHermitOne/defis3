#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ic.log import log
from . import icexceptions

__version__ = (0, 1, 1, 1)

ACCESS_PUBLIC = 0
ACCESS_PRIVATE = 1
ACCESS_PROTECTED = 2


class SecurityInfo(object):
    """
    Класс инкапсулирует информацию о безопасности.
    """
    def __init__(self):
        self.names = {}
        self.roles = {}

    def _setaccess(self, names, access):
        for name in names:
            if self.names.get(name, access) != access:
                log.warning(u'Конфликтные объявления безопасности для <%s>' % name)
            self.names[name] = access
        
    def declarePublic(self, name, *names):
        """
        Объявление имен общедоступными.
        """
        self._setaccess((name,) + names, ACCESS_PUBLIC)

    def declarePrivate(self, name, *names):
        """
        Объявление имен недоступными для ограниченного кода.
        """
        self._setaccess((name,) + names, ACCESS_PRIVATE)

    def declareProtected(self, permission_name, name, *names):
        """
        Объявление имен, связанных с разрешением.
        """
        self._setaccess((name,) + names, permission_name)

    def declareObjectPublic(self):
        """
        Объявить объект общедоступным.
        """
        self._setaccess(('',), ACCESS_PUBLIC)

    def declareObjectPrivate(self):
        """
        Объявить объект недоступным для ограниченного кода.
        """
        self._setaccess(('',), ACCESS_PRIVATE)

    def declareObjectProtected(self, permission_name):
        """
        Объявить объект, связанный с разрешением.
        """
        self._setaccess(('',), permission_name)


class ClassSecurityInfo(SecurityInfo):
    """
    Класс инкапсулирует информацию безопасности для объектов класса.
    """

    def can_access(self, name, permissions):
        """
        Определяет права доступа к атрибуту.
        """
        access = self.names.get(name, ACCESS_PUBLIC)
        if access == ACCESS_PUBLIC or access in [el.id for el in permissions]:
            return True
        print(self.names, name, permissions, access, ACCESS_PUBLIC)
        raise icexceptions.MethodAccessDeniedException(('Нет доступа к атрибуту <%s>' % name,))

    def is_permission(self, id_permission, permissions):
        """
        Проверка на есть ли такое право в списке?
        @param id_permission: Идентификатор.
        @param permissions: Список прав.
        @return: True/False.
        """
        return id_permission in [el.id for el in permissions]


_moduleSecurity = {}
_appliedModuleSecurity = {}


class _ModuleSecurityInfo(SecurityInfo):
    """
    Класс инкапсулирует информацию о безопасности для модулей.
    """
    def __init__(self, module_name=None):
        self.names = {}
        if module_name is not None:
            global _moduleSecurity
            _moduleSecurity[module_name] = self

    def declareProtected(self, permission_name, *names):
        """
        Невозможно объявить имена модулей.
        """
        pass

    def declareObjectProtected(self, permission_name):
        """
        Невозможно объявить модуль защищенным.
        """
        pass
