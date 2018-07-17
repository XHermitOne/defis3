#!/usr/bin/env python
# -*- coding: utf-8 -*-
print('import',__file__)
"""
Модуль ресурса <C:/defis/NSI/NSI/spravEditDlg.frm>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/spravEditDlg.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/spravEditDlg_frm.py
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

#--- Общие переменные ---
#Признак изменения справочника
is_changed=False

#--- Функции-обработчики событий ---
def onMouseClickAddTool(evalSpace):
    """
    Обработчик щелчка на кнопке панели инструментов addTool.
    """
    try:
        print('onMouseClickAddTool START!!!!!!!!!!!!!!!!!!')
        #print evalSpace.has_key('old_cod')
        #onMouseClickAddTool.func_globals['__builtins__']['locals']().update(evalSpace)
    
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #sprav=evalSpace['sprav']
        #old_cod=evalSpace['old_cod']
        sprav=evalSpace['OBJ']
        old_cod=sprav.getPrevCode()
        
        #GetInterface=evalSpace['GetInterface']

        if old_cod==None:
            old_cod=''

        if old_cod:
            #lev=sprav.getLevelByCod(old_cod)
            level=sprav.getLevelByCod(old_cod).getNext()
        else:
            level=sprav.getLevelByCod(old_cod)

        new_cod=old_cod
        try:
            grid=evalSpace.GetInterface('spravGrid').get_grid()
        except:
            grid=evalSpace.GetObject('spravGrid')
        if level:
            #print '$$$$',level.name,level.getCodLen()
            grid.GetDataset().SetStructFilter({'cod':[new_cod,level.getCodLen()]})
        #    cod_len=level.getCodLen()
        #    new_cod+='*'*cod_len
        grid.AddRows()
        #grid.setNameValue('cod',new_cod)
    
        #Внесено изменение
        global is_changed
        is_changed=True
    
        return old_cod
    except:
        ic_log.icLogErr(u'Ошибка обработчика щелчка на кнопке панели инструментов addTool.')
    
def onCodControl(evalSpace):
    """
    Контроль кода.
    """
    try:
        print('onCodControl START!!!!!!!!!!!!!!!!!!')
    
        #onCodControl.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        old_value=evalSpace['old_value']
        value=evalSpace['value']
        #sprav=evalSpace['sprav']
        sprav=evalSpace['OBJ']
        #GetInterface=evalSpace['GetInterface']
        #GetObject=evalSpace['GetObject']

        #Проверка уникальности кода
        try:
            new_cod=evalSpace.GetObject('spravTree').getSelectionRecord()[0]
        except:
            new_cod=None

        #Проверка, есть ли подкоды
        if old_value and sprav.isSubCodes(old_value):
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Нельзя изменять значение кода. Есть подкоды.')
            return (3,None)

        try:
            grid=evalSpace.GetInterface('spravGrid').get_grid()
        except:
            grid=evalSpace.GetObject('spravGrid')
        buff_codes=map(lambda rec: rec[0],grid.GetDataset().data)[:-1]

        ctrl_ret=coderror.IC_CTRL_OK
        if value in buff_codes:
            ctrl_ret=coderror.IC_CTRL_FAILED_IGNORE

        if not ctrl_ret in [coderror.IC_CTRL_OK,coderror.IC_CTRL_REPL]:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',u'Такой код есть уже в справочнике!')
            return (ctrl_ret,None)

        # Проверяем по связанному справочнику, если он есть
        if new_cod == None:
            new_cod = ''

        #print '*********** NEW_COD=', new_cod
        ref_sprav = sprav.getLevelRefSpravByCod(new_cod)
        if ref_sprav:
            return ref_sprav.Ctrl(value, field='cod')
        return (ctrl_ret,None)    
    except:
        ic_log.icLogErr(u'Ошибка контроля кода справочника.')
        return (coderror.IC_CTRL_FAILED_IGNORE,None)
    
def onMouseClickDelTool(evalSpace):
    """
    Нажатие кнопки delTool на панели инструментов.
    """
    try:
        #onMouseClickDelTool.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #GetInterface=evalSpace['GetInterface']
        #GetObject=evalSpace['GetObject']

        try:
            grid=evalSpace.GetInterface('spravGrid').get_grid()
        except:
            grid=evalSpace.GetObject('spravGrid')
        i_row=grid.GetGridCursorRow()
        grid.DelRows(i_row)
    
        #Внесено изменение
        global is_changed
        is_changed=True
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки delTool на панели инструментов.')

def onMouseClickSaveTool(evalSpace):
    """
    Сохранение внесенных изменений.
    """
    try:
        #onMouseClickSaveTool.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #GetInterface=evalSpace['GetInterface']
        #sprav=evalSpace['sprav']
        #old_cod=evalSpace['old_cod']
        sprav=evalSpace['OBJ']
        old_cod=sprav.getPrevCode()
        #GetObject=evalSpace['GetObject']

        #Внесено изменение
        global is_changed
        is_changed=False
    
        print('>>> Update old_cod=', old_cod)
        try:
            grid=evalSpace.GetInterface('spravGrid').get_grid()
        except:
            grid=evalSpace.GetObject('spravGrid')
        tab=grid.GetTable().GetDataset().data
        tab=sprav.getStorage().setTypeLevelTable(tab)
        sprav.getStorage().setLevelTable(old_cod,tab)
        #Перегрузить дерево справочника
        sprav_tree=sprav.getStorage().getLevelTree()
        evalSpace.GetObject('spravTree').LoadTree(sprav_tree)
    except:
        #print 'XXX::',sprav_tree
        ic_log.icLogErr(u'Ошибка обработчика кнопки сохрания изменения справочника.')
    
def onMouseClickFindTool(evalSpace):
    """
    """
    try:
        #onMouseClickFindTool.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #GetInterface=evalSpace['GetInterface']
        #GetObject=evalSpace['GetObject']
    
        #grid = GetInterface('spravGrid').get_grid()
        grid=evalSpace.GetObject('spravGrid')
        find_str=evalSpace.GetObject('findEdit').GetValue()
        cur_cursor=grid.GetGridCursorRow()
        i_row,field=grid.GetDataset().FindRowString(find_str,
            cursor=cur_cursor,fields=['name'])
        if i_row>=0:
            grid.SetCursor(i_row,1)
    except:
        ic_log.icLogErr(u'Ошибка обработчика конпки поиска в справочнике.')
        
def onInitSpravTree(evalSpace, bRefresh=True):
    """
    Обработчик события инициализации дерева справочника.
    """
    try:
        print('!!! onInitSpravTree START')
        #onInitSpravTree.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #sprav=evalSpace['sprav']
        sprav=evalSpace['OBJ']
        #GetObject=evalSpace['GetObject']
        #GetObject=evalSpace.GetObject
        #GetInterface=evalSpace['GetInterface']
        
        tree=evalSpace.GetObject('spravTree')
        sprav_tree=sprav.getStorage().getLevelTree()
        tree.LoadTree(sprav_tree)
        #Получить таблицу
        level_tab_tuple=sprav.getStorage().getLevelTable(None)
        level_tab=[list(rec) for rec in level_tab_tuple]
        if level_tab is not None:
            #grid=GetObject('spravGrid')
            try:
                #Использование шаблона
                grid=evalSpace.GetInterface('spravGrid').get_grid()
            except:
                #Использование объекта
                grid=evalSpace.GetObject('spravGrid')
            print('GRID:::',grid)
            #grid=grid.get_grid()
            dataset=grid.GetDataset()
            if dataset:
                dataset.SetDataBuff(level_tab)
            #
            len_cod=sprav.getLevelByIdx(0).getCodLen()
    
            grid.GetDataset().SetStructFilter({'cod':[len_cod]})
            if bRefresh:
                grid.RefreshGrid()
    except:
        ic_log.icLogErr(u'Ошибка инициализации дерева справочника.')
    
def onSelectChangedSpravTree(evalSpace):
    """
    Обработчик смены элемента дерева справочника.
    """
    try:
        #onSelectChangedSpravTree.func_globals['__builtins__']['locals']().update(evalSpace)
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        #sprav=evalSpace['sprav']
        sprav=evalSpace['OBJ']
        #GetObject=evalSpace['GetObject']
        GetObject=evalSpace.GetObject
        GetInterface=evalSpace.GetInterface
        #old_cod=evalSpace['old_cod']
        old_cod=sprav.getPrevCode()

        #Внесено изменение
        global is_changed
        #print 'DBG is_changed',is_changed,GetObject('spravTree').GetSelections()
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
        #print '>>spravGrid',evalSpace.GetInterface('spravGrid')
        try:
            grid=evalSpace.GetInterface('spravGrid').get_grid()
        except:
            grid=evalSpace.GetObject('spravGrid')
        #grid=GetObject('spravGrid')

        #Получить таблицу
        level_tab=[list(rec) for rec in sprav.getStorage().getLevelTable(cod)]
        if level_tab is not None:
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
    except:
        ic_log.icLogErr(u'Ошибка обработчика смены элемента дерева справочника.')
        return None
    
def onChangedGrid(evalSpace):
    """
    Произошли изменения в гриде.
    """
    #onChangedGrid.func_globals['__builtins__']['locals']().update(evalSpace)

    global is_changed
    is_changed=True
    
    return coderror.IC_CTRL_OK