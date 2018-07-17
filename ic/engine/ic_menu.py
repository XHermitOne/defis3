#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания компонентов меню.

@var MENU_SEPARATOR: Символ, определяющий разделитель пунктов меню

@type SPC_IC_MENUBAR: C{dictionary}
@var SPC_IC_MENUBAR: Спецификация на ресурсное описание компонента icMenuBar.
Описание ключей SPC_IC_MENUBAR:
    - B{name = 'description'}: Описание.

@type SPC_IC_MENU: C{dictionary}
@var SPC_IC_MENU: Спецификация на ресурсное описание компонента icMenu.
Описание ключей SPC_IC_MENU:
    - B{name = 'description'}: Описание.
    - B{name = 'caption'}: Надпись.
    - B{name = 'menu_open'}: Скрипт, выполняемый при открытии меню.
    - B{name = 'menu_close'}: Скрипт, выполняемый при закрытии меню.

@type SPC_IC_MENUITEM: C{dictionary}
@var SPC_IC_MENUITEM: Спецификация на ресурсное описание компонента icMenuItem.
Описание ключей SPC_IC_MENUITEM:
    - B{name = 'description'}: Описание.
    - B{name = 'caption'}: Надпись.
    - B{name = 'hot_key'}: Горячая клавиша.
    - B{name = 'hint'}: Надпись, показываемая в статусной строке главного окна.
    - B{name = 'enabled'}: Вкл./выкл. пункт меню.
    - B{name = 'checkable'}: Признак помчаемого пункта меню.
    - B{name = 'checked'}: Признак метки.
    - B{name = 'radio'}: Признак переключаемого пункта меню.
    - B{name = 'image'}: Образ пункта меню.
    - B{name = 'help'}: Файл помощи.
    - B{name = 'onAction'}: Скрипт, выполняемый при щелчке/выборе пункта.
    - B{name = 'onCheckOn'}: Скрипт, выполняемый при отметке пункта.
    - B{name = 'onCheckOff'}: Скрипт, выполняемый при снятии метки пункта.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.ic_res
import ic.utils.ic_exec
import ic.bitmap.ic_color as ic_color
import ic.utils.ic_util
import ic.utils.util
from ic.kernel import io_prnt
import ic.bitmap.ic_bmp as ic_bmp
from . import icUser

import ic

__version__ = (0, 0, 0, 4)

# --- Основные константы ---
# Символ разделителя в надписи пункта
# Если текст пункта меню равен этому символу, тогда это разделитель
MENU_SEPARATOR = '-'

ITEM_ACTION_SUFFIX = 'action'
ITEM_CHECKON_SUFFIX = 'check_on'
ITEM_CHECKOFF_SUFFIX = 'check_off'

# Описание ключей
RES_MENU_MENUBAR = 'menubar'

RES_MENU_NAME = 'name'      # <имя (уникальный код) пункта всплывающих меню, строка>
RES_MENU_CAPTION = 'caption'    # <краткий текст изображения пункта в меню, строка>
RES_MENU_DESCRIPTION = 'description'
RES_MENU_HOTKEY = 'hot_key'     # <код 'горячей' клавиши, строка>
RES_MENU_HINT = 'hint'          # <подсказка отображаемая в статусной строке, строка>
RES_MENU_ENABLED = 'enabled'    # <признак включеного/выключенного пункта, флаг (0/1)>
RES_MENU_CHECKABLE = 'checkable'    # <признак помечаемого пункта, флаг (0/1)>
RES_MENU_CHECKED = 'checked'    # <признак отметки пункта, флаг (0/1)>
RES_MENU_RADIO = 'radio'    # <признак переключаемого пункта, флаг (0/1)>
RES_MENU_IMAGE = 'image'    # <файл значка пункта, строка>
RES_MENU_BITMAP = 'bitmap'  # паспорт значка пункта
RES_MENU_HELP = 'help'      # <файл помощи по F1, строка>
RES_MENU_ITEMCOLOR = 'item_color'   # <цвет пункта меню, кортеж из 3 элементов RGB >
RES_MENU_BACKCOLOR = 'back_color'   # <цвет фона пункта меню, кортеж из 3 элементов RGB >
RES_MENU_ACTION = 'onAction'    # <действие при выборе пункта, словарь функции>
RES_MENU_CHECKON = 'onCheckOn'  # <действие при отметке пункта, словарь функции>
RES_MENU_CHECKOFF = 'onCheckOff'    # <действие при снятии отметки пункта, словарь функции>
RES_MENU_OPEN = 'menu_open'     # <действие при активизации меню, словарь функции>
RES_MENU_CLOSE = 'menu_close'   # <действие по закрытию меню, словарь функции>
RES_MENU_ITEMS = 'child'    # <список имен (кодов) пунктов выпадающих меню, список строк>
RES_MENU_ACTIVATE = 'activate'  # Активация пункта меню/его видимость

