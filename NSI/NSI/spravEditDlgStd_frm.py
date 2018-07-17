#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module <C:/defis/NSI/NSI/spravEditDlgStd.frm>.
"""

### RESOURCE_MODULE: C:/defis/NSI/NSI/spravEditDlgStd.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/spravEditDlgStd_frm.py
# Purpose:     Resource module.
#
# Author:      <...>
#
# Created:
# RCS-ID:      $Id: $
# Copyright:   (c)
# Licence:     <your licence>
# -----------------------------------------------------------------------------
### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 2)

import wx
from ic.dlg import ic_dlg
from ic.log import ic_log
from ic.utils import coderror
from ic.db import icsimpledataset
from ic.kernel import io_prnt

# --- Общие переменные ---
# Признак изменения справочника
DLG_NAME = 'spravEditDlgStd'
SPR_TREE_NAME = 'spravTree'
SPR_GRID_NAME = 'spravGrid'
CONTEXT_SPRAV_NAME = 'OBJ'

# --- Функции-обработчики событий ---
def dialogTitle(obj):
    """
    Установить заголовок окна диалога.
    """
    evalSpace=obj.GetContext()
    sprav=evalSpace[CONTEXT_SPRAV_NAME]
    return u'Редактирование справочника: '+sprav.description if sprav.description else u''


def onMouseClickAddTool(obj):
    """ 
    Обработчик щелчка на кнопке панели инструментов addTool.
    """
    try:
        print('onMouseClickAddTool START!')
        evalSpace = obj.GetContext()
        sprav = evalSpace[CONTEXT_SPRAV_NAME]
        to_cod = sprav.getCurCode()
        if to_cod is None:
            # Если код не определен, тогда добавляем в корневой
            to_cod = ''

        if to_cod:
            level = sprav.getLevelByCod(to_cod).getNext()
        else:
            level = sprav.getLevelByCod(to_cod)

        grid = evalSpace.GetObject(SPR_GRID_NAME)
        if level:
            grid.GetDataset().SetStructFilter({'cod':[to_cod,level.getCodLen()]})

        grid.AddRows()
        return to_cod
    except:
        ic_log.icLogErr(u'Ошибка обработчика щелчка на кнопке панели инструментов addTool.')


def onCodControl(obj):
    """ 
    Контроль кода.
    """
    try:
        evalSpace = obj.GetView().context
        sprav = evalSpace[CONTEXT_SPRAV_NAME]
        value = evalSpace['value']
        #Проверка уникальности кода
        try:
            new_cod = evalSpace.GetObject(SPR_TREE_NAME).getSelectionRecord()[0]
        except:
            new_cod = None

        grid = evalSpace.GetObject(SPR_GRID_NAME)
        dataset = grid.GetDataset()
        prev_change_code = grid.getNameValue('cod')
        # Проверка, есть ли подкоды
        if prev_change_code and sprav.isSubCodes(prev_change_code):
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Нельзя изменять значение кода <%s>. Есть подкоды.' % prev_change_code,
                            evalSpace.GetObject(SPR_TREE_NAME))
            return coderror.IC_CTRL_FAILED_IGNORE, None

        buff_codes = [rec['cod'] for rec in dataset.getDataDict()]
        ctrl_ret = coderror.IC_CTRL_OK
        if value in buff_codes:
            ctrl_ret = coderror.IC_CTRL_FAILED_IGNORE

        if not ctrl_ret in [coderror.IC_CTRL_OK,coderror.IC_CTRL_REPL]:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Код <%s> есть уже в справочнике!' % value)
            return ctrl_ret, None

        # Проверяем по связанному справочнику, если он есть
        if new_cod is None:
            new_cod = ''

        ref_sprav = sprav.getLevelRefSpravByCod(new_cod)
        if ref_sprav:
            val = value[len(new_cod):]
            ref_cod = ''.join(_get_refspr_parent_cod(sprav, new_cod))
            crtl_ret = ref_sprav.Ctrl(ref_cod+val, field='cod', cod=ref_cod)
            return crtl_ret
        return ctrl_ret, None
    except:
        io_prnt.outErr(u'Code control Error!')
        return coderror.IC_CTRL_FAILED_IGNORE, None


def _get_refspr_parent_cod(sprav, cod):
    ref_sprav = sprav.getLevelRefSpravByCod(cod)
    lev = sprav.getLevelByCod(cod).getNext()
    cod_lst = sprav.StrCode2ListCode(cod)
    # определяем часть кода, которая относится к связанному справочнику
    rl = lev.getRefLevel()+1
    ix = lev.getIndex()+1
    beg = ix - rl
    old = cod_lst
    cod_lst = [el for el in cod_lst[beg:ix] if el]
    return cod_lst


def onCodHlpSprav(evalSpace):
    """
    Вызов заполнения кода из справочнка по F1.
    """
    sprav = evalSpace[CONTEXT_SPRAV_NAME]
    GetObject = evalSpace['GetObject']
    self = evalSpace['self']
    # Вызываем форму выбора для связанных справочников
    try:
        cod = GetObject(SPR_TREE_NAME).getSelectionRecord()[0]
    except:
        cod = ''
    sprav.setCurCode(cod)
    ref_sprav = sprav.getLevelRefSpravByCod(cod)
    if ref_sprav:
        cod_lst = _get_refspr_parent_cod(sprav, cod)
        prnt_cod = ''.join(cod_lst)
        res, new_cod, flds = ref_sprav.Hlp(ParentCode=cod_lst+[None], field={'name': 'name'}, parentForm=self.GetView())
        # Выделяем у кода внедренную часть
        if prnt_cod:
            pcod = cod[:-len(prnt_cod)]
        else:
            pcod = cod
        return res, pcod+new_cod, flds


def onMouseClickDelTool(obj):
    """ 
    Нажатие кнопки delTool на панели инструментов.
    """
    try:
        evalSpace = obj.GetContext()
        grid = evalSpace.GetObject(SPR_GRID_NAME)
        i_row = grid.GetGridCursorRow()
        grid.DelRows(i_row)
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки delTool на панели инструментов.')


def onMouseClickSaveTool(obj):
    """ 
    Сохранение внесенных изменений.
    """
    try:
        evalSpace = obj.GetContext()
        sprav = evalSpace[CONTEXT_SPRAV_NAME]
        cur_cod = sprav.getCurCode()
        grid = evalSpace.GetObject(SPR_GRID_NAME)
        tab = grid.GetTable().GetDataset().data
        tab = sprav.getStorage().setTypeLevelTable(tab)
        buff = grid.GetTable().GetDataset().allChangeBuff
        _tab = sprav.getStorage()._tab
        sprav.getStorage().setLevelTable(cur_cod, tab, change_buff=buff)
        grid.GetDataset().set_change_prz(False)
        # Перегрузить дерево справочника
        sprav_tree = sprav.getStorage().getLevelTree()
        evalSpace.GetObject(SPR_TREE_NAME).LoadTree(sprav_tree)
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки сохрания изменения справочника.')


def _onMouseClickFindTool(obj):
    try:
        evalSpace = obj.GetContext()
        grid = evalSpace.GetObject(SPR_GRID_NAME)
        find_str = evalSpace.GetObject('findEdit').GetValue()
        cur_cursor = grid.GetGridCursorRow()
        i_row,field = grid.GetDataset().FindRowString(find_str,
                                                      cursor = cur_cursor,
                                                      fields=['name'])
        if i_row >= 0:
            grid.SetCursor(i_row, 1)
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки поиска в справочнике.')


def onMouseClickFindTool(obj):
    try:
        evalSpace = obj.GetContext()
        tree = evalSpace.GetObject(SPR_TREE_NAME)
        find_str = evalSpace.GetObject('findEdit').GetValue()
        if find_str.strip():
            tree.selectFindItem(find_str)
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки поиска в справочнике.')


def onKeyDownFindEdit(obj,event):
    try:
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            evalSpace = obj.GetContext()
            tree = evalSpace.GetObject(SPR_TREE_NAME)
            find_str = obj.GetValue()
            if find_str.strip():
                tree.selectFindItem(find_str)
        event.Skip()
    except:
        ic_log.icLogErr(u'Ошибка обработчика нажатия клавиши в поле поиска строки в справочнике.')


def _onInitSpravTree(obj, bRefresh=True):
    """ 
    Обработчик события инициализации дерева справочника.
    """
    try:
        evalSpace = obj.GetContext()
        sprav = evalSpace[CONTEXT_SPRAV_NAME]
        _tab = sprav.getStorage()._tab

        tree = evalSpace.GetObject(SPR_TREE_NAME)
        tree.GetParent().Freeze()
        tree.begin_load()
        sprav_tree = sprav.getStorage().getLevelTree()
        tree.LoadTree(sprav_tree)
        tree.GetParent().Thaw()
        # Получить таблицу
        level_tab_tuple = sprav.getStorage().getLevelTable(None)
        level_tab = [list(rec) for rec in level_tab_tuple]
        if level_tab is not None:
            grid = evalSpace.GetObject(SPR_GRID_NAME)
            # Устанвливаем буфер изменений, [0] - задает список индексных колонок
            buff = icsimpledataset.CChangeBuff([0])
            grid.GetDataset().set_change_buff(buff)
            dataset = grid.GetDataset()
            if dataset:
                dataset.SetDataBuff(level_tab)
            #
            len_cod = sprav.getLevelByIdx(0).getCodLen()
            grid.GetDataset().SetStructFilter({'cod': [len_cod]})
            if bRefresh:
                grid.RefreshGrid()
    except:
        ic_log.icLogErr(u'Ошибка инициализации дерева справочника.')


def onSelectChangedSpravTree(obj):
    """ 
    Обработчик смены элемента дерева справочника.
    """
    try:
        evalSpace = context = obj.GetContext()
        sprav = context[CONTEXT_SPRAV_NAME]
        old_cod = sprav.getPrevCode()
        grid = context.GetObject(SPR_GRID_NAME)
        grid.ClearSortPrz()
        # Внесено изменение
        if grid.GetDataset().isChanged():
            if ic_dlg.icAskDlg(u'ВНИМАНИЕ!',
                               u'В справочник были внесены изменения. Сохранить?')==wx.YES:
                onMouseClickSaveTool(obj)
            else:
                # Если отказались от изменений, то сбросить флаг изменения
                grid.GetDataset().set_change_prz(False)

        # Сбрасываем признак изменения таблицы
        # Выбранный код
        try:
            cod = context.GetObject(SPR_TREE_NAME).getSelectionRecord()[0]
        except:
            cod = ''
        sprav.setCurCode(cod)

        # Сохранение внесенных изменений
        old_cod = cod
        level = sprav.getLevelByCod(cod)

        # Получить таблицу
        level_tab = [list(rec) for rec in sprav.getStorage().getLevelTable(cod)]
        if level_tab is not None:
            dataset = grid.GetDataset()
            if dataset:
                dataset.SetDataBuff(level_tab)
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
                if dataset:
                    dataset.SetStructFilter({'cod': [cod, len_cod]})
            grid.RefreshGrid()

        # Поменять надписи колонок
        if level:
            context.GetObject(SPR_TREE_NAME).setLabelCols(level.labelsNotice())
            is_next_level = level.isNext() or context.GetObject(SPR_TREE_NAME).isRootSelected()
            context.GetObject('spravToolBar').enableTool('addTool', is_next_level)
            context.GetObject('spravToolBar').enableTool('delTool', is_next_level)
            context.GetObject('spravToolBar').enableTool('saveTool', is_next_level)
            if is_next_level:
                grid.Enable(True)
                if cod:
                    grid.setColLabels(level.getNext().getNoticeDict())
                else:
                    grid.setColLabels(level.getNoticeDict())
                print('**** level:', level._index, cod)
            else:
                grid.Enable(False)

        return old_cod
    except:
        ic_log.icLogErr(u'Ошибка обработчика смены элемента дерева справочника.')
        return None


def onChangedGrid(obj):
    """ 
    Произошли изменения в гриде.
    """
    obj.GetContext().GetObject(SPR_GRID_NAME).GetDataset().set_change_prz(True)
    return coderror.IC_CTRL_OK


def spravToolBar_init_expr(obj):
    obj.SetPosition((3, 2))
    bgr = obj.GetParent().GetBackgroundColour()
    obj.SetBackgroundColour(bgr)


def _RefreshSpravGrid(obj, *arg, **kwarg):
    evalSpace = obj.GetContext()
    grid = evalSpace.GetObject(SPR_GRID_NAME)
    grid.RefreshGrid()


def onInitSpravTree(obj):
    return _onInitSpravTree(obj)
    from ic.utils import delayedres
    pr = delayedres.DelayedFunction(_onInitSpravTree, _RefreshSpravGrid,
                                    obj, False)
    pr.start()


def onMouseClickOK(obj):
    """ 
    Кнопка <ОК>.
    """
    obj.EndModal(wx.ID_OK)
    return True


def onMouseClickCancel(obj):
    """ 
    Кнопка <Отмена>.
    """
    obj.EndModal(wx.ID_OK)
    return None


def spravEditDlgStd_title(obj):
    spr = obj.GetContext()[CONTEXT_SPRAV_NAME]
    if spr.description:
        return u'Редактирование справочника: %s' % spr.description
    else:
        return u''
