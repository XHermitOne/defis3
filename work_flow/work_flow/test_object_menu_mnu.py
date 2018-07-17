#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/test_object_menu.mnu>.
"""
### RESOURCE_MODULE: C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/test_object_menu.mnu
# -----------------------------------------------------------------------------
# Name:        C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/test_object_menu_mnu.py
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

class TestObjectMenubarManager(icmanagerinterface.icWidgetManager):
    def Init(self):
        """
        
        """
        wx.CallAfter(self._init)

    def _init(self):
        """
        Основная функция инициализации внутренних объектов.
        """        
        self.main_win=ic.getKernel().GetContext().getMainWin()
        #Тестируемый бизнес объект
        #print 'DEBUGER ic.metadata:',ic.metadata
        self.business_obj=ic.metadata.work_flow.mtd.test_businessobject.BusinessObj.create()
        #print 'Context DEBUG::::::',self.business_obj.GetContext().__class__,self.business_obj.evalSpace.__class__

    def onCreateObjectMenuItem(self,event):
        """
        Обработчик выбора пункта меню 'Создать...'
        """
        #print 'BUSINESS OBJECT:',self.business_obj
        self.business_obj.Init(self.main_win)
        
    def onSearchObjectMenuItem(self,event):
        """
        Обработчик выбора пункта меню 'Поиск...'
        """
        #print 'BUSINESS OBJECT:',self.business_obj
        self.business_obj.Search(self.main_win)
        
manager_class = TestObjectMenubarManager