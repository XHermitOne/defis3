#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Страницы визарда патчера.
"""

# --- Imports ---
import os

import wx
import wx.wizard

from ic.log import log

from . import parse_cmd

from . import icparsepanel
from . import icsmarttreelistctrl


__version__ = (0, 0, 0, 3)


# --- Functions ---
def makeStdPageTitle(wizPg, title):
    """
    Функция стандартного создания заголовка страницы
    """
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND | wx.ALL, 5)
    return sizer


# --- Classes ---
class icCFParsePage(wx.wizard.PyWizardPage):
    """
    Страница парсинга CF файла конфигурации 1с.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)

        self.cf_parse_panel = icparsepanel.icParsePanel(self)
        self.sizer.Add(self.cf_parse_panel, 1, wx.EXPAND | wx.GROW, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """
        """
        wizard = self.GetParent()
        cf_filename = self.cf_parse_panel.cfFileTxt.GetValue()
        cf_dir = self.cf_parse_panel.cfDirTxt.GetValue()
        if not cf_filename or not cf_dir:
            self.SetNext(wizard.getFinishPage())
        return self.next
        
    def GetPrev(self):
        return self.prev

    def on_changing(self, event):
        """
        Обработчик смены страницы визарда.
        Это обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard = self.GetParent()

        # Сохранить в окружении визарда выбранный CF файл
        # и директорию конфигурации 1с
        wizard.environment['cf_filename'] = self.cf_parse_panel.cfFileTxt.GetValue()
        wizard.environment['cf_dir'] = self.cf_parse_panel.cfDirTxt.GetValue()

        # Запустить парсинг файла конфигурации
        self.parse_cf_file(wizard.environment['cf_filename'], wizard.environment['cf_dir'])

    def parse_cf_file(self, cf_filename, cf_dirname):
        """
        Парсинг файла конфигурации 1с.
        @param cf_filename: Полное имя CF файла конфигурации 1c.
        @param cf_dirname: Директория, в которую бедет происходить парсинг.
        """
        return parse_cmd.parse_cf_file(cf_filename, cf_dirname,
                                       txt_ctrl=self.cf_parse_panel.logTxt)


class icCFChoicePage(wx.wizard.PyWizardPage):
    """
    Страница выбора метаобъектов конфигурации 1с для изменения.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)
        
        id = wx.NewId()
        wizard = self.GetParent()
        
        title_root = u'----'
        if 'cf_filename' in wizard.environment:
            title_root = os.path.basename(wizard.environment['cf_filename'])
        img_root_filename = os.path.join(os.path.dirname(__file__), 'img', '1c.png')
        img_root = None
        if os.path.exists(img_root_filename):
            img_root = wx.Image(img_root_filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        self.cf_tree_list_ctrl = icsmarttreelistctrl.icSmartTreeListCtrl(self, id,
                                                                         position=wx.DefaultPosition,
                                                                         size=wx.DefaultSize,
                                                                         style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS,
                                                                         labels=[u'Метаобъект',u''], wcols=[500, 100],
                                                                         titleRoot=title_root, imgRoot=img_root)
        self.sizer.Add(self.cf_tree_list_ctrl, 1, wx.EXPAND | wx.GROW, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev

    def on_changed(self, event):
        """
        Перед открытием этой страницы.
        """
        # Построить список метаобъектов конфигурации 1с для компонента выбора
        wizard = self.GetParent()
        cf_analyzer = wizard.getCFAnalyzer()
        log.debug(u'Запуск анализатора папки конфигурации <%s>' % wizard.environment['cf_dir'])
        cf_obj_lst = cf_analyzer.createCFList(wizard.environment['cf_dir'])
        log.debug(u'Загрузка дерева метаобъектов')
        self.cf_tree_list_ctrl.LoadTree(cf_obj_lst, is_progress=True)

    def on_changing(self, event):
        """
        Обработчик смены страницы визарда.
        Этот обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard = self.GetParent()
        cf_analyzer = wizard.getCFAnalyzer()
        metaobjects = cf_analyzer.getMetaobjects(self.cf_tree_list_ctrl.getItemCheckList())
        wizard.environment['cf_metaobjects'] = metaobjects
        wizard.environment['cf_root'] = cf_analyzer.getRootMetaobject()
        self.gen_resources(metaobjects)

    def gen_resources(self, metaobjects):
        """
        Генерация ресурсов, соответствующих метаобъектам 1С.
        @return:
        """
        log.debug(u'Запуск генерации ресурсов')
        for metaobject in metaobjects:
            metaobject.gen_resource()

        
class icCFEndPage(wx.wizard.PyWizardPage):
    """
    Страница окончания установки.
    """
    def __init__(self, parent, title, txt=None):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        @param txt: Текст.
        """
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev
