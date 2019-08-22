#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль меню добавления/редактирования корневого узла/папки проекта.
"""

# Подключение библиотек
import sys
import wx
from wx.lib.agw import flatmenu
import os
import os.path

from ic.imglib import common as imglib
from ic.utils import filefunc
from ic.utils import execfunc
from ic.install import InstallWiz as install_wiz
from ic.bitmap import icimagelibrarybrowser
from ic.utils import ini
from ic.bitmap import bmpfunc
from ic.dlg import dlgfunc
from ic.log import log

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

PRJ_INI_FILE = os.path.join(filefunc.getProfilePath(), 'prjsettings.ini')

DEFAULT_WWW_BROWSER = 'firefox'


class icMenuRootNode(flatmenu.FlatMenu):
    """
    Меню добавления/редактирования корневого узла/папки проекта.
    """

    def __init__(self, parent):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self)
        self._Parent = parent
        # Контрол дерева проекта
        prj_tree_ctrl = self._Parent.getRoot().getParent()

        # Новый проект
        self.newPrjID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.newPrjID,
                                     u'Новый проект', u'Новый проект',
                                     normalBmp=imglib.imgNewPrj)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onNew, id=self.newPrjID)

        # Открыть
        self.openID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.openID,
                                     u'Открыть', u'Открыть',
                                     normalBmp=imglib.imgFolderOpen)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onOpen, id=self.openID)
        
        # Последний открытый проект
        pth = ini.loadParamINI(PRJ_INI_FILE, 'PRJ', 'LastOpenedPaths')
        if pth:
            self.lastOpenID = wx.NewId()
            item = flatmenu.FlatMenuItem(self, self.lastOpenID,
                                         u'Последний открытый проект: %s' % pth, u'Последний открытый проект',
                                         normalBmp=imglib.imgFolderOpen)
            self.AppendItem(item)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onLastOpen, id=self.lastOpenID)

        # Список открытых ранее проектов
        prj_paths = ini.loadParamINIValue(PRJ_INI_FILE, 'PRJ', 'OpenedPaths')
        if prj_paths:
            prj_submenu = flatmenu.FlatMenu()
            for prj_path in prj_paths:
                if prj_path != pth:
                    item_id = wx.NewId()
                    item = flatmenu.FlatMenuItem(prj_submenu, item_id,
                                                 prj_path, u'Проект',
                                                 normalBmp=imglib.imgFolderOpen)
                    prj_submenu.AppendItem(item)
                    prj_tree_ctrl.Bind(wx.EVT_MENU, self.onOpenPrj, id=item_id)

            self.AppendSubMenu(prj_submenu, u'Ранее открытые проекты')

        # Определен проект открыт уже или нет?
        prj_none = self._Parent.isOpened()
        log.info(u'Проект открыт <%s>' % self._Parent.isOpened())

        # 'Сохранить'
        self.saveID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.saveID,
                                     u'Сохранить', u'Сохранить',
                                     normalBmp=imglib.imgSave)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onSave, id=self.saveID)

        # Обновить
        self.refreshID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.refreshID,
                                     u'Обновить', u'Обновить',
                                     normalBmp=imglib.imgRefreshPage)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRefresh, id=self.refreshID)
        
        self.AppendSeparator()
        # Запустить
        self.runID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.runID,
                                     u'Выполнить', u'Выполнить',
                                     normalBmp=imglib.imgPlay)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRun, id=self.runID)
        # Отладка
        self.debugID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.debugID,
                                     u'Отладка', u'Отладка',
                                     normalBmp=imglib.imgDebug)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onDebug, id=self.debugID)
       
        self.AppendSeparator()
        # 'Редактировать'
        self.editID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.editID,
                                     u'Редактировать', u'Редактировать',
                                     normalBmp=imglib.imgEdit)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onEdit, id=self.editID)

        self.editIniID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.editIniID,
                                     u'Параметры проекта', u'Параметры проекта',
                                     normalBmp=imglib.imgProperty)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onEditIni, id=self.editIniID)

        self.AppendSeparator()

        # 'Переименовать'
        self.renameID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.renameID,
                                     u'Переименовать', u'Переименовать',
                                     normalBmp=imglib.imgRename)
        self.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRename, id=self.renameID)

        self.AppendSeparator()
 
        # Подменю инструментов
        tool_submenu = flatmenu.FlatMenu()
        
        # 'Создать инсталяционный пакет'
        if wx.Platform == '__WXMSW__':
            self.installID = wx.NewId()
            item = flatmenu.FlatMenuItem(tool_submenu, self.installID, _('Install package'), _('Install package'),
                                         normalBmp=imglib.imgDemo)
            tool_submenu.AppendItem(item)
            item.Enable(prj_none)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onMakeInstall, id=self.installID)
        
            # 'Создать демо-проект'
            self.demoID = wx.NewId()
            item = flatmenu.FlatMenuItem(tool_submenu, self.demoID,
                                         u'Демо', u'Демо',
                                         normalBmp=imglib.imgDemo)
            tool_submenu.AppendItem(item)
            item.Enable(False)
            prj_tree_ctrl.Bind(wx.EVT_MENU, self.onMakeDemo, id=self.demoID)
        
        # 'Создать публикацию'
        self.publicID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.publicID,
                                     u'Публикация', u'Публикация',
                                     normalBmp=imglib.imgInstall)
        tool_submenu.AppendItem(item)
        item.Enable(prj_none)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onMakePublic, id=self.publicID)

        # 'Браузер библиотеки образов'
        self.imglibID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.imglibID,
                                     u'Библиотека образов', u'Библиотека образов',
                                     normalBmp=imglib.imgEdtImgBrowser)
        tool_submenu.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onImgLibBrowser, id=self.imglibID)

        # 'Редактор регулярных выражений'
        self.regexpeditID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.regexpeditID,
                                     u'Редактор регулярных выражений', u'Редактор регулярных выражений',
                                     normalBmp=bmpfunc.createLibraryBitmap('regular-expression-delimiter.png'))
        tool_submenu.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onRegExpEditor, id=self.regexpeditID)

        # 'Утилита сравнения файлов'
        self.diffID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.diffID,
                                     u'Утилита сравнения файлов', u'Утилита сравнения файлов',
                                     normalBmp=bmpfunc.createLibraryBitmap('edit-diff.png'))
        tool_submenu.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onDiffTool, id=self.diffID)

        # 'Импорт метаобъектов 1С'
        self.imp1cID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.imp1cID,
                                     u'Импорт метаобъектов 1С', u'Импорт метаобъектов 1С',
                                     normalBmp=bmpfunc.createLibraryBitmap('1c.png'))
        tool_submenu.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onImport1C, id=self.imp1cID)

        # 'Дизайнер форм wxFormBuilder'
        self.wxfbID = wx.NewId()
        item = flatmenu.FlatMenuItem(tool_submenu, self.wxfbID,
                                     u'Дизайнер форм wxFormBuilder', u'Дизайнер форм wxFormBuilder',
                                     normalBmp=bmpfunc.createLibraryBitmap('wxformbuilder.png'))
        tool_submenu.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onWXFormBuilder, id=self.wxfbID)

        self.AppendSubMenu(tool_submenu, u'Инструменты')

        self.AppendSeparator()

        # 'Показывать всплывающие подсказки'
        self.popup_helpID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.popup_helpID,
                                     u'Всплывающая подсказка', u'Всплывающая подсказка',
                                     kind=wx.ITEM_CHECK)
        self.AppendItem(item)
        # Галку ставить только после присоединения пункта к меню
        item.Check(self._Parent.show_popup_help)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onPopupHelp, id=self.popup_helpID)
        
        # 'Помощь'
        self.hlpID = wx.NewId()
        item = flatmenu.FlatMenuItem(self, self.hlpID,
                                     u'Помощь', u'Помощь',
                                     normalBmp=imglib.imgHelpBook)
        self.AppendItem(item)
        prj_tree_ctrl.Bind(wx.EVT_MENU, self.onHelp, id=self.hlpID)

    def onNew(self, event):
        """
        Новый проект.
        """
        node = self._Parent
        node.newPrj()
        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()

    def onOpen(self, event):
        """
        Открыть проект.
        """
        node = self._Parent
        node.openPrj()
        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()
        
        # Сохраняем открытые ранее проекты в INI файле
        prj_path = node.getPrjFileName()
        self.saveINIOpenedPath(prj_path)

    def saveINIOpenedPath(self, prj_path):
        """
        Сохранить в INI файле путь открытого проекта.
        @param prj_path: Путь открытого проекта.
        """
        ini.saveParamINI(PRJ_INI_FILE, 'PRJ', 'LastOpenedPaths', prj_path)
        prj_paths = ini.loadParamINIValue(PRJ_INI_FILE, 'PRJ', 'OpenedPaths')
        if not prj_paths:
            prj_paths = list()
        if prj_path not in prj_paths:
            prj_paths.append(prj_path)
        ini.saveParamINI(PRJ_INI_FILE, 'PRJ', 'OpenedPaths', prj_paths)

    def onLastOpen(self, event):
        """
        Открыть последний открытый проект.
        """
        path = ini.loadParamINI(PRJ_INI_FILE, 'PRJ', 'LastOpenedPaths')
        node = self._Parent
        node.openPrj(path)
        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()

    def onOpenPrj(self, event):
        """
        Открыть ранее уже открытый проект.
        """
        sub_menu = event.GetEventObject()
        item_id = event.GetId()
        path = sub_menu.GetLabel(item_id)
        node = self._Parent
        node.openPrj(path)

        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()

        self.saveINIOpenedPath(path)

    def onSave(self, event):
        """
        Сохранить проект.
        """
        node = self._Parent
        node.save()
        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()

    def onRename(self, event):
        """
        Переименовать.
        """
        node = self._Parent
        tree_prj = self._Parent.getRoot().getParent()
        tree_prj.EditLabel(node.tree_id)
        tree_prj.Refresh()

    def onRun(self, event):
        """
        Запустить.
        """
        node = self._Parent
        node.run()

    def onDebug(self, event):
        """
        Запустить в режиме отладки.
        """
        node = self._Parent
        node.debug()
        
    def onEdit(self, event):
        """
        Редактировать.
        """
        node = self._Parent
        node.edit()

    def onEditIni(self, event):
        """
        Редактировать INI файл проекта.
        """
        node = self._Parent
        prj_path = node.getPrjFileName()
        ini_prj_filename = os.path.splitext(prj_path)[0] + '.ini'
        self.editFileIDE(ini_prj_filename)

    def editFileIDE(self, filename):
        """
        Редактирование файла в редакторе.
        @param filename: Полное имя редактируемого файла.
        @return: True/Falseю
        """
        if not os.path.exists(filename):
            dlgfunc.openMsgBox(u'ПРОЕКТ',
                            u'Редактирование. Файл <%s> не найден в проекте' % filename)
            return False

        node = self._Parent
        ide = node.getParent().getIDE()
        if ide:
            if not ide.selectFile(filename):
                return ide.openFile(filename, True, bReadonly=False)
            return True
        else:
            log.warning(u'Не определен IDE для редактирования модуля <%s>' % filename)
        return False

    def onPopupHelp(self, event):
        """
        Управление отображением всплывающих подсказок.
        """
        node = self._Parent
        node.show_popup_help = event.IsChecked()
        
    def onHelp(self, event):
        """
        Помощь...
        """
        import ic
        hlp_file_name = os.path.join(os.path.dirname(ic.__file__), 'doc', 'index.html')
        if os.path.exists(hlp_file_name):
            if wx.Platform == '__WXMSW__':
                hlp_file_name = os.path.normpath(hlp_file_name)
                execfunc.doSysCmd('start explorer ' + hlp_file_name)
            elif wx.Platform == '__WXGTK__':
                try:
                    www_browser = os.environ.get('BROWSER', DEFAULT_WWW_BROWSER)
                    execfunc.doSysCmd(www_browser + ' ' + hlp_file_name)
                except:
                    log.error()
        else:
            dlgfunc.openWarningBox(u'ПОМОЩЬ',
                                u'Файл помощи <%s> не найден. Запустите генерацию документации :-)' % hlp_file_name)

    def onMakeInstall(self, event):
        """
        Создание инсталяционного пакета.
        """
        install_wiz.runInstallWizard(self._Parent.getRoot().getParent(),
                                     self._Parent.getRoot().getPrjFileName())

    def onMakeDemo(self, event):
        """
        Создание демо-проекта.
        """
        install_wiz.runDemoWizard(self._Parent.getRoot().getParent(),
                                  self._Parent.getRoot().getPrjFileName())

    def onImgLibBrowser(self, event):
        """
        Браузер библиотек картинок.
        """
        prj_file_name = self._Parent.getRoot().getPrjFileName()
        prj_ini_file = None
        if prj_file_name:
            prj_ini_file = os.path.splitext(prj_file_name)[0]+'.ini'
        icimagelibrarybrowser.runImageLibraryBrowser(self._Parent.getRoot().getParent(),
                                                     prj_ini_file)

    def onRegExpEditor(self, event):
        """
        Редактор регулярных выражений.
        """
        start_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'contrib', 'pyreditor', 'pyreditor.pyw')
        cmd = '%s %s&' % (sys.executable, start_filename)
        log.info(u'Выполнение команды ОС <%s>' % cmd)
        os.system(cmd)

    def onDiffTool(self, event):
        """
        Утилита сравнения файлов.
        """
        cmd = 'meld &'
        log.info(u'Выполнение команды ОС <%s>' % cmd)
        os.system(cmd)

    def onMakePublic(self, event):
        """
        Создание публикации.
        """
        install_wiz.runPublicWizard(self._Parent.getRoot().getParent(),
                                    self._Parent.getRoot().getPrjFileName())
            
    def onRefresh(self, event):
        """
        Обновить дерево проектов/Переоткрыть проект.
        """
        node = self._Parent
        node.openPrj(node.getPrjFileName())
        # Обновление дерева проектов
        self._Parent.getRoot().getParent().Refresh()

    def onImport1C(self, event):
        """
        Импорт метаобъектов 1С.
        """
        node = self._Parent
        prj_filename = node.getPrjFileName()
        # Проверить открыт ли какой-нибудь проект
        if not prj_filename:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                u'''Импорт можно производить только в определенный проект.
 Откройте проект для возможности импорта''')
            return

        import_system_names = [sub_sys.name for sub_sys in node.getImpSystems().getSubSytems()]
        # Проверить импортированны ли NSI и work_flow
        if 'NSI' not in import_system_names or 'work_flow' not in import_system_names:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                u'''Импортирование метаобъектов возможно
 только при подключенных подсистемах <NSI> и <work_flow>''')

        try:
            from work_flow.cf_importer import icWizard

            icWizard.run_wizard()

            # Обновление дерева проектов
            self._Parent.getRoot().getParent().Refresh()
        except:
            log.fatal(u'Ошибка запуска визарда импорта метаобъектов 1С')

    def onWXFormBuilder(self, event):
        """
        Вызов wxFormBuilder.
        """
        from ic.editor import wxfb_manager
        wxfb_manager.run_wxformbuilder()
