#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль меню управления правами и пользователями системы.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import flatmenu

from ic.imglib import common as imglib
from . import prj_security

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


class icMenuUserNode(flatmenu.FlatMenu):
    """
    Меню управления правами и пользователями системы.
    """

    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getRoot().getParent()

        if issubclass(self._Parent.__class__, prj_security.icPrjSecurity):
            # 'Новый пользователь'
            self.newID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newID, u'Новый пользователь', u'Новый пользователь',
                                         normalBmp=imglib.imgUser)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onNewUser, id=self.newID)
            # 'Новая группа пользователей'
            self.newGrpID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newGrpID,
                                         u'Новая группа пользователей',
                                         u'Новая группа пользователей',
                                         normalBmp=imglib.imgUsers)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onNewUserGroup, id=self.newGrpID)
            # 'Новая роль'
            self.newID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newID, u'Новая роль', u'Новая роль',
                                         normalBmp=imglib.imgRole)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onNewRole, id=self.newID)

        elif issubclass(self._Parent.__class__, prj_security.icPrjUser) or \
            issubclass(self._Parent.__class__, prj_security.icPrjUserGroup) or \
            issubclass(self._Parent.__class__, prj_security.icPrjRole):
            
            if issubclass(self._Parent.__class__, prj_security.icPrjUserGroup):
                # Новый юзер
                self.newID = wx.NewId()
                item = flatmenu.FlatMenuItem(self, self.newID, u'Новый пользователь', u'Новый пользователь',
                                             normalBmp=imglib.imgUser)
                self.AppendItem(item)
                prj_tree_ctrl.Bind(wx.EVT_MENU, self.onNewUser, id=self.newID)

                self.AppendSeparator()

            # 'Переиментвать пользователя'
            self.renameID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.renameID, u'Переименовать', u'Переименовать',
                                         normalBmp=imglib.imgRename)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRenameUser, id=self.renameID)

            self.AppendSeparator()

            # 'Удалить пользователя'
            self.delID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.delID, u'Удалить', u'Удалить',
                                         normalBmp=imglib.imgTrash)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onDelUser, id=self.delID)

    def onNewUser(self, event):
        """
        Добавить нового пользователя.
        """
        users_node = self._Parent
        new_user = users_node.createUser()
        tree_prj = self._Parent.getRoot().getParent()
        if new_user:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.addBranchInSelection(new_user)
            tree_prj.SelectItem(new_item)
            new_user.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def onNewRole(self, event):
        """
        Добавить новую роль.
        """
        security_node = self._Parent
        new_role = security_node.createRole()
        tree_prj = self._Parent.getRoot().getParent()
        if new_role:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.addBranchInSelection(new_role)
            tree_prj.SelectItem(new_item)
            new_role.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()
        
    def onNewUserGroup(self, event):
        """
        Добавить новую группу пользователей.
        """
        users_node = self._Parent
        new_user_grp = users_node.createUserGroup()
        tree_prj = self._Parent.getRoot().getParent()
        if new_user_grp:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.addBranchInSelection(new_user_grp)
            tree_prj.SelectItem(new_item)
            new_user_grp.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()
        
    def onDelUser(self, event):
        """
        Удалить.
        """
        users_node = self._Parent.getParent()
        ok = users_node.delUser(self._Parent.name)
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Удалить объект из отображаемого дерева
            tree_prj.Delete(self._Parent.tree_id)
        # Обновление дерева проектов
        tree_prj.Refresh()

    def onRenameUser(self, event):
        """
        Переименовать.
        """
        tree_prj = self._Parent.getRoot().getParent()
        node = self._Parent
        tree_prj.EditLabel(node.tree_id)
        # Обновление дерева проектов
        tree_prj.Refresh()
