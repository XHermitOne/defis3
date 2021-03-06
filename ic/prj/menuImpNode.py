#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль меню добавления/редактирования импортируемых подсистем.
"""

import wx
from wx.lib.agw import flatmenu

from ic.imglib import common as imglib
from ic.utils import clipboard

_ = wx.GetTranslation

__version__ = (0, 1, 1, 1)


class icMenuImpNode(flatmenu.FlatMenu):
    """
    Меню добавления/редактирования импортируемых подсистем.
    """
    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getParentRoot().getParent()

        # Дополнительные ресурсы
        if self._Parent.include_nodes:
            # Дополнительные ресурсы для добавления
            # Внутренний реестр ресурсов для доступа к ним по идентификатору
            self._node_reg = {}
            for node_class in self._Parent.include_nodes:
                node = node_class(self._Parent)

                # Обработка меню добавления ресурса
                res_id = wx.NewId()
                # Зарегистрировать ресурс во внутреннем реестре
                self._node_reg[res_id] = node
                item = flatmenu.FlatMenuItem(self, res_id, node.label, node.label,
                                             normalBmp=node.img)
                self.AppendItem(item)
                prj_tree_ctrl.Bind(wx.EVT_MENU, self.onAddSubSys, id=res_id)

            self.AppendSeparator()

            # Обновление подсистем
            refresh_id = wx.NewId()
            item = flatmenu.FlatMenuItem(self, refresh_id,
                                         u'Обновить подсистемы', u'Обновить подсистемы',
                                         normalBmp=imglib.imgRefreshPage)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRefreshSubSys, id=refresh_id)

    def onAddSubSys(self, event):
        """
        Функция добавления подсистемы.
        """
        sub_sys_node = self._node_reg[event.GetId()]
        imp_sub_systems = sub_sys_node.newImpSys()
        if imp_sub_systems is not None:
            ok = sub_sys_node.buildSubSysTree()

            # Добавить объект в отображаемом дереве
            tree_prj = self._Parent.getRoot().getParent()
            if ok:
                # Сразу сохранить проект
                self._Parent.getRoot().save()
                # Построить ветку дерева,
                # соответствующую импортируемой подсистеме
                new_item = tree_prj.addBranchInSelection(sub_sys_node)
            # Обновление дерева проектов
            tree_prj.Refresh()

    def onRefreshSubSys(self, event):
        """
        Обновление подсистем.
        """
        sub_systems = self._Parent
        sub_systems.refreshSubSystems()


class icMenuImpSysNode(flatmenu.FlatMenu):
    """
    Меню обновления импортируемой подсистемы.
    """
    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getParentRoot().getParent()

        # Обновление подсистемы
        refresh_id = wx.NewId()
        item = flatmenu.FlatMenuItem(self, refresh_id,
                                     u'Обновить подсистему', u'Обновить подсистему',
                                     normalBmp=imglib.imgRefreshPage)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRefreshSubSys, id=refresh_id)
        
        self.AppendSeparator()

        # Переподключить подсистему
        link_id = wx.NewId()
        # Связь с подсистемой
        item = flatmenu.FlatMenuItem(self, link_id,
                                     u'Подключить подсистему', u'Подключить подсистему',
                                     normalBmp=imglib.imgEdtPluginIn)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onLinkSubSys, id=link_id)

        # Отключение подсистемы
        unlink_id = wx.NewId()
        item = flatmenu.FlatMenuItem(self, unlink_id,
                                     u'Отключить подсистему', u'Отключить подсистему',
                                     normalBmp=imglib.imgEdtPluginOut)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnUnlinkSubSys, id=unlink_id)
    
    def onRefreshSubSys(self, event):
        """
        Обновление подсистем.
        """
        sub_system = self._Parent
        sub_system.refreshSubSys()
        
    def onLinkSubSys(self, event):
        """
        Изменить связь с подсистемой.
        """
        sub_system = self._Parent
        sub_system.changeLink()

    def OnUnlinkSubSys(self, event):
        """
        Отключить подсистему.
        """
        sub_system = self._Parent
        sub_system.unLink()


class icMenuNotImpSysNode(flatmenu.FlatMenu):
    """
    Меню обновления не импортированной подсистемы.
    """
    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getParentRoot().getParent()

        # Переподключить подсистему
        link_id = wx.NewId()
        item = flatmenu.FlatMenuItem(self, link_id,
                                     u'Подключить подсистему', u'Подключить подсистему',
                                     normalBmp=imglib.imgEdtPluginIn)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onLinkSubSys, id=link_id)

        # Отключение подсистемы
        unlink_id = wx.NewId()
        item = flatmenu.FlatMenuItem(self, unlink_id,
                                     u'Отключить подсистему', u'Отключить подсистему',
                                     normalBmp=imglib.imgEdtPluginOut)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onUnlinkSubSys, id=unlink_id)

    def onLinkSubSys(self, event):
        """
        Переимпортировать подсистему.
        """
        sub_system = self._Parent
        sub_system.changeLink()
        prj = sub_system.getParentRoot()
        prj.synchroPrj(True)

    def onUnlinkSubSys(self, event):
        """
        Отключить подсистему.
        """
        sub_system = self._Parent
        sub_system.unLink()


class icMenuImpResNode(flatmenu.FlatMenu):
    """
    Меню копирования ресурсов из импортируемых подсистем.
    """
    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getParentRoot().getPrjTreeCtrl()

        # Копирование ресурсов из импортированных подсистемм
        copy_id = wx.NewId()
        item = flatmenu.FlatMenuItem(self, copy_id,
                                     u'Копировать', u'Копировать',
                                     normalBmp=imglib.imgEdtMnuCopy)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onCopyRes, id=copy_id)

    def onCopyRes(self, event):
        """
        Копировать ресурс.
        """
        node = self._Parent.copy()
        # Работа с системным клиппордом
        clipboard.toClipboard(node)        
