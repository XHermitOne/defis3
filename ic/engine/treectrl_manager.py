#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного древовидного контрола WX.
"""

# Подключение библиотек
# import wx

from ic.log import log
from ic.utils import ic_str


__version__ = (0, 1, 1, 1)


class icTreeCtrlManager(object):
    """
    Менеджер WX древовидного контрола.
    В самом общем случае в этот класс перенесены функции работы
    с древовидными контролами из менеджера форм.
    Перенос сделан с целью рефакторинга.
    Также этот класс могут наследовать классы специализированных
    менеджеров, которые работают со деревьями записей/объектов.
    """
    def _setTree_TreeListCtrl(self, treelist_ctrl=None, tree_data=None, columns=(),
                              ext_func=None, do_expand_all=False):
        """
        Установить данные в контрол wx.TreeListCtrl.
        @param treelist_ctrl: Контрол wx.TreeListCtrl.
        @param tree_data: Данные дерева:
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        @param columns: Кортеж колонок:
            ('ключ словаря данных 1', ...)
            Первый ключ будет являться главным.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            treelist_ctrl - Контрол wx.TreeListCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @param do_expand_all: Произвести автоматическое распахивание дерева?
        @return: True/False.
        """
        if treelist_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeListCtrl для заполнения данными')
            return False
        if not tree_data:
            log.warning(u'Не определены данные для заполнения контрола wx.TreeListCtrl')
            return False

        treelist_ctrl.DeleteAllItems()
        self.appendBranch_TreeListCtrl(treelist_ctrl=treelist_ctrl,
                                       node=tree_data, columns=columns,
                                       ext_func=ext_func)

        if do_expand_all:
            treelist_ctrl.ExpandAll(treelist_ctrl.GetRootItem())
        return True

    def setTree_TreeListCtrl(self, treelist_ctrl=None, tree_data=None, columns=(),
                             ext_func=None, do_expand_all=False):
        """
        Установить данные в контрол wx.TreeListCtrl.
        @param treelist_ctrl: Контрол wx.TreeListCtrl.
        @param tree_data: Данные дерева:
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        @param columns: Кортеж колонок:
            ('ключ словаря данных 1', ...)
            Первый ключ будет являться главным.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            treelist_ctrl - Контрол wx.TreeListCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @param do_expand_all: Произвести автоматическое распахивание дерева?
        @return: True/False.
        """
        try:
            return self._setTree_TreeListCtrl(treelist_ctrl, tree_data, columns,
                                              ext_func, do_expand_all)
        except:
            log.fatal(u'Ошибка установки данных в контрол wx.TreeListCtrl.')

    def _appendTree_root(self, treelist_ctrl=None, node=None, columns=(), ext_func=None):
        """
        Внутренняя функция.
        Добавление корневого элемента.
        @return:
        """
        # Добавление корневого элемента
        label = ic_str.toUnicode(node.get(columns[0], u''))
        parent_item = treelist_ctrl.AddRoot(label)
        for i, column in enumerate(columns[1:]):
            label = ic_str.toUnicode(node.get(columns[i + 1], u''))
            treelist_ctrl.SetItemText(parent_item, label, i + 1)

        # Прикрепляем данные к элементу дерева
        treelist_ctrl.SetPyData(parent_item, node)

        # Дополнительная обработка
        if ext_func:
            ext_func(treelist_ctrl, parent_item, node)
        return parent_item

    def _appendBranch_TreeListCtrl(self, treelist_ctrl=None,
                                  parent_item=None, node=None, columns=(),
                                  ext_func=None):
        """
        Добавить ветку в узел дерева контрола wx.TreeListCtrl.
        @param treelist_ctrl: Контрол wx.TreeListCtrl.
        @param parent_item: Родительский элемент, в который происходит добавление.
            Если не указан, то создается корневой элемент.
        @param node: Данные узла.
            Если словарь, то добавляется 1 узел.
            Если список, то считается что необходимо добавить несколько узлов.
        @param columns: Кортеж колонок:
            ('ключ словаря данных 1', ...)
            Первый ключ будет являться главным.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            treelist_ctrl - Контрол wx.TreeListCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @return: True/False.
        """
        if treelist_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeListCtrl для заполнения данными')
            return False

        if parent_item is None:
            if (isinstance(node, list) or isinstance(node, tuple)) and len(node) > 1:
                log.warning(u'Создается фиктивный корневой элемент wx.TreeListCtrl')
                parent_item = treelist_ctrl.AddRoot(u'')
                result = self.appendBranch_TreeListCtrl(treelist_ctrl,
                                                        parent_item=parent_item,
                                                        node=dict(__children__=node),
                                                        columns=columns,
                                                        ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self._appendTree_root(treelist_ctrl, node, columns, ext_func)
            elif isinstance(node, dict):
                parent_item = self._appendTree_root(treelist_ctrl, node, columns, ext_func)
            else:
                log.warning(u'Не поддерживаемый тип данных узла данныж wx.TreeListCtrl')
                return False

        for record in node.get('__children__', list()):
            label = ic_str.toUnicode(record.get(columns[0], u''))
            item = treelist_ctrl.AppendItem(parent_item, label)
            for i, column in enumerate(columns[1:]):
                label = ic_str.toUnicode(record.get(columns[i + 1], u''))
                treelist_ctrl.SetItemText(item, label, i + 1)

            # Дополнительная обработка
            if ext_func:
                ext_func(treelist_ctrl, item, record)

            # Прикрепляем данные к элементу дерева
            treelist_ctrl.SetPyData(item, record)

            if '__children__' in record and record['__children__']:
                for child in record['__children__']:
                    self.appendBranch_TreeListCtrl(treelist_ctrl,
                                                   item, child,
                                                   columns=columns,
                                                   ext_func=ext_func)

    def appendBranch_TreeListCtrl(self, treelist_ctrl=None,
                                  parent_item=None, node=None, columns=(),
                                  ext_func=None):
        """
        Добавить ветку в узел дерева контрола wx.TreeListCtrl.
        @param treelist_ctrl: Контрол wx.TreeListCtrl.
        @param parent_item: Родительский элемент, в который происходит добавление.
            Если не указан, то создается корневой элемент.
        @param node: Данные узла.
            Если словарь, то добавляется 1 узел.
            Если список, то считается что необходимо добавить несколько узлов.
        @param columns: Кортеж колонок:
            ('ключ словаря данных 1', ...)
            Первый ключ будет являться главным.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            treelist_ctrl - Контрол wx.TreeListCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @return: True/False.
        """
        try:
            return self._appendBranch_TreeListCtrl(treelist_ctrl, parent_item,
                                                   node, columns, ext_func)
        except:
            log.fatal(u'Ошибка добавления ветки в узел дерева контрола wx.TreeListCtrl.')
        return False

