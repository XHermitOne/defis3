#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания всплывающих меню.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.execfunc
import ic.utils.toolfunc
from ic.utils import resfunc
from ic.log import log

from . import icmenu

__version__ = (0, 1, 1, 1)


# Спецификации:
SPC_IC_POPUPMENU = {'description': '',
                    'title': '',  # Заголовок по умолчанию
                    'title_readonly': True,  # Признак статического заголовка
                    'title_exp': None,  # Блок кода на определение динамического заголовка
                    'hot_key': '',  # Горячая клавиша
                    'on_open': None,  # Блок кода на открытие меню
                    'on_close': None,  # Блок кода на закрытие меню
                    'child': [],  # Вложенные пункты
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
            popup_struct = resfunc.loadObjStruct(resfunc.RES_IDX_POPUP, Name_, PopupData_)
        elif isinstance(PopupData_, dict):
            popup_struct = PopupData_[Name_]
        else:
            log.warning(u'Ошибка создания всплывающего меню <%s>' % Name_)
            return None
        if popup_struct == {}:
            log.warning(u'Всплывающее меню <%s> не найдено' % Name_)
            return None
        return icPopupMenu(Name_, popup_struct, PopupData_, Win_)
    except:
        log.fatal(u'Ошибка создания всплывающего меню <%s>' % Name_)
    return None


class icPopupMenu(icmenu.icMenu):
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
            MenuStruct_ = ic.utils.toolfunc.defineSpcStruct(SPC_IC_POPUPMENU, MenuStruct_)

            # Вызов конструктора родителя
            icmenu.icMenu.__init__(self, None, MenuName_, MenuStruct_)
            # Инициализация внутренних параметров
            self._ResData = ResData_
            self._Window = Win_
            # Установка обработчиков событий
            if 'child' in MenuStruct_ and MenuStruct_['child'] is not None:
                self.DoMenu(MenuStruct_['child'])

            # Установка остальных атибутов всплывающег меню
            if 'title' in MenuStruct_ and MenuStruct_['title'] is not None:
                # ВНИМАНИЕ!!! Добавление заголовка необходимо производить
                # после добавления всех пунктов меню
                self.SetTitle(MenuStruct_['title'])
            if 'hot_key' in MenuStruct_ and MenuStruct_['hot_key'] is not None:
                self._HotKey = MenuStruct_['hot_key']
            # Установить параметры заголовка
            if 'title_readonly' in MenuStruct_ and MenuStruct_['title_readonly'] is not None:
                self._TitleReadOnly = MenuStruct_['title_readonly']
            if 'title_exp' in MenuStruct_ and MenuStruct_['title_exp'] is not None:
                self._TitleFunc = MenuStruct_['title_exp']
        except:
            log.fatal(u'Ошибка создания всплываюшего меню')

    def DoMenu(self, MenuItems_):
        """
        Создать меню .
        @param MenuItems_: список имен пунктов меню.
        @return: Возвращает ссылку на объект меню или None в случае ошибки.
        """
        try:
            # Проверка аргументов
            if not MenuItems_:
                log.warning(u'Не определены пункты меню')
                return None
            # Перед загрузкой удалить все
            self.RemoveAll()
            menu = self.AddToLoadMenu(MenuItems_)
            return menu
        except:
            log.fatal(u'Ошибка загрузки меню')
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
                    item_struct = resfunc.loadObjStruct(resfunc.RES_IDX_POPUP_ITEM, item_name, self._ResData)
                elif isinstance(self._ResData, dict):
                    item_struct = self._ResData[item_name]
                else:
                    log.warning(u'Ошибка загрузки меню:')
                    return None
                    
                self.AppendMenuItem(self, item_name, item_struct)
            return self
        except:
            log.fatal(u'Ошибка загрузки меню')
        return None

    def AppendMenuItem(self, Menu_, ItemName_, ItemStruct_):
        """
        Добавить пункт.
        @param Menu_: меню-владелец пункта меню.
        @param ItemName_: имя пункта .
        @param ItemStruct_: структура пункта.
        """
        # Если надпись у объекта не определена, то не обрабатывать его
        if 'label' in ItemStruct_ and ItemStruct_['label'] is not None:
            item_caption = ItemStruct_['label']
        else:
            return
        # Если ниже по уровню есть еще пункты, то
        if 'child' in ItemStruct_ and ItemStruct_['child']:
            # Если меню с таким именем уже существует,  то не создавать его
            subitem = Menu_.FindMenuItemByAlias(ItemName_)
            find = True
            if subitem is None:
                find = False
                # Создать подменю и заполнить его
                subitem = icmenu.icMenu(Menu_, ItemName_, ItemStruct_)
            item_id = subitem.GetID()
            for cur_item in ItemStruct_['child']:
                if isinstance(self._ResData, str):
                    subitem_struct = resfunc.loadObjStruct(resfunc.RES_IDX_MENU_ITEM, cur_item, self._ResData)
                elif isinstance(self._ResData, dict):
                    subitem_struct = self._ResData[cur_item]
                else:
                    log.warning(u'Ошибка добавления пункта меню')
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
            log.fatal(u'Ошибка очистки меню')

    def OnOpenPopup(self, event):
        """
        Обработчик открытия всплывающего меню. ! Пока не используется !.
        """
        try:
            self.DoOpenMethod()
        except:
            log.fatal(u'Ошибка открытия всплывающего меню')
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
        ic.utils.execfunc.execute_method(self.GetOpenMethod(), self)
        
    def DoCloseMethod(self):
        """
        Выполнить метод на закрытие всплывающего меню.
        """
        ic.utils.execfunc.execute_method(self.GetCloseMethod(), self)

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
            log.fatal(u'Ошибка открытия всплывающего меню')
        
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
                new_title = ic.utils.execfunc.execute_method(self._TitleFunc, self)
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
