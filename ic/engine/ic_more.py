#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль дополнительных функций обслуживания системы.
"""

# --- Подключение библиотек ---
import ic.iccomponents.icmenutree

from . import ic_menu
import ic.utils.ic_res
from ic.kernel import io_prnt


def MenuToTree(Tree_, Name_, Index_, Data_):
    """
    Перекодировка описания движка в описание дерева.
    @param Name_: Имя объекта.
    @param Index_: Индекс группы объектов в списке данных.
    @param Data_: Данные ДВИЖКОВ системы (формат файла *.mnu).
    """
    try:
        # Определение ключа
        if Index_ == ic.utils.ic_res.RES_IDX_RUN:  # <(0)словарь главных меню>,
            key = ic_menu.RES_MENU_MENUBAR
            next_idx = ic.utils.ic_res.RES_IDX_MENUBAR
        elif Index_ == ic.utils.ic_res.RES_IDX_MENUBAR:  # <(1)словарь пунктов горизонтальных меню>,
            key = ic_menu.RES_MENU_ITEMS
            next_idx = ic.utils.ic_res.RES_IDX_MENU_ITEM
        elif Index_ == ic.utils.ic_res.RES_IDX_MENU_ITEM:  # <(2)словарь пунктов выпадающих меню>,
            key = ic_menu.RES_MENU_ITEMS
            next_idx = ic.utils.ic_res.RES_IDX_MENU_ITEM
        elif Index_ == ic.utils.ic_res.RES_IDX_POPUP_ITEM:  # <(3)словарь пунктов всплывающих меню>,
            key = ic_menu.RES_MENU_ITEMS
            next_idx = ic.utils.ic_res.RES_IDX_POPUP_ITEM
        elif Index_ == ic.utils.ic_res.RES_IDX_POPUP:  # <(4)словарь всплывающих меню>,
            key = ic_menu.RES_MENU_ITEMS
            next_idx = ic.utils.ic_res.RES_IDX_POPUP_ITEM
        else:
            io_prnt.outLog(u'Недопустимый индекс')
            return {}
        
        tree = []
        # Определить список пунктов
        items = Data_[Index_][Name_][key]
        # Перебор всех пунктов
        for item in items:
            tree_item = {}
            tree.append(tree_item)
            # Заполнение узла
            # Имя узла
            tree_item[ic.iccomponents.icmenutree.MENU_ITEM_NAME_KEY] = item
            # Заголовок
            if ic_menu.RES_MENU_CAPTION in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_CAPTION] is not None:
                tree_item[ic_menu.RES_MENU_CAPTION] = Data_[next_idx][item][ic_menu.RES_MENU_CAPTION]
            else:
                tree_item[ic_menu.RES_MENU_CAPTION] = ''
            # Горячая клавиша
            if ic_menu.RES_MENU_HOTKEY in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_HOTKEY] is not None:
                tree_item[ic_menu.RES_MENU_HOTKEY] = Data_[next_idx][item][ic_menu.RES_MENU_HOTKEY]
            else:
                tree_item[ic_menu.RES_MENU_HOTKEY] = ''
            # Цвет текста пункта меню
            if ic_menu.RES_MENU_ITEMCOLOR in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_ITEMCOLOR] is not None:
                tree_item[ic_menu.RES_MENU_ITEMCOLOR] = Data_[next_idx][item][ic_menu.RES_MENU_ITEMCOLOR]
            else:
                tree_item[ic_menu.RES_MENU_ITEMCOLOR] = Tree_.GetForegroundColour()
            # Цвет фона пункта меню
            if ic_menu.RES_MENU_BACKCOLOR in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_BACKCOLOR] is not None:
                tree_item[ic_menu.RES_MENU_BACKCOLOR] = Data_[next_idx][item][ic_menu.RES_MENU_BACKCOLOR]
            else:
                tree_item[ic_menu.RES_MENU_BACKCOLOR] = Tree_.GetBackgroundColour()
            # Образ
            if ic_menu.RES_MENU_IMAGE in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_IMAGE] is not None:
                tree_item[ic_menu.RES_MENU_IMAGE] = Data_[next_idx][item][ic_menu.RES_MENU_IMAGE]
            else:
                tree_item[ic_menu.RES_MENU_IMAGE] = ''
            # Вложенные пункты
            if ic_menu.RES_MENU_ITEMS in Data_[next_idx][item] and \
               Data_[next_idx][item][ic_menu.RES_MENU_ITEMS] is not None and \
               Data_[next_idx][item][ic_menu.RES_MENU_ITEMS] != []:
                tree_item[ic_menu.RES_MENU_ITEMS] = MenuToTree(Tree_, item, next_idx, Data_)
            else:
                tree_item[ic_menu.RES_MENU_ITEMS] = []

        return tree
    except:
        io_prnt.outErr(u'Ошибка перекодировки описания движка в описание дерева')
        raise
