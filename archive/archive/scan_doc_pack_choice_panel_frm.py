#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль ресурса </mnt/defis/defis/archive/archive/scan_doc_pack_choice_panel.frm>.
"""

### RESOURCE_MODULE: /mnt/defis/defis/archive/archive/scan_doc_pack_choice_panel.frm
# -----------------------------------------------------------------------------
# Name:        /mnt/defis/defis/archive/archive/scan_doc_pack_choice_panel_frm.py
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
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface

class scan_doc_pack_choice_panel_ChoicePanelManager(icmanagerinterface.icWidgetManager):
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

    def onOkButton(self, event):
        """
        Обработчик кнопки <OK>.
        """
        try:
            dlg = self.GetObject('choice_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result'] = self.GetObject('view_obj_grid').getSelectedObjUUID()
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        try:
            dlg = self.GetObject('choice_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()

    def onInit(self, event):
        """
        Инициализация всех контролов диалогового окна.
        """
        self.GetObject('view_obj_grid').refreshDataset()

    def onSearchTool(self, event):
        """
        Запуск поиска объектов, соответствующих фильтру.
        """
        obj = self.context['OBJ']
        filter = self.GetObject('filter_constructor_tree').getEditResult()
        query = obj.getFilterSQLAlchemy(filter)
        records = query.execute().fetchall()        
        dataset = obj._resultFilter2Dataset(records)
        self.GetObject('view_obj_grid').setDataset(dataset)
    
    def onClearFilterTool(self, event):
        """
        Очистка фильтра.
        """
        self.GetObject('filter_constructor_tree').clearTree()
    
    def onHideFilterTool(self, event):
        """
        Скрыть дерево фильтра.
        """
        self.GetObject('choice_splitter').hideWindow1()
        toolbar = self.GetObject('search_toolbar')
        toolbar.EnableTool(toolbar.getToolId('hide_filter_tool'), False)
        toolbar.EnableTool(toolbar.getToolId('show_filter_tool'), True)
    
    def onShowFilterTool(self, event):
        """
        Показать дерево фильтра.
        """
        self.GetObject('choice_splitter').showWindow1()
        toolbar = self.GetObject('search_toolbar')
        toolbar.EnableTool(toolbar.getToolId('hide_filter_tool'), True)
        toolbar.EnableTool(toolbar.getToolId('show_filter_tool'), False)
    
    def onViewObjTool(self, event):
        """
        Просмотр объекта.
        """
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.View(UUID_=obj_uuid)        

    def onEditObjTool(self, event):
        """
        Редактирование объекта.
        """
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.Edit(UUID_=obj_uuid)        
            obj_list.refreshDataset()

    def onAddObjTool(self, event):
        """
        Добавление объекта.
        """
        obj_list = self.GetObject('view_obj_grid')
        obj = self.context['OBJ']
        rec = obj.Add()
        if rec:
            obj.addRequisiteData(rec)
            obj_list.refreshDataset()

    def onDelObjTool(self, event):
        """
        Удаление объекта.
        """
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.Del(UUID_=obj_uuid)
            obj_list.refreshDataset()

    def getSelectedObjUUID(self):
        """
        UUID выбранного объекта.
        """
        return self.GetObject('view_obj_grid').getSelectedObjUUID()
        
        
manager_class = scan_doc_pack_choice_panel_ChoicePanelManager

