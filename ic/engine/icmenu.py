#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания компонента выпадающего меню.

@type SPC_IC_MENU: C{dictionary}
@var SPC_IC_MENU: Спецификация на ресурсное описание компонента icMenu.
Описание ключей SPC_IC_MENU:
    - B{name = 'description'}: Описание.
    - B{name = 'caption'}: Надпись.
    - B{name = 'menu_open'}: Скрипт, выполняемый при открытии меню.
    - B{name = 'menu_close'}: Скрипт, выполняемый при закрытии меню.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.ic_res
import ic.utils.ic_exec
import ic.utils.ic_util
import ic.utils.util
from ic.log import log

import ic

from . import icmenuitem


__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_MENU = {'type': 'Menu',
               'description': u'',
               'label': 'Menu',   # Надпись
               'action': True,    # Активация меню
               'on_open': None,    # Блок кода на открытие меню
               'on_close': None,   # Блок кода на закрытие меню
               'child': [],     # Вложенные пункты меню
               }


class icMenu(wx.Menu):
    """
    Класс выпадающего меню.
    """

    def __init__(self, ParentMenu_, MenuName_, MenuStruct_, Window_=None):
        """
        Конструктор.
        """
        # Идентификатор
        self._ID = 0
        # Имя (уникальное!!!)
        self._Name = ''
        # Команды,  выполняющиеся при входе/выходе в подменю
        self._Open = dict()
        self._Close = dict()
        # Окно к которому прикриплено меню
        self._Window = None
        # Надпись
        self._Caption = ''
        # Реестр всех пунктов меню (В ПОРЯДКЕ ИХ СЛЕДОВАНИЯ)
        self._item_reg = list()
        # Родительское меню
        self._ParentMenu = None
        # Признак открытой/закрытой менюшки
        self._IsOpened = 0
        # Дочернее открытое меню
        self._ChildOpenedMenu = None

        # Реестр всех меню и пунктов (доступ можно производить по Id и по имени)
        self._register = dict()

        try:
            self._Name = MenuName_
            self._ParentMenu = ParentMenu_
            if Window_ is None:
                self._Window = self.getParentWindow()
            else:
                self._Window = Window_

            self._ID = wx.NewId()

            # Расширение структуры до спецификации
            MenuStruct_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_MENU, MenuStruct_)

            if 'on_open' in MenuStruct_:
                self._Open = MenuStruct_['on_open']
            if 'on_close' in MenuStruct_:
                self._Close = MenuStruct_['on_close']
            if 'label' in MenuStruct_ and MenuStruct_['label']:
                self._Caption = MenuStruct_['label']

            # Вызов конструктора предка
            wx.Menu.__init__(self)

            self.DoMenu(MenuStruct_['child'])
        except:
            log.fatal(u'Ошибка создания выпадающего меню!')

    def getParentWindow(self):
        """
        Окно родительской менюшки.
        """
        if self._ParentMenu is not None and hasattr(self._ParentMenu, 'GetWindow'):
            return self._ParentMenu.GetWindow()
        elif self._ParentMenu is not None:
            return self._ParentMenu

    def GetContext(self):
        return None

    def DoMenu(self, MenuItems_):
        """
        Создать меню .
        @param MenuItems_: список ресурсов пунктов меню.
        @return: Возвращает ссылку на созданное горизонтальное меню или
            None в случае ошибки.
        """
        try:
            # Проверка аргументов
            if not MenuItems_:
                log.warning(u'Не определены пункты меню!')
                return None

            for item_struct in MenuItems_:
                if item_struct['type'] == 'MenuItem':
                    self.AppendItemByStruct(item_struct['name'], item_struct)
                elif item_struct['type'] == 'Menu':
                    self.AppendMenuByStruct(item_struct['name'], item_struct)

            return self
        except:
            log.fatal(u'Ошибка загрузки выпадающего меню')
        return None

    def AppendMenuByStruct(self, MenuName_, MenuStruct_):
        """
        Добавить меню по его структуре.
        @param MenuName_: имя меню.
        @param MenuStruct_: структура меню.
        @return: Возвращает ссылку на меню или None.
        """
        # Создать подменю и заполнить его
        if ic.utils.ic_util.getAttrValue('activate', MenuStruct_):
            from ic.components.user import ic_menu_wrp
            submenu = ic_menu_wrp.icMenu(self, component=MenuStruct_, evalSpace=self.GetContext())
            self.AppendMenu(submenu.GetID(), submenu.GetCaption(), submenu)
            return submenu
        return None

    def AppendItemByStruct(self, ItemName_, ItemStruct_):
        """
        Добавить пункт меню по его структуре.
        @param ItemName_: имя пункта.
        @param ItemStruct_: структура пункта.
        @return: Возвращает ссылку на пункт меню или None.
        """
        if not ic.utils.ic_util.getAttrValue('activate', ItemStruct_):
            return None
        # Если надпись у объекта не определена, то не обрабатывать его
        if 'label' in ItemStruct_ and ItemStruct_['label']:
            item_caption = ItemStruct_['label']
        else:
            return None
        item_hint = ''
        if 'short_help' in ItemStruct_ and ItemStruct_['short_help']:
            item_hint = ItemStruct_['short_help']
        # Если новый пункт не разделитель, тогда это обычный пункт
        if item_caption != icmenuitem.MENU_SEPARATOR and item_hint != icmenuitem.MENU_SEPARATOR:
            # Создать пункт меню И ПРИВЯЗАТЬ К МЕНЮ!
            from ic.components.user import ic_menuitem_wrp
            item = ic_menuitem_wrp.icMenuItem(self, component=ItemStruct_, evalSpace=self.GetContext())
        else:
            # Новый пункт-разделитель
            self.AppendSeparator()
            items = self.GetMenuItems()
            len_items_1 = len(items) - 1
            if items[len_items_1].IsSeparator():
                item = items[len_items_1]
            else:
                item = None
        # Зарегестрировать пункт во внеутреннем реестре
        self._item_reg.append(item)
        # Зарегестрировать пункт в общем реестре
        self.Register(item)
        return item

    def Close(self):
        """
        Закрыть меню.
        """
        # Сначала по рекурсии закрыть все дочернии открытые меню
        if self._ChildOpenedMenu is not None:
            self._ChildOpenedMenu.Close()
        # Выполнить метод по закрытию
        ic.utils.ic_exec.execute_method(self._Close, self)
        self.SetClosed()
        self._ParentMenu.SetChildOpenedMenu(None)

    def FindMenuItemByAlias(self, Name_):
        """
        Найти объект-пункт/меню по его имени.
        @param Name_: имя пункта/подменю.
        @return: Возвращает ссылку на объект-пункт/меню или None.
        """
        if Name_ in self._register:
            return self._register[Name_]
        return None

    def FindMenuItemByID(self, ID_):
        """
        Найти объект-пункт/меню по его ID.
        @param ID_: ID пункта/подменю.
        @return: Возвращает ссылку на объект-пункт/меню или None.
        """
        if ID_ in self._register:
            return self._register[ID_]
        return None

    def FindItemByAlias(self, Name_):
        """
        Найти пункт меню в самом меню или во всех дочерних меню.
        @param Name_: имя пункта.
        @return: Возвращает ссылку на пункт меню или None.
        """
        prev_item = None
        for item in self._register.values():
            # Т.к. в реестр записывается значение по индексу
            # и по имени, поэтому я сделал этот фильтр
            if item != prev_item:
                if item.__class__.__name__ != 'icMenu':
                    # Обработка пунктов, но не разделителей
                    if not item.IsSeparator():
                        if item.GetAlias() == Name_:
                            return item
                else:
                    find = item.FindItemByAlias(Name_)
                    if find is not None:
                        return find
            prev_item = item
        return None

    def FindItemByID(self, ID_):
        """
        Найти пункт меню в самом меню или во всех дочерних меню.
        @param ID_: ID пункта/подменю.
        @return: Возвращает ссылку на пункт меню или None.
        """
        prev_item = None
        for item in self._register.values():
            # Т.к. в реестр записывается значение по индексу
            # и по имени, поэтому я сделал этот фильтр
            if item != prev_item:
                if item.__class__.__name__ != 'icMenu':
                    # Обработка пунктов, но не разделителей
                    if not item.IsSeparator():
                        if item.GetId() == ID_:
                            return item
                else:
                    find = item.FindItemByID(ID_)
                    if find is not None:
                        return find
            prev_item = item
        return None

    def Register(self, Item_):
        """
        Прописать в реестре.
        @param Item_: объект пункта меню.
        """
        if Item_.__class__.__name__ != 'icMenu':
            if Item_.IsSeparator():
                item_id = Item_.GetId()
                item_name = 'separator' + str(item_id)
            else:
                item_id = Item_.GetID()
                item_name = Item_.GetAlias()
        else:
            item_id = Item_.GetID()
            item_name = Item_.GetAlias()
        if item_id not in self._register:
            self._register[item_id] = Item_
        if item_name not in self._register:
            self._register[item_name] = Item_

    def ClearReg(self):
        """
        Очистить весь внутренний реестр.
        """
        items = self._register.values()
        for item in items:
            # Если это меню,  тогда очистиь реестр
            if item.__class__.__name__ == 'icMenu':
                item.ClearReg()
        if self._register:
            self._register.clear()

    def Enable(self, item_id, enable):
        """
        Переопределенная функция для выключения/включения
            пункта меню по идентификатору.
        """
        self.FindMenuItemById(item_id).Enable(enable)

    # --- Функции-свойства ---
    def GetID(self):
        return self._ID

    def GetWindow(self):
        return self._Window

    def GetAlias(self):
        return self._Name

    def GetOpenMethod(self):
        return self._Open

    def GetCloseMethod(self):
        return self._Close

    def GetCaption(self):
        return self._Caption

    def GetLastItem(self):
        if self._item_reg:
            return self._item_reg[-1]
        else:
            return None

    def GetFirstItem(self):
        if self._item_reg:
            return self._item_reg[0]
        else:
            return None

    def GetItemList(self):
        return self._item_reg

    def GetParentMenu(self):
        return self._ParentMenu

    def IsOpened(self):
        return self._IsOpened

    def SetOpened(self):
        self._IsOpened = True

    def SetClosed(self):
        self._IsOpened = False

    def GetChildOpenedMenu(self):
        return self._ChildOpenedMenu

    def SetChildOpenedMenu(self, ChildOpenedMenu_):
        self._ChildOpenedMenu = ChildOpenedMenu_

