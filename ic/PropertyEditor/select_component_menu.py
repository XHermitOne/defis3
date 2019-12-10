#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Генерация меню выбора компонента из всех возможных.

ВНИМАНИЕ! wx.FlatMenu глючит при вне зоны диалога.
Поэтому здесь используется просто wx.Menu.
"""

import wx
from wx.lib.agw import flatmenu

from ic.log import log
from ic.components import icwidget
# from ic.engine import icflatmenu
# from ic.engine import icflatmenuitem

from . import icDefInf
from . import icResTree

__version__ = (0, 1, 2, 1)


class icSelectComponentMenuManager:
    """
    Класс общих функций управления заполнения меню выбора компонента из всех возможных.
    """
    def __init__(self):
        """
        Конструктор.
        """
        # Описание всех компонентов
        self.ObjectsInfo = icResTree.GetObjectsInfo()

        # Словарь соответствий тип компонента : идентификатор пункта меню
        self.menuIdDict = dict()
        # Словарь соответствий идентификатор пункта меню : тип компонента
        self.menuDict = dict()
        self._menuGrp = dict()

        self.ObjList = None
        self.NonObjList = list()

        # Выбранный компонент
        self.selected_component = None

        # Родительское окно
        self._parent_window = None

    def init(self, parent=None, parent_component=None):
        """
        Инициализация внутренних переменных.
        :param parent: Родительское окно.
        :param parent_component: Описание родительского компонента.
        """
        self._parent_window = parent
        # Родительский компонент не определен,
        # надо получить полный список компонентов
        if parent_component is None:
            info = (-1, -1, -1, {}, -1, [], None)
        # В зависимости от типа объекта настраиваем фильтр, который
        # отсекает объекты, которые не могут быть добавлены
        else:
            info = self.ObjectsInfo.get(parent_component['type'], None)

        # Определяем список разрешенных элементах
        mod = info[-1]

        if mod and hasattr(mod, 'get_can_contain_lst'):
            self.ObjList = mod.get_can_contain_lst(None)
        elif info[4] == -1 or info[4] is None:
            if len(info) > 5:
                self.NonObjList = info[5]
            self.ObjList = list(self.ObjectsInfo.keys())
        else:
            self.ObjList = info[4]

    def create(self):
        """
        Создание меню выбора компонента из всех возможных.
        :return: Объект wx.FlatMenu с заполненными компонентами или
            None в случае ошибки.
        """
        try:
            return self._create()
        except:
            log.fatal(u'Ошибка создания меню выбора компонента')
        return None

    def _create(self):
        """
        Создание меню выбора компонента из всех возможных.
        :return: Объект wx.FlatMenu с заполненными компонентами или
            None в случае ошибки.
        """
        log.warning(u'Не определен метод создания меню')
        return self


class icSelectComponentMenu(wx.Menu, icSelectComponentMenuManager):
    """
    Класс меню выбора компонента.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Menu.__init__(self, *args, **kwargs)

        icSelectComponentMenuManager.__init__(self)

    def _create(self):
        """
        Создание меню выбора компонента из всех возможных.
        :return: Объект wx.FlatMenu с заполненными компонентами или
            None в случае ошибки.
        """
        # Цикл по группам
        if (icResTree.ObjectsInfo is not None) and (self.ObjList is not None) and (self.NonObjList is not None):
            for group in icDefInf.GroupsInfo.keys():
                menuObj = wx.Menu()
                self._menuGrp[group] = menuObj
                # Цикл по элементам группы
                for key in [key for key, el in self.ObjectsInfo.items() if el[0] == group]:
                    comp_type = icResTree.ObjectsInfo[key][3]['type']
                    if comp_type in self.ObjList and comp_type not in self.NonObjList:
                        id = icwidget.icNewId()
                        bitmap = icResTree.ObjectsInfo[key][1]
                        item = wx.MenuItem(menuObj, id, key)
                        item.SetBitmap(bitmap)
                        menuObj.Append(item)

                        self.menuDict[id] = comp_type
                        self.menuIdDict[comp_type] = id

                        if self._parent_window:
                            self._parent_window.Bind(wx.EVT_MENU, self.onSelectComponentMenuItem, id=id)
                        else:
                            log.warning(u'Необходмо обязательно указать родительсоке окно при вызове меню выбора компонента')

                id = icwidget.icNewId()
                self.Append(id, icDefInf.GroupsInfo[group], menuObj)
        return self

    def onSelectComponentMenuItem(self, event):
        """
        Обработчик выбора компонента из меню выбора компонентов.
        """
        menuitem_id = event.GetId()
        component_type = self.menuDict.get(menuitem_id, None)
        log.debug(u'Выбранный компонент <%s>' % component_type)
        self.selected_component = self.ObjectsInfo.get(component_type, None)
        event.Skip()


