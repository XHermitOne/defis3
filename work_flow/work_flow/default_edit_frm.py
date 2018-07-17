#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль ресурса </home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_edit.frm>.
"""

### RESOURCE_MODULE: /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_edit.frm
# -----------------------------------------------------------------------------
# Name:        /home/xhermit/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_edit_frm.py
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0,0,0,1)

#--- Imports ---
import wx
import ic 

if ic.ic_mode.isDebugMode():
    print('import',__file__)
    
def onCancelButtonMouseClick(Context_):
    """Обработчик нажатия на кнопку <Отмена>."""
    try:
        dlg=Context_['_root_obj']
        dlg.EndModal(wx.ID_CANCEL)
        Context_['result']=None
    except:
        ic.io_prnt.outErr(u'ОШИБКА.Обработчик нажатия на кнопку <Отмена>.')
    return None
    
def onOkButtonMouseClick(Context_):
    """Обработчик нажатия на кнопку <OK>."""
    try:
        OBJ=Context_['OBJ']

        OBJ.requisites['requisite1'].setValue(Context_['requisite1_edit'].getValue())
        OBJ.requisites['requisite2'].setValue(Context_['requisite2_edit'].getValue())
        OBJ.save()


        dlg=Context_['_root_obj']
        dlg.EndModal(wx.ID_OK)
        
        return OBJ
    except:
        ic.io_prnt.outErr(u'ОШИБКА.Обработчик нажатия на кнопку <OK>.')
    return None
    
