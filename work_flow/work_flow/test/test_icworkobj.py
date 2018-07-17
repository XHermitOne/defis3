#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Функции тестирования классов META-ОБЪЕКТА WORKFLOW.
Author(s): Колчанов А.В.
"""

# Version
__version__ = (0, 0, 0, 1)

#--- Imports ---
import sys,os,os.path
cur_sub_sys_import_pth=os.path.dirname(os.path.dirname(os.getcwd()))
if cur_sub_sys_import_pth not in sys.path:
    print('>>> ADD PATH:::',cur_sub_sys_import_pth)
    sys.path.append(cur_sub_sys_import_pth)
    print('>>> SYS.PATH::::',sys.path)

import copy

import ic
from ic import ic_mode
from work_flow.work_sys import icworkobj
#from work_flow.usercomponents import workobj

#from ic.components import icResourceParser
from ic.utils import util

#--- Functions ---
def testClass():
    """
    Запуск тестов класса мета-объекта workflow.
    """
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CLASS START TEST')
    work_obj=icworkobj.icWorkObjectPrototype()
    work_obj._db_psp=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)

    #Проверка создания ресурса таблицы
    tab_res=work_obj._createTabRes()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CLASS TEST CREATE TAB RES:',tab_res)
        if tab_res:
            print('>>> ...OK')
            
    #Проверка создания ресурса формы инициализации/создания
    init_frm_res=work_obj._genInitDialogRes()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CLASS TEST CREATE INIT FORM RES:',init_frm_res)
        if init_frm_res:
            print('>>> ...OK')
            
    #Проверка создания ресурса формы редактирования
    edit_frm_res=work_obj._genEditDialogRes()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CLASS TEST CREATE EDIT FORM RES:',edit_frm_res)
        if edit_frm_res:
            print('>>> ...OK')
            
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CLASS STOP TEST')

def testComponent():
    """
    Запуск тестов компонента ьета-объекта workflow.
    """
    from work_flow.usercomponents import workobj
    from work_flow.usercomponents import requisite
    from work_flow.usercomponents import nsi_requisite
    
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT COMPONENT START TEST')
    work_obj_spc=copy.deepcopy(workobj.ic_class_spc)
    work_obj_spc['name']='tst_workobj'
    work_obj_spc['db']=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)
    #Добавление реквизитов
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite1'
    work_obj_spc['child'].append(requisite_spc)
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite2'
    work_obj_spc['child'].append(requisite_spc)

    requisite_spc=copy.deepcopy(nsi_requisite.ic_class_spc)
    requisite_spc['name']='nsi_requisite1'
    requisite_spc['fields']={'nsi_requisite1_fld':'cod','nsi_req1_name_fld':'name'}
    requisite_spc['nsi_psp']=(('Sprav','NSITst',None,'nsi_sprav.mtd','work_flow'),)
    work_obj_spc['child'].append(requisite_spc)
    
    #Добавление подчиненных объектов
    work_obj_child_spc=copy.deepcopy(workobj.ic_class_spc)
    work_obj_child_spc['name']='child_obj1'
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite11'
    work_obj_child_spc['child'].append(requisite_spc)
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite12'
    work_obj_child_spc['child'].append(requisite_spc)
    work_obj_spc['child'].append(work_obj_child_spc)
    
    
    #Создание объекта по спецификации
    work_obj=workobj.icWorkObject(None,-1,work_obj_spc,evalSpace=None)
    #work_obj=ic.getKernel().createObjBySpc(None,work_obj_spc)
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT SPC:',[child['name'] for child in work_obj_spc['child']])
        print('>>> WORKOBJECT:',work_obj)
    
    #Проверить получение дочерних реквизитов
    children=work_obj.getChildrenRequisites()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT CHILDREN REQUISITES:',children)
    #Проверка создания таблицы
    tab=work_obj.getTable()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST CREATE TAB:',tab)
        if tab:
            print('>>> ...OK')
        else:
            print('>>> ...ERROR')
    #Синхронизация таблиц
    if tab:
        sync_ok=tab.syncDB()
        if ic_mode.isDebugMode():
            print('TABLE',tab.getDBTableName(),'SYNC DB RESULT:',sync_ok)

    #Проверка создания дочерних таблиц
    #if tab:
    #    print '>>> CHILD TABLE:',tab._children_tables

    #Проверка создания формы инициализации/создания
    init_frm=work_obj.createInitFormRes()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST CREATE INIT FORM:',init_frm)
        if init_frm:
            print('>>> ...OK')
        else:
            print('>>> ...ERROR')

    #Проверка создания формы редактирования
    edit_frm=work_obj.createEditFormRes()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST CREATE EDIT FORM:',edit_frm)
        if edit_frm:
            print('>>> ...OK')
        else:
            print('>>> ...ERROR')
            
    #Проверка добавления объектов
    work_obj.requisites_dict['requisite1'].setValue('---1')
    work_obj.requisites_dict['requisite2'].setValue('---2')
    child_obj=work_obj.GetChildByName('child_obj1')
    child_obj.requisites_dict['requisite11'].setValue('---11')
    child_obj.requisites_dict['requisite12'].setValue('---12')
    
    result=work_obj.add()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST ADD: ...',result)

    #Проверка удаления объектов
    result=work_obj.delete()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST DEL: ...',result)
    
    #Проверка загрузки объектов
    work_obj.add()
    work_obj.requisites_dict['requisite1'].setValue('----')
    child_obj.requisites_dict['requisite12'].setValue('####')
    result=work_obj.load()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST LOAD: ...',result,bool(work_obj.requisites_dict['requisite1'].getValue()=='---1'),bool(child_obj.requisites_dict['requisite12'].getValue()=='---12'))
    
    #Проверка записи объектов
    work_obj.requisites_dict['requisite2'].setValue('----')
    child_obj.requisites_dict['requisite11'].setValue('$$$$')
    result=work_obj.save()
    work_obj.requisites_dict['requisite2'].setValue('++++')
    child_obj.requisites_dict['requisite11'].setValue('####')
    work_obj.load()
    if ic_mode.isDebugMode():
        print('>>> WORKOBJECT TEST SAVE: ...',result,bool(work_obj.requisites_dict['requisite2'].getValue()=='----'),bool(child_obj.requisites_dict['requisite11'].getValue()=='$$$$'))
                                
if __name__=='__main__':
    ic_mode.setDebugMode()
    print('>>> START DEBUG MODE')
    testClass()