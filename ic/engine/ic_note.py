#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль объектов-записных книжек с закладками.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.ic_exec
import ic.bitmap.ic_bmp as ic_bmp
from ic.kernel import io_prnt

__version__ = (0, 0, 1, 2)

# --- Основные константы ---
OPEN_CODE_IDX = 0
CLOSE_CODE_IDX = 1
CAN_CLOSE_IDX = 2

ORG_PAGE_IMG_DX = 16
ORG_PAGE_IMG_DY = 16


class icMainNotebook(wx.Notebook):
    """
    Класс главного менеджера панелей главного окна системы (органайзер).
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        @param Parent_: Окно, куда будет помещен менеджер (главное окно).
        """
        try:
            # У органайзера заголовки страниц(ярлычки) находятся снизу
            wx.Notebook.__init__(self, Parent_, wx.NewId(), style=wx.NB_BOTTOM)

            self.SetClientSize(Parent_.GetClientSize())

            # Создаем контейнер для картинок на закладках
            self._img_name = {}
            self._img_list = wx.ImageList(ORG_PAGE_IMG_DX, ORG_PAGE_IMG_DY)
            self.SetImageList(self._img_list)

            # Установка обработчика
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, id=self.GetId())

            # Стандартное всплывающее меню для страниц
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

            # Списки скриптов
            self._page_attr = []
            # Индекс текущей страницы
            self._cur_selected_page = -1
        except:
            io_prnt.outErr(u'Ошибка создания объекта главного органайзера')

    def addPage(self, Page_, Title_, OpenExists_=False, Image_=None,
                CanClose_=True, OpenScript_=None, CloseScript_=None, DefaultPage_=-1):
        """
        Добавить страницу в органайзер.
        @param Page_: Страница. Ею м.б. любой наследник wx.Window.
        @param Title_: Заголовок. Строка.
        @param OpenExists_: Если страница уже есть,  то открыть ее.
        @param Image_: Образ страницы. Если это строка, тогда файл.
            Или объект wx.Bitmap.
        @param OpenScript_: Строка-скрипт, выполняемый при открытии страницы.
        @param CloseScript_: Строка-скрипт, выполняемый при закрытии страницы.
        @param DefaultPage_: Индекс страницы,  открываемой по умолчанию.
            Если -1, то открывается текущая добавляемая страница.
        """
        try:
            if OpenExists_:
                # Открыть страницу по указанному заголовку
                idx = self.OpenPageByTitle(Title_)
                if idx is not None:
                    return self.GetPage(idx)

            if isinstance(Page_, str):
                import ic.components.icResourceParser
                page = ic.components.icResourceParser.CreateForm(Page_, parent=self)
            else:
                page = Page_

            io_prnt.outLog(u'Новая страница главного органайзера: %s' % page)
            # Проверка корректности типа страницы
            if not page:
                io_prnt.outErr(u'Ошибка типа страницы, помещаемой в органайзер. %s' % str(page))
                return None
                
            self._page_attr.append([OpenScript_, CloseScript_, CanClose_])
            if Image_ not in self._img_name:
                if not Image_:
                    img = wx.ArtProvider_GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16))
                else:
                    # Создание образа
                    img = ic_bmp.icCreateBitmap(Image_, False)
                    if img is None:
                        img = wx.ArtProvider_GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16))

                # Добавление образа
                img_idx = self._img_list.Add(img)
                # Запомнить индекс
                self._img_name[Image_] = img_idx
            else:
                img_idx = self._img_name[Image_]

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
                ic.utils.ic_exec.ExecuteMethod(self.getMainWin()._OnOrgOpen, self)

            if DefaultPage_ != -1:
                # Добавление страницы
                ret = self.AddPage(page, Title_, False, img_idx)
                # Сразу сделать активной страницу по умолчанию
                self.SetSelection(DefaultPage_)
            else:
                # Добавление страницы
                ret = self.AddPage(page, Title_, True, img_idx)

            return ret
        except:
            io_prnt.outErr(u'Ошибка добавления страницы в органайзер.')
            return None

    def deletePage(self, Index_):
        """
        Удалить страницу из органайзера.
        @param Index_: Номер страницы.
        """
        try:
            # Удалить картинку прикрепленную к этой странице ОБЯЗАТЕЛЬНО!!!
            # self._img_list.Remove(Index_)
            # Обязательно поменять выделенную страницу!!!
            self.AdvanceSelection()
            # Очистить окно страницы
            page = self.GetPage(Index_)
            page.DestroyWin()
            # Удалить страницу
            result = self.DeletePage(Index_)
            # Изменить привязку картинок к страницам
            for i in range(Index_, self.GetPageCount()):
                self.SetPageImage(i, i)
            # Если страниц в органайзере больше не осталось, то ...
            if self.GetPageCount() <= 0:
                # Удалить сам объект органайзера  c экрана
                self.Show(False)
                # Если количество страниц - 0,
                # тогда считается что ораганайзер только закрылся
                ic.utils.ic_exec.ExecuteMethod(self.getMainWin()._OnOrgClose, self)

            # При удалении страницы меняется и текущая выбранная страница
            self._cur_selected_page = self.GetSelection()
            # Удалить атрибуты соответствующие этой странице
            del self._page_attr[Index_]
            # Обновить объект
            self.Refresh()
            return result
        except:
            io_prnt.outErr(u'deletePage')
            return None
    
    def deleteAllPages(self):
        """
        Удалить все страницы из органайзера.
        """
        self._page_attr = []
        # Очистить окно страницы
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.DestroyWin()
        # Удалить картинки ОБЯЗАТЕЛЬНО!!!
        self._img_list.RemoveAll()
        result = wx.Notebook.DeleteAllPages(self)
        # Удалить сам объект органайзера c экрана
        self.Show(False)
        # Если количество страниц - 0,
        # тогда считается что ораганайзер только закрылся
        ic.utils.ic_exec.ExecuteMethod(self.getMainWin()._OnOrgClose, self)
        return result

    def OpenPageByTitle(self, Title_):
        """
        Открыть страницу по указанному заголовку.
        @param Title_: Заголовок страницы.
        """
        idx = None
        filter_page = [i for i in range(self.GetPageCount()) if Title_ == self.GetPageText(i)]
        if filter_page:
            idx = filter_page[0]
            self.SetSelection(idx)
        return idx

    # --- Обработчики событий ---
    def OnPageChanged(self, event):
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
                        ic.utils.ic_exec.ExecuteMethod(self._page_attr[i_old_page][CLOSE_CODE_IDX], self)
                # Потом выполняем скрипт на открытие
                if i_new_page >= 0:
                    if self._page_attr[i_new_page][OPEN_CODE_IDX] is not None:
                        ic.utils.ic_exec.ExecuteMethod(self._page_attr[i_new_page][OPEN_CODE_IDX], self)
            # ЗДЕСЬ ОБЯЗАТЕЛЬНО ДОЛЖЕН БЫТЬ Skip() ИНАЧЕ ОБЪЕКТ ГЛЮЧИТ!!!
            event.Skip()
        except:
            io_prnt.outErr(u'Ошибка функции изменения страницы.')
            event.Skip()

    def OnRightClick(self, event):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        try:
            std_popup_menu = wx.Menu()
            # Пункты навигации
            id_ = wx.NewId()
            bmp = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Предыдущая страница')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnPrevPage, id=id_)

            id_ = wx.NewId()
            bmp = wx.ArtProvider_GetBitmap(wx.ART_GO_FORWARD, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Следующая страница')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnNextPage, id=id_)
            # Разделитель
            std_popup_menu.AppendSeparator()
            # Закрытие страницы
            id_ = wx.NewId()
            bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            item = wx.MenuItem(std_popup_menu, id_, u'Закрыть')
            item.SetBitmap(bmp)
            std_popup_menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnClosePage, id=id_)
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
            io_prnt.outErr(u'Ошибка вывода стандартного меню страницы')
            event.Skip()
    
    def OnClosePage(self, event):
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
            io_prnt.outErr(u'Ошибка закрытия страницы')
            event.Skip()

    def OnPrevPage(self, event):
        """
        Обработчик переключения на предыдущую страницу.
        """
        try:
            self.AdvanceSelection(False)
        except:
            io_prnt.outLog(u'Ошибка переключения страницы')
            event.Skip()

    def OnNextPage(self, event):
        """
        Обработчик переключения на следующую страницу.
        """
        try:
            self.AdvanceSelection(True)
        except:
            io_prnt.outLog(u'Ошибка переключения страницы')
            event.Skip()

    # --- Свойства ---
    def icGetCurPage(self):
        """
        Определеить объект текущей страницы.
        """
        try:
            if 0 <= self._cur_selected_page < self.GetPageCount():
                return self.GetPage(self._cur_selected_page)
        except:
            io_prnt.outLog(u'Ошибка определения объекта текущей страницы')
        return None

    def SetPageImg(self, Image_, NPage_):
        """
        Установить картинку у страницы главного органайзера.
        @param Image_: Имя файла образа.
        @param NPage_: Номер страницы.
        """
        try:
            if Image_ not in self._img_name:
                # Создание образа
                img = ic_bmp.createBitmap(Image_, False)
                if img is None:
                    img = wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16))
                # Добавление образа
                img_idx = self._img_list.Add(img)
                # Запомнить индекс
                self._img_name[Image_] = img_idx
            else:
                img_idx = self._img_name[Image_]
            return self.SetPageImage(NPage_, img_idx)
        except:
            io_prnt.outErr(u'Ошибка установки картинки страницы')

    def getMainWin(self, CurObj_=None):
        """
        Главное окно.
        """
        if CurObj_ is None:
            CurObj_ = self.GetParent()
        if CurObj_ is not None:
            if issubclass(CurObj_.__class__, wx.Frame):
                return CurObj_
            else:
                return self.getMainWin(CurObj_.GetParent())
        return None
