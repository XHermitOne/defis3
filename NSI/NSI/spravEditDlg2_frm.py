#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### RESOURCE_MODULE: C:/defis/NSI/NSI/spravEditDlg2.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/spravEditDlg2_frm.py
# Purpose:     Модуль ресурса.
#
# Author:      <...>
#
# Created:
# RCS-ID:      $Id: $
# Copyright:   (c)
# Licence:     <your licence>
# -----------------------------------------------------------------------------

"""
Модуль ресурса <C:/defis/NSI/NSI/spravEditDlg2.frm>.
"""

import wx
from ic.dlg import ic_dlg
from ic.utils import coderror
from NSI.spravEditDlg_frm import *

#   Версия модуля
__version__ = (0, 1, 1, 1)

# --- Общие переменные ---
# Признак изменения справочника
is_changed = False


# --- Функции-обработчики событий ---
def onMouseClickAddTool2(evalSpace):
    """
    Обработчик щелчка на кнопке панели инструментов addTool.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    sprav = evalSpace['OBJ']
    old_cod = sprav.getPrevCode()
    GetInterface = evalSpace['GetInterface']

    if old_cod is None:
        old_cod = ''

    if old_cod:
        level = sprav.getLevelByCod(old_cod).getNext()
    else:
        level = sprav.getLevelByCod(old_cod)

    new_cod = old_cod
    grid = GetInterface('spravGrid').get_grid()
    if level:
        grid.GetDataset().SetStructFilter({'cod': [new_cod, level.getCodLen()]})
    grid.AddRows()
    
    # Внесено изменение
    global is_changed
    is_changed = True
    return old_cod


def onCodControl2(evalSpace):
    """
    Контроль кода.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    old_value = evalSpace['old_value']
    value = evalSpace['value']
    sprav = evalSpace['OBJ']
    GetInterface = evalSpace['GetInterface']
    GetObject = evalSpace['GetObject']

    # Проверка уникальности кода
    try:
        new_cod = GetObject('spravTree').getSelectionRecord()[0]
    except:
        new_cod = None

    # Проверка, есть ли подкоды
    if old_value and sprav.isSubCodes(old_value):
        ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Нельзя изменять значение кода. Есть подкоды.')
        return 3, None

    buff_codes = [rec[0] for rec in GetInterface('spravGrid').get_grid().GetDataset().data][:-1]

    ctrl_ret = coderror.IC_CTRL_OK
    if value in buff_codes:
        ctrl_ret = coderror.IC_CTRL_FAILED_IGNORE

    if ctrl_ret not in [coderror.IC_CTRL_OK, coderror.IC_CTRL_REPL]:
        ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Такой код есть уже в справочнике!')
        return ctrl_ret, None

    # Проверяем по связанному справочнику, если он есть
    if new_cod is None:
        new_cod = ''

    ref_sprav = sprav.getLevelRefSpravByCod(new_cod)
    if ref_sprav:
        return ref_sprav.Ctrl(value, field='cod')
    return ctrl_ret, None


def onMouseClickDelTool2(evalSpace):
    """
    Нажатие кнопки delTool на панели инструментов.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    GetInterface = evalSpace['GetInterface']
    grid = GetInterface('spravGrid').get_grid()
    i_row = grid.GetGridCursorRow()
    grid.DelRows(i_row)
    # Внесено изменение
    global is_changed
    is_changed = True


def onMouseClickSaveTool2(evalSpace):
    """
    Сохранение внесенных изменений.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    GetInterface = evalSpace['GetInterface']
    sprav = evalSpace['OBJ']
    old_cod = sprav.getPrevCode()
    GetObject = evalSpace['GetObject']
    # Внесено изменение
    global is_changed
    is_changed = False
    grid = GetInterface('spravGrid').get_grid()
    tab = grid.GetTable().GetDataset().data
    tab = sprav.getStorage().setTypeLevelTable(tab)
    sprav.getStorage().setLevelTable(old_cod, tab)
    # Перегрузить дерево справочника
    sprav_tree = sprav.getStorage().getLevelTree()
    GetObject('spravTree').LoadTree(sprav_tree)


def onMouseClickFindTool2(evalSpace):
    """
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    GetInterface = evalSpace['GetInterface']
    GetObject = evalSpace['GetObject']
    
    grid = GetInterface('spravGrid').get_grid()
    find_str = GetObject('findEdit').GetValue()
    cur_cursor = grid.GetGridCursorRow()
    i_row, field = grid.GetDataset().FindRowString(find_str,
                                                   cursor=cur_cursor,
                                                   fields=['name'])
    if i_row >= 0:
        grid.SetCursor(i_row, 1)


def _onInitSpravTree2(evalSpace):
    """
    Обработчик события инициализации дерева справочника.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    sprav = evalSpace['OBJ']
    GetObject = evalSpace['GetObject']
    GetInterface = evalSpace['GetInterface']
    
    sprav_tree = sprav.getStorage().getLevelTree()
    GetObject('spravTree').LoadTree(sprav_tree)
    # Получить таблицу
    level_tab_tuple = sprav.getStorage().getLevelTable(None)
    level_tab = [list(rec) for rec in level_tab_tuple]
    if level_tab is not None:
        grid = GetInterface('spravGrid').get_grid()
        grid.GetDataset().SetDataBuff(level_tab)
        #
        len_cod = sprav.getLevelByIdx(0).getCodLen()
        grid.GetDataset().SetStructFilter({'cod': [len_cod]})


