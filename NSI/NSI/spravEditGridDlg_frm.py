#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/spravEditGridDlg.frm>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/spravEditGridDlg.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/spravEditGridDlg_frm.py
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
__version__ = (0,0,0,1)
from ic.kernel import io_prnt
import wx
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.db import icsimpledataset
from sqlalchemy.sql import and_, or_, not_, select
from NSI.nsi_sys import icsprav_search
import time
import wx.grid as gridlib

HLP_DLG_NAME = 'spravEditGridDlg'
SPR_TREE_NAME = 'spravTable'
SPR_GRID_NAME = 'spravGrid'
CONTEXT_SPRAV_NAME = 'OBJ'
SPR_LABEL_NAME = 'sprLevNames'
PREV_LEVEL_COD = '...'

def spravToolBar_init_expr(obj):
#    return
    obj.SetPosition((3,2))
    bgr = obj.GetParent().GetBackgroundColour()
    obj.SetBackgroundColour(bgr)

def spravTable_onInit(obj, evt):
    try:
        grid=obj.GetContext().GetObject(SPR_TREE_NAME)
        sprav=obj.GetContext()[CONTEXT_SPRAV_NAME]
#        grid.SetSelectionMode(grid.wxGridSelectRows)
        grid.set_sprav(sprav)
        #Получить таблицу
        cod = ''
        level_tab = [('', sprav.description, '', '', '')]
        grid.SetDataset(level_tab, cod=cod)
    except:
        io_prnt.outErr(u'Ошибка инициализации таблицы справочника.')

def spravTable_keyDown(obj, evt):
    key = evt.GetKeyCode()
    if key == wx.WXK_RETURN:
        obj.select_cod()

def spravTable_cellDClick(obj, evt):
    obj.select_cod()

def onMouseClickAddTool(obj):
    """ Обработчик щелчка на кнопке панели инструментов addTool."""
    try:
        evalSpace = obj.GetContext()
        sprav=evalSpace[CONTEXT_SPRAV_NAME]
        to_cod=sprav.getCurCode()
        if to_cod is None:
            #Если код не определен, тогда добавляем в корневой
            to_cod=''

        if to_cod:
            level=sprav.getLevelByCod(to_cod).getNext()
        else:
            level=sprav.getLevelByCod(to_cod)

        grid=evalSpace.GetObject(SPR_GRID_NAME)
        if level:
            grid.GetDataset().SetStructFilter({'cod':[to_cod,level.getCodLen()]})

        grid.AddRows()
        return to_cod
    except:
        io_prnt.outErr(u'Ошибка обработчика щелчка на кнопке панели инструментов addTool.')

def onCodControl(evalSpace):
    """ Контроль кода."""
    try:
        #Вытащить глобальные переменные из пространства имен,
        #иначе они не попадут в локальное пространство имен
        sprav=evalSpace[CONTEXT_SPRAV_NAME]
        value=evalSpace['value']
        tree_grid = evalSpace.GetObject(SPR_TREE_NAME)
        #Проверка уникальности кода
        new_cod = tree_grid.get_sel_cod()
        grid=evalSpace.GetObject(SPR_GRID_NAME)
        dataset=grid.GetDataset()
        prev_change_code=dataset.getNameValue('cod')
        #Проверка, есть ли подкоды
        print('***** ver prev_change_code:', value, prev_change_code, dataset.cursor)
        if prev_change_code and sprav.isSubCodes(prev_change_code):
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                u'Нельзя изменять значение кода %s. Есть подкоды.' % prev_change_code,
                evalSpace.GetObject(SPR_TREE_NAME))
            return (coderror.IC_CTRL_FAILED_IGNORE,None)

        buff_codes=[rec['cod'] for rec in dataset.getDataDict()]
        ctrl_ret=coderror.IC_CTRL_OK
        if value in buff_codes:
            ctrl_ret=coderror.IC_CTRL_FAILED_IGNORE

        if not ctrl_ret in [coderror.IC_CTRL_OK,coderror.IC_CTRL_REPL]:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Код %s есть уже в справочнике!'%value)
            return (ctrl_ret,None)

        # Проверяем по связанному справочнику, если он есть
        if new_cod is None:
            new_cod = ''

        ref_sprav = sprav.getLevelRefSpravByCod(new_cod)
        if ref_sprav:
#            val = value[len(new_cod):]
#            crtl_ret = ref_sprav.Ctrl(val, field='cod')
#            print '****** CTRL VAL$$:', value, new_cod, val, ctrl_ret
            val = value[len(new_cod):]
            ref_cod = ''.join(sprav._get_refspr_parent_cod(new_cod))
            crtl_ret = ref_sprav.Ctrl(ref_cod+val, field='cod', cod=ref_cod)

            return crtl_ret

        return (ctrl_ret,None)
    except:
        io_prnt.outErr(u'Ошибка контроля кода справочника.')
        return (coderror.IC_CTRL_FAILED_IGNORE,None)