def popup_component_menu(parent=None, button=None):
    """
    Вызов всплывающего меню выбора компонента.
    :param parent: Родительское окно для отображения.
    :param button: Объект кнопки wx.Button, по которой производится вызов меню.
    :return: Описание выбранного компонента или
        None, если компонент не выбран.
    """
    if parent is None:
        log.warning(u'Не определено родительское окно для вывода всплывающего меню выбора компонента')
        return None

    select_menu = icSelectComponentMenu()
    select_menu.init(parent)
    select_menu.create()

    if button:
        button.PopupMenu(select_menu)
    return select_menu.selected_component


class icSelectComponentFlatMenu(flatmenu.FlatMenu,
                                icSelectComponentMenuManager):
    """
    Класс меню выбора компонента.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        flatmenu.FlatMenu.__init__(self, *args, **kwargs)

        icSelectComponentMenuManager.__init__(self)

    def _create(self):
        """
        Создание меню выбора компонента из всех возможных.
        :return: Объект wx.FlatMenu с заполненными компонентами или
            None в случае ошибки.
        """
        # Цикл по группам
        if (icResTree.ObjectsInfo is not None) and (self.ObjList is not None) and (self.NonObjList is not None):
            for group in icDefInf.GroupsInfo.keys():
                menuObj = flatmenu.FlatMenu()
                self._menuGrp[group] = menuObj
                # Цикл по элементам группы
                for name in [key for key, el in self.ObjectsInfo.items() if el[0] == group]:
                    comp_type = icResTree.ObjectsInfo[name][3]['type']
                    if comp_type in self.ObjList and comp_type not in self.NonObjList:
                        id = wx.NewId()
                        bitmap = icResTree.ObjectsInfo[name][1]
                        menuitem = flatmenu.FlatMenuItem(menuObj, id, label=name, normalBmp=bitmap)

                        menuObj.AppendItem(menuitem)

                        self.menuDict[id] = comp_type
                        self.menuIdDict[comp_type] = id

                        if self._parent_window:
                            self._parent_window.Bind(wx.EVT_MENU, self.onSelectComponentMenuItem, id=id)
                        else:
                            log.warning(u'Необходимо обязательно указать родительсоке окно при вызове меню выбора компонента')

                id = wx.NewId()
                self.AppendMenu(id, icDefInf.GroupsInfo[group], menuObj)
        return self

    def onSelectComponentMenuItem(self, event):
        """
        Обработчик выбора компонента из меню выбора компонентов.
        """
        menuitem_id = event.GetId()
        component_type = self.menuDict.get(menuitem_id, None)
        log.debug(u'Выбранный компонент <%s>' % component_type)
        self.selected_component = self.ObjectsInfo.get(component_type, None)
        event.Skip()


def popup_component_flatmenu(parent=None, button=None):
    """
    Вызов всплывающего меню выбора компонента.
    :param parent: Родительское окно для отображения.
    :param button: Объект кнопки wx.Button, по которой производится вызов меню.
    :return: Описание выбранного компонента или
        None, если компонент не выбран.
    """
    if parent is None:
        log.warning(u'Не определено родительское окно для вывода всплывающего меню выбора компонента')
        return None

    select_menu = icSelectComponentFlatMenu()
    select_menu.init(parent)
    select_menu.create()

    if button:
        button_size = button.GetSize()
        button_point = button.GetPosition()
        button_point = button.GetParent().ClientToScreen(button_point)

        select_menu.SetOwnerHeight(button_size.y)
        select_menu.Popup(wx.Point(button_point.x, button_point.y), parent)
    else:
        select_menu.Popup(wx.GetMousePosition(), parent)

    return select_menu.selected_component
