#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания класса AUI нотебуков. Технология AUI.
"""

# Подключение библиотек
import wx
from wx.lib.agw import aui
from ic.log import log
from ic.dlg import dlgfunc

__version__ = (0, 1, 1, 2)


class icAUINotebook(aui.AuiNotebook):
    """
    Менеджер панелей с закладками. Технология AUI.
    """

    def __init__(self, parent):
        """
        Конструктор.

        :param: parent: Родительское окно.
        """
        aui.AuiNotebook.__init__(self, parent)
        
        self.SetClientSize(parent.GetClientSize())
    
    def addPage(self, page, title, bAutoSelect=False, image=None, bNotDuplicate=True):
        """
        Добавить страницу.

        :param page: Страница-объект наследник wx.Window.
        :param title: Заголовок страницы.
        :param bAutoSelect: Выбирается по умолчанию эта страница?
        :param image: Файл образа или сам образ в заголовке страницы.
        :param bNotDuplicate: Не открывать страницу с таким же именем?
        """
        if page is None:
            log.warning(u'Не определена страница для добавления в главный нотебук')
            return

        if bNotDuplicate:
            # Запретить открытие страницы с таким же заголовком
            page_titles = [page['title'] for page in self.getPages()]
            if title in page_titles:
                msg = u'Страница <%s> уже открыта' % title
                log.warning(msg)
                page.Destroy()
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!', msg)
                return None

        # У объекта страницы поменять хозяина
        # Чтобы органайзер синхронно переразмеривался с главным окном
        if page.GetParent() != self:
            log.debug(u'Смена родителя <%s> страницы <%s>' % (page.GetParent(), page.__class__.__name__))
            page.Reparent(self)
        return self.AddPage(page, title, bAutoSelect, image)

    # Удалить страницу по индексу
    deletePage = aui.AuiNotebook.DeletePage

    def getPages(self):
        """
        Список страниц.

        :return: Список в формате:
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

    def __init__(self, parent):
        """
        Конструктор.

        :param: parent: Родительское окно.
        """
        icAUINotebook.__init__(self, parent)
