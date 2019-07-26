#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговой формы отображения текущего системного окружения имен для отладки.
"""

import wx

try:
    from . import view_debug_env_dlg_proto
except ImportError:
    import view_debug_env_dlg_proto

from ic.log import log
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)

VIEW_OBJECT_TYPES = (int, float, str, dict, tuple, list)

DEFAULT_NAME_COLUMN_WIDTH = 250


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

    def init(self):
        """
        Инициализация диалогового окна.
        """
        self.local_treeListCtrl.SetColumnWidth(0, DEFAULT_NAME_COLUMN_WIDTH)
        self.global_treeListCtrl.SetColumnWidth(0, DEFAULT_NAME_COLUMN_WIDTH)

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

    def refresh_env(self, tree_ctrl=None, env=None, bHideProtected=True):
        """
        Обновить контрол древовидного представления пространства имен.
        @param tree_ctrl: Контрол древовидного представления пространства имен.
        @param env: Словарь пространства имен.
        @param bHideProtected: Скрыть имена, начинающиеся на '__' т.е.
            специально скрываемые/системные.
        @return: True/False.
        """
        if not isinstance(env, dict):
            log.warning(u'Не корректный тип <%s> словаря пространства имен' % env.__class__.__name__)
            return False

        tree_content = {'name': u'Локальное пространство имен', 'content': u'', 'type': u'', '__children__': list()}
        for name, obj in env.items():
            if bHideProtected and name.startswith('__'):
                # Скрыть имена специально скрываемые / системные
                continue

            if type(obj) in VIEW_OBJECT_TYPES:
                item = dict(name=name, content=str(obj), type=obj.__class__.__name__, obj=obj)
                tree_content['__children__'].append(item)
        return self.setTreeContent(ctrl=tree_ctrl, tree_data=tree_content,
                                   columns=('name', 'content', 'type'))

    def build_item_children(self, tree_ctrl=None, parent_item=None, children_dict=None, bHideProtected=True):
        """
        Достроить дочерние элементы.
        @param tree_ctrl: Контрол древовидного представления пространства имен.
        @param parent_item: Элемент дерева
        @param children_dict: Словарь дочерних элементов.
        @param bHideProtected: Скрыть имена, начинающиеся на '__' т.е.
            специально скрываемые/системные.
        @return: True/False.
        """
        if not isinstance(children_dict, dict):
            log.warning(u'Не корректный тип <%s> словаря пространства имен' % children_dict.__class__.__name__)
            return False

        parent_item_content = self.getItemData_tree(ctrl=tree_ctrl, item=parent_item)
        for name, obj in children_dict.items():
            if bHideProtected and name.startswith('__'):
                # Скрыть имена специально скрываемые / системные
                continue

            if type(obj) in VIEW_OBJECT_TYPES:
                child_content = dict(name=name, content=str(obj), type=obj.__class__.__name__, obj=obj)
                if '__children__' not in parent_item_content:
                    parent_item_content['__children__'] = list()
                parent_item_content['__children__'].append(child_content)
        return self.appendBranch_TreeListCtrl(treelist_ctrl=tree_ctrl, parent_item=parent_item,
                                              node=parent_item_content,
                                              columns=('name', 'content', 'type'))

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

    def onOkButtonClick(self, event):
        """
        Обработчик нажатия кнопки OK.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onLocalSelectionChange(self, event):
        """
        Обработчик смены выбора элемента в дереве локального пространства имен.
        """
        item = event.GetItem()
        item_data = self.getItemData_tree(ctrl=self.local_treeListCtrl, item=item)
        obj = item_data.get('obj', None)
        if isinstance(obj, object) and not item_data['__children__']:
            children_dict = dict([(name, getattr(obj, name)) for name in dir(obj)])
            self.build_item_children(tree_ctrl=self.local_treeListCtrl,
                                     parent_item=item, children_dict=children_dict)
        event.Skip()

    def onGlobalSelectionChange(self, event):
        """
        Обработчик смены выбора элемента в дереве глобального пространства имен.
        """
        item = event.GetItem()
        item_data = self.getItemData_tree(ctrl=self.global_treeListCtrl, item=item)
        obj = item_data.get('obj', None)
        if isinstance(obj, object) and not item_data.get('__children__', None):
            children_dict = dict([(name, getattr(obj, name)) for name in dir(obj)])
            self.build_item_children(tree_ctrl=self.global_treeListCtrl,
                                     parent_item=item, children_dict=children_dict)
        event.Skip()


def view_debug_namespace_dialog(parent=None, env_locals=None, env_globals=None):
    """
    Отобразить пространство имен (локальное и глобальное) для просмотра.
    @param parent: Родительское окно.
        Если не определено, то берется главное.
    @param env_locals: Словарь локального пространства имен (locals).
    @param env_globals: Словарь глобального пространства имен (locals).
    @return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    if env_locals is None:
        env_locals = dict()

    if env_globals is None:
        env_globals = dict()

    dlg = None
    try:
        dlg = icViewDebugEnvDlg(parent=parent)
        # dlg.init()
        dlg.set_locals(env_locals=env_locals)
        dlg.set_globals(env_globals=env_globals)

        dlg.ShowModal()

        dlg.Destroy()
        return True
    except:
        log.fatal(u'Ошибка отображения диалогового окна просмотра пространств имен')
        if dlg:
            dlg.Destroy()

    return False


def test():
    """
    Функция тестирования.
    @return:
    """
    app = wx.PySimpleApp()

    frame = wx.Frame()
    view_debug_namespace_dialog(parent=frame,
                                env_locals=locals(), env_globals=globals())
    app.MainLoop()


if __name__ == '__main__':
    test()