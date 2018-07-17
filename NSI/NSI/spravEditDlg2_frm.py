#!/usr/bin/env python
# -*- coding: utf-8 -*-
print('import',__file__)
"""
Модуль ресурса <C:/defis/NSI/NSI/spravEditDlg2.frm>.
"""
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

#   Версия модуля
__version__ = (0,0,0,1)

import wx
from ic.dlg import ic_dlg
from ic.log import ic_log
from ic.utils import coderror
import wx.lib.delayedresult as delayedresult
from NSI.spravEditDlg_frm import *

#--- Общие переменные ---
#Признак изменения справочника
is_changed=False

#--- Функции-обработчики событий ---
def onMouseClickAddTool2(evalSpace):
    """Обработчик щелчка на кнопке панели инструментов addTool."""
    #onMouseClickAddTool.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    #sprav=evalSpace['sprav']
    #old_cod=evalSpace['old_cod']
    sprav=evalSpace['OBJ']
    old_cod=sprav.getPrevCode()
    GetInterface=evalSpace['GetInterface']

    if old_cod==None:
        old_cod=''

    if old_cod:
        level=sprav.getLevelByCod(old_cod).getNext()
    else:
        level=sprav.getLevelByCod(old_cod)

    new_cod=old_cod
    grid = GetInterface('spravGrid').get_grid()
    if level:
        grid.GetDataset().SetStructFilter({'cod':[new_cod,level.getCodLen()]})
    grid.AddRows()
    
    #Внесено изменение
    global is_changed
    is_changed=True
    return old_cod
    
def onCodControl2(evalSpace):
    """Контроль кода."""
    #onCodControl.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    old_value=evalSpace['old_value']
    value=evalSpace['value']
    #sprav=evalSpace['sprav']
    sprav=evalSpace['OBJ']
    GetInterface=evalSpace['GetInterface']
    GetObject=evalSpace['GetObject']

    #Проверка уникальности кода
    try:
        new_cod=GetObject('spravTree').getSelectionRecord()[0]
    except:
        new_cod=None

    #Проверка, есть ли подкоды
    if old_value and sprav.isSubCodes(old_value):
        ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Нельзя изменять значение кода. Есть подкоды.')
        return (3,None)

    buff_codes=map(lambda rec: rec[0],
        GetInterface('spravGrid').get_grid().GetDataset().data)[:-1]

    ctrl_ret=coderror.IC_CTRL_OK
    if value in buff_codes:
        ctrl_ret=coderror.IC_CTRL_FAILED_IGNORE

    if not ctrl_ret in [coderror.IC_CTRL_OK,coderror.IC_CTRL_REPL]:
        ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Такой код есть уже в справочнике!')
        return (ctrl_ret,None)

    # Проверяем по связанному справочнику, если он есть
    if new_cod == None:
        new_cod = ''

    ref_sprav = sprav.getLevelRefSpravByCod(new_cod)
    if ref_sprav:
        return ref_sprav.Ctrl(value, field='cod')
    return (ctrl_ret,None)    
    
def onMouseClickDelTool2(evalSpace):
    """Нажатие кнопки delTool на панели инструментов."""
    #onMouseClickDelTool.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    GetInterface=evalSpace['GetInterface']
    grid = GetInterface('spravGrid').get_grid()
    i_row=grid.GetGridCursorRow()
    grid.DelRows(i_row)
    #Внесено изменение
    global is_changed
    is_changed=True

def onMouseClickSaveTool2(evalSpace):
    """Сохранение внесенных изменений."""
    #onMouseClickSaveTool.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    GetInterface=evalSpace['GetInterface']
    #sprav=evalSpace['sprav']
    #old_cod=evalSpace['old_cod']
    sprav=evalSpace['OBJ']
    old_cod=sprav.getPrevCode()
    GetObject=evalSpace['GetObject']
    #Внесено изменение
    global is_changed
    is_changed=False
    grid = GetInterface('spravGrid').get_grid()
    tab=grid.GetTable().GetDataset().data
    tab=sprav.getStorage().setTypeLevelTable(tab)
    sprav.getStorage().setLevelTable(old_cod,tab)
    #Перегрузить дерево справочника
    sprav_tree=sprav.getStorage().getLevelTree()
    GetObject('spravTree').LoadTree(sprav_tree)
    
def onMouseClickFindTool2(evalSpace):
    """
    """
    #onMouseClickFindTool.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    GetInterface=evalSpace['GetInterface']
    GetObject=evalSpace['GetObject']
    
    grid = GetInterface('spravGrid').get_grid()
    find_str=GetObject('findEdit').GetValue()
    cur_cursor=grid.GetGridCursorRow()
    i_row,field=grid.GetDataset().FindRowString(find_str,
        cursor=cur_cursor,fields=['name'])
    if i_row>=0:
        grid.SetCursor(i_row,1)
        
def _onInitSpravTree2(evalSpace):
    """Обработчик события инициализации дерева справочника."""
    #onInitSpravTree.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    #sprav=evalSpace['sprav']
    sprav=evalSpace['OBJ']
    GetObject=evalSpace['GetObject']
    GetInterface=evalSpace['GetInterface']
    
    sprav_tree=sprav.getStorage().getLevelTree()
    GetObject('spravTree').LoadTree(sprav_tree)
    #Получить таблицу
    level_tab_tuple=sprav.getStorage().getLevelTable(None)
    level_tab=[list(rec) for rec in level_tab_tuple]
    if level_tab is not None:
        grid=GetInterface('spravGrid').get_grid()
        grid.GetDataset().SetDataBuff(level_tab)
        #
        len_cod=sprav.getLevelByIdx(0).getCodLen()
        grid.GetDataset().SetStructFilter({'cod':[len_cod]})
        #grid.RefreshGrid()
        
