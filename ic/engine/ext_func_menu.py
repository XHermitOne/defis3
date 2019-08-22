#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций сборки ресурсов и создания горизонтальных меню.
"""

# --- Подключение библиотек ---
import ic.utils.resfunc
import ic.utils.execfunc
import ic.utils.toolfunc
import ic.utils.util
from ic.log import log

import ic

from . import icmenubar


__version__ = (0, 1, 2, 1)


# --- Функции ---
def createMenuBarByRes(parent, name, menubar_res):
    """
    Функция создает из ресурса горизонтальное меню и окно по его имени.
    @param parent: окно,  к которому привязано горизонтальное меню.
    @param name: имя объекта горизонтального меню в файле ресурсов.
    @param menubar_res: Данные о горизонтальном меню.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        return icmenubar.icMenuBar(parent, name, None, menubar_res)
    except:
        log.fatal(u'Ошибка создания меню <%s>!' % name)
    return None


def appendMenuBarByRes(parent, name, menubar_res, menubar=None):
    """
    Функция дополняет из ресурса горизонтальное меню.
    @param parent: окно,  к которому привязано горизонтальное меню.
    @param name: имя объекта горизонтального меню в файле ресурсов.
    @param menubar_res: Данные о горизонтальном меню.
        Если menubar_res - строка, то это имя *.mnu файла,
        где нанаходятся данные о меню.
        Если menubar_res - словарь, то это словарь данных меню.
    @param menubar: Объект меню, к которому добавляются пункты или описания.
        Если этот параметр равен None, тогда создается новое горизонтальное меню.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        if isinstance(menubar_res, str):
            run_struct = ic.utils.resfunc.loadObjStruct(name, menubar_res)
        elif isinstance(menubar_res, dict):
            run_struct = menubar_res[name]
        else:
            log.warning(u'Ошибка создания меню <%s>!' % name)
            return None
        if not run_struct:
            log.warning(u'Данные горизонтального меню <%s> не найдены!' % name)
            return None
        find_menubar_res = ic.utils.toolfunc.findChildResByName(run_struct['type'],
                                                                run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct['child'][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if 'type' in run_struct and run_struct['type'] == 'MenuBar':
            menu_items = menubar_struct['child']
        if menubar is None:
            return icmenubar.icMenuBar(parent, name, menu_items, menubar_struct)
        else:
            menubar.addResData(run_struct)
            menubar.AddToLoadMenu(menu_items)
            return menubar
    except:
        log.fatal(u'Ошибка создания меню <%s>!' % name)
    return None


def appendMenuBar(parent, name, menubar_res, menubar=None, engine_res=None):
    """
    Функция дополняет из ресурса горизонтальное меню.
    @param parent: окно,  к которому привязано горизонтальное меню.
    @param name: имя объекта горизонтального меню в файле ресурсов.
    @param menubar_res: Данные о горизонтальном меню.
        Если menubar_res - строка, то это имя *.mnu файла,
        где нанаходятся данные о меню.
        Если menubar_res - словарь, то это словарь данных меню.
    @param menubar: Объект меню, к которому добавляются пункты или описания.
        Если этот параметр равен None, тогда создается новое горизонтальное меню.
    @param engine_res: Ресурс движка. На самом деле это нужно для модуля ресурса.
    @return: Возвращает ссылку на объект горизонтального меню или None.
    """
    try:
        from ic.components.user import ic_menubar_wrp
        
        if isinstance(menubar_res, str):
            run_struct = ic.utils.resfunc.loadObjStruct(name, menubar_res)
        elif isinstance(menubar_res, dict):
            run_struct = menubar_res[name]
        else:
            log.warning(u'Ошибка создания меню <%s>!' % name)
            return None
        if not run_struct:
            log.warning(u'Данные горизонтального меню <%s> не найдены!' % name)
            return None
        find_menubar_res = ic.utils.toolfunc.findChildResByName(run_struct['type'],
                                                                run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct['child'][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if 'type' in run_struct and run_struct['type'] == 'MenuBar':
            menu_items = menubar_struct['child']
        if menubar is None:
            # Передать модуль ресурса движка меню
            try:
                menubar_struct['res_module'] = engine_res['res_module']
                menubar_struct['__file_res'] = engine_res['__file_res']
                context_dict = {'__file_res': menubar_struct['__file_res']}
                context = ic.utils.util.InitEvalSpace(context_dict)
            except KeyError:
                context = None
            # Создать главное меню
            menu_bar = ic_menubar_wrp.icMenuBar(parent=parent, component=menubar_struct,
                                                evalSpace=context)
            return menu_bar
        else:
            menubar.addResData(run_struct)
            menubar.AddToLoadMenu(menu_items)
            return menubar
    except:
        log.fatal(u'Ошибка создания меню <%s>!' % name)
    return None