# Спецификации:
SPC_IC_MENUBAR = {'type': 'MenuBar',
                  RES_MENU_DESCRIPTION: '',
                  RES_MENU_ITEMS: [],  # Вложенные пункты меню
                  }

SPC_IC_MENU = {'type': 'Menu',
               RES_MENU_CAPTION: 'Menu',   # Надпись
               RES_MENU_DESCRIPTION: '',
               RES_MENU_ACTIVATE: True,    # Активация меню
               RES_MENU_OPEN: None,    # Блок кода на открытие меню
               RES_MENU_CLOSE: None,   # Блок кода на закрытие меню
               RES_MENU_ITEMS: [],     # Вложенные пункты меню
               # '__parent__':ic.components.icwidget.SPC_IC_WIDGET,
               }

SPC_IC_MENUITEM = {'type': 'MenuItem',
                   RES_MENU_CAPTION: 'Item',   # Надпись
                   RES_MENU_DESCRIPTION: '',
                   RES_MENU_ACTIVATE: True,    # Активация пункта меню
                   RES_MENU_HOTKEY: '',    # Горячая клавиша
                   RES_MENU_HINT: '',      # Всплывающая подсказка
                   RES_MENU_ENABLED: True,     # Вкл./выкл. пункт меню
                   RES_MENU_CHECKABLE: False,  # Признак помчаемого пункта меню
                   RES_MENU_CHECKED: False,    # Признак метки
                   RES_MENU_RADIO: False,      # Признак переключаемого пункта меню
                   RES_MENU_IMAGE: '',     # Файл образа пункта меню
                   RES_MENU_BITMAP: None,  # Паспорт образа пункта меню
                   RES_MENU_HELP: '',      # Файл помощи
                   RES_MENU_ACTION: None,      # Блок кода на выбор пункта
                   RES_MENU_CHECKON: None,     # Блок кода на пометку пункта
                   RES_MENU_CHECKOFF: None,    # Блок кода на разметку пункта
                   #'__parent__':ic.components.icwidget.SPC_IC_WIDGET,
                   }


