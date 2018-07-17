#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/spravHlpDlgXP.frm>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/spravHlpDlgXP.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/spravHlpDlgXP_frm.py
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
import wx
from ic.utils import coderror

HLP_DLG_NAME = 'spravHlpDlgXP'
HLP_TREE_NAME = 'HlpTreeList'

def spravToolBar_init_expr(obj):
#    return 
    obj.SetPosition((3,2))
    bgr = obj.GetParent().GetBackgroundColour()
    obj.SetBackgroundColour(bgr)

def HlpTreeList(obj):
    pass

def HlpTreeList_onInit(obj):
#    print 'SPRAV TREE OnInit start', obj
    sprav = obj.GetContext()['OBJ']
    param = sprav.get_hlp_param() or {}
    sprav_storage=sprav.getStorage()
    sprav_code = param.get('sprav_code', '')
    sprav_tree=sprav_storage.getLevelBranch(sprav_code)
    sprav_tree=sprav_storage.limitLevelTree(sprav_tree,sprav_code.count(None)-1)

    title = u'Редактирование справочника: '+(sprav.description or u'')
    obj.GetContext().GetObject(HLP_DLG_NAME).SetTitle(title)
    
    if not sprav_tree:
        print('SPRAV TREE ERROR',sprav_tree)
        
    ctrl = obj.GetContext().GetObject(HLP_TREE_NAME)
    ctrl.LoadTree(sprav_tree)    

def ok_button_mouseClick(obj, evt):
    """ Обработка нажатия кнопки ОК."""
    result= obj.GetContext().GetObject(HLP_TREE_NAME).getSelectionName()
    obj.GetContext().GetObject(HLP_DLG_NAME).EndModal(wx.ID_OK)
    try:
        cod, name = result.split('  ')
    except:
        cod = result
        name = u''
        
    #obj.GetContext()['result'] = (coderror.IC_HLP_OK, cod, {'name':name})
    obj.GetContext()['result'] = cod

def cancel_button_mouseClick(obj, evt):
    """ Обработка нажатия кнопки Cancel."""
    obj.GetContext().GetObject(HLP_DLG_NAME).EndModal(wx.ID_CANCEL)
    obj.GetContext()['result'] = None

def HlpTreeList_itemActivated(obj, evt):
    """ Обработка выбора элемента списка."""
    return ok_button_mouseClick(obj, evt)

def HlpTreeList_keyDown(obj, evt):
    """ Обработка нажатия кнопки."""
    key=evt.GetKeyCode()
    if key==wx.WXK_ESCAPE:
        obj.GetContext()['result'] = None
        obj.GetContext().GetObject(HLP_DLG_NAME).EndModal(wx.ID_CANCEL)
    elif key==wx.WXK_RETURN:
        return ok_button_mouseClick(obj, evt)

def HlpTreeList_selectChanged(obj, evt):
    """ Обработка изменения текущего элемента списка."""
    sprav = obj.GetContext()['OBJ']
    cod=obj.getSelectionName()
    level=sprav.getLevelByCod(cod)
    if level:
        obj.setLabelCols(level.labelsNotice())

def onMouseClickFindTool(obj):
    try:
        evalSpace = obj.GetContext()
        tree=evalSpace.GetObject(HLP_TREE_NAME)
        find_str=evalSpace.GetObject('findEdit').GetValue()
        tree.selectFindItem(find_str)
    except:
        ic_log.icLogErr(u'Ошибка обработчика кнопки поиска в справочнике.')