def _RefreshSpravGrid(evalSpace, *arg, **kwarg):
    GetInterface = evalSpace['GetInterface']
    grid = GetInterface('spravGrid').get_grid()
    grid.RefreshGrid()


def onInitSpravTree(context):
    from ic.utils import delayedres
    pr = delayedres.DelayedFunction(_onInitSpravTree, _RefreshSpravGrid,
                                    context, False)
    pr.start()


_onInitSpravTree = onInitSpravTree


def onSelectChangedSpravTree2(evalSpace):
    """
    Обработчик смены элемента дерева справочника.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    sprav = evalSpace['OBJ']
    GetObject = evalSpace['GetObject']
    GetInterface = evalSpace['GetInterface']

    # Внесено изменение
    global is_changed
    if is_changed:
        if ic_dlg.icAskDlg(u'ВНИМАНИЕ!',
                           u'В справочник были внесены изменения. Сохранить?') == wx.YES:
            is_changed = False
            onMouseClickSaveTool2(evalSpace)
    
    # Выбранный код
    try:
        cod = GetObject('spravTree').getSelectionRecord()[0]
    except:
        cod = ''
    sprav.setCurCode(cod)

    # Сохранение внесенных изменений
    old_cod = cod
    level = sprav.getLevelByCod(cod)
    grid = GetInterface('spravGrid').get_grid()

    # Получить таблицу
    level_tab = [list(rec) for rec in sprav.getStorage().getLevelTable(cod)]
    if level_tab is not None:
        grid.GetDataset().SetDataBuff(level_tab)
        # Определение длины кода
        if level and cod:
            level_next = level.getNext()
            if level_next:
                len_cod = level_next.getCodLen()
            else:
                len_cod = -1
        else:
            len_cod = sprav.getLevelByIdx(0).getCodLen()
        if len_cod >= 0:
            grid.GetDataset().SetStructFilter({'cod': [cod, len_cod]})
        grid.RefreshGrid()

    # Поменять надписи колонок
    if level:
        GetObject('spravTree').setLabelCols(level.labelsNotice())
        grid.setColLabels(level.getNoticeDict())
        is_next_level = level.isNext() or GetObject('spravTree').isRootSelected()
        GetObject('spravToolBar').enableTool('addTool', is_next_level)
        GetObject('spravToolBar').enableTool('delTool', is_next_level)
        GetObject('spravToolBar').enableTool('saveTool', is_next_level)
        
    return old_cod


def onCodHlpSprav(evalSpace):
    """
    Вызов заполнения кода из справочнка по F1.
    """
    # Вытащить глобальные переменные из пространства имен,
    # иначе они не попадут в локальное пространство имен
    sprav = evalSpace['OBJ']
    GetObject = evalSpace['GetObject']
    self = evalSpace['self']
    
    # Вызываем форму выбора для связанных справочников
    try:
        cod = GetObject('spravTree').getSelectionRecord()[0]
    except:
        cod = ''

    ref_sprav = sprav.getLevelRefSpravByCod(cod)
    if ref_sprav:
        return ref_sprav.Hlp(field={'name': 'name', 'cod': 'cod'},
                             parentForm=self.GetView())


def onChangedGrid2(evalSpace):
    """
    Произошли изменения в гриде.
    """
    global is_changed
    is_changed = True
    return coderror.IC_CTRL_OK


def onTreeKeyDown(obj, evt):
    """
    Обработка нажатия клавиши в дереве.
    """
    GetObject = obj.GetContext()['GetObject']
    key = evt.GetKeyCode()
    if key == wx.WXK_ESCAPE:
        obj.GetContext()['result'] = None
        GetObject('SpravEditDlg').EndModal(wx.ID_CANCEL)
        return True
    evt.Skip()
    return False


def onGridKeyDown(obj, evt):
    """
    Обработка нажатия клавиши на гриде.
    """
    GetObject = obj.GetContext()['GetObject']
    key = evt.GetKeyCode()
    if key == wx.WXK_ESCAPE:
        obj.GetContext()['result'] = None
        GetObject('SpravEditDlg').EndModal(wx.ID_CANCEL)
        return True
    return True


def onDlgKeyDown(obj, evt):
    """
    Обработка нажатия клавиши в диалоговом окне.
    """
    return onTreeKeyDown(obj, evt)
