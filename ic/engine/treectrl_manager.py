#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного древовидного контрола WX.
"""

# Подключение библиотек
import hashlib

import wx
import wx.dataview
import wx.gizmos

from ic.log import log
from ic.utils import strfunc
from ic.bitmap import bmpfunc
from ic.dlg import dlgfunc


__version__ = (0, 1, 6, 1)

UNKNOWN = u'Не определено'

# Размер картинок элементов дерева по умолчанию
DEFAULT_ITEM_IMAGE_WIDTH = 16
DEFAULT_ITEM_IMAGE_HEIGHT = 16
DEFAULT_ITEM_IMAGE_SIZE = (DEFAULT_ITEM_IMAGE_WIDTH, DEFAULT_ITEM_IMAGE_HEIGHT)

TREE_CTRL_IMAGE_LIST_CACHE_NAME = '__image_list_cache'


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
            treelist_ctrl.ExpandAll()
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
        label = strfunc.toUnicode(node.get(columns[0], UNKNOWN))
        # log.debug(u'Надпись %s : %s' % (columns, label))
        if isinstance(treelist_ctrl, wx.gizmos.TreeListCtrl):
            parent_item = treelist_ctrl.AddRoot(label)
            # Заполнение данных колонок
            for i, column in enumerate(columns[1:]):
                label = strfunc.toUnicode(node.get(columns[i + 1], UNKNOWN))
                treelist_ctrl.SetItemText(parent_item, label, i + 1)
            # Прикрепляем данные к элементу дерева
            treelist_ctrl.SetItemData(parent_item, node)
        elif isinstance(treelist_ctrl, wx.dataview.TreeListCtrl):
            root = treelist_ctrl.GetRootItem()
            parent_item = treelist_ctrl.AppendItem(root, label)
            # Заполнение данных колонок
            for i, column in enumerate(columns[1:]):
                label = strfunc.toUnicode(node.get(columns[i + 1], UNKNOWN))
                treelist_ctrl.SetItemText(parent_item, i + 1, label)
            # Прикрепляем данные к элементу дерева
            treelist_ctrl.SetItemData(parent_item, node)
        elif isinstance(treelist_ctrl, wx.TreeCtrl):
            parent_item = treelist_ctrl.AddRoot(label)
            # Прикрепляем данные к элементу дерева
            treelist_ctrl.SetItemData(parent_item, node)
        else:
            log.warning(u'Не поддерживаемый тип <%s> контрола дерева' % treelist_ctrl.__class__.__name__)
            return None

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
                parent_item = treelist_ctrl.AddRoot(UNKNOWN)
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
            label = strfunc.toUnicode(record.get(columns[0], u''))
            if isinstance(treelist_ctrl, wx.gizmos.TreeListCtrl):
                item = treelist_ctrl.AppendItem(parent_item, label)
                for i, column in enumerate(columns[1:]):
                    label = strfunc.toUnicode(record.get(columns[i + 1], u''))
                    treelist_ctrl.SetItemText(item, label, i + 1)
            elif isinstance(treelist_ctrl, wx.dataview.TreeListCtrl):
                item = treelist_ctrl.AppendItem(parent_item, label)
                for i, column in enumerate(columns[1:]):
                    label = strfunc.toUnicode(record.get(columns[i + 1], u''))
                    treelist_ctrl.SetItemText(item, i + 1, label)
            elif isinstance(treelist_ctrl, wx.TreeCtrl):
                item = treelist_ctrl.AppendItem(parent_item, label)
            else:
                log.warning(u'Не поддерживаемый тип контрола <> списко-древовидного представления' % treelist_ctrl.__class__.__name__)
                continue

            # Дополнительная обработка
            if ext_func:
                ext_func(treelist_ctrl, item, record)

            # Прикрепляем данные к элементу дерева
            treelist_ctrl.SetItemData(item, record)

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

    def getItemData_tree(self, ctrl=None, item=None):
        """
        Получить прикрепленные данные к элементу дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева.
            Если None, то берется корневой элемент дерева.
        @return: Прикрепленные данные к элементу дерева или None в случае ошибки.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для определения прикрепленных данных к элементу')
            return None

        if item is None:
            item = ctrl.GetRootItem()

        if not item.IsOk():
            log.warning(u'Не корректный элемент дерева <%s>' % str(item))
            return None

        if isinstance(ctrl, wx.TreeCtrl):
            return ctrl.GetItemData(item)
        elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
            return ctrl.GetMainWindow().GetItemData(item)
        elif isinstance(ctrl, wx.dataview.TreeListCtrl):
            return ctrl.GetItemData(item)
        else:
            log.warning(u'Не поддерживаемый тип древовидного контрола <%s>' % ctrl.__class__.__name__)
        return None

    # Другое наименование метода
    getItemData_TreeCtrl = getItemData_tree
    getItemRecord_TreeCtrl = getItemData_tree

    def getSelectedItemData_tree(self, ctrl=None):
        """
        Данные выбранного элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @return: Данные выбранного элемента дерева или None в случае ошибки.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для определения прикрепленных данных к элементу')
            return None

        selected_item = ctrl.GetSelection()
        if selected_item:
            return self.getItemData_tree(ctrl=ctrl, item=selected_item)
        return None

    # Другое наименование метода
    getSelectedItemData_TreeCtrl = getSelectedItemData_tree
    getSelectedItemRecord_TreeCtrl = getSelectedItemData_tree

    def setItemData_tree(self, ctrl=None, item=None, data=None):
        """
        Прикрепить данные к элементу дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент дерева.
        @param data: Прикрепляемые данные.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для прикрепления данных к элементу')
            return False

        if item is None:
            item = ctrl.GetRootItem()
        if isinstance(ctrl, wx.TreeCtrl):
            return ctrl.SetItemData(item, data)
        elif isinstance(ctrl, wx.dataview.TreeListCtrl) or isinstance(ctrl, wx.gizmos.TreeListCtrl):
            return ctrl.GetMainWindow().SetItemData(item, data)
        else:
            log.warning(u'Не поддерживаемый тип древовидного контрола <%s>' % ctrl.__class__.__name__)
        return False

    # Другое наименование метода
    setItemData_TreeCtrl = setItemData_tree
    setItemRecord_TreeCtrl = setItemData_tree

    def setSelectedItemData_tree(self, ctrl=None, data=None):
        """
        Установить данные выбранного элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param data: Устанавливаемые данные.
        @return: Данные выбранного элемента дерева или None в случае ошибки.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для установки прикрепленных данных к элементу')
            return None

        selected_item = ctrl.GetSelection()
        if selected_item:
            return self.setItemData_tree(ctrl=ctrl, item=selected_item, data=data)
        return None

    # Другое наименование метода
    setSelectedItemData_TreeCtrl = setSelectedItemData_tree
    setSelectedItemRecord_TreeCtrl = setSelectedItemData_tree

    def getItemChildren(self, ctrl=None, item=None):
        """
        Список дочерних элементов узла дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Узел/элемент дерева. Если None, то корневой элемент.
        @return: Список дочерних элементов узла дерева 
            или None в случае ошибки.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для определения списка дочерних элементов')
            return list()

        try:
            # Определить узел
            if item is None:
                item = ctrl.GetRootItem()

            # Список дочерних элементов
            children = list()

            children_count = ctrl.GetChildrenCount(item, False)
            cookie = None
            for i in range(children_count):
                if i == 0:
                    child, cookie = ctrl.GetFirstChild(item)
                else:
                    child, cookie = ctrl.GetNextChild(item, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            log.fatal(u'ОШИБКА компонента <%s> метода определения списка дочерних элементов' % str(ctrl))
        return None

    def getItemChildrenCount(self, ctrl=None, item=None):
        """
        Количество дочерних элементов узла дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Узел/элемент дерева. Если None, то корневой элемент.
        @return: Количество дочерних элементов или -1 в случае ошибки.
        """
        try:
            # Определить узел
            if item is None:
                item = ctrl.GetRootItem()
            return ctrl.GetChildrenCount(item)
        except:
            log.fatal(u'ОШИБКА компонента <%s> метода определения количества дочерних элементов' % str(ctrl))
        return None

    def setItemColour_requirement(self, ctrl=None, fg_colour=None, bg_colour=None, requirement=None, item=None):
        """
        Установить цвет элементов дерева в контроле по определенному условию.
        @param ctrl: Контрол wx.TreeCtrl.
        @param fg_colour: Цвет текста, если условие выполненно.
        @param bg_colour: Цвет фона, если условие выполненно.
        @param requirement: lambda выражение, формата:
            lambda item: ...
            Которое возвращает True/False.
            Если True, то установка цвета будет сделана.
            False - строка не расцвечивается.
        @param item: Текущий обрабатываемый элемент дерева.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для установки цвета')
            return False

        if requirement is None:
            log.warning(u'Не определено условие установки цвета')
            return False

        if fg_colour is None and bg_colour is None:
            log.warning(u'Не определены цвета')
            return False

        for child in self.getItemChildren(ctrl=ctrl, item=item):

            colorize = requirement(child)
            if fg_colour and colorize:
                self.setItemForegroundColour(ctrl, child, fg_colour)
            if bg_colour and colorize:
                self.setItemBackgroundColour(ctrl, child, bg_colour)

            # Рекурсивно обработать дочерние элементы
            if ctrl.ItemHasChildren(child):
                self.setItemColour_requirement(ctrl, fg_colour=fg_colour,
                                               bg_colour=bg_colour,
                                               requirement=requirement,
                                               item=child)
        return True

    def setItemForegroundColour(self, ctrl, item, colour):
        """
        Установить цвет текста элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева.
        @param colour: Цвет.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для установки цвета')
            return False
        try:
            ctrl.SetItemTextColour(item, colour)
            return True
        except:
            log.fatal(u'Ошибка установки цвета текста элемента дерева')
        return False

    def setItemBackgroundColour(self, ctrl, item, colour):
        """
        Установить цвет фона элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева.
        @param colour: Цвет.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для установки цвета')
            return False
        try:
            ctrl.SetItemBackgroundColour(item, colour)
            return True
        except:
            log.fatal(u'Ошибка установки цвета фона элемента дерева')
        return False

    def _setTree_TreeCtrl(self, tree_ctrl=None, tree_data=None, label=None,
                          ext_func=None, do_expand_all=False):
        """
        Установить данные в контрол wx.TreeCtrl.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param tree_data: Данные дерева:
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        @param label: Ключ для определения надписи элемента дерева.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            tree_ctrl - Контрол wx.TreeCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @param do_expand_all: Произвести автоматическое распахивание дерева?
        @return: True/False.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для заполнения данными')
            return False
        if not tree_data:
            log.warning(u'Не определены данные для заполнения контрола wx.TreeCtrl')
            return False

        tree_ctrl.DeleteAllItems()
        self.appendBranch_TreeCtrl(tree_ctrl=tree_ctrl, node=tree_data,
                                   label=label, ext_func=ext_func)

        if do_expand_all:
            tree_ctrl.ExpandAll()
        return True

    def setTree_TreeCtrl(self, tree_ctrl=None, tree_data=None, label=None,
                         ext_func=None, do_expand_all=False):
        """
        Установить данные в контрол wx.TreeCtrl.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param tree_data: Данные дерева:
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        @param label: Ключ для определения надписи элемента дерева.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            tree_ctrl - Контрол wx.TreeCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @param do_expand_all: Произвести автоматическое распахивание дерева?
        @return: True/False.
        """
        try:
            return self._setTree_TreeCtrl(tree_ctrl, tree_data, label,
                                          ext_func, do_expand_all)
        except:
            log.fatal(u'Ошибка установки данных в контрол wx.TreeCtrl.')

    def _appendBranch_TreeCtrl(self, tree_ctrl=None,
                               parent_item=None, node=None,
                               label=None, ext_func=None):
        """
        Добавить ветку в узел дерева контрола wx.TreeCtrl.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param parent_item: Родительский элемент, в который происходит добавление.
            Если не указан, то создается корневой элемент.
        @param node: Данные узла.
            Если словарь, то добавляется 1 узел.
            Если список, то считается что необходимо добавить несколько узлов.
        @param label: Ключ для определения надписи элемента дерева.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            tree_ctrl - Контрол wx.TreeCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @return: True/False.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для заполнения данными')
            return False

        if parent_item is None:
            if (isinstance(node, list) or isinstance(node, tuple)) and len(node) > 1:
                log.warning(u'Создается фиктивный корневой элемент wx.TreeCtrl')
                parent_item = tree_ctrl.AddRoot(UNKNOWN)
                result = self._appendBranch_TreeCtrl(tree_ctrl,
                                                     parent_item=parent_item,
                                                     node=dict(__children__=node),
                                                     label=label,
                                                     ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self._appendTree_root(tree_ctrl, node, (), ext_func)
            elif isinstance(node, dict):
                # log.debug(u'Ключ надписи %s : %s. Узел %s' % (label, item_label, str(node)))
                parent_item = self._appendTree_root(tree_ctrl, node, (label,), ext_func)
            else:
                log.warning(u'Не поддерживаемый тип данных узла данныж wx.TreeCtrl')
                return False

        for record in node.get('__children__', list()):
            item_label = strfunc.toUnicode(record.get(label, UNKNOWN))
            item = tree_ctrl.AppendItem(parent_item, item_label)

            # Дополнительная обработка
            if ext_func:
                ext_func(tree_ctrl, item, record)

            # Прикрепляем данные к элементу дерева
            tree_ctrl.SetItemData(item, record)

            if '__children__' in record and record['__children__']:
                self._appendBranch_TreeCtrl(tree_ctrl,
                                            parent_item=item, node=record,
                                            label=label,
                                            ext_func=ext_func)
        return True

    def appendBranch_TreeCtrl(self, tree_ctrl=None,
                              parent_item=None, node=None,
                              label=None,
                              ext_func=None):
        """
        Добавить ветку в узел дерева контрола wx.TreeCtrl.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param parent_item: Родительский элемент, в который происходит добавление.
            Если не указан, то создается корневой элемент.
        @param node: Данные узла.
            Если словарь, то добавляется 1 узел.
            Если список, то считается что необходимо добавить несколько узлов.
        @param label: Ключ для определения надписи элемента дерева.
        @param ext_func: Дополнительная функция обработки:
            В качестве аргументов длжна принимать:
            tree_ctrl - Контрол wx.TreeCtrl.
            item - Текущий обрабатываемый элемент контрола.
            node - Данные узла, соответствующие элементу контрола.
        @return: True/False.
        """
        try:
            return self._appendBranch_TreeCtrl(tree_ctrl, parent_item,
                                               node, label, ext_func)
        except:
            log.fatal(u'Ошибка добавления ветки в узел дерева контрола wx.TreeCtrl.')
        return False

    def setRootTitle(self, tree_ctrl, title):
        """
        Поменять надпись корневого элемента.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param title: Надпись.
        @return: True/False.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для установки надписи корневого элемента')
            return False

        try:
            root = tree_ctrl.GetRootItem()
            if root:
                tree_ctrl.SetItemText(root, title)
                return True
        except:
            log.fatal(u'Ошибка установки надписи корневого элемента <%s>' % str(tree_ctrl))
        return False

    def expandChildren(self, tree_ctrl=None, item=None, all_children=False):
        """
        Распахнуть дочерние элементы.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент.
        @param all_children: Распахнуть все дочерние элементы?
        @return: True/False.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для распахивания дочерних элементов')
            return False

        try:
            if item is None:
                if isinstance(tree_ctrl, wx.dataview.TreeListCtrl):
                    # Для этого контролакорнем считем первый дочерний элемент корня
                    item = tree_ctrl.GetFirstChild(tree_ctrl.GetRootItem())
                else:
                    item = tree_ctrl.GetRootItem()

            if all_children:
                tree_ctrl.ExpandAllChildren(item)
            else:
                tree_ctrl.Expand(item)
            return True
        except:
            log.fatal(u'Ошибка функции распахивания дочерних элементов <%s>' % str(tree_ctrl))
        return False

    def collapseChildren(self, tree_ctrl=None, item=None, all_children=False):
        """
        Свернуть дочерние элементы.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент.
        @param all_children: Свернуть все дочерние элементы?
        @return: True/False.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для сворачивания дочерних элементов')
            return False

        try:
            if item is None:
                item = tree_ctrl.GetRootItem()

            if all_children:
                tree_ctrl.CollapseAllChildren(item)
            else:
                tree_ctrl.Collapse(item)
            return True
        except:
            log.fatal(u'Ошибка функции сворачивания дочерних элементов <%s>' % str(tree_ctrl))
        return False

    def getItemPathLabel(self, tree_ctrl=None, item=None, lPath=None):
        """
        Путь до элемента. Путь - список имен элементов.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент.
        @param lPath: Текущий заполненный путь.
        @return: Список пути до элемента или None в случае ошибки.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для сворачивания дочерних элементов')
            return None

        try:
            if item is None:
                # У корневого элемента пустой путь
                return []

            parent = tree_ctrl.GetItemParent(item)
            # Если есть родительский элемент, то вызвать рекурсивно
            if parent and parent.IsOk():
                if lPath is None:
                    lPath = []
                lPath.insert(-1, tree_ctrl.GetItemText(item))
                return self.getItemPathLabel(tree_ctrl=tree_ctrl, item=parent, lPath=lPath)

            if lPath is None:
                # Это корневой элемент
                lPath = []
            return lPath
        except:
            log.fatal(u'Ошибка определение пути элемента объекта <%s>' % str(tree_ctrl))
        return None

    def getItemLevel(self, tree_ctrl=None, item=None):
        """
        Определить уровень дерева элемента.
        Например у корневого элемента уровень 0.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент.
        @return: Номер уровня или None в случае ошибки.
        """
        label_path = self.getItemPathLabel(tree_ctrl=tree_ctrl, item=item)
        # log.debug(u'Путь до элемента <%s> %s' % (item, str(label_path)))
        return len(label_path) if label_path is not None else None

    def getItemPathData(self, tree_ctrl=None, item=None, lPath=None):
        """
        Путь до элемента. Путь - список данных элементов.
        @param tree_ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то берется корневой элемент.
        @param lPath: Текущий заполненный путь.
        @return: Список пути данных до элемента или None в случае ошибки.
        """
        if tree_ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для сворачивания дочерних элементов')
            return None

        if lPath is None:
            lPath = []

        try:
            item_data = self.getItemData_tree(ctrl=tree_ctrl, item=item)
            lPath.insert(-1, item_data)

            if item is not None and item.IsOk():
                parent = tree_ctrl.GetItemParent(item)
                if not parent.IsOk():
                    # ВНИМАНИЕ! GetItemParent возвращает не None а
                    # не существующий item. Поэтому необходимо делать
                    # проверку на IsOk
                    return lPath
                elif self.isRootTreeItem(ctrl=tree_ctrl, item=parent):
                    parent = None
                # Если есть родительский элемент, то вызвать рекурсивно
                return self.getItemPathData(tree_ctrl=tree_ctrl, item=parent, lPath=lPath)
            return lPath
        except:
            log.fatal(u'Ошибка определение пути элемента объекта <%s>' % str(tree_ctrl))
        return None

    def findItem_requirement(self, ctrl=None, requirement=None, item=None):
        """
        Поиск элемента дерева по требованию.
        @param ctrl: Контрол wx.TreeCtrl.
        @param requirement: lambda выражение, формата:
            lambda item: ...
            Которое возвращает True/False.
            Если True, то элемент удовлетворяет критерию поиска.
            False - строка не удовлетворяет.
        @param item: Текущий обрабатываемый элемент дерева.
        @return: Найденный элемент или None если не найден элемент.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для поиска элемента дерева')
            return False

        if requirement is None:
            log.warning(u'Не определено условие поиска элемента дерева')
            return False

        for child in self.getItemChildren(ctrl=ctrl, item=item):
            is_found = requirement(child)
            if is_found:
                return child

            # Рекурсивно обработать дочерние элементы
            if ctrl.ItemHasChildren(child):
                found_item = self.findItem_requirement(ctrl, requirement=requirement, item=child)
                if found_item:
                    return found_item
        return None

    def getSelectedTreeItem(self, ctrl):
        """
        Выбранный элемент дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @return: Выбранный элемент дерева или None ничего не выбрано.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для выбора элемента дерева')
            return False

        if isinstance(ctrl, wx.TreeCtrl):
            selected_item = ctrl.GetSelection()
            return selected_item if selected_item and selected_item.IsOk() else None
        elif isinstance(ctrl, wx.dataview.TreeListCtrl):
            selected_item = ctrl.GetSelection()
            return selected_item if selected_item and selected_item.IsOk() else None
        elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
            selected_item = ctrl.GetMainWindow().GetSelection()
            return selected_item if selected_item and selected_item.IsOk() else None
        else:
            log.warning(u'Выбранный элемент дерева. Не обрабатываемый тип контрола дерева <%s>' % ctrl.__class__.__name__)
        return None

    def selectTreeItem(self, ctrl, item=None, select=True):
        """
        Выбор элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param item: Элемент дерева. Если item - None, то берется корневой элемент.
        @param select: True - выбрать элемент. False - наоборот снять выбор.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол wx.TreeCtrl для выбора элемента дерева')
            return False

        if item is None:
            item = ctrl.GetRootItem()

        ctrl.SelectItem(item, select=select)
        return True

    def selectTreeRoot(self, ctrl, select=True):
        """
        Выбор корневого элемента дерева.
        @param ctrl: Контрол wx.TreeCtrl.
        @param select: True - выбрать элемент. False - наоборот снять выбор.
        @return: True/False.
        """
        return self.selectTreeItem(ctrl, select=select)

    def setColumns_tree_list_ctrl(self, ctrl=None, cols=()):
        """
        Установить колонки в контрол TreeListCtrl.
        @param ctrl: Объект контрола.
        @param cols: Список описаний колонок.
            колонка может описываться как списком
            ('Заголовок колонки', Ширина колонки, Выравнивание)
            так и словарем:
            {'label': Заголовок колонки,
            'width': Ширина колонки,
            'align': Выравнивание}
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол TreeListCtrl для добавления колонок')
            return False

        if isinstance(ctrl, wx.gizmos.TreeListCtrl):
            col_count = ctrl.GetColumnCount()
            if col_count:
                for i_col in range(col_count-1, -1, -1):
                    ctrl.RemoveColumn(i_col)
            for i_col, col in enumerate(cols):
                if isinstance(col, dict):
                    self.appendColumn_TreeListCtrl(ctrl, label=col.get('label', u''),
                                                   width=col.get('width', -1),
                                                   align=col.get('align', 'LEFT'))
                elif isinstance(col, list) or isinstance(col, tuple):
                    self.appendColumn_TreeListCtrl(ctrl, label=col[0], width=col[1], align=col[2])
                else:
                    log.warning(u'Не поддерживаемый тип данных колонки')
            # Назначить первую колонку главной
            ctrl.SetMainColumn(0)
            return True
        else:
            log.warning(u'Добавление колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def appendColumn_TreeListCtrl(self, ctrl, label=u'', width=-1, align='LEFT'):
        """
        Добавить колонку в wx.TreeListCtrl.
        @param ctrl: Объект контрола wx.TreeListCtrl.
        @param label: Надпись колонки.
        @param width: Ширина колонки.
        @param align: Выравнивание: LEFT/RIGHT.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        try:
            if width <= 0:
                width = wx.DefaultSize.GetWidth()

            col_align = str(align).strip().upper()
            if col_align == 'RIGHT':
                col_format = wx.ALIGN_RIGHT
            elif col_align == 'CENTRE':
                col_format = wx.ALIGN_CENTRE
            elif col_align == 'CENTER':
                col_format = wx.ALIGN_CENTER
            else:
                col_format = wx.ALIGN_LEFT
            ctrl.AddColumn(label, width=width, flag=col_format)
            return True
        except:
            log.fatal(u'Ошибка добавления колонки в контрол wx.TreeListCtrl')
        return False

    def getTreeCtrlImageList(self, ctrl=None, image_width=DEFAULT_ITEM_IMAGE_WIDTH,
                             image_height=DEFAULT_ITEM_IMAGE_HEIGHT):
        """
        Получить список картинок элементов контрола дерева wx.TreeCtrl/wx.TreeListCtrl.
        @param ctrl: Объект контрола wx.TreeListCtrl / wx.TreeCtrl.
        @param image_width: Ширина картинки.
        @param image_height: Высота картинки.
        @return: Объект списка образов.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        image_list = ctrl.GetImageList()
        if not image_list:
            image_list = wx.ImageList(image_width, image_height)
            # ВНИМАНИЕ! Здесь необходимо вставить хотя бы пустой Bitmap
            # Иначе при заполнении контрол валиться
            empty_dx = image_list.Add(bmpfunc.createEmptyBitmap(image_width, image_height))
            ctrl.SetImageList(image_list)
        return image_list

    def getTreeCtrlImageListCache(self, ctrl=None):
        """
        Кеш списка образов.
        @param ctrl: Объект контрола wx.TreeListCtrl / wx.TreeCtrl.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        if not hasattr(ctrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME):
            setattr(ctrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME, dict())
        return getattr(ctrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME)

    def setItemImage_tree_ctrl(self, ctrl=None, item=None, image=None):
        """
        Установить картинку элемента дерева.
        @param ctrl: Объект контрола wx.TreeListCtrl / wx.TreeCtrl.
        @param item: Элемент дерева. Если None, то имеется ввиду корневой элемент.
        @param image: Объект картинки wx.Bitmap. Если не определен, то картинка удаляется.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        if item is None:
            item = ctrl.GetRootItem()

        if image is None:
            ctrl.SetItemImage(item, None)
        else:
            img_idx = self.getImageIndex_tree_ctrl(ctrl=ctrl, image=image, auto_add=True)
            ctrl.SetItemImage(item, img_idx)
        return True

    def getImageIndex_tree_ctrl(self, ctrl=None, image=None, auto_add=True):
        """
        Поиск образа в списке образов wx.TreeCtrl.
        @param ctrl: Объект контрола дерева.
        @param image: Объект образа.
        @param auto_add: Автоматически добавить в список, если отсутствует?
        @return: Индекс образа или -1 если образ не найден.
        """
        if image is None:
            return -1

        if isinstance(image, wx.Bitmap):
            img = image.ConvertToImage()
            img_id = hashlib.md5(img.GetData()).hexdigest()
        elif isinstance(image, wx.Image):
            img_id = hashlib.md5(image.GetData()).hexdigest()
        else:
            log.warning(u'Не обрабатываему тип образа <%s>' % image.__class__.__name__)
            return -1

        # Сначала проверяем в кеше
        img_cache = self.getTreeCtrlImageListCache(ctrl=ctrl)

        img_idx = -1
        if img_id in img_cache:
            img_idx = img_cache[img_id]
        else:
            if auto_add:
                image_list = self.getTreeCtrlImageList(ctrl=ctrl)
                img_idx = image_list.Add(image)
                # Запоминаем в кеше
                img_cache[img_id] = img_idx
        return img_idx

    def appendChildItem_tree_ctrl(self, ctrl=None, parent_item=None,
                                  label=u'', image=None, data=None, select=True):
        """
        Добавить дочерний элемент дерева.
        @param ctrl: Объект контрола дерева.
        @param parent_item: Родительский элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @param label: Надпись нового элемента.
        @param image: Образ нового элемента.
        @param data: Данные, автоматически прикрепляемые к новому элементу.
        @param select: Автоматически выбрать новый элемент?
        @return: Новый элемент дерева или None в случае ошибки.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        if parent_item is None:
            parent_item = ctrl.GetRootItem()

        img_idx = self.getImageIndex_tree_ctrl(ctrl=ctrl, image=image, auto_add=True)

        if isinstance(ctrl, wx.TreeCtrl):
            try:
                new_item = ctrl.AppendItem(parent_item, text=label, image=img_idx, data=data)
                if select:
                    ctrl.SelectItem(new_item)
                return new_item
            except:
                log.fatal(u'Ошибка добавления дочернего элемента')
        else:
            log.warning(u'Не поддерживается добавление дочернего элемента для объекта <%s>' % ctrl.__class__.__name__)
        return None

    def deleteItem_tree_ctrl(self, ctrl=None,item=None, ask=False, select=True):
        """
        Удалить элемент дерева.
        @param ctrl: Объект контрола дерева.
        @param item: Удаляемый элемент дерева.
            Если не определен, то считается что это текущий выбранный элемент.
        @param ask: Спросить о подтверждении удаления?
        @param select: Автоматически выбрать новый элемент?
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        if item is None:
            item = ctrl.GetSelection()

        if not item:
            log.warning(u'Текущий элемент дерева не определен для удаления')
            return False

        do_del = True
        if ask:
            label = ctrl.GetItemText(item)
            do_del = dlgfunc.openAskBox(u'УДАЛЕНИЕ', u'Удалить <%s>' % label)

        if do_del:
            if isinstance(ctrl, wx.TreeCtrl):
                ctrl.Delete(item)
            else:
                log.warning(u'Не обрабатываемый тип объекта контрола дерева <%s>' % ctrl.__class__.__name__)
            return True
        return False

    def _getTreeData(self, ctrl=None, item=None):
        """
        Получить данные дерева.
        @param ctrl: Объект контрола дерева.
        @param item: Текущий обрабатываемый элемент дерева.
            Если не определен, тоберется корневой элемент.
        @return: Словарно-списковая структура дерева или None в случае ошибки.
        """
        if item is None:
            item = ctrl.GetRootItem()

        item_data = self.getItemData_tree(ctrl=ctrl, item=item)
        if item_data is None:
            item_data = dict()

        children = self.getItemChildren(ctrl=ctrl, item=item)
        if children:
            item_data['__children__'] = list()
        for child in children:
            child_data = self._getTreeData(ctrl=ctrl, item=child)
            item_data['__children__'].append(child_data)
        return item_data

    def getTreeData(self, ctrl=None, *args, **kwargs):
        """
        Получить данные дерева.
        @param ctrl: Объект контрола дерева.
        @return: Словарно-списковая структура дерева или None в случае ошибки.
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        try:
            if isinstance(ctrl, wx.TreeCtrl):
                return self._getTreeData(ctrl=ctrl)
            elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
                return self._getTreeData(ctrl=ctrl)
            else:
                log.warning(u'Чтение данных дерева. Не поддерживаемый класс контрола дерева <%s>' % ctrl.__class__.__name__)
            return None
        except:
            log.fatal(u'Ошибка получения данных дерева из <%s>' % str(ctrl))
        return None

    def setTreeData(self, ctrl=None, tree_data=None, bRootExpand=True, *args, **kwargs):
        """
        Установить данные дерева.
        @param ctrl: Объект контрола дерева.
        @param tree_data: Данные дерева.
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        @param bRootExpand: Распахнуть корневой элемент?
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        result = False
        try:
            if isinstance(ctrl, wx.TreeCtrl):
                result = self.setTree_TreeCtrl(tree_ctrl=ctrl, tree_data=tree_data, *args, **kwargs)
            elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
                result = self.setTree_TreeListCtrl(treelist_ctrl=ctrl, tree_data=tree_data, *args, **kwargs)
            elif isinstance(ctrl, wx.dataview.TreeListCtrl):
                result = self.setTree_TreeListCtrl(treelist_ctrl=ctrl, tree_data=tree_data, *args, **kwargs)
            else:
                log.warning(u'Установка данных дерева. Не поддерживаемый класс контрола дерева <%s>' % ctrl.__class__.__name__)

            if result and bRootExpand:
                self.expandChildren(tree_ctrl=ctrl, item=None, all_children=kwargs.get('bExpandAll', False))
            return result
        except:
            log.fatal(u'Ошибка установки данных дерева в <%s>' % str(ctrl))
        return False

    # Другое название метода
    setTreeContent = setTreeData

    def isRootTreeItem(self, ctrl=None, item=None):
        """
        Проверить является ли элемент дерева корневым.
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
        @return: True - корневой элемент / False - нет.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        # log.debug(u'Проверка на корневой элемент %s : %s : %s : %s' % (ctrl.GetRootItem(), item, ctrl.GetRootItem() == item, ctrl.GetItemParent(item).IsOk()))
        return ctrl.GetRootItem() == item

    def isFirstTreeItem(self, ctrl=None, item=None):
        """
        Проверка является ли элемент первым на текущем уровне?
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @return: True - первый элемент / False - нет.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        if item is None:
            # Это корневой элемент. Он всегда первый
            return True

        parent_item = ctrl.GetItemParent(item)
        if parent_item and parent_item.IsOk():
            first_child, cookie = ctrl.GetFirstChild(parent_item)
            # log.debug(u'Проверка на первый элемент [%s]' % str(first_child == item))
            return first_child == item
        elif self.isRootTreeItem(ctrl=ctrl, item=item):
            # Это корневой элемент. Он всегда первый
            return True
        else:
            log.warning(u'Не корректный элемент дерева')
        return False

    def isLastTreeItem(self, ctrl=None, item=None):
        """
        Проверка является ли элемент последним на текущем уровне?
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @return: True - первый элемент / False - нет.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        if item is None:
            # Это корневой элемент. Он всегда последний
            return True

        parent_item = ctrl.GetItemParent(item)
        if parent_item and parent_item.IsOk():
            last_child = ctrl.GetLastChild(parent_item)
            # log.debug(u'Проверка на последний элемент [%s]' % str(last_child == item))
            return last_child == item
        elif self.isRootTreeItem(ctrl=ctrl, item=item):
            # Это корневой элемент. Он всегда последний
            return True
        else:
            log.warning(u'Не корректный элемент дерева')
        return False

    def getParentTreeItem(self, ctrl=None, item=None):
        """
        Получить родительский элемент дерева.
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @return: Родительский элемент или None если его нет.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return None

        parent_item = ctrl.GetItemParent(item)
        return parent_item if parent_item and parent_item.IsOk() else None

    def moveUpTreeItem(self, ctrl=None, item=None, auto_select=True):
        """
        Передвинуть элемент дерева выше в текущем списке.
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @param auto_select: Автоматически выбрать перемещаемый элемент?
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        if item is None:
            # Корневой элемент двигать нельзя
            return False

        parent_item = self.getParentTreeItem(ctrl=ctrl, item=item)
        if parent_item:
            prev_item = ctrl.GetPrevSibling(ctrl.GetPrevSibling(item))
            if prev_item and not prev_item.IsOk():
                prev_item = None
            new_item = ctrl.InsertItem(parent_item, prev_item,
                                       text=ctrl.GetItemText(item),
                                       image=ctrl.GetItemImage(item),
                                       data=self.getItemData_tree(ctrl=ctrl, item=item))
            ctrl.Delete(item)
            if auto_select:
                self.selectTreeItem(ctrl=ctrl, item=new_item)
            return True
        return False

    def moveDownTreeItem(self, ctrl=None, item=None, auto_select=True):
        """
        Передвинуть элемент дерева ниже в текущем списке.
        @param ctrl: Объект контрола дерева.
        @param item: Элемент дерева.
            Если не определен, то считается что это корневой элемент.
        @param auto_select: Автоматически выбрать перемещаемый элемент?
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.TreeCtrl/wx.TreeListCtrl')
            return False

        if item is None:
            # Корневой элемент двигать нельзя
            return False

        parent_item = self.getParentTreeItem(ctrl=ctrl, item=item)
        if parent_item:
            next_item = ctrl.GetNextSibling(item)
            if next_item and not next_item.IsOk():
                next_item = None
            new_item = ctrl.InsertItem(parent_item, next_item,
                                       text=ctrl.GetItemText(item),
                                       image=ctrl.GetItemImage(item),
                                       data=self.getItemData_tree(ctrl=ctrl, item=item))
            ctrl.Delete(item)
            if auto_select:
                self.selectTreeItem(ctrl=ctrl, item=new_item)
            return True
        return False
