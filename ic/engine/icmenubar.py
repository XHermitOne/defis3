#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания компонента линейки горизонтального меню.

@type SPC_IC_MENUBAR: C{dictionary}
@var SPC_IC_MENUBAR: Спецификация на ресурсное описание компонента icMenuBar.
Описание ключей SPC_IC_MENUBAR:
    - B{name = 'description'}: Описание.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.resfunc
import ic.utils.execfunc
import ic.utils.toolfunc
import ic.utils.util
from ic.log import log

import ic

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_MENUBAR = {'type': 'MenuBar',
                  'description': '',
                  'child': [],  # Вложенные пункты меню
                  }


class icMenuBar(wx.MenuBar):
    """
    Класс горизонтального меню.
    """

    def __init__(self, Win_, Name_, MenuItems_, ResData_):
        """
        Конструктор.
        """
        # Расширение структуры до спецификации
        ResData_ = ic.utils.toolfunc.defineSpcStruct(SPC_IC_MENUBAR, ResData_)

        # --- Свойства класса ---
        # Имя объекта
        self._Name = ''
        # ИМя ресурсного файла
        self._ResData = ''
        # Окно к которому прикриплено меню
        self._Window = None
        # Реестр всех меню и пунктов
        # (доступ можно производить по Id и по имени)
        self._register = dict()

        # Дочернее открытое меню
        self._ChildOpenedMenu = None

        self._Name = Name_
        self._ResData = ResData_
        self._Window = Win_

        wx.MenuBar.__init__(self)

        # Установка обработчиков событий
        self._Window.Bind(wx.EVT_MENU_CLOSE, self.OnClose)

        self.DoMenu(ResData_['child'])

    def GetContext(self):
        return None

    def appendMenuBar(self, MenuBar_=None):
        """
        Добавить к существующему меню выпадающие меню из другого горизонтального меню.
        @param MenuBar_: Объект добавляемого горизонтального меню.
        """
        if MenuBar_:
            for i_menu in range(MenuBar_.GetMenuCount()):
                menu = MenuBar_.Remove(0)
                self.Append(menu, menu.GetCaption())

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
            # Перед загрузкой удалить все
            self.RemoveAll()
            self.AddToLoadMenu(MenuItems_)
            # Привязать,  созданное меню к окну

            #   ВНИМАНИЕ:
            #     Без привязки меню к окну, меню будет создано,
            #     но не будет отображатся в окне.
            return self
        except:
            log.fatal(u'Ошибка загрузки меню')
        return None

    def AddToLoadMenu(self, MenuItems_):
        """
        Догрузить меню.
        @param MenuItems_: список имен пунктов меню.
        @return: Возвращает ссылку на созданное горизонтальное меню или
            None в случае ошибки.
        """
        try:
            # Обработка всех пунктов по порядку
            for item_struct in MenuItems_:
                # Если меню с таким именем уже существует,  то не создавать его
                item = self.FindMenuByAlias(item_struct['name'])
                if item is None:
                    if ic.utils.toolfunc.getAttrValue('activate', item_struct):
                        from ic.components.user import ic_menu_wrp
                        item = ic_menu_wrp.icMenu(self, component=item_struct,
                                                  evalSpace=self.GetContext())
                        # Проверка на ограничение доступа
                        # Добавление в главную линейку меню
                        ok = self.Append(item, item.GetCaption())
                        # Прописать в реестре
                        self.Register(item)
            return self
        except:
            log.fatal(u'Ошибка загрузки горизонтального меню <%s>' % self._Name)
        return None

    def AppendMenuItem(self, Menu_, ItemName_, ItemStruct_):
        """
        Добавить пункт.
        @param Menu_: объект меню,  к которому привязывается пункт.
        @param ItemName_: имя пункта меню.
        @param ItemStruct_: струтура пункта (его атрибуты и поля).
        """
        # Если надпись у объекта не определена,
        # то не обрабатывать его
        if 'label' in ItemStruct_ and ItemStruct_['label']:
            item_caption = ItemStruct_['label']
        else:
            return
        # Если ниже по уровню есть еще пункты, то
        if 'child' in ItemStruct_ and ItemStruct_['child']:
            # Если меню с таким именем уже существует,
            # то не создавать его
            subitem = Menu_.FindMenuItemByAlias(ItemName_)
            find = True
            if subitem is None:
                if ic.utils.toolfunc.getAttrValue('activate', ItemStruct_):
                    find = False
                    # Создать подменю и заполнить его
                    from ic.components.user import ic_menu_wrp
                    subitem = ic_menu_wrp.icMenu(Menu_, component=ItemStruct_,
                                                 evalSpace=Menu_.GetContext())
            item_id = subitem.GetID()
            for cur_item in ItemStruct_['child']:
                if isinstance(self._ResData, str):
                    subitem_struct = ic.utils.resfunc.loadObjStruct(ic.utils.resfunc.RES_IDX_MENU_ITEM,
                                                                    cur_item, self._ResData)
                elif isinstance(self._ResData, dict):
                    subitem_struct = self._ResData[cur_item]
                else:
                    log.warning(u'Ошибка добавления пункта')
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
            menu_count = self.GetMenuCount()
            for i in range(menu_count):
                # Удалять всегда первую менюшку
                self.Remove(0)
            # очистить реестр
            self.ClearReg()
        except:
            log.fatal(u'Ошибка очистки меню <%s>' % self._Name)

    def FindMenuByAlias(self, Name_):
        """
        Найти объект-пункт/меню по его имени.
        Поиск производится только на уровне данного меню.
        @param Name_: имя пункта/меню.
        @return: Возвращает ссылку на меню или None.
        """
        if Name_ in self._register:
            return self._register[Name_]
        return None

    def FindMenuByID(self, ID_):
        """
        Найти объект-пункт/меню по его идентификатору.
        Поиск производится только на уровне данного меню.
        @param ID_: идентификатор пункта/меню.
        @return: Возвращает ссылку на меню или None.
        """
        if ID_ in self._register:
            return self._register[ID_]
        return None

    def FindItemByAlias(self, Name_):
        """
        Найти пункт меню по его имени во всей иерархии.
        Поиск производится рекурсивно во всех подменю данного меню.
        @param Name_: имя пункта меню.
        @return: Возвращает ссылку на пункт меню или None.
        """
        prev_menu = None
        for menu in self._register.values():
            # Т.к. в реестр записывается значение по индексу
            # и по имени, поэтому я сделал этот фильтр
            if menu != prev_menu:
                find = menu.FindItemByAlias(Name_)
                if find is not None:
                    return find
            prev_menu = menu
        return None

    def FindMenuItemByID(self, ID_):
        """
        Найти пункт меню по его record_id во всей иерархии.
        Поиск производится рекурсивно во всех подменю данного меню.
        @param ID_: record_id пункта меню.
        @return: Возвращает ссылку на пункт меню или None.
        """
        prev_menu = None
        for menu in self._register.values():
            # Т.к. в реестр записывается значение по индексу
            # и по имени, поэтому я сделал этот фильтр
            if menu != prev_menu:
                find = menu.FindItemByID(ID_)
                if find is not None:
                    return find
            prev_menu = menu
        return None

    def Register(self, Item_):
        """
        Прописать во внутреннем реестре.
        @param Item_: объект пункта.
        """
        item_id = Item_.GetID()
        item_name = Item_.GetAlias()
        if item_id not in self._register:
            self._register[item_id] = Item_
        if item_name not in self._register:
            self._register[item_name] = Item_

    def ClearReg(self):
        """
        Полная очистка внутреннего реестра.
        """
        items = self._register.values()
        for item in items:
            item.ClearReg()
        if not self._register:
            self._register.clear()

    def OnClose(self, event):
        """
        Обработчик закрытия всех выпадающих меню.
        """
        # Если дочерняя открытая меню установлена, то закрыть ее
        if self._ChildOpenedMenu is not None:
            self._ChildOpenedMenu.Close()
        else:
            # Если дочерняя открытая меню не установленна,
            # то возможно остались незакрытые меню
            # и тогда ПРИНУДИТЕЛЬНО ЗАКРЫТЬ ВСЕ
            count = self.GetMenuCount()
            for i in range(count):
                menu = self.GetMenu(i)
                menu.Close()

    def Enable(self, item_id, enable):
        """
        Переопределенная функция для выключения/включения
            пункта меню по идентификатору.
        """
        self.FindMenuItemByID(item_id).Enable(enable)

    # --- Функции-свойства ---
    def GetWindow(self):
        """
        Определить окно.
        """
        return self._Window

    def GetAlias(self):
        return self._Name

    def GetResFile(self):
        if isinstance(self._ResData, str):
            return self._ResData
        else:
            return ''

    def SetResData(self, ResData_):
        if isinstance(ResData_, dict):
            self._ResData = ResData_

    def addResData(self, ResData_):
        """
        Добавить описание ресурса.
        """
        if self._ResData:
            if isinstance(ResData_, dict):
                self._ResData.update(ResData_)
        else:
            self.SetResData(ResData_)

    def GetChildOpenedMenu(self):
        return self._ChildOpenedMenu

    def SetChildOpenedMenu(self, ChildOpenedMenu_):
        self._ChildOpenedMenu = ChildOpenedMenu_

