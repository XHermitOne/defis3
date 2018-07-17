#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль меню управления механизмом модулей.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import flatmenu

import os
import os.path
import ic.imglib.common as imglib
import ic.dlg.ic_dlg as ic_dlg
import ic.utils.clipboard as clipboard
from ic.utils import ic_file
from . import prj_node
from . import prj_module

from ic.bitmap import icimagelibrarybrowser

_ = wx.GetTranslation


class icMenuModNode(flatmenu.FlatMenu):
    """
    Меню управления механизмом модулей.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = Parent_
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getRoot().getParent()

        if issubclass(self._Parent.__class__, prj_node.PrjFolder):
            # Дополнительные ресурсы для добавления
            # Внутренний реестр ресурсов для доступа к ним по идентификатору
            self._node_reg = {}

            node = self._Parent.include_nodes[0](self._Parent)

            # Добавить Модуль
            self.addModuleID = wx.NewId()

            # Зарегистрировать Модуль во внутреннем реестре
            self._node_reg[self.addModuleID] = node

            item = flatmenu.FlatMenuItem(self, self.addModuleID, u'Добавить модуль', u'Добавить модуль',
                                         normalBmp=imglib.imgEdtModule)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddModule, id=self.addModuleID)

            # Добавить Пакет
            self.addPackageID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.addPackageID, u'Добавить пакет', u'Добавить пакет',
                                         normalBmp=imglib.imgPackageOpen)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddPackage, id=self.addPackageID)

            # Добавить проект wxFormBuilder
            self.addFBPID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.addFBPID, u'Добавить wxFormBuilder проект',
                                         u'Добавить wxFormBuilder проект',
                                         normalBmp=imglib.imgDesigner)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddFBP, id=self.addFBPID)
            self._node_reg[self.addFBPID] = self._Parent.include_nodes[1](self._Parent)
    
            # Подменю 'Добавить'
            res_class_menu = flatmenu.FlatMenu()
            for node_class in self._Parent.include_nodes[2:]:
                node = node_class(self._Parent)
                # Обработка меню добавления ресурсного класса
                class_id = wx.NewId()
                # Зарегистрировать ресурс во внутреннем реестре
                self._node_reg[class_id] = node
                item = flatmenu.FlatMenuItem(res_class_menu, class_id,
                                             node.description, node.description,
                                             normalBmp=node.img)
                res_class_menu.AppendItem(item)
                # ВНИМАНИЕ! Выключение пункта меню делать только после
                #   присоединения к меню. Иначе выключение не срабатывает.
                if not node.enable:
                    item.Enable(node.enable)

                res_class_menu.Bind(wx.EVT_MENU, self.OnAddResClass, id=class_id)

            self.AppendMenu(wx.NewId(), u'Добавить ресурсный класс', res_class_menu)
            self.AppendSeparator()
            
        if not issubclass(self._Parent.__class__, prj_module.PrjModules):
            # Подменю 'Буфер обмена'
            self.cutID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.cutID, u'Вырезать', u'Вырезать',
                                         normalBmp=imglib.imgCut)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnCut, id=self.cutID)

            self.copyID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.copyID, u'Копировать', u'Копировать',
                                         normalBmp=imglib.imgEdtMnuCopy)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnCopy, id=self.copyID)

            self.pasteID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.pasteID, u'Вставить', u'Вставить',
                                         normalBmp=imglib.imgEdtMnuPaste)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnPaste, id=self.pasteID)
            item.Enable(not clipboard.emptyClipboard())

            self.AppendSeparator()

            # Подменю 'Клонировать'
            self.cloneID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.cloneID, u'Клонировать', u'Клонировать',
                                         normalBmp=imglib.imgClone)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnClone, id=self.cloneID)

            # Подменю 'Удалить'
            self.delID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.delID, u'Удалить', u'Удалить',
                                         normalBmp=imglib.imgTrash)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnDelete, id=self.delID)
            self.AppendSeparator()

            # Подменю 'Переименовать'
            # Первый уровень нельзя переименовать
            if self._Parent.getLevel() > 1:
                self.renameID = wx.NewId()
                item = flatmenu.FlatMenuItem(self, self.renameID, u'Переименовать', u'Переименовать',
                                             normalBmp=imglib.imgRename)
                self.AppendItem(item)
                prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnRename, id=self.renameID)
                self.AppendSeparator()

        if issubclass(self._Parent.__class__, prj_module.PrjImageModule):
            # Библиотека картинок
            # Открыть в браузере
            self.brwsID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.brwsID, u'Просмотр', u'Просмотр',
                                         normalBmp=imglib.imgEdtImgBrowser)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnImgLibBrowser, id=self.brwsID)
            
            self.AppendSeparator()
            
        # Редактировать
        self.editID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.editID, u'Редактировать', u'Редактировать',
                                     normalBmp=imglib.imgEdit)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnEdit, id=self.editID)

        self.AppendSeparator()

        # Подменю 'Сохранить'
        self.saveID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.saveID, u'Сохранить', u'Сохранить',
                                     normalBmp=imglib.imgSave)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnSave, id=self.saveID)

    def OnAddPackage(self, event):
        """
        Добавить Пакет.
        """
        package = self._Parent.include_folder(self._Parent)
        ok = package.create()
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Добавить папку в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(package)
            tree_prj.SelectItem(new_item)
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnAddModule(self, event):
        """
        Функция добавления модуля.
        """
        mod = self._node_reg[event.GetId()]
        ok = mod.create()
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(mod)
            tree_prj.SelectItem(new_item)
            mod.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnAddResClass(self, event):
        """
        Функция добавления ресурсного класса.
        """
        res = self._node_reg[event.GetId()]
        ok = res.createResClass()
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(res)
            tree_prj.SelectItem(new_item)
            res.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnCut(self, event):
        """
        Вырезать.
        """
        node = self._Parent.cut()
        # Работа с системным клиппордом
        clipboard.toClipboard(node)

    def OnCopy(self, event):
        """
        Копировать.
        """
        node = self._Parent.copy()
        # Работа с системным клиппордом
        clipboard.toClipboard(node)

    def OnPaste(self, event):
        """
        Вставить.
        """
        # Работа с системным клиппордом
        node = clipboard.fromClipboard(False)
        ok = self._Parent.paste(node)
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInParentSelection(node)
            tree_prj.SelectItem(new_item)
            node.edit()
            # Если добавление прошло успешно, то очистить
            clipboard.clearClipboard()
            
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnRename(self, event):
        """
        Переименовать.
        """
        tree_prj = self._Parent.getRoot().getParent()
        node = self._Parent
        tree_prj.EditLabel(node.tree_id)
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnSave(self, event):
        """
        Сохранить.
        """
        node = self._Parent
        node.save()

    def OnEdit(self, event):
        """
        Редактирование.
        """
        node = self._Parent
        node.edit()

    def OnDelete(self, event):
        """
        Редактирование.
        """
        node = self._Parent
        node.delete()

    def OnClone(self, event):
        """
        Клонировать.
        """
        node = self._Parent.clone()
        tree_prj = self._Parent.getRoot().getParent()
        if node:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInParentSelection(node)
            tree_prj.SelectItem(new_item)
            node.edit()
            
        # Обновление дерева проектов
        tree_prj.Refresh()
        
    def OnImgLibBrowser(self, event):
        """
        Браузер библиотек картинок.
        """
        prj_file_name = self._Parent.getRoot().getPrjFileName()
        prj_ini_file = None
        if prj_file_name:
            prj_ini_file = os.path.splitext(prj_file_name)[0]+'.ini'
            
        node = self._Parent
        img_lib_file_name = node.getFullModuleFileName()
        
        icimagelibrarybrowser.runImageLibraryBrowser(self._Parent.getRoot().getParent(),
                                                     prj_ini_file, img_lib_file_name)

    def OnAddFBP(self, event):
        """ 
        Добавить wxformbuilder project.
        """
        fbp = self._node_reg[event.GetId()]
        ok = fbp.create()
        tree_prj = self._Parent.getRoot().getParent()
        # Обновление дерева проектов
        tree_prj.Refresh()
