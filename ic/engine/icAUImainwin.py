#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса главного окна системы. Технология AUI.
"""

# Подключение библиотек
import wx
from wx.lib.agw import aui

from ic.log import log
from ic.utils import util
from ic.utils import ic_file
from ic.kernel import io_prnt

from . import ic_win
from . import ic_menu
from . import icAUImanager
from . import icAUInotebook
from . import ic_user

from ic.components import icResourceParser

__version__ = (0, 0, 1, 2)

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
    
                     '__parent__': ic_win.SPC_IC_WIN,
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


class icAUIMainWinPrototype(ic_win.icMainWindow):
    """
    Главное окно. Технология AUI.
    """

    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param: Resource_: Ресурсное представление объекта.
        """
        Resource_ = util.icSpcDefStruct(SPC_IC_AUIMAINWIN, Resource_)

        ic_win.icMainWindow.__init__(self, Resource_['name'], Resource_)

        # AUI Менеджер
        self.aui_manager = icAUImanager.icAUIManager(self)

        if Resource_['is_main_notebook'] and not Resource_['is_main_notebook'] in ('None', 'False', '0', 'false'):
            self.aui_manager.AddPane(self.createMainNotebook(), 
                                     aui.AuiPaneInfo().Name('main_notebook').CenterPane())

        # Установить флаги
        flags = 0
        if Resource_['allow_floating']:
            flags |= aui.AUI_MGR_ALLOW_FLOATING
        if Resource_['allow_active_pane']:
            flags |= aui.AUI_MGR_ALLOW_ACTIVE_PANE
        if Resource_['transparent_drag']:
            flags |= aui.AUI_MGR_TRANSPARENT_DRAG
        if Resource_['transparent_hint']:
            flags |= aui.AUI_MGR_TRANSPARENT_HINT
        if Resource_['venetian_blinds_hint']:
            flags |= aui.AUI_MGR_VENETIAN_BLINDS_HINT
        if Resource_['rectangle_hint']:
            flags |= aui.AUI_MGR_RECTANGLE_HINT
        if Resource_['hint_fade']:
            flags |= aui.AUI_MGR_HINT_FADE
        if Resource_['no_venetian_blinds_fade']:
            flags |= aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        
        self.aui_manager.SetFlags(flags)
        
        # Установка градиентной заливки AUI панелей
        gradient = AUI_PANE_GRADIENTS[Resource_['pane_gradient']]
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
        @param page_idx: Индекс страницы в главном нотебуке.
        @return: Объект страницы или None  в случае ошибки.
        """
        main_notebook = self.getMainNotebook()
        if main_notebook:
            try:
                return main_notebook.GetPage(page_idx)
            except:
                io_prnt.outErr(u'Ошибка определения страницы главного нотебука приложения')
        else:
            io_prnt.outWarning(u'Не определен главный нотебук главного окна прораммы')
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
                if self.isICAttrValue(ic_win.RES_WIN_OPEN):
                    self.evalSpace['evt'] = event
                    self.evalSpace['event'] = event
                    self.eval_attr(ic_win.RES_WIN_OPEN)
            except:
                io_prnt.outErr(u'Ошибка открытия главного окна')
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
            if self.isICAttrValue(ic_win.RES_WIN_CLOSE):
                self.evalSpace['evt'] = event
                self.evalSpace['event'] = event
                result = self.eval_attr(ic_win.RES_WIN_CLOSE)
                if result and not result[1]:
                    # Не нажато подтверждение выхода из главного окна
                    io_prnt.outWarning(u'Условия корректного выхода из программы не подтверждены')
                    return

            # ВНИМАНИЕ! Для корректного выхода из приложения необходимо
            # закрыть все внутренние циклы ядра
            # А затем произвести все остальные действия
            kernel = ic_user.getKernel()
            if kernel:
                kernel.stop()

            # Остановить основной цикл выполнения приложения
            app = wx.GetApp()
            if app:
                app.ExitMainLoop()
        except:
            io_prnt.outErr(u'Ошибка закрытия главного окна')
        # ВНИМАНИЕ! При выходе из программы не надо вызывать
        # event.Skip(), чтобы не было повторного вызова процедуры
        # закрытия

    def getMainNotebook(self):
        """
        Нотебук в главном окне.
        """
        return self._MainNotebook

    def addMainNotebookPage(self, Page_, Title_, Select_=False, Image_=None,
                            not_dublicate=True):
        """
        Добавить страницу.
        @param Page_: Страница-объект наследник wx.Window.
        @param Title_: Заголовок страницы.
        @param Select_: Выбирается по умолчанию эта страница?
        @param Image_: Файл образа или сам образ в заголовке страницы.
        @param not_dublicate: Не открывать страницу с таким же именем?
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook:
                
                if Image_ is None:
                    Image_ = wx.NullBitmap
                if type(Title_) not in (str, unicode):
                    io_prnt.outWarning(u'Не допустимый тип <%s> заголовка страницы нотебука' % type(Title_))
                    Title_ = str(Title_)

                # Добавить страницу
                return self._MainNotebook.addPage(Page_, Title_, Select_, Image_, not_dublicate)
        except:
            io_prnt.outErr(u'Ошибка добавления страницы в главное окно.')
        return None
    
    def OnPaint(self, evt):
        evt.Skip()
        
    def AddOrgPage(self, Page_, Title_, OpenExists_=False, Image_=None,
                   CanClose_=True, OpenScript_=None, CloseScript_=None, DefaultPage_=-1,
                   not_duplicate=True):
        """
        Добавить страницу.
        @param Page_: Страница-объект наследник wx.Window.
        @param Title_: Заголовок страницы.
        @param OpenExists_: Если страница уже создана-открыть ее.
        @param Image_: Файл образа или сам образ в заголовке страницы.
        @param CanClose_: Признак разрешения закрытия страницы при помощи
            стандартного всплывающего меню.
        @param OpenScript_: Блок кода открытия страницы при переключенни
            м/у страницами.
        @param CloseScript_: Блок кода закрытия страницы при переключенни
            м/у страницами.
        @param DefaultPage_: Индекс страницы,  открываемой по умолчанию.
            Если -1, то открывается текущая добавляемая страница.
        @param not_dublicate: Не открывать страницу с таким же именем?
        """
        select = DefaultPage_ == -1
        if type(Page_) in (str, unicode):
            res_name, res_ext = ic_file.SplitExt(Page_)
            # По умолчанию ресурс форм: *.frm
            if not res_ext:
                res_ext = '.frm'

            # Создание объекта страницы
            main_notebook = self.GetMainNotebook()
            page_parent = main_notebook if main_notebook else self
            Page_ = icResourceParser.icCreateObject(res_name, res_ext[1:],
                                                    parent=page_parent)
        return self.addMainNotebookPage(Page_, Title_, select, Image_, not_dublicate=not_duplicate)

    # Можно использовать и другое наименование метода
    AddPage = AddOrgPage

    def DelOrgPage(self, Index_):
        """
        Удалить страницу.
        @param Index_: Индекс страницы.
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook is None:
                return None
            self._MainNotebook.deletePage(Index_)
            return self._MainNotebook
        except:
            io_prnt.outErr(u'Ошибка удаления страницы из органайзера.')
            return None

    def delPageByTitle(self, page_title):
        """
        Удалить страницу по заголовку страницы.
        @param page_title: Заголовок страницы.
        """
        try:
            # Объект главного менеджера системных панелей
            if self._MainNotebook is None:
                return None
            pages = self._MainNotebook.getPages()
            for i, page in enumerate(pages):
                title = page.get('title', None)
                if title == page_title:
                    io_prnt.outLog(u'Удаление страницы <%s> с индексом %d' %(title, i))
                    self._MainNotebook.deletePage(i + 1)
            return self._MainNotebook
        except:
            io_prnt.outErr(u'Ошибка удаления страницы из органайзера.')
            return None

    def DelOrg(self):
        """
        Удалить органайзер(Объект главного менеджера системных панелей).
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            if self._MainNotebook:
                self._MainNotebook.deleteAllPages()
            return True
        except:
            io_prnt.outErr(u'Ошибка удаления главного органайзера')
            return False

    def CloseOrgPages(self):
        """
        Закрыть все страницы органайзера(Объект главного менеджера системных панелей).
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            if self._MainNotebook:
                self._MainNotebook.closeAllPages()
            return True
        except:
            io_prnt.outErr(u'Ошибка удаления главного органайзера')
            return False

    def getAUIManager(self):
        """
        AUI менеджер.
        """
        return self.aui_manager

    def DestroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except: 
                    pass
        except:
            pass

    def openChildPane(self, Page_, PaneName_):
        """
        Открыть дочернее окно как AUI панель.
        @param Page_: Имя ресурсного файла окна.
        @param PaneName_: Имя дочерней AUI панели.
        """
        pane = self.GetChildByName(PaneName_)
        if type(Page_) in (str, unicode):
            res_name, res_ext = ic_file.SplitExt(Page_)
            # По умолчанию ресурс форм: *.frm
            if not res_ext:
                res_ext = '.frm'
            Page_ = icResourceParser.icCreateObject(res_name, res_ext[1:], parent=self)
            if Page_:
                pane.control_name = ic_file.BaseName(res_name)
                pane.control_res = res_name+res_ext
        return pane.showControl(Page_)

    def setChildPane(self, PageObj_, PaneName_):
        """
        Установить дочернее окно как AUI панель.
        @param PageObj_: Объект окна/панели.
        @param PaneName_: Имя дочерней AUI панели.
        """
        pane = self.GetChildByName(PaneName_)
        return pane.showControl(PageObj_)

    def setMenuBar(self,MenuBar_):
        """
        Установить горизонтальное меню.
        """
        if issubclass(MenuBar_.__class__, ic_menu.icMenuBar):
            ic_win.icMainWindow.setMenuBar(self, MenuBar_)
