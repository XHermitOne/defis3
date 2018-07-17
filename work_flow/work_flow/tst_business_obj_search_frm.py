#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль ресурса <C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_search.frm>.
"""

### RESOURCE_MODULE: C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_search.frm
# -----------------------------------------------------------------------------
# Name:        C:\develop\python_projects_svn_repository\work\defis\work_flow\work_flow/tst_business_obj_search_frm.py
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

class tst_business_obj_search_SearchPanelManager(icmanagerinterface.icWidgetManager):
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
        #
        self._OBJ=self.context['OBJ']

    def onSearchTool(self,event):
        """
        Обработчик нахатия на кнопке <Поиск> на панели инструментов.
        """
        pass

    def onClearTool(self,event):
        """
        Обработчик нахатия на кнопке <Очистить> на панели инструментов.
        """
        self.context.clearValueInCtrl(self.GetObject('search_panel'))
        event.Skip()
    
    def onShowGridTool(self,event):
        """
        Обработчик нахатия на кнопке <Показать/скрыть объекты> на панели инструментов.
        """
        pass
    
    def onViewTool(self,event):
        """
        Обработчик нахатия на кнопке <Режим просмотра> на панели инструментов.
        """
        pass
    
    def onEditTool(self,event):
        """
        Обработчик нахатия на кнопке <Режим редактирования> на панели инструментов.
        """
        pass
    
manager_class = tst_business_obj_search_SearchPanelManager

