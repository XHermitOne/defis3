#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания класса главного окна системы. Технология AUI.
"""

# Подключение библиотек
import os
import os.path
import wx
from wx.lib.agw import aui

from ic.log import log
from ic.utils import util

from . import main_window
from . import icAUImanager
from . import icAUInotebook
from . import glob_functions
from . import icmenubar

from ic.components import icResourceParser

__version__ = (0, 1, 1, 2)

# Основные константы
# Градиент заголовков AUI панелей
AUI_PANE_GRADIENTS = {'None': aui.AUI_GRADIENT_NONE,
                      'Vertical': aui.AUI_GRADIENT_VERTICAL,
                      'Horizontal': aui.AUI_GRADIENT_HORIZONTAL,
                      None: aui.AUI_GRADIENT_NONE,
                      }
    
# Спецификации
SPC_IC_AUIMAINWIN = {'is_main_notebook': True,  # Присутствует в главном окне нотебук?
                     'is_menubar': True,        # Присутствует в главном окне меню?
                     'is_statusbar': True,      # Присутствует в главном окне статусная строка?
                     'content': None,           # Заполнить фрейм главного окна объектом ...
                     # Флаги AUI менеджера
                     'allow_floating': True,    # Разрешать плавающие панели
                     'allow_active_pane': False,  # Есть активная панель
                     'transparent_drag': False,
                     'transparent_hint': True,  # Прозрачная подсказка прикрепления
                     'venetian_blinds_hint': False,  # Полупрозрачная подсказка прикрепления
                     'rectangle_hint': False,  # Прямоугольная подсказка прикрепления
                     'hint_fade': True,
                     'max_button': 1,
                     'sys_menu': 1,
                     'min_button': 1,
                     'no_venetian_blinds_fade': True,  # Отключить эффект заполнения подсказки
    
                     # Градиент заголовков AUI панелей
                     'pane_gradient': 'Horizontal',
    
                     '__parent__': main_window.SPC_IC_WIN,
                     '__attr_hlp__': {'is_main_notebook': u'Присутствует в главном окне нотебук?',
                                      'is_menubar': u'Присутствует в главном окне меню?',
                                      'is_statusbar': u'Присутствует в главном окне статусная строка?',
                                      'content': u'Заполнить фрейм главного окна объектом ...',
                                      'allow_floating': u'Разрешать плавающие панели',
                                      'allow_active_pane': u'Есть активная панель',
                                      'transparent_hint': u'Прозрачная подсказка прикрепления',
                                      'venetian_blinds_hint': u'Полупрозрачная подсказка прикрепления',
                                      'rectangle_hint': u'Прямоугольная подсказка прикрепления',
                                      'no_venetian_blinds_fade': u'Отключить эффект заполнения подсказки',
                                      'pane_gradient': u'Градиент заголовков AUI панелей',
                                      },
                     }


class icAUIMainWinPrototype(main_window.icMainWindow):
    """
    Главное окно. Технология AUI.
    """

    def __init__(self, component=None):
        """
        Конструктор.

        :param: component: Ресурсное представление объекта.
        """
        component = util.icSpcDefStruct(SPC_IC_AUIMAINWIN, component)

        main_window.icMainWindow.__init__(self, component['name'], component)

        # AUI Менеджер
        self.aui_manager = icAUImanager.icAUIManager(self)

        if component['is_main_notebook'] and not component['is_main_notebook'] in ('None', 'False', '0', 'false'):
            self.aui_manager.AddPane(self.createMainNotebook(), 
                                     aui.AuiPaneInfo().Name('main_notebook').CenterPane())

        # Установить флаги
        flags = 0
        if component['allow_floating']:
            flags |= aui.AUI_MGR_ALLOW_FLOATING
        if component['allow_active_pane']:
            flags |= aui.AUI_MGR_ALLOW_ACTIVE_PANE
        if component['transparent_drag']:
            flags |= aui.AUI_MGR_TRANSPARENT_DRAG
        if component['transparent_hint']:
            flags |= aui.AUI_MGR_TRANSPARENT_HINT
        if component['venetian_blinds_hint']:
            flags |= aui.AUI_MGR_VENETIAN_BLINDS_HINT
        if component['rectangle_hint']:
            flags |= aui.AUI_MGR_RECTANGLE_HINT
        if component['hint_fade']:
            flags |= aui.AUI_MGR_HINT_FADE
        if component['no_venetian_blinds_fade']:
            flags |= aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        
        self.aui_manager.SetFlags(flags)
        
        # Установка градиентной заливки AUI панелей
        gradient = AUI_PANE_GRADIENTS[component['pane_gradient']]
        self.aui_manager.setGradient(gradient)
        
        # События
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SHOW, self.OnOpen)

    def createMainNotebook(self):
        """
        Создание главного нотебука.
        """
        if self._MainNotebook is None:
            self._MainNotebook = icAUInotebook.icAUIMainNotebook(self)

            # Установить обработчики
            self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onClosePage, self._MainNotebook)
            self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.onClosedPage, self._MainNotebook)
        return self._MainNotebook        

    def getPage(self, page_idx):
        """
        Получить объект страницы по ее индексу.

        :param page_idx: Индекс страницы в главном нотебуке.
        :return: Объект страницы или None  в случае ошибки.
        """
        main_notebook = self.getMainNotebook()
        if main_notebook:
            try:
                return main_notebook.GetPage(page_idx)
            except:
                log.error(u'Ошибка определения страницы главного нотебука приложения')
        else:
            log.warning(u'Не определен главный нотебук главного окна прораммы')
        return None

    def onClosePage(self, event):
        """
        Обработчик закрытия страницы главного нотебука.
        """
        log.debug(u'Закрытие страницы главного нотебука')
        event.Skip()

    def onClosedPage(self, event):
        """
        Обработчик закрытой страницы главного нотебука.
        """
        event.Skip()

    def OnSize(self, event):
        """
        Изменение размеров.
        """
        event.Skip()

    def OnOpen(self, event):
        """
        Открытие.
        """
        if not self._is_opened:
            # ВНИМАНИЕ! Обработчик открытия вызывается только
            # 1 раз при открытии. Этим он отличается от
            # обработчика OnShow
            try:
                if self.isICAttrValue(main_window.RES_WIN_OPEN):
                    self.evalSpace['event'] = event
                    self.evalSpace['evt'] = event
                    self.eval_attr(main_window.RES_WIN_OPEN)
            except:
                log.fatal(u'Ошибка открытия главного окна')
            self._is_opened = True
        event.Skip()

    def OnClose(self, event):
        """
        Закрытие.
        ВНИМАНИЕ! При выходе из программы не надо вызывать
        <event.Skip()>, чтобы не было повторного вызова процедуры
        закрытия
        """
        try:
            if self.isICAttrValue(main_window.RES_WIN_CLOSE):
                self.evalSpace['event'] = event
                self.evalSpace['evt'] = event
                result = self.eval_attr(main_window.RES_WIN_CLOSE)
                if result and not result[1]:
                    # Не нажато подтверждение выхода из главного окна
                    log.warning(u'Условия корректного выхода из программы не подтверждены')
                    return

            # ВНИМАНИЕ! Для корректного выхода из приложения необходимо
            # закрыть все внутренние циклы ядра
            # А затем произвести все остальные действия
            kernel = glob_functions.getKernel()
            if kernel:
                kernel.stop()

            # Остановить основной цикл выполнения приложения
            app = wx.GetApp()
            if app:
                app.ExitMainLoop()
        except:
            log.fatal(u'Ошибка закрытия главного окна')
        # ВНИМАНИЕ! При выходе из программы не надо вызывать
        # event.Skip(), чтобы не было повторного вызова процедуры
        # закрытия

    def getMainNotebook(self):
        """
        Нотебук в главном окне.
        """
        return self._MainNotebook

    def addMainNotebookPage(self, page, title, bAutoSelect=False, image=None,
                            bNotDuplicate=True):
        """
        Добавить страницу.

        :param page: Страница-объект наследник wx.Window.
        :param title: Заголовок страницы.
        :param bAutoSelect: Выбирается по умолчанию эта страница?
        :param image: Файл образа или сам образ в заголовке страницы.
        :param bNotDuplicate: Не открывать страницу с таким же именем?
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook:
                
                if image is None:
                    image = wx.NullBitmap
                if not isinstance(title, str):
                    log.warning(u'Не допустимый тип <%s> заголовка страницы нотебука' % type(title))
                    title = str(title)

                # Добавить страницу
                return self._MainNotebook.addPage(page, title, bAutoSelect, image, bNotDuplicate)
        except:
            log.fatal(u'Ошибка добавления страницы в главное окно.')
        return None
    
    def OnPaint(self, event):
        event.Skip()
        
    def addOrgPage(self, page, title, open_exists=False, image=None,
                   bCanClose=True, open_script=None, close_script=None, default_page=-1,
                   bNotDuplicate=True):
        """
        Добавить страницу.

        :param page: Страница-объект наследник wx.Window.
        :param title: Заголовок страницы.
        :param open_exists: Если страница уже создана-открыть ее.
        :param image: Файл образа или сам образ в заголовке страницы.
        :param bCanClose: Признак разрешения закрытия страницы при помощи
            стандартного всплывающего меню.
        :param open_script: Блок кода открытия страницы при переключенни
            м/у страницами.
        :param close_script: Блок кода закрытия страницы при переключенни
            м/у страницами.
        :param default_page: Индекс страницы,  открываемой по умолчанию.
            Если -1, то открывается текущая добавляемая страница.
        :param bNotDuplicate: Не открывать страницу с таким же именем?
        """
        select = default_page == -1
        if isinstance(page, str):
            res_name, res_ext = os.path.splitext(page)
            # По умолчанию ресурс форм: *.frm
            if not res_ext:
                res_ext = '.frm'

            # Создание объекта страницы
            main_notebook = self.getMainNotebook()
            page_parent = main_notebook if main_notebook else self
            page = icResourceParser.icCreateObject(res_name, res_ext[1:],
                                                   parent=page_parent)
        return self.addMainNotebookPage(page, title, select, image, bNotDuplicate=bNotDuplicate)

    # Можно использовать и другое наименование метода
    addPage = addOrgPage

    def delOrgPage(self, page_index):
        """
        Удалить страницу.

        :param page_index: Индекс страницы.
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook is None:
                return None
            self._MainNotebook.deletePage(page_index)
            return self._MainNotebook
        except:
            log.fatal(u'Ошибка удаления страницы из органайзера.')
            return None

    def delPageByTitle(self, page_title):
        """
        Удалить страницу по заголовку страницы.

        :param page_title: Заголовок страницы.
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook is None:
                return None
            pages = self._MainNotebook.getPages()
            for i, page in enumerate(pages):
                title = page.get('title', None)
                if title == page_title:
                    log.info(u'Удаление страницы <%s> с индексом %d' %(title, i))
                    self._MainNotebook.deletePage(i + 1)
            return self._MainNotebook
        except:
            log.fatal(u'Ошибка удаления страницы из органайзера.')
            return None

    def delOrg(self):
        """
        Удалить органайзер(Объект главного менеджера системных панелей).

        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            if self._MainNotebook:
                self._MainNotebook.deleteAllPages()
            return True
        except:
            log.fatal(u'Ошибка удаления главного органайзера')
            return False

    def closeOrgPages(self):
        """
        Закрыть все страницы органайзера(Объект главного менеджера системных панелей).

        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            if self._MainNotebook:
                self._MainNotebook.closeAllPages()
            return True
        except:
            log.fatal(u'Ошибка удаления главного органайзера')
            return False

    def getAUIManager(self):
        """
        AUI менеджер.
        """
        return self.aui_manager

    def destroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].destroyObj()
                except: 
                    pass
        except:
            pass

    def openChildPane(self, page, pane_name):
        """
        Открыть дочернее окно как AUI панель.

        :param page: Имя ресурсного файла окна.
        :param pane_name: Имя дочерней AUI панели.
        """
        pane = self.GetChildByName(pane_name)
        if isinstance(page, str):
            res_name, res_ext = os.path.splitext(page)
            # По умолчанию ресурс форм: *.frm
            if not res_ext:
                res_ext = '.frm'
            page = icResourceParser.icCreateObject(res_name, res_ext[1:], parent=self)
            if page:
                pane.control_name = os.path.basename(res_name)
                pane.control_res = res_name+res_ext
        return pane.showControl(page)

    def setChildPane(self, page, pane_name):
        """
        Установить дочернее окно как AUI панель.

        :param page: Объект окна/панели.
        :param pane_name: Имя дочерней AUI панели.
        """
        pane = self.GetChildByName(pane_name)
        return pane.showControl(page)

    def setMenuBar(self, menubar):
        """
        Установить горизонтальное меню.
        """
        if issubclass(menubar.__class__, icmenubar.icMenuBar):
            main_window.icMainWindow.setMenuBar(self, menubar)