# --- Функции ---
def CreateICMenuBar(Win_, Name_, MenubarData_):
    """
    Функция создает из ресурса горизонтальное меню и окно по его имени.
    @param Win_: окно,  к которому привязано горизонтальное меню.
    @param Name_: имя объекта горизонтального меню в файле ресурсов.
    @param MenubarData_: Данные о горизонтальном меню.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        return icMenuBar(Win_, Name_, None, MenubarData_)
    except:
        io_prnt.outErr(u'Ошибка создания меню <%s>!' % Name_)
        return None


def AppendICMenuBar(Win_, Name_, MenubarData_, MenuBar_=None):
    """
    Функция дополняет из ресурса горизонтальное меню.
    @param Win_: окно,  к которому привязано горизонтальное меню.
    @param Name_: имя объекта горизонтального меню в файле ресурсов.
    @param MenubarData_: Данные о горизонтальном меню.
        Если MenubarData_ - строка, то это имя *.mnu файла,
        где нанаходятся данные о меню.
        Если MenubarData_ - словарь, то это словарь данных меню.
    @param MenuBar_: Объект меню, к которому добавляются пункты или описания.
        Если этот параметр равен None, тогда создается новое горизонтальное меню.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        if isinstance(MenubarData_, str):
            run_struct = ic.utils.ic_res.LoadObjStruct(Name_, MenubarData_)
        elif isinstance(MenubarData_, dict):
            run_struct = MenubarData_[Name_]
        else:
            io_prnt.outWarning(u'Ошибка создания меню <%s>!' % Name_)
            return None
        if not run_struct:
            io_prnt.outWarning(u'Данные горизонтального меню <%s> не найдены!' % Name_)
            return None
        find_menubar_res = ic.utils.ic_util.findChildResByName(run_struct[RES_MENU_ITEMS],
                                                               run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct[RES_MENU_ITEMS][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if RES_MENU_MENUBAR in run_struct and run_struct[RES_MENU_MENUBAR]:
            menu_items = menubar_struct[RES_MENU_ITEMS]
        if MenuBar_ is None:
            return icMenuBar(Win_, Name_, menu_items, menubar_struct)
        else:
            MenuBar_.addResData(run_struct)
            MenuBar_.AddToLoadMenu(menu_items)
            return MenuBar_
    except:
        io_prnt.outErr(u'Ошибка создания меню <%s>!' % Name_)
        return None


def appendMenuBar(Win_, Name_, MenubarData_, MenuBar_=None, RunnerResource_=None):
    """
    Функция дополняет из ресурса горизонтальное меню.
    @param Win_: окно,  к которому привязано горизонтальное меню.
    @param Name_: имя объекта горизонтального меню в файле ресурсов.
    @param MenubarData_: Данные о горизонтальном меню.
        Если MenubarData_ - строка, то это имя *.mnu файла,
        где нанаходятся данные о меню.
        Если MenubarData_ - словарь, то это словарь данных меню.
    @param MenuBar_: Объект меню, к которому добавляются пункты или описания.
        Если этот параметр равен None, тогда создается новое горизонтальное меню.
    @param RunneerResource_: Ресурс движка. На самом деле это нужно для модуля ресурса.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        from ic.components.user import ic_menubar_wrp
        
        if isinstance(MenubarData_, str):
            run_struct = ic.utils.ic_res.LoadObjStruct(Name_, MenubarData_)
        elif isinstance(MenubarData_, dict):
            run_struct = MenubarData_[Name_]
        else:
            io_prnt.outWarning(u'Ошибка создания меню <%s>!' % Name_)
            return None
        if not run_struct:
            io_prnt.outWarning(u'Данные горизонтального меню <%s> не найдены!' % Name_)
            return None
        find_menubar_res = ic.utils.ic_util.findChildResByName(run_struct[RES_MENU_ITEMS],
                                                               run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct[RES_MENU_ITEMS][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if RES_MENU_MENUBAR in run_struct and run_struct[RES_MENU_MENUBAR]:
            menu_items = menubar_struct[RES_MENU_ITEMS]
        if MenuBar_ is None:
            # Передать модуль ресурса движка меню
            try:
                menubar_struct['res_module'] = RunnerResource_['res_module']
                menubar_struct['__file_res'] = RunnerResource_['__file_res']
                context_dict = {'__file_res': menubar_struct['__file_res']}
                context = ic.utils.util.InitEvalSpace(context_dict)
            except KeyError:
                context = None
            # Создать главное меню
            menu_bar = ic_menubar_wrp.icMenuBar(parent=Win_, component=menubar_struct,
                                                evalSpace=context)
            return menu_bar
        else:
            MenuBar_.addResData(run_struct)
            MenuBar_.AddToLoadMenu(menu_items)
            return MenuBar_
    except:
        io_prnt.outErr(u'Ошибка создания меню <%s>!' % Name_)
        return None
        

# --- Описания классов ---
class icMenuBar(wx.MenuBar):
    """
    Класс горизонтального меню.
    """

    def __init__(self, Win_, Name_, MenuItems_, ResData_):
        """
        Конструктор.
        """
        # Расширение структуры до спецификации
        ResData_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_MENUBAR, ResData_)

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

        self.DoMenu(ResData_[RES_MENU_ITEMS])

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
                io_prnt.outWarning(u'Не определены пункты меню!')
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
            io_prnt.outErr(u'Ошибка загрузки меню')
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
                    if ic.utils.ic_util.getAttrValue('activate', item_struct):
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
            io_prnt.outErr(u'Ошибка загрузки горизонтального меню <%s>' % self._Name)
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
        if RES_MENU_CAPTION in ItemStruct_ and ItemStruct_[RES_MENU_CAPTION]:
            item_caption = ItemStruct_[RES_MENU_CAPTION]
        else:
            return
        # Если ниже по уровню есть еще пункты, то
        if RES_MENU_ITEMS in ItemStruct_ and ItemStruct_[RES_MENU_ITEMS]:
            # Если меню с таким именем уже существует,
            # то не создавать его
            subitem = Menu_.FindMenuItemByAlias(ItemName_)
            find = True
            if subitem is None:
                if ic.utils.ic_util.getAttrValue('activate', ItemStruct_):
                    find = False
                    # Создать подменю и заполнить его
                    from ic.components.user import ic_menu_wrp
                    subitem = ic_menu_wrp.icMenu(Menu_, component=ItemStruct_,
                                                 evalSpace=Menu_.GetContext())
            item_id = subitem.GetID()
            for cur_item in ItemStruct_[RES_MENU_ITEMS]:
                if isinstance(self._ResData, str):
                    subitem_struct = ic.utils.ic_res.LoadObjStruct(ic.utils.ic_res.RES_IDX_MENU_ITEM,
                                                                   cur_item, self._ResData)
                elif isinstance(self._ResData, dict):
                    subitem_struct = self._ResData[cur_item]
                else:
                    io_prnt.outWarning(u'Ошибка добавления пункта')
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
            io_prnt.outErr(u'Ошибка очистки меню <%s>' % self._Name)

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
        Найти пункт меню по его id во всей иерархии.
        Поиск производится рекурсивно во всех подменю данного меню.
        @param ID_: id пункта меню.
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

            if RES_MENU_OPEN in MenuStruct_:
                self._Open = MenuStruct_[RES_MENU_OPEN]
            if RES_MENU_CLOSE in MenuStruct_:
                self._Close = MenuStruct_[RES_MENU_CLOSE]
            if RES_MENU_CAPTION in MenuStruct_ and MenuStruct_[RES_MENU_CAPTION]:
                self._Caption = MenuStruct_[RES_MENU_CAPTION]
            
            # Вызов конструктора предка
            wx.Menu.__init__(self)

            self.DoMenu(MenuStruct_[RES_MENU_ITEMS])
        except:
            io_prnt.outErr(u'Ошибка создания выпадающего меню!')

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
                io_prnt.outWarning(u'Не определены пункты меню!')
                return None

            for item_struct in MenuItems_:
                if item_struct['type'] == 'MenuItem':
                    self.AppendItemByStruct(item_struct['name'], item_struct)
                elif item_struct['type'] == 'Menu':
                    self.AppendMenuByStruct(item_struct['name'], item_struct)

            return self
        except:
            io_prnt.outErr(u'Ошибка загрузки выпадающего меню')
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
        if RES_MENU_CAPTION in ItemStruct_ and ItemStruct_[RES_MENU_CAPTION]:
            item_caption = ItemStruct_[RES_MENU_CAPTION]
        else:
            return None
        item_hint = ''
        if RES_MENU_HINT in ItemStruct_ and ItemStruct_[RES_MENU_HINT]:
            item_hint = ItemStruct_[RES_MENU_HINT]
        # Если новый пункт не разделитель, тогда это обычный пункт
        if item_caption != MENU_SEPARATOR and item_hint != MENU_SEPARATOR:
            # Создать пункт меню И ПРИВЯЗАТЬ К МЕНЮ!
            from ic.components.user import ic_menuitem_wrp
            item = ic_menuitem_wrp.icMenuItem(self, component=ItemStruct_, evalSpace=self.GetContext())
        else:
            # Новый пункт-разделитель
            self.AppendSeparator()
            items = self.GetMenuItems()
            len_items_1 = len(items)-1
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
        ic.utils.ic_exec.ExecuteMethod(self._Close, self)
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


class icMenuItem(wx.MenuItem):
    """
    Класс пункта меню.
    """

    def __init__(self, ParentMenu_, ItemName_, ItemStruct_, context=None):
        """
        Конструктор.
        """
        # Контекст
        self.context = context
        # --- Свойства класса ---
        # Имя (уникальное!!!)
        self._Name = ''
        # Команда, выполняющаяся при выборе пункта меню
        self._Action = dict()
        # Команда, выполняющаяся при отметке пункта меню
        self._CheckOn = dict()
        # Команда, выполняющаяся при разметке пункта меню
        self._CheckOff = dict()
        # Окно к которому прикриплен пункт меню
        self._Window = None
        # Родительское меню
        self._ParentMenu = None
    
        # Признак включенного пункта (ТОЛЬКО для пунктов РАДИО!)
        self._radio_checked = False
        # Предыдущий и следующий элемент группы Radio (ТОЛЬКО для пунктов РАДИО!)
        self._RadioPrev = None
        self._RadioNext = None
        # Информация о привязанном инструменте
        self._Toolbar = None
        self._ToolID = 0
        # Собственная метка, необходимая для обновления состояния
        # помечаемых и радио пунктов в всплывающем меню
        self._SelfChecked = 0

        try:
            self._ParentMenu = ParentMenu_
            item_id = wx.NewId()
            self._Name = ItemName_
            item_name = self._Name+str(item_id)
            item_hotkey = ''

            # Расширение структуры до спецификации
            ItemStruct_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_MENUITEM, ItemStruct_)

            if RES_MENU_HOTKEY in ItemStruct_ and ItemStruct_[RES_MENU_HOTKEY]:
                item_hotkey = ItemStruct_[RES_MENU_HOTKEY]
            if RES_MENU_CAPTION in ItemStruct_ and ItemStruct_[RES_MENU_CAPTION]:
                if ItemStruct_[RES_MENU_CAPTION] != MENU_SEPARATOR:
                    item_label = ItemStruct_[RES_MENU_CAPTION]
                    if item_hotkey:
                        item_label = item_label+'\t'+item_hotkey
                else:
                    return
            item_checkable = False
            if RES_MENU_CHECKABLE in ItemStruct_ and ItemStruct_[RES_MENU_CHECKABLE] is not None:
                item_checkable = ItemStruct_[RES_MENU_CHECKABLE]
            item_radio = False
            if RES_MENU_RADIO in ItemStruct_ and ItemStruct_[RES_MENU_RADIO] is not None:
                item_radio = ItemStruct_[RES_MENU_RADIO]
            
            item_kind = wx.ITEM_NORMAL
            if item_checkable:
                item_kind = wx.ITEM_CHECK
            else:
                if item_radio:
                    item_kind = wx.ITEM_RADIO
            # Создать пункт
            wx.MenuItem.__init__(self, ParentMenu_, item_id, item_label,
                                 item_name, item_kind, None)
            # Инициализировать некоторые атрибуты
            self._Window = self._ParentMenu.GetWindow()
            if RES_MENU_ACTION in ItemStruct_:
                self._Action = ItemStruct_[RES_MENU_ACTION]
            else:
                if 'action' in ItemStruct_:
                    self._Action = ItemStruct_['action']
            if RES_MENU_CHECKON in ItemStruct_:
                self._CheckOn = ItemStruct_[RES_MENU_CHECKON]
            else:
                if 'check_on' in ItemStruct_:
                    self._CheckOn = ItemStruct_['check_on']
            if RES_MENU_CHECKOFF in ItemStruct_:
                self._CheckOff = ItemStruct_[RES_MENU_CHECKOFF]
            else:
                if 'check_off' in ItemStruct_:
                    self._CheckOff = ItemStruct_['check_off']

            if RES_MENU_BITMAP in ItemStruct_ and ItemStruct_[RES_MENU_BITMAP]:
                self.setBitmap(ItemStruct_[RES_MENU_BITMAP])
            elif RES_MENU_IMAGE in ItemStruct_ and ItemStruct_[RES_MENU_IMAGE]:
                self.SetImage(ItemStruct_[RES_MENU_IMAGE])
            
            item_hint = ''
            if RES_MENU_HINT in ItemStruct_ and ItemStruct_[RES_MENU_HINT] is not None:
                item_hint = ItemStruct_[RES_MENU_HINT]
            self.SetHelp(item_hint)

            # --- Обработка РАДИО пунктов ---
            # Установка признака метки (ТОЛЬКО для РАДИО ПУНКТОВ!)
            self._radio_checked = item_kind == wx.ITEM_RADIO and self.is_checked()
            # Установить связи RADIO GROUP
            last_item = self._ParentMenu.GetLastItem()
            if last_item is not None:
                if last_item.GetKind() == wx.ITEM_RADIO:
                    self._RadioPrev = last_item
                    last_item.SetRadioNext(self)

            # Установить цвета

            # ВНИМАНИЕ! Цвета необходимо установливать до присоединения
            #            пункта к меню!

            if RES_MENU_ITEMCOLOR in ItemStruct_ and ItemStruct_[RES_MENU_ITEMCOLOR] is not None:
                if isinstance(ItemStruct_[RES_MENU_ITEMCOLOR], tuple):
                    self.SetTextColour(wx.Colour(ItemStruct_[RES_MENU_ITEMCOLOR][ic_color.I_RED],
                                                 ItemStruct_[RES_MENU_ITEMCOLOR][ic_color.I_GREEN],
                                                 ItemStruct_[RES_MENU_ITEMCOLOR][ic_color.I_BLUE]))
                else:
                    try:
                        self.SetTextColour(ItemStruct_[RES_MENU_ITEMCOLOR])
                    except:
                        pass
            if RES_MENU_BACKCOLOR in ItemStruct_ and ItemStruct_[RES_MENU_BACKCOLOR] is not None:
                if isinstance(ItemStruct_[RES_MENU_ITEMCOLOR], tuple):
                    self.SetBackgroundColour(wx.Colour(ItemStruct_[RES_MENU_BACKCOLOR][ic_color.I_RED],
                                                       ItemStruct_[RES_MENU_BACKCOLOR][ic_color.I_GREEN],
                                                       ItemStruct_[RES_MENU_BACKCOLOR][ic_color.I_BLUE]))
                else:
                    try:
                        self.SetBackgroundColour(ItemStruct_[RES_MENU_BACKCOLOR])
                    except:
                        pass

            # ---------------------------------
            # Добавить новый пункт выпадающего меню

            # ВНИМАНИЕ:
            #    Без добавления, пункты не будут отображаться в меню.

            self._ParentMenu.AppendItem(self)
            if self._Window:
                self._Window.Bind(wx.EVT_MENU, self.OnActionItem, id=self.GetID())
                self._Window.Bind(wx.EVT_MENU_HIGHLIGHT, self.OnHighlight, id=self.GetID())
                if item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_RADIO:
                    self._Window.Bind(wx.EVT_UPDATE_UI, self.OnUpdate, id=item_id)
                
            # Установить атрибуты пункта меню

            # ВНИМАНИЕ:
            #    Все атрибуты пункта необходимо менять после прсоединения
            #    к меню, иначе атрибуты не отобразятся в меню

            if self.IsCheckable():
                item_checked = False
                if RES_MENU_CHECKED in ItemStruct_ and ItemStruct_[RES_MENU_CHECKED] is not None:
                    item_checked = ItemStruct_[RES_MENU_CHECKED]
                self.Check(item_checked)
            item_enabled = True
            if RES_MENU_ENABLED in ItemStruct_ and ItemStruct_[RES_MENU_ENABLED] is not None:
                item_enabled = ItemStruct_[RES_MENU_ENABLED]
            # Проверка на ограничение доступа к функциональному ресурсу
            if not icUser.canAuthent(icUser.ACCESS_USE, self._Name, icUser.ACC_MENUITEM, False):
                item_enabled = False

            wx.MenuItem.Enable(self, item_enabled)

            self._SelfChecked = self.is_checked()
        except:
            io_prnt.outErr(u'Ошибка создания пункта меню <%s>' % self._Name)

    def GetContext(self):
        return None
        
    def SetImage(self, Image_):
        """
        Функция установки образов пункта меню.
        @param Image_: имя файла образа (BMP).
        """
        try:
            item_kind = self.GetKind()
            # для разделителя нельзя установить картинку
            if item_kind == wx.ITEM_SEPARATOR:
                return

            if Image_ and type(Image_) in (str, unicode):
                eval_space = self.context or ic.utils.util.InitEvalSpace({'MENUITEM': self})
                ret, img = ic.utils.util.ic_eval(Image_, evalSpace=eval_space)
                if not ret:
                    img = Image_
            else:
                img = Image_
            if not img:
                return
            elif isinstance(img, str):
                # Задается имя файла образа
                img = ic_bmp.createBitmap(img)
            if img and (item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_NORMAL):
                # ВНИМАНИЕ:
                #    Картинки необходимо устанавливать до присоединения
                #    пункта к меню. Иначе она не будет отображаться!
                self.SetBitmap(img)
        except:
            io_prnt.outErr(u'Ошибка установки образа для пункта меню <%s>!' % Image_)
            return
        
    def setBitmap(self, BmpPsp_):
        """
        Функция установки картинки пункта меню.
        @param BmpPsp_: Паспорт картинки.
        """
        try:
            item_kind = self.GetKind()
            # для разделителя нельзя установить картинку
            if item_kind == wx.ITEM_SEPARATOR:
                return

            # Паспорт не определен
            if not BmpPsp_:
                return

            bitmap_obj = ic.getKernel().Create(BmpPsp_)
            img = bitmap_obj.getBitmap()
            
            if img and (item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_NORMAL):
                # ВНИМАНИЕ:
                #    Картинки необходимо устанавливать до присоединения
                #    пункта к меню. Иначе она не будет отображаться!
                self.SetBitmap(img)
        except:
            io_prnt.outErr(u'Ошибка установки картинки %s для пункта меню %s!' % (BmpPsp_, self.GetID()))
            return

    def DoAction(self):
        """
        Выполнить действие,  привязанное к пункту меню.
        """
        self.ExecuteItem()

        kind = self.GetKind()
        # Синхронизировать изображение с инструментом
        if kind == wx.ITEM_CHECK or kind == wx.ITEM_RADIO:
            self.ToggleTool(self.is_checked())

        # Если пункт переключаемый,  то он выключил другой пункт
        if kind == wx.ITEM_RADIO and self._SelfChecked:
            self.ToggleOffRadioPrev()
            self.ToggleOffRadioNext()

    def OnActionItem(self, event):
        """
        Обработчик события выбора пункта меню.
        """
        try:
            if not ic.ic_mode.isRuntimeMode():
                # Если режим дизайнера, то ничего не делать
                return
            
            # Определить объект, который вызвал событие
            item_id = event.GetId()
            # Если это пункт меню,  тогда выполнить его
            if item_id == self.GetID():
                self.DoAction()
        except:
            io_prnt.outErr(u'Ошибка выполнения команды:')
            event.Skip()

    def ToggleOffRadio(self):
        """
        Переключить радио пункт.
        @return: Возвращает True в случае удачного выполнения операции или
            иначе False.
        """
        if self.GetKind() == wx.ITEM_RADIO and self._radio_checked:
            ic.utils.ic_exec.ExecuteMethod(self.GetCheckOffMethod(), self)
            self._radio_checked = False
            # Установить собственную метку
            self._SelfChecked = False
            return True
        return False

    def ToggleOffRadioPrev(self):
        """
        Выключить радио пункт.
        """
        if self._RadioPrev is not None:
            if self._RadioPrev.ToggleOffRadio():
                return
            self._RadioPrev.ToggleOffRadioPrev()

    def ToggleOffRadioNext(self):
        """
        Выключить радио пункт.
        """
        if self._RadioNext is not None:
            if self._RadioNext.ToggleOffRadio():
                return
            self._RadioNext.ToggleOffRadioNext()

    def OnHighlight(self, event):
        """
        Обработчик подсветки пункта меню.
        """
        # Если существуют в данной менюшке дочерние открытые меню,
        # тогда закрыть их, т.к. текущая меню получила фокус
        if self._ParentMenu is not None:
            if self._ParentMenu.GetChildOpenedMenu() is not None:
                self._ParentMenu.GetChildOpenedMenu().Close()
            # Закрыть предыдущую открытую дочернюю меню
            parent_parent_menu = self._ParentMenu.GetParentMenu()
            if parent_parent_menu is not None:
                if parent_parent_menu.GetChildOpenedMenu() is not None:
                    if parent_parent_menu.GetChildOpenedMenu() != self._ParentMenu:
                        parent_parent_menu.GetChildOpenedMenu().Close()
                # Установить связи подчинения открытых меню
                parent_parent_menu.SetChildOpenedMenu(self._ParentMenu)
            # Если менюшка прежде не открывалась, тогда выполнить метод на открытие
            if not self._ParentMenu.IsOpened():
                ic.utils.ic_exec.ExecuteMethod(self._ParentMenu.GetOpenMethod(), self)
            # Установить признак открытой меню
            self._ParentMenu.SetOpened()

        # Вызов стандартного обработчика события окна для отображения
        # строки помощи в статусной строке
        if self._Window is not None and self._Window.GetStatusBar() is not None:
            self._Window.SetStatusText(self.GetHelp())

    def OnUpdate(self, event):
        """
        Обработчик обновления.
        Необходим для обновления состояния пунктов всплывающего меню.
        """
        if self.is_checked() != self._SelfChecked:
            item_kind = self.GetKind()
            if item_kind == wx.ITEM_CHECK:
                self.Check(self._SelfChecked)
            elif item_kind == wx.ITEM_RADIO and self._SelfChecked:
                self.Check(self._SelfChecked)

    def LinkTool(self, Toolbar_, ToolID_):
        """
        Связать пункт меню с инструментом.
        @param Toolbar_: объект панели инструментов.
        @param ToolID_: идентификатор инструмента.
        """
        if Toolbar_ is None:
            return
        self._Toolbar = Toolbar_
        self._ToolID = ToolID_

    def ToggleTool(self, Toggle_):
        """
        Переключить инструмент,  связанный с пунктом меню.
        @param Toggle_: включить-True/выключить-False.
        """
        if self._Toolbar is not None:
            self._Toolbar.ToggleTool(self._ToolID, Toggle_)

    def ExecuteItem(self):
        """
        Выполнить действие,  привязанное к пункту меню.
        @param Item_: объект пункта меню.
        """
        try:
            item_kind = self.GetKind()
            ic.utils.ic_exec.ExecuteMethod(self.GetActionMethod(), self)
    
            # Если пункт меню отмечен как переключаемый, то ...
            if item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_RADIO:
                if self._SelfChecked:
                    result = ic.utils.ic_exec.ExecuteMethod(self.GetCheckOffMethod(), self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.Check(True)
                            self._SelfChecked = True
                        else:
                            self._SelfChecked = False
                    else:
                        self._SelfChecked = False
                else:
                    result = ic.utils.ic_exec.ExecuteMethod(self.GetCheckOnMethod(), self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.Check(False)
                            self._SelfChecked = False
                        else:
                            self._SelfChecked = True
                    else:
                        self._SelfChecked = True
        except:
            raise   # Повторная генерация исключения

    def is_checked(self):
        if self.IsCheckable():
            return self.IsChecked()
        return False
        
    # --- Функции-свойства ---
    def GetParentMenu(self):
        return self._ParentMenu

    def GetWindow(self):
        return self._Window

    def GetID(self):
        return self.GetId()

    def GetAlias(self):
        return self._Name

    def GetActionMethod(self):
        return self._Action

    def GetCheckOnMethod(self):
        return self._CheckOn

    def GetCheckOffMethod(self):
        return self._CheckOff
    
    def GetRadioPrev(self):
        return self._RadioPrev

    def SetRadioPrev(self, RadioPrev_):
        self._RadioPrev = RadioPrev_

    def GetRadioNext(self):
        return self._RadioNext

    def SetRadioNext(self, RadioNext_):
        self._RadioNext = RadioNext_

    def GetToolID(self):
        return self._ToolID

    def GetToolBar(self):
        return self._Toolbar

    def Enable(self, enable=True):
        """
        Включить/выключить пункт меню.
        @param enable: Флаг включения/выключения.
        """
        # Если вообще нельзя использовать этот пункт, то ничего и не делать
        if icUser.canAuthent(icUser.ACCESS_USE, self._Name, icUser.ACC_MENUITEM, False):
            # Если есть связанный инструмент,  тогда отключить и его
            if self._Toolbar and self._ToolID:
                self._Toolbar.EnableTool(self._ToolID, enable)
            # Вызов метода предка
            wx.MenuItem.Enable(self, enable)
