#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса AUI нотебуков. Технология AUI.
"""

# Подключение библиотек
import wx
from wx.lib.agw import aui
from ic.log import log
from ic.dlg import ic_dlg

__version__ = (0, 0, 1, 2)


class icAUINotebook(aui.AuiNotebook):
    """
    Менеджер панелей с закладками. Технология AUI.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        @param: Parent_: Родительское окно.
        """
        aui.AuiNotebook.__init__(self, Parent_)
        
        self.SetClientSize(Parent_.GetClientSize())
    
    def addPage(self, Page_, Title_, Select_=False, Image_=None, not_dublicate=True):
        """
        Добавить страницу.
        @param Page_: Страница-объект наследник wx.Window.
        @param Title_: Заголовок страницы.
        @param Select_: Выбирается по умолчанию эта страница?
        @param Image_: Файл образа или сам образ в заголовке страницы.
        @param not_dublicate: Не открывать страницу с таким же именем?
        """
        if Page_ is None:
            log.warning(u'Не определена страница для добавления в главный нотебук')
            return

        if not_dublicate:
            # Запретить открытие страницы с таким же заголовком
            page_titles = [page['title'] for page in self.getPages()]
            if Title_ in page_titles:
                msg = u'Страница <%s> уже открыта' % Title_
                log.warning(msg)
                Page_.Destroy()
                ic_dlg.icWarningBox(u'ВНИМАНИЕ!', msg)
                return None

        # У объекта страницы поменять хозяина
        # Чтобы органайзер синхронно переразмеривался с главным окном
        if Page_.GetParent() != self:
            log.debug(u'Смена родителя <%s> страницы <%s>' % (Page_.GetParent(), Page_.__class__.__name__))
            Page_.Reparent(self)
        return self.AddPage(Page_, Title_, Select_, Image_)

    # Удалить страницу по индексу
    deletePage = aui.AuiNotebook.DeletePage

    def getPages(self):
        """
        Список страниц.
        @return: Список в формате:
            [
            {'title': Заголовок страницы, 'page': Объект страницы}, ...
            ]
        """
        result = list()
        for i in range(self.GetPageCount()):
            title = self.GetPageText(i)
            page = self.GetPage(i)
            result.append(dict(title=title, page=page))
        return result

    def closeAllPages(self):
        """
        Закрыть все страницы.
        """
        for i in range(self.GetPageCount()):
            self.deletePage(i)

        return True

    def deleteAllPages(self):
        """
        Удаление всех страниц.
        """
        self.closeAllPages()
        # Удалить сам объект органайзера c экрана
        self.Show(False)
        return True


class icAUIMainNotebook(icAUINotebook):
    """
    Менеджер панелей с закладками для главного окна. Технология AUI.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        @param: Parent_: Родительское окно.
        """
        icAUINotebook.__init__(self, Parent_)
