#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_history_panel.frm>.
"""
### RESOURCE_MODULE: C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_history_panel.frm
# -----------------------------------------------------------------------------
# Name:        C:/develop/python_projects_svn_repository/work/defis/work_flow/work_flow/default_history_panel_frm.py
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
from work_flow.interfaces import icnewperioddialog

class DefaultHistoryPanelManager(icmanagerinterface.icWidgetManager):
    def Init(self):
        """
        Инициализация внутренних переменных менеджера.
        """
        wx.CallAfter(self._init)

    def _init(self):
        """
        Основная функция инициализации внутренних объектов.
        """
        #Редактируемый объект
        self.OBJ=None
        
        self.periods=[]
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


    def setOBJ(self,OBJ):
        """
        Установить редактируемый объект.
        """
        self.OBJ=OBJ
        
        #Если определена история у объекта, тогда проинициализировать
        #контролы панели состояний объекта
        state_choice=self.GetObject('state_choice')
        state_choice.setChoiceList(self.OBJ.getHistory().getTypeStateLabels())
        state_choice.SetSelection(0)        
        
        #Проинициализировать периоды
        period_choice=self.GetObject('period_choice')
        self.periods=self.OBJ.getHistory().getPeriodRecords(self.OBJ.getUUID())
        period_labels=self._convertPeriodLabels(self.periods)
        period_choice.setChoiceList(period_labels)
        period_choice.SetSelection(0)

        #Заполнение панели реквизитов состояния
        state_idx=state_choice.GetSelection()
        state=self.OBJ.getHistory().getStateByIdx(state_idx)
        #state_data=state.loadRequisiteData(state.getUUIDByPeriod(period_uuid))
        state.fillRequisiteDataPanel(self.GetObject('data_panel'))
            
        #надо обновить дерево
        if self.periods and period_choice.GetSelection()<len(self.periods):
            period_uuid=self.periods[period_choice.GetSelection()]['uuid']
            attach_node=self.OBJ.getHistory().getStateByIdx().getAttachNode()
            attach_uuid=self.OBJ.getHistory().getAttachUUID(period_uuid)
            attach_data=attach_node.getTreeData(attach_uuid)
            self.GetObject('obj_tree').LoadTree(attach_data)

            docs_node=self.OBJ.getHistory().getStateByIdx().getDocumentsNode()
            docs_uuid=self.OBJ.getHistory().getDocumentsUUID(period_uuid)
            docs_data=attach_node.getTreeData(docs_uuid)
            self.GetObject('docs_tree').LoadTree(docs_data)

            #Заполнение панели реквизитов состояния
            state_data=state.loadRequisiteData(state.getUUIDByPeriod(period_uuid))
            self.GetObject('data_panel').setChildrenData(state_data)

    def onAddPeriodButton(self,event):
        """
        Обработчик нажатия на кнопку добавления нового периода.
        """
        result=icnewperioddialog.icNewPeriodDlg(self.GetObject('default_history_panel'),
            self.OBJ)
        if result:
            #Нажата кнопка <ОК>  и надо сохранить изменения
            #print '<<>>',result
            obj_uuid=self.OBJ.getUUID()
            subj_uuid=self.OBJ.getHistory().getSubject().getUUIDByCod(result['subj_cod'])
            
            begin_date=result['begin_date']
            end_date=None
            if result['end_period']:
                end_date=result['end_date']
                
            self.OBJ.getHistory().addPeriod(obj_uuid,subj_uuid,begin_date,end_date)
            
            #После сохранения обновить контрол выбора периода
            self.periods=self.OBJ.getHistory().getPeriodRecords(obj_uuid)
            period_labels=self._convertPeriodLabels(self.periods)
            period_choice=self.GetObject('period_choice')
            period_choice.setChoiceList(period_labels)
            labels_count=len(period_labels)
            if labels_count>0:
                period_choice.SetSelection(len(period_labels)-1)
                
            #Обновить контрол дерева прикрепленных объектов
            state_idx=self.GetObject('state_choice').GetSelection()
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            attach_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
            attach_data=attach_node.getTreeData(attach_uuid)
            #print '!!!!!!!!DBG!!!!!!!!!!!',attach_uuid,attach_data,type(attach_data)
            self.GetObject('obj_tree').LoadTree(attach_data)
                
    def _convertPeriodLabels(self,PeriodRecords_):
        """
        Конвертировать записи периодов истории объекта в надписи контрола.
        """
        subj_nsi=self.OBJ.getHistory().getSubject()
        labels=[]
        for record in PeriodRecords_:
            begin_date=record['begin_date']
            end_date=record['end_date'] if record['end_date'] else '   ...    '
            subj_cod=record['subj_cod']
            subj_name=subj_nsi.Find(subj_cod)
            
            label='%s-%s : %s'%(begin_date,end_date,subj_name)
            labels.append(label)
        return labels
        
    def onDelPeriodButton(self,event):
        """
        Обработчик нажатия на кнопку удаления периода.
        """
        period_choice=self.GetObject('period_choice')
        select_period_idx=period_choice.GetSelection()
        select_period_rec=self.periods[select_period_idx]
        obj_uuid=select_period_rec['obj_uuid']
        if ic.ic_dlg.icAskBox(u'Внимание!',
            u'Вы действительно хотите удалить выбранный период?'):
            result=self.OBJ.getHistory().delPeriod(select_period_rec['uuid'],
                select_period_rec['prev_uuid'])
            if result:
                #Если удаление прошло нормально, то перечитать 
                #список периодов.
                self.periods=self.OBJ.getHistory().getPeriodRecords(obj_uuid)
                period_labels=self._convertPeriodLabels(self.periods)
                period_choice.setChoiceList(period_labels)
                period_choice.SetSelection(0)
                
    #--- Панель управления объектами ---
    def onAttachObjectTool(self,event):
        """
        Обработчик нажатия на кнопку прикрепления объекта.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            select_obj=attach_node.choiceAttachObject()
            if select_obj:
                obj_uuid=select_obj.Choice(self.GetObject('default_history_panel'))
                if obj_uuid:
                    select_obj.loadRequisiteData(obj_uuid)
                    #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
                    selected_record=self.GetObject('obj_tree').getSelectionRecord()
                    if selected_record:
                        parent_node_uuid=selected_record[0]
                    else:
                        parent_node_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_idx]['uuid'],state_idx)
                    
                    attach_node.addNode(Name_=select_obj.getObjDescription(obj_uuid),
                        ParentUUID_=parent_node_uuid,
                        AttachObj_=select_obj,
                        ObjUUID_=self.OBJ.getUUID(),
                        ObjPsp_=self.OBJ.GetPassport(),
                        PeriodUUID_=self.periods[period_idx]['uuid'],
                        HistoryPsp_=self.OBJ.getHistory().GetPassport(),
                        StateUUID_=None,
                        StatePsp_=self.OBJ.getHistory().getStateByIdx(state_idx).GetPassport())
                    #После добавления нового узла 
                    #надо обновить дерево контрола
                    attach_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                    attach_data=attach_node.getTreeData(attach_uuid)
                    self.GetObject('obj_tree').LoadTree(attach_data)
                    
    def onDetachObjectTool(self,event):
        """
        Обработчик нажатия на кнопку открепления объекта.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            #select_obj=attach_node.choiceAttachObject()
            #if select_obj:
            #    obj_uuid=select_obj.Choice(hist_panel)
            #    if obj_uuid:
            #select_obj.loadRequisiteData(obj_uuid)
            #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
            selected_record=self.GetObject('obj_tree').getSelectionRecord()
            if selected_record:
                del_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Нельзя удалить этот элемент',hist_panel)
                return
                    
            if ic.ic_dlg.icAskBox(u'Внимание!',
                u'Вы уверены, что хотите удалить этот объект?'):
                attach_node.delNode(del_node_uuid)
                #После удаления узла 
                #надо обновить дерево контрола
                attach_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                attach_data=attach_node.getTreeData(attach_uuid)
                self.GetObject('obj_tree').LoadTree(attach_data)
        
    def onAddObjectTool(self,event):
        """
        Обработчик нажатия на кнопку добавления объекта.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            select_obj=attach_node.choiceAttachObject()
            if select_obj:
                obj_uuid=select_obj.Init(self.GetObject('default_history_panel'))
                if obj_uuid:
                    select_obj.loadRequisiteData(obj_uuid)
                    #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
                    selected_record=self.GetObject('obj_tree').getSelectionRecord()
                    if selected_record:
                        parent_node_uuid=selected_record[0]
                    else:
                        parent_node_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_idx]['uuid'],state_idx)
                    
                    attach_node.addNode(Name_=select_obj.getObjDescription(obj_uuid),
                        ParentUUID_=parent_node_uuid,
                        AttachObj_=select_obj,
                        ObjUUID_=self.OBJ.getUUID(),
                        ObjPsp_=self.OBJ.GetPassport(),
                        PeriodUUID_=self.periods[period_idx]['uuid'],
                        HistoryPsp_=self.OBJ.getHistory().GetPassport(),
                        StateUUID_=None,
                        StatePsp_=self.OBJ.getHistory().getStateByIdx(state_idx).GetPassport())
                    #После добавления нового узла 
                    #надо обновить дерево контрола
                    attach_uuid=self.OBJ.getHistory().getAttachUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                    attach_data=attach_node.getTreeData(attach_uuid)
                    self.GetObject('obj_tree').LoadTree(attach_data)
                    
    def onEditObjectTool(self,event):
        """
        Обработчик нажатия на кнопку редактирования объекта.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            selected_record=self.GetObject('obj_tree').getSelectionRecord()
            if selected_record:
                edit_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Не найден элемент',hist_panel)
                return
                    
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            attach_obj=attach_node.getAttachObj(edit_node_uuid)
            if attach_obj:
                root_obj=hist_panel.getRootObject()
                if root_obj:
                    root_obj.Close()
                attach_obj.Edit(hist_panel)
                    
    def onViewObjectTool(self,event):
        """
        Обработчик нажатия на кнопку редактирования объекта.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            selected_record=self.GetObject('obj_tree').getSelectionRecord()
            if selected_record:
                edit_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Не найден элемент',hist_panel)
                return
                    
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            attach_obj=attach_node.getAttachObj(edit_node_uuid)
            if attach_obj:
                attach_obj.View()

    #--- Панель управления документами ---
    def onAttachDocTool(self,event):
        """
        Обработчик нажатия на кнопку прикрепления документа.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            select_obj=attach_node.choiceAttachObject()
            if select_obj:
                obj_uuid=select_obj.Choice(self.GetObject('default_history_panel'))
                if obj_uuid:
                    select_obj.loadRequisiteData(obj_uuid)
                    #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
                    selected_record=self.GetObject('doc_tree').getSelectionRecord()
                    if selected_record:
                        parent_node_uuid=selected_record[0]
                    else:
                        parent_node_uuid=self.OBJ.getHistory().getDocumentsUUID(self.periods[period_idx]['uuid'],state_idx)
                    
                    attach_node.addNode(Name_=select_obj.getObjDescription(obj_uuid),
                        ParentUUID_=parent_node_uuid,
                        AttachObj_=select_obj,
                        ObjUUID_=self.OBJ.getUUID(),
                        ObjPsp_=self.OBJ.GetPassport(),
                        PeriodUUID_=self.periods[period_idx]['uuid'],
                        HistoryPsp_=self.OBJ.getHistory().GetPassport(),
                        StateUUID_=None,
                        StatePsp_=self.OBJ.getHistory().getStateByIdx(state_idx).GetPassport())
                    #После добавления нового узла 
                    #надо обновить дерево контрола
                    attach_uuid=self.OBJ.getHistory().getDocumentsUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                    attach_data=attach_node.getTreeData(attach_uuid)
                    self.GetObject('doc_tree').LoadTree(attach_data)
        
    def onDetachDocTool(self,event):
        """
        Обработчик нажатия на кнопку открепления документа.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            #select_obj=attach_node.choiceAttachObject()
            #if select_obj:
            #    obj_uuid=select_obj.Choice(hist_panel)
            #    if obj_uuid:
            #select_obj.loadRequisiteData(obj_uuid)
            #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
            selected_record=self.GetObject('doc_tree').getSelectionRecord()
            if selected_record:
                del_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Нельзя удалить этот элемент',hist_panel)
                return
                    
            if ic.ic_dlg.icAskBox(u'Внимание!',
                u'Вы уверены, что хотите удалить этот документ?'):
                attach_node.delNode(del_node_uuid)
                #После удаления узла 
                #надо обновить дерево контрола
                attach_uuid=self.OBJ.getHistory().getDocumentsUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                attach_data=attach_node.getTreeData(attach_uuid)
                self.GetObject('doc_tree').LoadTree(attach_data)
        
    def onAddDocTool(self,event):
        """
        Обработчик нажатия на кнопку добавления документа.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            select_obj=attach_node.choiceAttachObject()
            if select_obj:
                obj_uuid=select_obj.Init(self.GetObject('default_history_panel'))
                if obj_uuid:
                    select_obj.loadRequisiteData(obj_uuid)
                    #print 'DBG:::',self.GetObject('obj_tree').getSelectionRecord()
                    selected_record=self.GetObject('doc_tree').getSelectionRecord()
                    if selected_record:
                        parent_node_uuid=selected_record[0]
                    else:
                        parent_node_uuid=self.OBJ.getHistory().getDocumentsUUID(self.periods[period_idx]['uuid'],state_idx)
                    
                    attach_node.addNode(Name_=select_obj.getObjDescription(obj_uuid),
                        ParentUUID_=parent_node_uuid,
                        AttachObj_=select_obj,
                        ObjUUID_=self.OBJ.getUUID(),
                        ObjPsp_=self.OBJ.GetPassport(),
                        PeriodUUID_=self.periods[period_idx]['uuid'],
                        HistoryPsp_=self.OBJ.getHistory().GetPassport(),
                        StateUUID_=None,
                        StatePsp_=self.OBJ.getHistory().getStateByIdx(state_idx).GetPassport())
                    #После добавления нового узла 
                    #надо обновить дерево контрола
                    attach_uuid=self.OBJ.getHistory().getDocumentsUUID(self.periods[period_choice.GetSelection()]['uuid'],state_idx)
                    attach_data=attach_node.getTreeData(attach_uuid)
                    self.GetObject('doc_tree').LoadTree(attach_data)
        
    def onEditDocTool(self,event):
        """
        Обработчик нажатия на кнопку редактирования документа.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            selected_record=self.GetObject('doc_tree').getSelectionRecord()
            if selected_record:
                edit_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Не найден элемент',hist_panel)
                return
                    
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            attach_obj=attach_node.getAttachObj(edit_node_uuid)
            if attach_obj:
                root_obj=hist_panel.getRootObject()
                if root_obj:
                    root_obj.Close()
                attach_obj.Edit(hist_panel)

    def onViewDocTool(self,event):
        """
        Обработчик нажатия на кнопку просмотра документа.
        """
        hist_panel=self.GetObject('default_history_panel')
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        state_idx=self.GetObject('state_choice').GetSelection()
        if state_idx>=0 and period_idx>=0:
            selected_record=self.GetObject('doc_tree').getSelectionRecord()
            if selected_record:
                edit_node_uuid=selected_record[0]
            else:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Не найден элемент',hist_panel)
                return
                    
            attach_node=self.OBJ.getHistory().getStateByIdx(state_idx).getAttachNode()
            attach_obj=attach_node.getAttachObj(edit_node_uuid)
            if attach_obj:
                attach_obj.View()
        
    def onStateChoiceChange(self,event):
        """
        Обработчик изменения вида состояния объекта.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        period_uuid=self.periods[period_choice.GetSelection()]['uuid']
        state_idx=self.GetObject('state_choice').GetSelection()
        state=self.OBJ.getHistory().getStateByIdx(state_idx)
        if state_idx>=0 and period_idx>=0:
            #надо обновить дерево
            attach_node=state.getAttachNode()
            attach_uuid=self.OBJ.getHistory().getAttachUUID(period_uuid)
            attach_data=attach_node.getTreeData(attach_uuid)
            self.GetObject('obj_tree').LoadTree(attach_data)

            docs_node=state.getDocumentsNode()
            docs_uuid=self.OBJ.getHistory().getDocumentsUUID(period_uuid)
            docs_data=attach_node.getTreeData(docs_uuid)
            self.GetObject('docs_tree').LoadTree(docs_data)
            
            #Сначала сохранить предыдущие изменения
            data_panel=self.GetObject('data_panel')
            prev_state=None
            if prev_state:
                save_data=data_panel.GetContext().getValueInCtrl(data_panel)
                prev_state.saveRequisiteData(save_data)
            
            #Заполнить реквизитами панель
            #state_data=state.loadRequisiteData(state.getUUIDByPeriod(period_uuid))
            #state.fillRequisiteDataPanel(data_panel,state_data)            

    def onPeriodChoiceChange(self,event):
        """
        Обработчик изменения периода.
        """
        period_choice=self.GetObject('period_choice')
        period_idx=period_choice.GetSelection()
        period_uuid=self.periods[period_idx]['uuid']
        state_idx=self.GetObject('state_choice').GetSelection()
        state=self.OBJ.getHistory().getStateByIdx(state_idx)
        if state_idx>=0 and period_idx>=0:
            #надо обновить дерево
            obj_tree=self.GetObject('obj_tree')
            attach_node=state.getAttachNode()
            attach_uuid=self.OBJ.getHistory().getAttachUUID(period_uuid)
            attach_data=attach_node.getTreeData(attach_uuid)
            obj_tree.clearRoot()
            obj_tree.LoadTree(attach_data)

            docs_tree=self.GetObject('docs_tree')
            docs_node=state.getDocumentsNode()
            docs_uuid=self.OBJ.getHistory().getDocumentsUUID(period_uuid)
            docs_data=attach_node.getTreeData(docs_uuid)
            docs_tree.clearRoot()
            docs_tree.LoadTree(docs_data)
            
            #Сначала сохранить предыдущие изменения
            self.saveStateRequisites()
            
            #Заполнить реквизитами панель
            state_data=state.loadRequisiteData(state.getUUIDByPeriod(period_uuid))
            #state.fillRequisiteDataPanel(self.GetObject('data_panel'),state_data)            
            data_panel.setChildrenData(state_data)
       
    def saveStateRequisites(self):
        """
        Сохранить изменения реквизитов состояния.
        """
        #print '<<START>>'
        data_panel=self.GetObject('data_panel')
        save_data=data_panel.getChildrenData()
        #print '<<<SAVE DATA>>>',save_data
        if save_data:
            state_idx=self.GetObject('state_choice').GetSelection()
            state=self.OBJ.getHistory().getStateByIdx(state_idx)
            #Обязательно добавить UUID состояния иначе не понятно  куда сохранять
            period_choice=self.GetObject('period_choice')
            period_idx=period_choice.GetSelection()
            period_uuid=self.periods[period_idx]['uuid']
            save_data['uuid']=state.getUUIDByPeriod(period_uuid)
            #print '!!!'
            state.saveRequisiteData(save_data)
            #print '2!!!'
        
        
manager_class = DefaultHistoryPanelManager