#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания всплывающих меню.
"""

# --- Подключение библиотек ---
import wx

from . import ic_menu
import ic.utils.ic_exec
import ic.utils.ic_util
from ic.utils import ic_res
from ic.kernel import io_prnt

__version__ = (0, 0, 0, 3)

# --- Основные константы ---
# --- Описание ключей ---
RES_POPUP_TITLE = 'title'   # <краткий текст заголовка меню по умолчанию, строка>
RES_POPUP_TITLEREADONLY = 'title_readonly'  # <флаг заголовка, флаг (0 -статический/1-динамический)>
RES_POPUP_TITLEFUNC = 'title_exp'   # <выражение для формирования заголовка, блок кода>

# Спецификации:
SPC_IC_POPUPMENU = {ic_menu.RES_MENU_DESCRIPTION: '',
                    RES_POPUP_TITLE: '',    # Заголовок по умолчанию
                    RES_POPUP_TITLEREADONLY: True,  # Признак статического заголовка
                    RES_POPUP_TITLEFUNC: None,     # Блок кода на определение динамического заголовка
                    ic_menu.RES_MENU_HOTKEY: '',   # Горячая клавиша
                    ic_menu.RES_MENU_OPEN: None,   # Блок кода на открытие меню
                    ic_menu.RES_MENU_CLOSE: None,  # Блок кода на закрытие меню
                    ic_menu.RES_MENU_ITEMS: [],    # Вложенные пункты
                    }


def CreateICPopupMenu(Win_, Name_, PopupData_):
    """
    Функция создает всплывающее меню по его имени.
    @param Win_: окно-хозяин меню, к которому привязано меню.
    @param Name_: имя всплывающего меню.
    @param PopupData_: Данные о всплывающем меню.
        Если PopupData_ - строка, то это имя *.mnu файла,
        где нанаходятся данные о меню.
        Если PopupData_ - словарь, то это словарь данных всплывающего меню
        в формате: {
                    'имя меню':{
                                данные...,
                                items:[список имен пунктов меню],
                               }
                    'имя пункта1':{
                                   данные...,
                                   items:[список имен пунктов подменю],
                                  }
                   }
                    'имя пункта2':{
                                   данные...,
                                   items:[список имен пунктов подменю],
                                  }
                    .
                    .
                    .
                    'имя пунктаN':{
                                   данные...,
                                   items:[список имен пунктов подменю],
                                  }
                   }.
    @return: Возвращает ссылку на объект всплывающего меню
        или None в случае ошибки.
    """
    try:
        if isinstance(PopupData_, str):
            popup_struct = ic_res.LoadObjStruct(ic_res.RES_IDX_POPUP, Name_, PopupData_)
        elif isinstance(PopupData_, dict):
            popup_struct = PopupData_[Name_]
        else:
            io_prnt.outLog(u'Ошибка создания всплывающего меню <%s>' % Name_)
            return None
        if popup_struct == {}:
            io_prnt.outLog(u'Всплывающее меню <%s> не найдено!' % Name_)
            return None
        return icPopupMenu(Name_, popup_struct, PopupData_, Win_)
    except:
        io_prnt.outLog(u'Ошибка создания всплывающего меню <%s>' % Name_)
        return None


class icPopupMenu(ic_menu.icMenu):
    """
    Класс всплывающего меню. Наследуется от icMenu.
    """

    def __init__(self, MenuName_, MenuStruct_, ResData_, Win_):
        """
        Конструктор.
        """
        # --- Свойства класса ---
        # ИМя ресурсного файла
        self._ResData = ''

        # Код горячей клавиши
        self._HotKey = ''

        # Флаг разрешения/запрещения изменения заголовка окна
        self._TitleReadOnly = 1
        # Выражение для формирования заголовка окна
        self._TitleFunc = dict()

        try:
            # Расширение структуры до спецификации
            MenuStruct_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_POPUPMENU, MenuStruct_)

            # Вызов конструктора родителя
            ic_menu.icMenu.__init__(self, None, MenuName_, MenuStruct_)
            # Инициализация внутренних параметров
            self._ResData = ResData_
            self._Window = Win_
            # Установка обработчиков событий
            if ic_menu.RES_MENU_ITEMS in MenuStruct_ and MenuStruct_[ic_menu.RES_MENU_ITEMS] is not None:
                self.DoMenu(MenuStruct_[ic_menu.RES_MENU_ITEMS])

            # Установка остальных атибутов всплывающег меню
            if RES_POPUP_TITLE in MenuStruct_ and MenuStruct_[RES_POPUP_TITLE] is not None:
                # ВНИМАНИЕ!!! Добавление заголовка необходимо производить
                # после добавления всех пунктов меню
                self.SetTitle(MenuStruct_[RES_POPUP_TITLE])
            if ic_menu.RES_MENU_HOTKEY in MenuStruct_ and MenuStruct_[ic_menu.RES_MENU_HOTKEY] is not None:
                self._HotKey = MenuStruct_[ic_menu.RES_MENU_HOTKEY]
            # Установить параметры заголовка
            if RES_POPUP_TITLEREADONLY in MenuStruct_ and MenuStruct_[RES_POPUP_TITLEREADONLY] is not None:
                self._TitleReadOnly = MenuStruct_[RES_POPUP_TITLEREADONLY]
            if RES_POPUP_TITLEFUNC in MenuStruct_ and MenuStruct_[RES_POPUP_TITLEFUNC] is not None:
                self._TitleFunc = MenuStruct_[RES_POPUP_TITLEFUNC]
        except:
            io_prnt.outLog(u'Ошибка создания всплываюшего меню!')

    def DoMenu(self, MenuItems_):
        """
        Создать меню .
        @param MenuItems_: список имен пунктов меню.
        @return: Возвращает ссылку на объект меню или None в случае ошибки.
        """
        try:
            # Проверка аргументов
            if not MenuItems_:
                io_prnt.outLog(u'Не определены пункты меню!')
                return None
            # Перед загрузкой удалить все
            self.RemoveAll()
            menu = self.AddToLoadMenu(MenuItems_)
            return menu
        except:
            io_prnt.outLog(u'Ошибка загрузки меню!')
            return None

    def AddToLoadMenu(self, MenuItems_):
        """
        Догрузить меню.
        @param MenuItems_: список имен пунктов меню.
        @return: Возвращает ссылку на объект меню или None в случае ошибки.
        """
        try:
            # Обработка всех пунктов по порядку
            for item_name in MenuItems_:
                # Загрузить структуру пункта
                if isinstance(self._ResData, str):
                    item_struct = ic_res.LoadObjStruct(ic_res.RES_IDX_POPUP_ITEM, item_name, self._ResData)
                elif isinstance(self._ResData, dict):
                    item_struct = self._ResData[item_name]
                else:
                    io_prnt.outWarning(u'Ошибка загрузки меню:')
                    return None
                    
                self.AppendMenuItem(self, item_name, item_struct)
            return self
        except:
            io_prnt.outLastErr(u'Ошибка загрузки меню:')
            return None

    def AppendMenuItem(self, Menu_, ItemName_, ItemStruct_):
        """
        Добавить пункт.
        @param Menu_: меню-владелец пункта меню.
        @param ItemName_: имя пункта .
        @param ItemStruct_: структура пункта.
        """
        # Если надпись у объекта не определена, то не обрабатывать его
        if ic_menu.RES_MENU_CAPTION in ItemStruct_ and ItemStruct_[ic_menu.RES_MENU_CAPTION] is not None:
            item_caption = ItemStruct_[ic_menu.RES_MENU_CAPTION]
        else:
            return
        # Если ниже по уровню есть еще пункты, то
        if ic_menu.RES_MENU_ITEMS in ItemStruct_ and ItemStruct_[ic_menu.RES_MENU_ITEMS]:
            # Если меню с таким именем уже существует,  то не создавать его
            subitem = Menu_.FindMenuItemByAlias(ItemName_)
            find = True
            if subitem is None:
                find = False
                # Создать подменю и заполнить его
                subitem = ic_menu.icMenu(Menu_, ItemName_, ItemStruct_)
            item_id = subitem.GetID()
            for cur_item in ItemStruct_[ic_menu.RES_MENU_ITEMS]:
                if isinstance(self._ResData, str):
                    subitem_struct = ic_res.LoadObjStruct(ic_res.RES_IDX_MENU_ITEM, cur_item, self._ResData)
                elif isinstance(self._ResData, dict):
                    subitem_struct = self._ResData[cur_item]
                else:
                    io_prnt.outLog(u'Ошибка добавления пункта меню')
                    return None
                # Здесь рекурсия, так прикольней
                self.AppendMenuItem(subitem, cur_item, subitem_struct)
            if not find:
                # Добавить если необходимо
                Menu_.AppendMenu(item_id, item_caption, subitem)
                # Прописать в реестре
                Menu_.Register(subitem)
        else:
            item = Menu_.FindMenuItemByAlias(ItemName_)
            if item is None:
                item = Menu_.AppendItemByStruct(ItemName_, ItemStruct_)
                if item is not None:
                    Menu_.Register(item)

    def RemoveAll(self):
        """
        Очистить меню полностью.
        """
        try:
            # Определить количество меню
            items = self.GetMenuItems()
            for item in items:
                self.Destroy(item)
            # очистить реестр
            self.ClearReg()
        except:
            pass

    def OnOpenPopup(self, event):
        """
        Обработчик открытия всплывающего меню. ! Пока не используется !.
        """
        try:
            self.DoOpenMethod()
        except:
            event.Skip()

    def OnClosePopup(self, event):
        """
        Обработчик закрытия всплывающего меню. ! Пока не используется !.
        """
        # Если дочерняя открытая меню установлена, то закрыть ее
        if self._ChildOpenedMenu is not None:
            self._ChildOpenedMenu.Close()

    def DoOpenMethod(self):
        """
        Выполнить метод на открытие всплывающего меню.
        """
        ic.utils.ic_exec.ExecuteMethod(self.GetOpenMethod(), self)
        
    def DoCloseMethod(self):
        """
        Выполнить метод на закрытие всплывающего меню.
        """
        ic.utils.ic_exec.ExecuteMethod(self.GetCloseMethod(), self)

    def DoOpen(self, Win_, X_=0, Y_=0):
        """
        Открыть всплывающее меню.
        @param Win_: объект-наследник wx.Window,  к которому прикреплена меню.
        @param X_: координаты вывода.
        @param Y_: координаты вывода.
        """
        try:
            # Перед открытием выполнить метод открытия
            self.DoOpenMethod()
            # Установить динамический заголовок(если он определен)
            self.SetICTitle()
            # Показать менюху
            if Win_ is not None:
                Win_.PopupMenu(self, wx.Point(X_, Y_))
        except:
            pass
        
    # --- Функции-свойства ---
    def GetWindow(self):
        """
        Определить окно.
        """
        return self._Window

    def GetResFile(self):
        """
        Определить имя ресурсного файла.
        """
        if isinstance(self._ResData, str):
            return self._ResData
        else:
            return ''

    def GetHotKey(self):
        """
        Определить горячую клавишу для вызова меню.
        """
        return self._HotKey

    def SetICTitle(self, Title_=''):
        """
        Установить заголовок.
        @param Title_: Заголовок.
        """
        if Title_ != '':
            if not self._TitleReadOnly:
                self.SetTitle(Title_)
        else:
            if not self._TitleReadOnly and self._TitleFunc:
                new_title = ic.utils.ic_exec.ExecuteMethod(self._TitleFunc, self)
                if new_title and new_title:
                    self.SetTitle(new_title)

    def SetTitleFunc(self, TitleFunc_):
        """
        Установить метод заполнения заголовка.
        """
        self._TitleFunc = TitleFunc_

    def SetTitleReadOnly(self, TitleReadOnly_):
        """
        Установить Флаг разрешения/запрещения изменения заголовка.
        """
        self._TitleReadOnly = TitleReadOnly_
