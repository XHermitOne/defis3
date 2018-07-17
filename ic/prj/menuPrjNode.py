#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль меню управления проектом.
"""

# Подключение библиотек
import wx
from wx.lib.agw import flatmenu

import ic.imglib.common as imglib
import ic.dlg.ic_dlg as ic_dlg
import ic.utils.clipboard as clipboard

from . import prj_node

__version__ = (0, 0, 1, 2)

_ = wx.GetTranslation


class icMenuPrjNode(flatmenu.FlatMenu):
    """
    Меню управления проектом.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = Parent_
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getRoot().getParent()

        is_folder = issubclass(self._Parent.__class__, prj_node.PrjFolder)
        if is_folder:
            # Дополнительные ресурсы
            if self._Parent.include_nodes:
                # Подменю 'Добавить ресурс'
                submenu_res = flatmenu.FlatMenu()
                # Дополнительные ресурсы для добавления
                # Внутренний реестр ресурсов для доступа к ним по идентификатору
                self._node_reg = {}
                for node_class in self._Parent.include_nodes:
                    node = node_class(self._Parent)

                    # Обработка меню добавления ресурса
                    res_id = wx.NewId()
                    # Зарегистрировать ресурс во внутреннем реестре
                    self._node_reg[res_id] = node
                    item = flatmenu.FlatMenuItem(submenu_res, res_id, node.description, node.description,
                                                 normalBmp=node.img)
                    submenu_res.AppendItem(item)
                    # ВНИМАНИЕ! Выключение пункта меню делать только после
                    #   присоединения к меню. Иначе выключение не срабатывает.
                    if not node.enable:
                        item.Enable(node.enable)
                      
                    if wx.Platform == '__WXMSW__':
                        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddResource, id=res_id)
                    elif wx.Platform == '__WXGTK__':
                        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddResource, id=res_id)

                self.AppendMenu(wx.NewId(), 
                                u'Добавить ресурс', submenu_res)
                
                # Импортировть ресурс...
                self.importResID = wx.NewId()
                item = flatmenu.FlatMenuItem(self, self.importResID,
                                             u'Импорт ресурса', u'Импорт ресурса',
                                             normalBmp=imglib.imgEdtImport)
                self.AppendItem(item)
                prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnImportResource, id=self.importResID)
                
                self.AppendSeparator()

            # Добавить папку
            self.addFolderID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.addFolderID,
                                         u'Добавить папку', u'Добавить папку',
                                         normalBmp=imglib.imgFolder)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnAddFolder, id=self.addFolderID)
            self.AppendSeparator()

        # Подменю 'Буфер обмена'
        self.cutID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.cutID, u'Вырезать', u'Вырезать',
                                     normalBmp=imglib.imgCut)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnCut, id=self.cutID)
        item.Enable(not is_folder)

        self.copyID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.copyID,
                                     u'Копировать', u'Копировать',
                                     normalBmp=imglib.imgEdtMnuCopy)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnCopy, id=self.copyID)
        item.Enable(not is_folder)

        self.pasteID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.pasteID,
                                     u'Вставить', u'Вставить',
                                     normalBmp=imglib.imgEdtMnuPaste)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnPaste, id=self.pasteID)
        item.Enable(not is_folder and not clipboard.emptyClipboard())

        self.AppendSeparator()

        # Подменю 'Клогировать'
        self.cloneID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.cloneID,
                                     u'Клонировать', u'Клонировать',
                                     normalBmp=imglib.imgClone)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnClone, id=self.cloneID)
        item.Enable(not is_folder)

        # Подменю 'Удалить'
        self.delID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.delID,
                                     u'Удалить', u'Удалить',
                                     normalBmp=imglib.imgTrash)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnDel, id=self.delID)

        self.AppendSeparator()

        # Подменю 'Редактировать'
        # Редактировать только ресурсы
        if not is_folder:
            self.editID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.editID,
                                         u'Редактировать', u'Редактировать',
                                         normalBmp=imglib.imgEdit)
            self.AppendItem(item)
            self.AppendSeparator()
        # Подменю 'Переименовать'
        # Первый уровень нельзя переименовать
        if self._Parent.getLevel() > 1:
            self.renameID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.renameID,
                                         u'Переименовать', u'Переименовать',
                                         normalBmp=imglib.imgRename)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnRename, id=self.renameID)
            self.AppendSeparator()

        # Подменю 'Сохранить'
        self.saveID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.saveID,
                                     u'Сохранить', u'Сохранить',
                                     normalBmp=imglib.imgSave)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnSave, id=self.saveID)

        # Пункт дополнительных функций узла
        self.extID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.extID, u'Дополнительно', u'Дополнительно',
                                     normalBmp=imglib.imgAdvanced)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.OnExtend, id=self.extID)

    def OnAddFolder(self, event):
        """
        Добавить папку.
        """
        # Создать папку
        folder = self._Parent.include_folder(self._Parent)
        ok = folder.create()
        # Добавить папку в отображаемом дереве
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            new_item = tree_prj.AddBranchInSelection(folder)
            tree_prj.SelectItem(new_item)
            folder.getRoot().save()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnAddResource(self, event):
        """
        Функция добавления ресурса.
        """
        node = self._node_reg[event.GetId()].__class__(self._Parent)
        ok = node.create()
        tree_prj = self._Parent.getRoot().getParent()
        if ok:
            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(node)
            tree_prj.SelectItem(new_item)
            node.getRoot().save()
            node.edit()
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
        tree_prj = self._Parent.getRoot().getParent()
        if node:
            if self._Parent.paste(node):
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

    def OnDel(self, event):
        """
        Удалить.
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
        
    def OnSynchroTab(self, event):
        """
        Синхронизация описания таблицы с БД.
        """
        try:
            node = self._Parent
            table_psp = ((None, None, None,
                          node.getResFileName()+'.'+node.getResFileExt(), None),)
            from ic.engine import ic_user
            table = ic_user.getKernel().Create(table_psp)
            ok = table.syncDB()
        except:
            ok = False
            
        if ok:
            ic_dlg.icMsgBox(u'Синхронизация таблицы',
                            u'Создана копия таблицы <%s>. Старая таблица удалена.' % self._Parent.name)
        else:
            ic_dlg.icMsgBox(u'Синхронизация таблицы',
                            u'Ошибка синхронизации таблицы <%s>' % self._Parent.name)
            
    import_res_filter = u'Tables (*.tab)|*.tab|DB (*.src)|*.src|ODB (*.odb)|*.odb|Forms (*.frm)|*.frm|Main window (*.win)|*.win|Menu (*.mnu)|*.mnu|Metadata (*.mtd)|*.mtd'
    
    def OnImportResource(self, event):
        """
        Импортировать ресурс.
        """
        tree_prj = self._Parent.getRoot().getParent()

        res_file_name = ic_dlg.icFileDlg(tree_prj,
                                         u'Выберите ресурсный файл',
                                         self.import_res_filter)

        if res_file_name:
            node = self._Parent.importChild(res_file_name)

            # Добавить объект в отображаемом дереве
            new_item = tree_prj.AddBranchInSelection(node)
            tree_prj.SelectItem(new_item)
            node.edit()
        # Обновление дерева проектов
        tree_prj.Refresh()

    def OnExtend(self, event):
        """
        Дополнительные инструменты узла.
        """
        node = self._Parent
        node.extend()
