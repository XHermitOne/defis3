#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль объектов-записных книжек с закладками.
"""

# --- Подключение библиотек ---
import wx

from ic.utils import execfunc
from ic.bitmap import bmpfunc
from ic.log import log

__version__ = (0, 1, 2, 1)

# --- Основные константы ---
OPEN_CODE_IDX = 0
CLOSE_CODE_IDX = 1
CAN_CLOSE_IDX = 2

ORG_PAGE_IMG_WIDTH = 16
ORG_PAGE_IMG_HEIGHT = 16


class icMainNotebook(wx.Notebook):
    """
    Класс главного менеджера панелей главного окна системы (органайзер).
    """

    def __init__(self, parent):
        """
        Конструктор.

        :param parent: Окно, куда будет помещен менеджер (главное окно).
        """
        try:
            # У органайзера заголовки страниц(ярлычки) находятся снизу
            wx.Notebook.__init__(self, parent, wx.NewId(), style=wx.NB_BOTTOM)

            self.SetClientSize(parent.GetClientSize())

            # Создаем контейнер для картинок на закладках
            self._img_name = {}
            self._img_list = wx.ImageList(ORG_PAGE_IMG_WIDTH, ORG_PAGE_IMG_HEIGHT)
            self.SetImageList(self._img_list)

            # Установка обработчика
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged, id=self.GetId())

            # Стандартное всплывающее меню для страниц
            self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

            # Списки скриптов
            self._page_attr = []
            # Индекс текущей страницы
            self._cur_selected_page = -1
        except:
            log.fatal(u'Ошибка создания объекта главного органайзера')

    def addPage(self, page, title, bOpenExists=False, image=None,
                bCanClose=True, open_script=None, close_script=None, default_page=-1):
        """
        Добавить страницу в органайзер.

        :param page: Страница. Ею м.б. любой наследник wx.Window.
        :param title: Заголовок. Строка.
        :param bOpenExists: Если страница уже есть,  то открыть ее.
        :param image: Образ страницы. Если это строка, тогда файл.
            Или объект wx.Bitmap.
        :param open_script: Строка-скрипт, выполняемый при открытии страницы.
        :param close_script: Строка-скрипт, выполняемый при закрытии страницы.
        :param default_page: Индекс страницы,  открываемой по умолчанию.
            Если -1, то открывается текущая добавляемая страница.
        """
        try:
            if bOpenExists:
                # Открыть страницу по указанному заголовку
                idx = self.openPageByTitle(title)
                if idx is not None:
                    return self.GetPage(idx)

            if isinstance(page, str):
                import ic.components.icResourceParser
                page = ic.components.icResourceParser.CreateForm(page, parent=self)

            log.info(u'Новая страница главного органайзера: %s' % page)
            # Проверка корректности типа страницы
            if not page:
                log.error(u'Ошибка типа страницы, помещаемой в органайзер. %s' % str(page))
                return None
                
            self._page_attr.append([open_script, close_script, bCanClose])
            log.debug(u'Образ страницы <%s>' % str(image))
            if image not in self._img_name:
                if not image:
                    img = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER,
                                                   (ORG_PAGE_IMG_WIDTH, ORG_PAGE_IMG_HEIGHT))
                else:
                    # Создание образа
                    img = bmpfunc.createBitmap(image, False)
                    if img is None:
                        img = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16))

                # Добавление образа
                img_idx = self._img_list.Add(img)
                # Запомнить индекс
                self._img_name[image] = img_idx
            else:
                img_idx = self._img_name[image]

            # У объекта страницы поменять хозяина
            # Чтобы органайзер синхронно переразмеривался с главным окном
            if page.GetParent() != self:
                page.Reparent(self)
            # Если органайзер не отображается, то отобразить его
            if not self.IsShown():
                self.Show()
            # Если количество страниц - 0,
            # тогда считается что ораганайзер только открылся
            if self.GetPageCount() <= 0 and self.getMainWin()._OnOrgOpen:
                execfunc.execute_method(self.getMainWin()._OnOrgOpen, self)

            if default_page != -1:
                # Добавление страницы
                ret = self.AddPage(page, title, False, img_idx)
                # Сразу сделать активной страницу по умолчанию
                self.SetSelection(default_page)
            else:
                # Добавление страницы
                ret = self.AddPage(page, title, True, img_idx)
            return ret
        except:
            log.fatal(u'Ошибка добавления страницы в органайзер')
        return None

    def deletePage(self, idx):
        """
        Удалить страницу из органайзера.

        :param idx: Номер страницы.
        """
        try:
            # Удалить картинку прикрепленную к этой странице ОБЯЗАТЕЛЬНО!!!
            # self._img_list.Remove(page_index)
            # Обязательно поменять выделенную страницу!!!
            self.AdvanceSelection()
            # Очистить окно страницы
            page = self.GetPage(idx)
            page.destroyWin()
            # Удалить страницу
            result = self.DeletePage(idx)
            # Изменить привязку картинок к страницам
            for i in range(idx, self.GetPageCount()):
                self.SetPageImage(i, i)
            # Если страниц в органайзере больше не осталось, то ...
            if self.GetPageCount() <= 0:
                # Удалить сам объект органайзера  c экрана
                self.Show(False)
                # Если количество страниц - 0,
                # тогда считается что ораганайзер только закрылся
                execfunc.execute_method(self.getMainWin()._OnOrgClose, self)

            # При удалении страницы меняется и текущая выбранная страница
            self._cur_selected_page = self.GetSelection()
            # Удалить атрибуты соответствующие этой странице
            del self._page_attr[idx]
            # Обновить объект
            self.Refresh()
            return result
        except:
            log.fatal(u'Ошибка удаления страницы из органайзера')
        return None
    
    def deleteAllPages(self):
        """
        Удалить все страницы из органайзера.
        """
        self._page_attr = []
        # Очистить окно страницы
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.Destroy()
        # Удалить картинки ОБЯЗАТЕЛЬНО!!!
        self._img_list.RemoveAll()
        result = wx.Notebook.DeleteAllPages(self)
        # Удалить сам объект органайзера c экрана
        self.Show(False)
        # Если количество страниц - 0,
        # тогда считается что ораганайзер только закрылся
        execfunc.execute_method(self.getMainWin()._OnOrgClose, self)
        return result

    def openPageByTitle(self, title):
        """
        Открыть страницу по указанному заголовку.

        :param title: Заголовок страницы.
        """
        idx = None
        filter_page = [i for i in range(self.GetPageCount()) if title == self.GetPageText(i)]
        if filter_page:
            idx = filter_page[0]
            self.SetSelection(idx)
        return idx

    # --- Обработчики событий ---
    def onPageChanged(self, event):
        """
        Обработчик смены страницы.
        """
        try:
            i_old_page = event.GetOldSelection()
            i_new_page = event.GetSelection()
            # Необходимо запомнить текущую выделенную страницу
            # для стандартного всплывающего меню страницы
            self._cur_selected_page = i_new_page
            if i_old_page != i_new_page:
                # Сначала выполняем скрипт на закрытие
                if i_old_page >= 0:
                    if self._page_attr[i_old_page][CLOSE_CODE_IDX] is not None:
                        execfunc.execute_method(self._page_attr[i_old_page][CLOSE_CODE_IDX], self)
                # Потом выполняем скрипт на открытие
                if i_new_page >= 0:
                    if self._page_attr[i_new_page][OPEN_CODE_IDX] is not None:
                        execfunc.execute_method(self._page_attr[i_new_page][OPEN_CODE_IDX], self)
        except:
            log.fatal(u'Ошибка функции изменения страницы.')
        # ЗДЕСЬ ОБЯЗАТЕЛЬНО ДОЛЖЕН БЫТЬ Skip() ИНАЧЕ ОБЪЕКТ ГЛЮЧИТ!!!
        event.Skip()

    def onRightClick(self, event):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        try:
            std_popup_menu = wx.Menu()
            # Пункты навигации
            id_ = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Предыдущая страница')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.onPrevPage, id=id_)

            id_ = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Следующая страница')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.onNextPage, id=id_)
            # Разделитель
            std_popup_menu.AppendSeparator()
            # Закрытие страницы
            id_ = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Закрыть')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.onClosePage, id=id_)
            #
            if 0 <= self._cur_selected_page < self.GetPageCount():
                # Проверка разрешено закрытие страницы ч/з стандартное меню
                if not self._page_attr[self._cur_selected_page][CAN_CLOSE_IDX]:
                    # Заблокировать пункт меню на закрытие страницы
                    std_popup_menu.FindItemById(id_).Enable(False)

            # Вывод меню на экран
            self.PopupMenu(std_popup_menu, wx.Point(event.GetX(), event.GetY()))
            std_popup_menu.Destroy()
        except:
            log.fatal(u'Ошибка вывода стандартного меню страницы')
            event.Skip()
    
    def onClosePage(self, event):
        """
        Обработчик закрытия страницы.
        """
        try:
            # Текущая выбранная страница доступна?
            if 0 <= self._cur_selected_page < self.GetPageCount():
                # Проверка разрешено закрытие страницы ч/з стандартное меню
                if self._page_attr[self._cur_selected_page][CAN_CLOSE_IDX]:
                    # Удалить страницу
                    result = self.deletePage(self._cur_selected_page)
                    if self.GetPageCount() == 0:
                        self._cur_selected_page = -1
        except:
            log.fatal(u'Ошибка закрытия страницы')
            event.Skip()

    def onPrevPage(self, event):
        """
        Обработчик переключения на предыдущую страницу.
        """
        try:
            self.AdvanceSelection(False)
        except:
            log.fatal(u'Ошибка переключения страницы')
            event.Skip()

    def onNextPage(self, event):
        """
        Обработчик переключения на следующую страницу.
        """
        try:
            self.AdvanceSelection(True)
        except:
            log.fatal(u'Ошибка переключения страницы')
            event.Skip()

    # --- Свойства ---
    def getCurPage(self):
        """
        Определеить объект текущей страницы.
        """
        try:
            if 0 <= self._cur_selected_page < self.GetPageCount():
                return self.GetPage(self._cur_selected_page)
        except:
            log.fatal(u'Ошибка определения объекта текущей страницы')
        return None

    def setPageImg(self, image, n_page):
        """
        Установить картинку у страницы главного органайзера.

        :param image: Имя файла образа.
        :param n_page: Номер страницы.
        """
        try:
            if image not in self._img_name:
                # Создание образа
                img = bmpfunc.createBitmap(image, False)
                if img is None:
                    img = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER,
                                                   (ORG_PAGE_IMG_WIDTH, ORG_PAGE_IMG_HEIGHT))
                # Добавление образа
                img_idx = self._img_list.Add(img)
                # Запомнить индекс
                self._img_name[image] = img_idx
            else:
                img_idx = self._img_name[image]
            return self.SetPageImage(n_page, img_idx)
        except:
            log.fatal(u'Ошибка установки картинки страницы')

    def getMainWin(self, cur_object=None):
        """
        Главное окно.
        """
        if cur_object is None:
            cur_object = self.GetParent()
        if cur_object is not None:
            if issubclass(cur_object.__class__, wx.Frame):
                return cur_object
            else:
                return self.getMainWin(cur_object.GetParent())
        return None
