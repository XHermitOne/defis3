#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module </home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_brws_dlg.frm>.
"""
### RESOURCE_MODULE: /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_brws_dlg.frm
# -----------------------------------------------------------------------------
# Name:        /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/std_refbook_brws_dlg_frm.py
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
from .std_refbook_choice_dlg_frm import *

#   Version
__version__ = (0,0,0,1)

#--- Functions ---
def onSaveToolMouseClick(Context_):
    """
    Обработчик щелчка мыши на инструменте "Сохранение изменений".
    @param Context_: Контекст выполнения формы.
    """
    try:
        #Вытащить глобальные переменные из пространства имен, 
        #иначе они не попадут в локальное пространство имен
        onTreeBrwsInit.func_globals['__builtins__']['locals']().update(Context_)
        OBJ=Context_['OBJ']
        
        tree_ctrl=Context_.GetObject('tree_object_ctrl')
        grid_ctrl=Context_.GetObject('grid_obj')
        
        data_set=grid_ctrl.GetTable().GetDataset()
        if data_set:
            data=data_set.getDataDict()
            print('DATA:::',data)
            
            #Определить текущий выбранных код
            code=None
            if 'CUR_OBJ_CODE' in Context_:
                code=Context_['CUR_OBJ_CODE']
            
            OBJ.setListObjData(code,data)
            
            #После сохранения необходимо перегрузить дерево
            onTreeBrwsInit(Context_)
    except:
        ic.io_prnt.outErr(u'ОШИБКА. Сохранение изменений.')
    