def _RefreshSpravGrid(evalSpace, *arg, **kwarg):
    GetInterface=evalSpace['GetInterface']
    grid=GetInterface('spravGrid').get_grid()
    grid.RefreshGrid()
    
_onInitSpravTree = onInitSpravTree
def onInitSpravTree(context):
    from ic.utils import delayedres
    #return
    print('******** OOOOOOOO ********')
    pr = delayedres.DelayedFunction(_onInitSpravTree, _RefreshSpravGrid, 
                                    context, False)
    pr.start()
    
def onSelectChangedSpravTree2(evalSpace):
    """Обработчик смены элемента дерева справочника."""
    #onSelectChangedSpravTree.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    #sprav=evalSpace['sprav']
    sprav=evalSpace['OBJ']
    GetObject=evalSpace['GetObject']
    GetInterface=evalSpace['GetInterface']
    #old_cod=evalSpace['old_cod']
    old_cod=sprav.getPrevCode()

    #Внесено изменение
    global is_changed
    if is_changed:
        if ic_dlg.icAskDlg(u'ВНИМАНИЕ!',
            u'В справочник были внесены изменения. Сохранить?')==wx.YES:
            is_changed=False
            onMouseClickSaveTool(evalSpace)
    
    #Выбранный код
    try:
        cod=GetObject('spravTree').getSelectionRecord()[0]
    except:
        cod=''    
    sprav.setCurCode(cod)

    #Сохранение внесенных изменений
    #print '!!!1',old_cod,cod,sprav.getLevelByCod(cod)
    #if old_cod<>cod:
    #    tab=GetObject('spravGrid').GetTable().GetDataset().data
    #    print '!!!',old_cod,tab
    #    sprav.getStorage().setLevelTable(old_cod,tab)
    #    #Перегрузить дерево справочника
    #    sprav_tree=sprav.getStorage().getLevelTree()
    #    GetObject('spravTree'].LoadTree(sprav_tree)

    #sprav.getStorage().setLevelTable(old_cod,
    #    GetObject('spravGrid'].GetTable().GetDataset().data)
    old_cod=cod
    level=sprav.getLevelByCod(cod)
    grid = GetInterface('spravGrid').get_grid()

    #Получить таблицу
    level_tab=[list(rec) for rec in sprav.getStorage().getLevelTable(cod)]
    if level_tab is not None:
        grid.GetDataset().SetDataBuff(level_tab)
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
            print('$$$',len_cod,cod)
            grid.GetDataset().SetStructFilter({'cod':[cod,len_cod]})
        grid.RefreshGrid()

    #Поменять надписи колонок
    if level:
        GetObject('spravTree').setLabelCols(level.labelsNotice())
        grid.setColLabels(level.getNoticeDict())
        is_next_level=level.isNext() or GetObject('spravTree').isRootSelected()
        GetObject('spravToolBar').enableTool('addTool',is_next_level)
        GetObject('spravToolBar').enableTool('delTool',is_next_level)
        GetObject('spravToolBar').enableTool('saveTool',is_next_level)    
        
    return old_cod
    
def onCodHlpSprav(evalSpace):
    """Вызов заполнения кода из справочнка по F1."""
    #onCodHlpSprav.func_globals['__builtins__']['locals']().update(evalSpace)
    #Вытащить глобальные переменные из пространства имен, 
    #иначе они не попадут в локальное пространство имен
    #sprav=evalSpace['sprav']
    sprav=evalSpace['OBJ']
    GetObject=evalSpace['GetObject']
    self=evalSpace['self']
    
    # Вызываем форму выбора для связанных справочников
    try:
        cod=GetObject('spravTree').getSelectionRecord()[0]
    except:
        cod=''

    ref_sprav = sprav.getLevelRefSpravByCod(cod)
    if ref_sprav:
        return ref_sprav.Hlp(field={'name':'name','cod':'cod'}, parentForm=self.GetView())

def onChangedGrid2(evalSpace):
    """Произошли изменения в гриде."""
    #onChangedGrid.func_globals['__builtins__']['locals']().update(evalSpace)
    global is_changed
    is_changed=True
    return coderror.IC_CTRL_OK
    
def onTreeKeyDown(obj, evt):
    """Обработка нажатия клавиши в дереве."""
    GetObject=obj.GetContext()['GetObject']
    key=evt.GetKeyCode()
    if key==wx.WXK_ESCAPE:
        obj.GetContext()['result']=None
        GetObject('SpravEditDlg').EndModal(wx.ID_CANCEL)
        return True
    evt.Skip()
    return False

def onGridKeyDown(obj, evt):
    """Обработка нажатия клавиши на гриде."""
    GetObject=obj.GetContext()['GetObject']
    key=evt.GetKeyCode()
    if key==wx.WXK_ESCAPE:
        obj.GetContext()['result']=None
        GetObject('SpravEditDlg').EndModal(wx.ID_CANCEL)
        return True
    #evt.Skip()
    return True
    
def onDlgKeyDown(obj, evt):
    """Обработка нажатия клавиши в диалоговом окне."""
    return onTreeKeyDown(obj, evt)