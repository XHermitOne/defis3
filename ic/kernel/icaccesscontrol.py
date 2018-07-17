#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .io_prnt import outLog
from . import icexceptions

ACCESS_PUBLIC = 0
ACCESS_PRIVATE = 1
ACCESS_PROTECTED = 2


class SecurityInfo(object):
    """
    Encapsulate security information.
    """
    def __init__(self):
        self.names = {}
        self.roles = {}

    def _setaccess(self, names, access):
        for name in names:
            if self.names.get(name, access) != access:
                outLog(u'Conflicting security declarations for <%s>' % name)
            self.names[name] = access
        
    def declarePublic(self, name, *names):
        """
        Declare names to be publicly accessible.
        """
        self._setaccess((name,) + names, ACCESS_PUBLIC)

    def declarePrivate(self, name, *names):
        """
        Declare names to be inaccessible to restricted code.
        """
        self._setaccess((name,) + names, ACCESS_PRIVATE)

    def declareProtected(self, permission_name, name, *names):
        """
        Declare names to be associated with a permission.
        """
        self._setaccess((name,) + names, permission_name)

    def declareObjectPublic(self):
        """
        Declare the object to be publicly accessible.
        """
        self._setaccess(('',), ACCESS_PUBLIC)

    def declareObjectPrivate(self):
        """
        Declare the object to be inaccessible to restricted code.
        """
        self._setaccess(('',), ACCESS_PRIVATE)

    def declareObjectProtected(self, permission_name):
        """
        Declare the object to be associated with a permission.
        """
        self._setaccess(('',), permission_name)


class ClassSecurityInfo(SecurityInfo):
    """
    Encapsulate security information for class objects.
    """

    def can_access(self, name, permissions):
        """
        Определяет права доступа к атрибуту.
        """
        access = self.names.get(name, ACCESS_PUBLIC)
        if access == ACCESS_PUBLIC or access in [el.id for el in permissions]:
            return True
        print(self.names, name, permissions, access, ACCESS_PUBLIC)
        raise icexceptions.MethodAccessDeniedException(('Access denied to attribute <%s>' % name,))

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
    Encapsulate security information for modules.
    """
    def __init__(self, module_name=None):
        self.names = {}
        if module_name is not None:
            global _moduleSecurity
            _moduleSecurity[module_name] = self

    def declareProtected(self, permission_name, *names):
        """
        Cannot declare module names protected.
        """
        pass

    def declareObjectProtected(self, permission_name):
        """
        Cannot declare module protected.
        """
        pass