def onCodHlpSprav(evalSpace):
    """Вызов заполнения кода из справочнка по F1."""
    sprav=evalSpace[CONTEXT_SPRAV_NAME]
#    GetObject=evalSpace['GetObject']
    self=evalSpace['self']
    # Вызываем форму выбора для связанных справочников
    tree_grid = evalSpace.GetObject(SPR_TREE_NAME)
    cod = tree_grid.get_sel_cod()
    sprav.setCurCode(cod)
    ref_sprav = sprav.getLevelRefSpravByCod(cod)
    if ref_sprav:
#        res, new_cod, flds = ref_sprav.Hlp(field={'name':'name'}, parentForm=self.GetView())
#        print '*** RESULT:', (res, cod+new_cod, flds)
        cod_lst = sprav._get_refspr_parent_cod(cod)
        print(' **** _get_refspr_parent_cod(cod)=', cod, cod_lst)
        prnt_cod = ''.join(cod_lst)
        res, new_cod, flds = ref_sprav.Hlp(ParentCode=cod_lst+[None], field={'name':'name'}, parentForm=self.GetView())
        # Выделяем у кода внедренную часть
        if prnt_cod:
            pcod = cod[:-len(prnt_cod)]
        else:
            pcod = cod

        #return (res, cod+new_cod, flds)
        return (res, pcod+new_cod, flds)

def onMouseClickDelTool(obj):
    """ Нажатие кнопки delTool на панели инструментов."""
    try:
        #evalSpace = obj.GetContext()
        grid=obj.GetContext().GetObject(SPR_GRID_NAME)
        i_row=grid.GetGridCursorRow()
        grid.DelRows(i_row)
        #Внесено изменение
    except:
        io_prnt.outErr(u'Ошибка обработчика кнопки delTool на панели инструментов.')

def onMouseClickSaveTool(obj):
    """ Сохранение внесенных изменений."""
    try:
        context = obj.GetContext()
        sprav=context.GetObject(SPR_TREE_NAME).get_sprav()
        cur_cod=sprav.getCurCode()
        #Внесено изменение
        grid=context.GetObject(SPR_GRID_NAME)
        tab=grid.GetTable().GetDataset().data
        tab=sprav.getStorage().setTypeLevelTable(tab)
        buff=grid.GetTable().GetDataset().allChangeBuff
        sprav.getStorage().setLevelTable(cur_cod,tab, change_buff=buff)
        grid.GetDataset().set_change_prz(False)
    except:
        io_prnt.outErr(u'Ошибка обработчика кнопки сохрания изменения справочника.')

buff_find_str = None
def _find(obj):
    """ Поиск подстроки."""
    global buff_find_str
    context = obj.GetContext()
    grid=context.GetObject(SPR_GRID_NAME)
    tree_grid = context.GetObject(SPR_TREE_NAME)
    sprav=context.GetObject(SPR_TREE_NAME).get_sprav()
    find_str=context.GetObject('findEdit').GetValue().strip()
    cur_cursor=grid.GetGridCursorRow()
    old_cod=tree_grid.get_cur_cod()#sprav.getPrevCode()

    if not find_str:
        return

    if not buff_find_str or buff_find_str.find_str != find_str or buff_find_str.isEOF():
        io_prnt.outLog(u'  ... find string: %s' % find_str)
        tab = sprav.getStorage().getSpravTabClass()
        tabcls = sprav.getStorage().getSpravTabClass().dataclass
        conn = sprav.getStorage().getSpravTabClass().getConnection()
        typ = sprav.getType()

        # Если измениласть строка поиска
        if old_cod:
            fq = tabcls.c.type.like(typ) & tabcls.c.cod.like(old_cod+u'%') & tabcls.c.name.ilike(u'%' + find_str+u'%')
        else:
            fq = tabcls.c.type.like(typ) & tabcls.c.name.ilike(u'%' +find_str+u'%')

        print('   ... cod=%s query:%s' % (old_cod, fq))
        s = select([tabcls], fq)
        print('   ... select:', typ, s)
        res = conn.execute(s)
        #rec = res.fetchone()
        #print dir(res)

        if not buff_find_str:
            idx = res.keys.index('cod')
            buff_find_str = icsprav_search.sparv_search(find_str, res, cod_indx=idx)
        else:
            buff_find_str.set_data(find_str, res)
        print('   ... res:', res, buff_find_str.searchResult)

    if buff_find_str:
        rec = buff_find_str.next()
        if rec:
            fcod = rec[buff_find_str.cod_indx]
            if type(fcod) != unicode:
                fcod = unicode(fcod, 'utf-8')

            prnt_cod = sprav.getParentLevelCod(fcod)
            tree_grid.select_cod(prnt_cod, sel_cod=fcod)
            #print '.... select cod:', prnt_cod, fcod, len(prnt_cod), len(fcod), type(fcod)
            tree_grid.cod_name_lst = []

        elif buff_find_str.cursor == -1:
            wx.MessageBox(u'Подстрока "%s" в справочнике не найдена.' % find_str)
        else:
            wx.MessageBox(u'Вхождений подстроки "%s" больше не найдено.' % find_str)

