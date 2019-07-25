#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговой формы отображения текущего системного окружения имен для отладки.
"""

import wx

from . import view_debug_env_dlg_proto

from ic.log import log
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)

VIEW_OBJECT_TYPES = (int, float, str, dict, tuple, list, object)


class icViewDebugEnvDlg(view_debug_env_dlg_proto.icViewDebugEnvDialogProto,
                        form_manager.icFormManager):
    """
    Диалоговая форма отображения текущего системного окружения имен для отладки.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        view_debug_env_dlg_proto.icViewDebugEnvDialogProto.__init__(self, *args, **kwargs)

        self._locals = dict()
        self._globals = dict()

    def set_locals(self, env_locals=None, bRefresh=True):
        """
        Установить словарь локального пространства имен.
        @param env_locals: Словарь локального пространства имен.
        @param bRefresh: Автоматически обновить дерево локального пространства имен.
        @param: True/False
        """
        if env_locals is None:
            env_locals = dict()

        if not isinstance(env_locals, dict):
            log.warning(u'Не корректный тип <%s> словаря локального пространства имен' % env_locals.__class__.__name__)
            self._locals = dict()
            return False

        self._locals = env_locals

        if bRefresh:
            self.refresh_locals()
        return True

    def set_globals(self, env_globals=None, bRefresh=True):
        """
        Установить словарь глобального пространства имен.
        @param env_globals: Словарь глобального пространства имен.
        @param bRefresh: Автоматически обновить дерево глобального пространства имен.
        @param: True/False
        """
        if env_globals is None:
            env_globals = dict()

        if not isinstance(env_globals, dict):
            log.warning(u'Не корректный тип <%s> словаря глобального пространства имен' % env_globals.__class__.__name__)
            self._globals = dict()
            return False

        self._globals = env_globals

        if bRefresh:
            self.refresh_globals()
        return True

    def refresh_env(self, tree_ctrl=None, env=None):
        """
        Обновить контрол древовидного представления пространства имен.
        @param tree_ctrl: Контрол древовидного представления пространства имен.
        @param env: Словарь пространства имен.
        @return: True/False.
        """
        if not isinstance(env, dict):
            log.warning(u'Не корректный тип <%s> словаря пространства имен' % env.__class__.__name__)
            return False

        tree_content = {'name': u'Локальное пространство имен', 'content': u'', '__children__': list()}
        for name, obj in env.items():
            if type(obj) in VIEW_OBJECT_TYPES:
                item = dict(name=name, content=str(obj))
                tree_content['__children__'].append(item)
        return self.setTreeData(ctrl=tree_ctrl, tree_data=tree_content)

    def refresh_locals(self, env_locals=None):
        """
        Обновить контрол древовидного представления ЛОКАЛЬНОГО пространства имен.
        @param env_locals: Словарь ЛОКАЛЬНОГО пространства имен.
        @return: True/False.
        """
        if env_locals is None:
            env_locals = self._locals

        return self.refresh_env(self.local_treeListCtrl, env=env_locals)

    def refresh_globals(self, env_globals=None):
        """
        Обновить контрол древовидного представления ГЛОБАЛЬНОГО пространства имен.
        @param env_globals: Словарь ГЛОБАЛЬНОГО пространства имен.
        @return: True/False.
        """
        if env_globals is None:
            env_globals = self._globals

        return self.refresh_env(self.global_treeListCtrl, env=env_globals)
