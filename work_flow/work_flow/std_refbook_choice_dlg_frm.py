#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module </home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_choice_dlg.frm>.
"""
### RESOURCE_MODULE: /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_choice_dlg.frm
# -----------------------------------------------------------------------------
# Name:        /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_choice_dlg_frm.py
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

#--- Imports ---
from ic.utils import ic_mode
if ic_mode.isDebugMode():
    print('import',__file__)

import wx
import ic

#--- Functions ---
def onDialogTitle(Context_):
    """
    Генерация заголовка диалогового окна.
    """
    title=u'Справочник: '
    try:
        if 'OBJ' in Context_:
            description=Context_['OBJ'].description
            if type(description)<>type(u''):
                description=unicode(str(description),'utf-8')
            title+=description
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Генерация заголовка диалогового окна справочника.')
    return title

def onTreeRootTitle(Context_):
    """
    Генерация заголовка дерева справочника.
    """
    title=u'Справочник'
    try:
        if 'OBJ' in Context_:
            title=Context_['OBJ'].description
        if type(title)<>type(u''):
            title=unicode(str(title),'utf-8')
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Генерация заголовка дерева справочника.')
    return title
    
def onTreeBrwsInit(Context_):
    """
    Обработчик инициализации браузера дерева справочника.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onTreeBrwsInit.func_globals['__builtins__']['locals']().update(Context_)
        #print 'DBG>>>',Context_.keys()
        OBJ=Context_['OBJ']
        
        tree_ctrl=Context_.GetObject('tree_object_ctrl')
        if tree_ctrl:
            #tree_ctrl.clearRoot()
            tree_data=OBJ.getTreeObjData()
            #print 'TREE DATA:::',tree_data
            tree_ctrl.LoadTree(tree_data)
            tree_ctrl.expandAllRoot()
            tree_ctrl.reFresh()
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Обработчик инициализации браузера дерева справочника.')
        
def onBrwsModeTool(Context_):
    """
    Переключение в режим браузера.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onBrwsModeTool.func_globals['__builtins__']['locals']().update(Context_)
        OBJ=Context_['OBJ']
        
        return OBJ.Browse()
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Обработчик переключения в режим браузера справочника.')
        return False

def onCancelButtonMouseClick(Context_):
    """
    Нажание на кнопке ОТМЕНА.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #main_dlg=Context_.GetObject('std_ref_book_choice_dlg')
        main_dlg=Context_['_root_obj']
        main_dlg.EndModal(wx.ID_CANCEL)
        return None
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Обработчик нажатия на кнопке ОТМЕНА.')
    
def onOkButtonMouseClick(Context_):
    """
    Нажание на кнопке OK.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #main_dlg=Context_.GetObject('std_ref_book_choice_dlg')
        main_dlg=Context_['_root_obj']
        main_dlg.EndModal(wx.ID_OK)
        return True
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Обработчик нажатия на кнопке OK.')
    return False
    
def onDataGridInit(Context_):
    """
    Заполнение/Инициализация грида.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onDataGridInit.func_globals['__builtins__']['locals']().update(Context_)
        OBJ=Context_['OBJ']

        grid_ctrl=Context_.GetObject('grid_obj')
        if grid_ctrl:
            #Текущий выбранный код
            cur_obj_code=Context_['CUR_OBJ_CODE']
            
            #Длина кода текущего уровня
            code_len=OBJ.getLevelRefBook().getStructCodeLen()
            #Получить данные в виде списка
            data=OBJ.getListObjData(cur_obj_code)
            data=[rec['__record__'] for rec in data]
            #И загрузить их в грид
            grid_dataset=grid_ctrl.GetDataset()
            if grid_dataset:
                grid_dataset.SetDataBuff(data)
                #if code_len>0:
                #    grid_dataset.SetStructFilter({'code':[cur_obj_code,code_len]})
            grid_ctrl.RefreshGrid()
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Заполнение грида объектов.')
            
def onObjCodeChanged(Context_):
    """
    Изменение выбранного кода.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onObjCodeChanged.func_globals['__builtins__']['locals']().update(Context_)
    
        tree_ctrl=Context_.GetObject('tree_object_ctrl')
        if tree_ctrl:
            selection_rec=tree_ctrl.getSelectionRecord()
            if selection_rec is None:
                Context_['CUR_OBJ_CODE']=None
            else:
                Context_['CUR_OBJ_CODE']=selection_rec[0]
        #Если код выбран в браузере, то обновиться и грид заодно
        onDataGridInit(Context_)
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Изменения выбранного кода в дереве объекта.')

       
def onDelObjTool(Context_):
    """
    Удаление выбранного объекта.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onDelObjTool.func_globals['__builtins__']['locals']().update(Context_)
    
        tree_ctrl=Context_.GetObject('tree_object_ctrl')
        if tree_ctrl:
            selection_rec=tree_ctrl.getSelectionRecord()
            if selection_rec <> None:
                ask=ic.ic_dlg.icAskBox(u'ВНИМАНИЕ!',u'Удалить %s?'%selection_rec[0])
                if ask:
                    #Ответ утвердительный. Нужно удалять
                    OBJ=Context_['OBJ']
                    OBJ.Del(selection_rec[0],Context_)
                    #Перечитать дерево
                    tree_data=OBJ.getTreeObjData()
                    tree_ctrl.LoadTree(tree_data)
                    tree_ctrl.expandAllRoot()
                    tree_ctrl.reFresh()

                    #tree_ctrl.Refresh()
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Удаления выбранного объекта в дереве объекта.')
        
def onCodeObjControl(Context_):
    """
    Контроль кода объекта.
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onCodeObjControl.func_globals['__builtins__']['locals']().update(Context_)
        OBJ=Context_['OBJ']
        value=Context_['value']
        
        #Проверить вводимое значение на длину кода
        if value:
            code_len=OBJ.getStructCodeLen()
            value=value[:code_len]
        print('VALUE:::::',value)
        
        
        return (ic.coderror.IC_CTRL_OK,value)
    except:
        ic.io_prnt.outErr(u'ОШИБКА.Контроля кода объекта.')
        return (ic.coderror.IC_CTRL_FAILED_IGNORE,None)
