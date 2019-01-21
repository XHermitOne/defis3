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

UNKNOWN = u'Не определено'


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
        treelist_ctrl.SetItemData(parent_item, node)

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
            label = ic_str.toUnicode(record.get(columns[0], u''))
            item = treelist_ctrl.AppendItem(parent_item, label)
            for i, column in enumerate(columns[1:]):
                label = ic_str.toUnicode(record.get(columns[i + 1], u''))
                treelist_ctrl.SetItemText(item, label, i + 1)

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
            log.error(u'ОШИБКА компонента <%s> метода определения списка дочерних элементов' % str(ctrl))
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
            tree_ctrl.ExpandAll(tree_ctrl.GetRootItem())
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
                parent_item = self._appendTree_root(tree_ctrl, node, (), ext_func)
            else:
                log.warning(u'Не поддерживаемый тип данных узла данныж wx.TreeCtrl')
                return False

        for record in node.get('__children__', list()):
            item_label = ic_str.toUnicode(record.get(label, UNKNOWN))
            item = tree_ctrl.AppendItem(parent_item, item_label)

            # Дополнительная обработка
            if ext_func:
                ext_func(tree_ctrl, item, record)

            # Прикрепляем данные к элементу дерева
            tree_ctrl.SetItemData(item, record)

            if '__children__' in record and record['__children__']:
                self._appendBranch_TreeCtrl(tree_ctrl,
                                            item, record,
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

    def getItemPath(self, tree_ctrl=None, item=None, lPath=None):
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
                return list()

            parent = tree_ctrl.GetItemParent(item)
            # Если есть родительский элемент, то вызвать рекурсивно
            if parent:
                if lPath is None:
                    lPath = []
                lPath.insert(-1, tree_ctrl.GetItemText(item))
                return self.getItemPath(parent, lPath)
            return lPath
        except:
            log.fatal(u'Ошибка определение пути элемента объекта <%s>' % str(tree_ctrl))
        return None
