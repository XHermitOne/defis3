#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления мета-деревьями.
"""

import wx
import wx.dataview
import wx.gizmos

from ic.components import icwidget
from ic.engine import treectrl_manager
from ic.log import log

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_METATREELISTCTRL = {'metatree': None,    # Паспорт объекта описания мета-дерева
                           '__parent__': icwidget.SPC_IC_WIDGET,
                           '__attr_hlp__': {'metatree': u'Паспорт объекта описания мета-дерева',
                                            },
                           }

# Ширина колонки по умолчанию
DEFAULT_TREE_LIST_COLUMN_WIDTH = 200


class icMetaTreeListCtrlProto(wx.gizmos.TreeListCtrl,
                              treectrl_manager.icTreeCtrlManager):
    """
    Контрол управления мета-деревьями.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.gizmos.TreeListCtrl.__init__(self, *args, **kwargs)

        # Корневой элемент дерева
        self._root_item = None

        # Объект
        self._metatree = None

    def getColumnLabels(self):
        """
        Получить надписи колонок.
        Контрол в любом случае имеет одну колонку для отображения метадерева.
        Переопределяемый метод.
        @return: Список надписай колонок.
        """
        return list()

    def getColumnWidths(self):
        """
        Получить ширины колонок.
        Контрол в любом случае имеет одну колонку для отображения метадерева.
        Переопределяемый метод.
        @return: Список ширин колонок.
        """
        return list()

    def setMetaTree(self, metatree=None, auto_build=True):
        """
        Установить объект описания мета-дерева.
        @param metatree: Объект описания мета-дерева.
        @param auto_build: Автоматическое построение дерева?
        """
        self._metatree = metatree

        if auto_build:
            self.build(self._metatree)

    def build(self, metatree=None, column_labels=None, column_widths=None):
        """
        Построение дерева метаобъектов.
        @param metatree: Объект описания мета-дерева.
            Если не определен, то берется установленный объект.
        @param column_labels: Список надписей колонок.
        @param column_widths: Список ширин колонок.
        @return: True/False.
        """
        if metatree is None:
            metatree = self._metatree
        if metatree is None:
            log.warning(u'Не определен объект метадерева в контроле <%s>' % self.name)
            return False

        try:
            self.DeleteAllItems()
            metatree.Load()

            # Установить колонки
            if column_labels is None:
                column_labels = self.getColumnLabels()
            if column_widths is None:
                column_widths = self.getColumnWidths()
            column_labels = [u''] + column_labels
            column_widths = [DEFAULT_TREE_LIST_COLUMN_WIDTH] + column_widths
            column_widths = [column_widths[i] if i < len(column_widths) else 0 for i in range(len(column_labels))]

            cols = [dict(label=label, width=column_widths[i]) for i, label in enumerate(column_labels)]
            # log.debug(u'Установка колонок %s' % str(cols))
            self.setColumns_tree_list_ctrl(ctrl=self, cols=tuple(cols))

            self._root_item = self.AddRoot(metatree.description)
            self.setItemImage_tree_ctrl(ctrl=self, item=self._root_item, image=metatree.getPic())
            return self._build(metatree=metatree, meta_data=metatree.getStorage().items())
        except:
            log.fatal(u'Ошибка построения метадерева <%s> в контроле <%s>' % (metatree.name, self.name))
        return False

    def _build(self, metatree, meta_data):
        """
        Построение дерева метаобъектов.
        @param metatree: Объект описания мета-дерева.
        @param meta_data: Данные метадерева.
        @return: True/False.
        """
        log.debug(u'Загруженные данные %s' % str(meta_data))
        # item_data = metatree.

        return True