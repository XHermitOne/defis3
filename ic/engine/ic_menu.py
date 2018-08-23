#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций сборки ресурсов и создания горизонтальных меню.
"""

# --- Подключение библиотек ---
import ic.utils.ic_res
import ic.utils.ic_exec
import ic.utils.ic_util
import ic.utils.util
from ic.log import log

import ic

from . import icmenubar


__version__ = (0, 1, 1, 1)


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
        return icmenubar.icMenuBar(Win_, Name_, None, MenubarData_)
    except:
        log.fatal(u'Ошибка создания меню <%s>!' % Name_)
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
            log.warning(u'Ошибка создания меню <%s>!' % Name_)
            return None
        if not run_struct:
            log.warning(u'Данные горизонтального меню <%s> не найдены!' % Name_)
            return None
        find_menubar_res = ic.utils.ic_util.findChildResByName(run_struct['type'],
                                                               run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct['child'][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if 'type' in run_struct and run_struct['type'] == 'MenuBar':
            menu_items = menubar_struct['child']
        if MenuBar_ is None:
            return icmenubar.icMenuBar(Win_, Name_, menu_items, menubar_struct)
        else:
            MenuBar_.addResData(run_struct)
            MenuBar_.AddToLoadMenu(menu_items)
            return MenuBar_
    except:
        log.fatal(u'Ошибка создания меню <%s>!' % Name_)
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
            log.warning(u'Ошибка создания меню <%s>!' % Name_)
            return None
        if not run_struct:
            log.warning(u'Данные горизонтального меню <%s> не найдены!' % Name_)
            return None
        find_menubar_res = ic.utils.ic_util.findChildResByName(run_struct['type'],
                                                               run_struct['menubar'])
        if find_menubar_res >= 0:
            menubar_struct = run_struct['child'][find_menubar_res]
        else:
            menubar_struct = dict()
        # Выделить из движка описание пунктов горизонтального меню
        menu_items = list()
        if 'type' in run_struct and run_struct['type'] == 'MenuBar':
            menu_items = menubar_struct['child']
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
        log.fatal(u'Ошибка создания меню <%s>!' % Name_)
    return None
