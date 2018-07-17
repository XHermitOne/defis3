#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль меню управления правами и пользователями системы.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import flatmenu

import ic.imglib.common as imglib
import ic.dlg.ic_dlg as ic_dlg
from . import prj_security

_ = wx.GetTranslation


class icMenuUserNode(flatmenu.FlatMenu):
    """
    Меню управления правами и пользователями системы.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = Parent_
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getRoot().getParent()

        if issubclass(self._Parent.__class__, prj_security.PrjSecurity):
            # 'Новый пользователь'
            self.newID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newID, u'Новый пользователь', u'Новый пользователь',
                                         normalBmp=imglib.imgUser)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnNewUser, id=self.newID)
            # 'Новая группа пользователей'
            self.newGrpID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newGrpID,
                                         u'Новая группа пользователей',
                                         u'Новая группа пользователей',
                                         normalBmp=imglib.imgUsers)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnNewUserGroup, id=self.newGrpID)
            # 'Новая роль'
            self.newID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.newID, u'Новая роль', u'Новая роль',
                                         normalBmp=imglib.imgRole)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnNewRole, id=self.newID)

        elif issubclass(self._Parent.__class__, prj_security.PrjUser) or \
            issubclass(self._Parent.__class__, prj_security.PrjUserGroup) or \
            issubclass(self._Parent.__class__, prj_security.PrjRole):
            
            if issubclass(self._Parent.__class__, prj_security.PrjUserGroup):
                # Новый юзер
                self.newID = wx.NewId()
                item = flatmenu.FlatMenuItem(self, self.newID, u'Новый пользователь', u'Новый пользователь',
                                             normalBmp=imglib.imgUser)
                self.AppendItem(item)
                prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnNewUser, id=self.newID)

                self.AppendSeparator()

            # 'Переиментвать пользователя'
            self.renameID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.renameID, u'Переименовать', u'Переименовать',
                                         normalBmp=imglib.imgRename)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnRenameUser, id=self.renameID)

            self.AppendSeparator()

            # 'Удалить пользователя'
            self.delID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.delID, u'Удалить', u'Удалить',
                                         normalBmp=imglib.imgTrash)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnDelUser, id=self.delID)

    def OnNewUser(self, event):
        """
        Добавить нового пользователя.
        """
        users_node = self._Parent
        new_user = users_node.createUser()
        tree_prj = self._Parent.getRoot().getParent()
        if new_user:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(new_user)
            tree_prj.SelectItem(new_item)
            new_user.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnNewRole(self, event):
        """
        Добавить новую роль.
        """
        security_node = self._Parent
        new_role = security_node.createRole()
        tree_prj = self._Parent.getRoot().getParent()
        if new_role:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(new_role)
            tree_prj.SelectItem(new_item)
            new_role.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()
        
    def OnNewUserGroup(self, event):
        """
        Добавить новую группу пользователей.
        """
        users_node = self._Parent
        new_user_grp = users_node.createUserGroup()
        tree_prj = self._Parent.getRoot().getParent()
        if new_user_grp:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(new_user_grp)
            tree_prj.SelectItem(new_item)
            new_user_grp.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()
        
    def OnDelUser(self, event):
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

    def OnRenameUser(self, event):
        """
        Переименовать.
        """
        tree_prj = self._Parent.getRoot().getParent()
        node = self._Parent
        tree_prj.EditLabel(node.tree_id)
        # Обновление дерева проектов
        tree_prj.Refresh()
