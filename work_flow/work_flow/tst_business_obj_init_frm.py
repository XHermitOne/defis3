#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль ресурса <C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_init.frm>.
"""

### RESOURCE_MODULE: C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_init.frm
# -----------------------------------------------------------------------------
# Name:        C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_init_frm.py
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
from ic.interfaces import icmanagerinterface

if ic.ic_mode.isDebugMode():
    print('import',__file__)

class tst_business_obj_init_InitFormManager(icmanagerinterface.icWidgetManager):
    """
    Менеджер формы.
    """
    def Init(self):
        """     
        Функция инициализации менеджера.
        """
        wx.CallAfter(self._init)

    def _init(self):
        """
        Основная функция инициализации внутренних объектов.
        """
        pass
    
    def onOkButton(self,event):
        """
        Обработчик кнопки <OK>.
        """
        try:
            dlg=self.GetObject('init_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result']=True
        except:
            ic.io_prnt.outErr(u'ОШИБКА.Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self,event):
        """
        Обработчик кнопки <Отмена>.
        """
        try:
            dlg=self.GetObject('init_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result']=None
        except:
            ic.io_prnt.outErr(u'ОШИБКА.Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()

manager_class = tst_business_obj_init_InitFormManager