def onMouseClickFindTool(obj):
    """ Обработка нажатия кнопки поиск."""
    try:
        return _find(obj)
    except:
        io_prnt.outErr(u'Ошибка обработчика конпки поиска в справочнике.')

def spravTable_cellSelect(obj, evt):
    """ Обработчик смены элемента дерева справочника."""
    try:
        evalSpace = context = obj.GetContext()
        tree_grid = context.GetObject(SPR_TREE_NAME)
        sprav=tree_grid.get_sprav()
        old_cod=sprav.getPrevCode()
        grid=context.GetObject(SPR_GRID_NAME)
        grid.ClearSortPrz()
        #Внесено изменение
        if grid.GetDataset().isChanged():
            if ic_dlg.icAskDlg(u'ВНИМАНИЕ!',
                u'В справочник были внесены изменения. Сохранить?')==wx.YES:
                onMouseClickSaveTool(obj)
            else:
                #Если отказались от изменений, то сбросить флаг изменения
                grid.GetDataset().set_change_prz(False)

        # Сбрасываем признак изменения таблицы
        #Выбранный код
        row = evt.GetRow()
        cod=tree_grid.get_sel_cod(row) or ''
        sprav.setCurCode(cod)
        #Сохранение внесенных изменений
        old_cod=cod
        level=sprav.getLevelByCod(cod)

        #Получить таблицу
        if cod == PREV_LEVEL_COD:
            level_tab=[]
        else:
            level_tab=[list(rec) for rec in sprav.getStorage().getLevelTable(cod)]

        if level_tab != None:
            dataset=grid.GetDataset()
            if dataset:
                dataset.SetDataBuff(level_tab)
            #Определение длины кода
            if level and cod:
                level_next=level.getNext()
                if level_next:
                    len_cod=level_next.getCodLen()
                else:
                    len_cod=-1
            else:
                len_cod=sprav.getLevelByIdx(0).getCodLen()
            if len_cod>=0:
                if dataset:
                    dataset.SetStructFilter({'cod':[cod,len_cod]})
                    #print '***** set filter:', {'cod':[cod,len_cod]}
            grid.RefreshGrid()
            grid.SetGridCursor(0,0)
            wx.CallAfter(tree_grid.SetFocus)
            lab = context.GetObject(SPR_LABEL_NAME)
        nms = ' '
        for ind, nm in enumerate(tree_grid.cod_name_lst):
            if ind == 0:
                nms += u' %s' % nm
            else:
                nms += u' -> %s' % nm
        lab.SetLabel(nms)
#            row = tree_grid.GetGridCursorRow()
#            col = tree_grid.GetGridCursorCol()
#            tree_grid.SetGridCursor(row, col)

        #Поменять надписи колонок
        if level:
            context.GetObject(SPR_TREE_NAME).setColLabels(level.labelsNotice())
            is_next_level=(level.isNext() or not cod) and cod != PREV_LEVEL_COD #context.GetObject(SPR_TREE_NAME).isRootSelected()
            context.GetObject('spravToolBar').enableTool('addTool',is_next_level)
            context.GetObject('spravToolBar').enableTool('delTool',is_next_level)
            context.GetObject('spravToolBar').enableTool('saveTool',is_next_level)
            if is_next_level and cod != PREV_LEVEL_COD:
                grid.Enable(True)
                if cod:
                    grid.setColLabels(level.getNext().getNoticeDict())
                else:
                    grid.setColLabels(level.getNoticeDict())
            else:
                grid.Enable(False)

        return old_cod
    except:
        io_prnt.outErr(u'Ошибка обработчика смены элемента дерева справочника.')

def onChangedGrid(obj):
    """ Произошли изменения в гриде."""
    obj.GetContext().GetObject(SPR_GRID_NAME).GetDataset().set_change_prz(True)
    return coderror.IC_CTRL_OK

def spravGrid_onInit(obj, evt):
    # Устанавливаем буфер изменений у датасета
    buff = icsimpledataset.CChangeBuff([0])
    obj.context.GetObject(SPR_GRID_NAME).GetDataset().set_change_buff(buff)

def cancel_button_mouseClick(obj, evt):
    """ Обработка нажатия кнопки <Отмена>."""
    obj.GetContext().GetObject(HLP_DLG_NAME).EndModal(wx.ID_CANCEL)

def ok_button_mouseClick(obj, evt):
    """ Обработка нажатия кнопки <ОК>."""
    obj.GetContext().GetObject(HLP_DLG_NAME).EndModal(wx.ID_OK)

def spravEditGridDlg_onInit(obj, evt):
    # Устанавливаем заголовок окна
    tree_grid = obj.GetContext().GetObject(SPR_TREE_NAME)
    sprav=tree_grid.get_sprav()
    title = u'Редактирование справочника: '+ (sprav.description or u'')
    obj.GetContext().GetObject(HLP_DLG_NAME).SetLabel(title)