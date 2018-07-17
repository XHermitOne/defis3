#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/new_period_dlg.frm>.
"""
### RESOURCE_MODULE: C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/new_period_dlg.frm
# -----------------------------------------------------------------------------
# Name:        C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/new_period_dlg_frm.py
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
import ic
from ic.interfaces import icmanagerinterface

class NewPeriodDialogManager(icmanagerinterface.icWidgetManager):
    def Init(self):
        """
        Инициализация внутренних переменных менеджера.
        """
        wx.CallAfter(self._init)

    def _init(self):
        """
        Основная функция инициализации внутренних объектов.
        """
        self.OBJ=None
        
    def setObj(self,Obj_):
        """
        Установить редактируемый объект.
        """
        print('DBG###',Obj_)
        self.OBJ=Obj_
        if Obj_:
            self.GetObject('subject_choice').sprav=Obj_.getHistory().getSubject()

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

    def onOkButton(self,event):
        """
        Обработчик нажатия на кнопку <ОК>.
        """
        dlg=self.GetObject('new_period_dlg')
        dlg.EndModal(wx.ID_OK)
        self.context['result']=self._getEditData()
        event.Skip()
    
    def onCancelButton(self,event):
        """
        Обработчик нажатия на кнопку <Отмена>.
        """
        dlg=self.GetObject('new_period_dlg')
        dlg.EndModal(wx.ID_CANCEL)
        self.context['result']=None
        event.Skip()
     
    def onCloseDlg(self,event):
        """
        Обработчик закрытия диалогового окна.
        """
        self.context['result']=None
        event.Skip()
        
    def _getEditData(self):
        """
        Определить отредактированные данные.
        """
        dlg=self.GetObject('new_period_dlg')
        edit_data=dlg.GetContext().getValueInCtrl(dlg)
        return edit_data
        
manager_class = NewPeriodDialogManager