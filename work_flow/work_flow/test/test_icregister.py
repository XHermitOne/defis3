#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Функции тестирования классов регистров.
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
from work_flow.work_sys import icregister

from ic.utils import util

#--- Functions ---
def testClass():
    """
    Запуск тестов класса простого регистра.
    """
    if ic_mode.isDebugMode():
        print('>>> REGISTER CLASS START TEST')
    reg=icregister.icRegisterPrototype()
    reg._db_psp=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)

    #Проверка создания ресурса таблицы
    tab_res=reg._createTabRes()
    if ic_mode.isDebugMode():
        print('>>> REGISTER CLASS TEST CREATE TAB RES:',tab_res)
        if tab_res:
            print('>>> ...OK')
            
    #Проверка создания ресурса формы инициализации/создания
    #init_frm_res=reg._genInitDialogRes()
    #if ic_mode.isDebugMode():
    #    print '>>> REGISTER CLASS TEST CREATE INIT FORM RES:',init_frm_res
    #    if init_frm_res:
    #        print '>>> ...OK'
            
    #Проверка создания ресурса формы редактирования
    #edit_frm_res=work_obj._genEditDialogRes()
    #if ic_mode.isDebugMode():
    #    print '>>> REGISTERECT CLASS TEST CREATE EDIT FORM RES:',edit_frm_res
    #    if edit_frm_res:
    #        print '>>> ...OK'
            
    if ic_mode.isDebugMode():
        print('>>> REGISTER CLASS STOP TEST')

def testComponent():
    """
    Запуск тестов компонента простого регистра.
    """
    from work_flow.usercomponents import register
    from work_flow.usercomponents import requisite
    
    if ic_mode.isDebugMode():
        print('>>> REGISTER COMPONENT START TEST')
    reg_spc=copy.deepcopy(register.ic_class_spc)
    reg_spc['name']='tst_register'
    reg_spc['db']=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)
    #Добавление реквизитов
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite1'
    reg_spc['child'].append(requisite_spc)
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite2'
    reg_spc['child'].append(requisite_spc)
    
    #Создание объекта по спецификации
    reg=register.icRegister(None,-1,reg_spc,evalSpace=None)
    #reg=ic.getKernel().createObjBySpc(None,reg_spc)
    if ic_mode.isDebugMode():
        print('>>> REGISTER SPC:',[child['name'] for child in reg_spc['child']])
        print('>>> REGISTER:',reg)
    
    #Проверить получение дочерних реквизитов
    children=reg.getChildrenRequisites()
    if ic_mode.isDebugMode():
        print('>>> REGISTER CHILDREN REQUISITES:',children)
    #Проверка создания таблицы
    tab=reg.getTable()
    if ic_mode.isDebugMode():
        print('>>> REGISTER TEST CREATE TAB:',tab)
        if tab:
            print('>>> ...OK')
        else:
            print('>>> ...ERROR')
    #Синхронизация таблиц
    if tab:
        sync_ok=tab.syncDB()
        if ic_mode.isDebugMode():
            print('TABLE',tab.getDBTableName(),'SYNC DB RESULT:',sync_ok)

    #Проверка регистрации записей
    data={}
    data['requisite1']='value---1'
    data['requisite2']='value---2'
    
    result=reg.reg(**data)
    if ic_mode.isDebugMode():
        print('>>> REGISTER TEST REG: ...',result)

    #Проверка удаления объектов
    #result=work_obj.delete()
    #if ic_mode.isDebugMode():
    #    print '>>> REGISTER TEST DEL: ...',result

    #Проверка очистки
    result=reg.clear()
    if ic_mode.isDebugMode():
        print('>>> REGISTER TEST CLEAR: ...',result)

    if ic_mode.isDebugMode():
        print('>>> REGISTER COMPONENT STOP TEST')

def testClassAccumulating():
    """
    Запуск тестов класса накопительного регистра.
    """
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER CLASS START TEST')
    reg=icregister.icRegisterPrototype()
    reg._db_psp=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)

    #Проверка создания ресурса таблицы
    tab_res=reg._createTabRes()
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER CLASS TEST CREATE TAB RES:',tab_res)
        if tab_res:
            print('>>> ...OK')
            
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER CLASS STOP TEST')

def testComponentAccumulating():
    """
    Запуск тестов компонента накопительного регистра.
    """
    #from work_flow.usercomponents import register
    from work_flow.usercomponents import accumulating_register
    from work_flow.usercomponents import requisite
    from work_flow.usercomponents import reg_group
    from work_flow.usercomponents import reg_sum
    
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER COMPONENT START TEST')
        
    reg_spc=copy.deepcopy(accumulating_register.ic_class_spc)
    reg_spc['name']='tst_accumulating_register'
    reg_spc['db']=(('PostgreSQLDB','work_db_psgress',None,'work_db_psgress.src','work_flow'),)
    
    #Добавление реквизитов
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite1'
    reg_spc['child'].append(requisite_spc)
    requisite_spc=copy.deepcopy(requisite.ic_class_spc)
    requisite_spc['name']='requisite2'
    reg_spc['child'].append(requisite_spc)
    grp_spc=copy.deepcopy(reg_group.ic_class_spc)
    grp_spc['name']='group1'
    reg_spc['child'].append(grp_spc)
    grp_spc=copy.deepcopy(reg_group.ic_class_spc)
    grp_spc['name']='group2'
    reg_spc['child'].append(grp_spc)
    sum_spc=copy.deepcopy(reg_sum.ic_class_spc)
    sum_spc['name']='sum1'
    reg_spc['child'].append(sum_spc)
    sum_spc=copy.deepcopy(reg_sum.ic_class_spc)
    sum_spc['name']='sum2'
    reg_spc['child'].append(sum_spc)
    
    #Создание объекта по спецификации
    reg=accumulating_register.icAccumulatingRegister(None,-1,reg_spc,evalSpace=None)
    #reg=ic.getKernel().createObjBySpc(None,reg_spc)
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER SPC:',[child['name'] for child in reg_spc['child']])
        print('>>> ACCUMULATING REGISTER:',reg)
    
    #Проверить получение дочерних реквизитов
    children=reg.getChildrenRequisites()
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER CHILDREN REQUISITES:',children)
    #Проверка создания таблицы
    tab=reg.getTable()
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER TEST CREATE TAB:',tab)
        if tab:
            print('>>> ...OK')
        else:
            print('>>> ...ERROR')
    #Синхронизация таблиц
    if tab:
        sync_ok=tab.syncDB()
        if ic_mode.isDebugMode():
            print('TABLE',tab.getDBTableName(),'SYNC DB RESULT:',sync_ok)

    #Проверка регистрации записей
    data={}
    data['requisite1']='value---1'
    data['requisite2']='value---2'
    data['group1']='grp1'
    data['group2']='grp2'
    data['sum1']=10
    data['sum2']=20
    
    result=reg.reg(**data)
    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER TEST REG: ...',result)

    #Проверка удаления объектов
    #result=work_obj.delete()
    #if ic_mode.isDebugMode():
    #    print '>>> REGISTER TEST DEL: ...',result

    #Проверка очистки
    #result=reg.clear()
    #if ic_mode.isDebugMode():
    #    print '>>> ACCUMULATING REGISTER TEST CLEAR: ...',result

    if ic_mode.isDebugMode():
        print('>>> ACCUMULATING REGISTER COMPONENT STOP TEST')
                                
if __name__=='__main__':
    ic_mode.setDebugMode()
    print('>>> START DEBUG MODE')
    testClass()