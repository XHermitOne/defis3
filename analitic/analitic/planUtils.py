#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Функции расчета/разноса сумм и коэффициентов планов и файктов.
Автор(ы) Оконешников, Колчанов:
"""
import time
import copy

from metadatainterfaces import IMetaplan
from ic.components import icResourceParser as prs
#import ic.db.ic_sqlobjtab as ic_sqlobjtab
from ic.db import icsqlalchemy
#import NSI.spravfunc as spravfunc
#from NSI import spravctrl

from ic.engine import ic_user
from ic.dlg import ic_dlg
#from ic.dlg import progress
#from ic.dlg import threaded_progress as t_progress
import plan.interfaces.ieditpanel as ieditpanel
import plan.interfaces.IODBSprav as IODBSprav
import ic.dlg.msgbox as msgbox
import win32api
from ic.log import ic_log
import ic.utils.ic_cache as ic_cache
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg
# Версия
__version__ = (0, 0, 0, 1)

#--- Статические переменные
sprav_dict_buff = None

#--- Функции групповой обработки
def init_plan_node_func(x, descr):
    """
    Функция инициализации элемента плана.
    """
    x.value.summa = 0
    x.value.kol = 0
    x.value.description = descr

def add_node_plan_sum(x, summa, kol):
    """
    функция агрегации.
    """
    x.value.summa += summa
    x.value.kol += kol

#--- Функции
def CountParPlan(metaObj):
    """
    Вычисление весовых коэфициентов плана по агрегированным суммам планов.
    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на метаобъект классификатора мониторов.
    """
    if not metaObj.isRoot():
        #print '>>> Enter To CountParPlan', metaObj.value.metatype, metaObj.value.summa
        S = metaObj.value.summa
        Sk = metaObj.value.kol
        
    L = len(metaObj.values())
    
    for obj in metaObj.values():
        if not metaObj.isRoot():
            #print '   ::: name, typ:', obj.value.name, obj.value.summa, S, L
            if S <> 0:
                obj.value.w = L*obj.value.summa/S
                
            if Sk <> 0:
                obj.value.w_kol = L*obj.value.kol/Sk
                
        CountParPlan(obj)
    
def getSpravBuffDict(metaObj, bRefreshBuff=False):
    """
    Возвращает словаь забуферезированных словарей.
    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на метаобъект классификатора планов.
    """
    global sprav_dict_buff
    
    if sprav_dict_buff and not bRefreshBuff:
        return sprav_dict_buff
    
    lst = metaObj.getContainerMetaItems().values()
    dict = {}
    
    try:
        for i, item_cls in enumerate(lst):
            #   Буферизируем справочники
            try:
                dict[item_cls.name] = spravfunc.getReplDict(item_cls.value.sprav, 'cod', 'name')
                #progress.icUpdateProgressBar("Буферизируем справочник: %s" % item_cls.value.sprav, i*100/len(lst))
            except:
                print '$EXCEPTION spravfunc.getReplDict(...)', item_cls.name
                
    #        #   Задаем словарь отношений {<тип элемента>:<имя поля>, ...}
    #        try:
    #            typfldDict[item_cls.name] = item_cls.value.field
    #        except:
    #            print 'EXCEPTION item_cls.value.field', item_cls.name
        sprav_dict_buff = dict
    except:
        print '### getSpravBuffDict ERROR:'
        
    return dict

def getTypFldDict(metaObj):
    """
    Возвращает словарь отношений {<тип элемента>:<имя поля>, ...}
    
    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на метаобъект классификатора планов.
    """
    lst = metaObj.getContainerMetaItems().values()
    typfldDict = {}
    
    for i, item_cls in enumerate(lst):
        #   Задаем словарь отношений {<тип элемента>:<имя поля>, ...}
        try:
            typfldDict[item_cls.name] = item_cls.value.field
        except:
            print 'EXCEPTION item_cls.value.field', item_cls.name
    
    return typfldDict
    
#@ic_dlg.wait_noparent_deco
@ic_proccess_dlg.proccess_noparent_deco
def genPlanTemplate(metaObj, source, yearTempl, monthTempl=1, year=2005, month=None):
    """
    Функция генерит шаблон месячного плана по статистике.
    
    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на метаобъект классификатора мониторов.
    @type source: C{string}
    @param source: Имя источника данных.
    @type yearTempl: C{int}
    @param yearTempl: Год генерируемого плана.
    @type monthTempl: C{int}
    @param monthTempl: Месяц генерируемого плана..
    @type year: C{int}
    @param year: За какой год используется статистика.
    @type month: C{int}
    @param month: За какой месяц используется статистика.
    """
#    progress.icCloseProgressBar()
#    progress.icOpenProgressBar("Выборка",0,100)
    #ic_dlg.SetWaitBoxLabel('Получаем выборку')
    ic_proccess_dlg.SetProccessBoxLabel('Получаем выборку', 10)

    if month==None:
        month = monthTempl

    #obj = ic_sqlobjtab.icSQLObjTabClass(source)
    obj=icsqlalchemy.icSQLAlchemyTabClass(source)
    
    sql = """
    SELECT substr(codt, 1,3) as codt, reg, substr(mens, 2, 4) as mens, sum(summa) as summa, sum(kolf) as kolf
    FROM (
         select *
         from analitic
         where dtoper LIKE ('%s%s')
         ) as filter
    group by reg, substr(mens, 2, 4), substr(codt, 1,3)
    ORDER BY codt, reg, mens""" % (str(yearTempl)+'.' +('0'+str(monthTempl))[-2:], '%')

    print 'SQL STRING:', sql
    rec = obj.queryRecs(sql)
    
    if rec:
        #print 'SQL EXECUTE rec:', rec.count()
        #lst = metaObj.getContainerMetaItems().values()
        
        #   Буферизируем справочники
        dict = getSpravBuffDict(metaObj)#{}
        #   Определяем словарь отношений {<тип элемента>:<имя поля>, ...}
        typfldDict = getTypFldDict(metaObj)
        t1 = time.clock()
        
        #   Определям узел года
        if metaObj.has_key(str(year)):
            itemObj = metaObj[str(year)]
        #   Если узла нет, то создаем
        else:
            itemObj = metaObj.Add(str(year), 'mYear')

        yearObj = itemObj
        #   Определям узел месяца
        mcod = 'm'+('0'+str(month))[-2:]
        if itemObj.has_key(mcod):
            itemObj = itemObj[mcod]
        #   Если узла нет, то создаем
        else:
            itemObj = itemObj.Add(mcod, 'mMonth')
            itemObj.value.description = dict['mMonth'][mcod]

        #   Заполняем структуру плана
        kwarg = {}
        mnthObj = itemObj
        
        #ic_dlg.SetWaitBoxLabel('Создаем необходимую структуру')
        ic_proccess_dlg.SetProccessBoxLabel('Создаем необходимую структуру', 20)
    
        #   Начинаем транзакцию
        mnthObj.transact()
        
        #   Создаем необходимую структуру и обнуляем суммы планов, перед тем
        #   как вычислять агрегированные суммы планов
        for i, r in enumerate(rec):
            for typ, fld in typfldDict.items():
                #print ' getattr typ,fld=', typ, fld
                kwarg[typ] = getattr(r, fld)
                
            fo = GetOrCreateMetaPlanObj(itemObj, dict, None, init_plan_node_func, **kwarg)
            #progress.icUpdateProgressBar("Создаем необходимую структуру: %s" % fo.value.description, i*100/len(rec))
        t2 = time.clock()
        print ' :::: change struct', t2-t1
            
        #   Делаем пересчет плановых и агрегирующих сум (кроме месячных и
        #   годовых планов)
        #ic_dlg.SetWaitBoxLabel('Делаем пересчет плановых сумм групп')
        ic_proccess_dlg.SetProccessBoxLabel('Делаем пересчет плановых сумм групп', 50)
        
        for r in rec:
            for typ, fld in typfldDict.items():
                #print ' getattr typ,fld=', typ, fld
                kwarg[typ] = getattr(r, fld)
                
            fo = SetMetaPlan(itemObj, add_node_plan_sum, r.summa, r.kolf, **kwarg)
        
        #   Вычисляем месячный план
        #print ' :::: mnthObj-', mnthObj.value.name, mnthObj.value.summa
        mnthObj.value.summa = 0
        mnthObj.value.kol = 0
        for obj in mnthObj.values():
            mnthObj.value.summa += obj.value.summa
            mnthObj.value.kol += obj.value.kol
        
        #   Деламе пересчет коэфициентов по вычисленным суммам планов
        #ic_dlg.SetWaitBoxLabel('Делаем пересчет сумм и коэфициентов')
        ic_proccess_dlg.SetProccessBoxLabel('Делаем пересчет сумм и коэфициентов', 80)
        CountParPlan(mnthObj)
        
        #ieditpanel.recount_prnt(mnthObj, bSave=False)
#        chld_lst = mnthObj.values()
#        if chld_lst:
#            ieditpanel.recount_prnt(chld_lst[0], bSave=False)
        ieditpanel.CountWeightBySum(mnthObj)
        ieditpanel.recount_prnt(mnthObj, bSave=False)

        #   Завершаем транзакцию
        mnthObj.commit()
        
        #t2 = time.clock()
        #print '>>>> CountParPlan time update struct:', t2-t1

        #progress.icUpdateProgressBar("Сохраняем структуру планов", 80)
        #yearObj.SaveAllChildren()
        #progress.icCloseProgressBar()
        
def getSQLByStruct():
    """
    Возвращает SQL выражение в зависимости от структуры дерева планирования.
    """

def getChildTypesByStructPlan(defPlanLst, typ):
    """
    По стуктуре плана определяет дочерние типы узлов плана.
    """
    try:
        i = defPlanLst.index(typ)
        if i+1 < len(defPlanLst):
            return [defPlanLst[i+1]]
    except:
        print '>>> Error Invalid Plan Node Type <%s>: %s' % (typ, defPlanLst)
    
    return []
        
def GetOrCreateMetaPlanObj(metaObj, sprBuff, defPlanLst, init_func, **kwarg):
    """
    Функция находит или создает объект по заданному списку ключей.
    
    @type defPlanLst: C{list}
    @param defPlanLst: Список, описывающий структуру плана.
    """
    typ = metaObj.value.metatype
    if not defPlanLst:
        tps = [cl.value.metatype for cl in metaObj.getMyContainerMetaItems()]
    else:
        tps = getChildTypesByStructPlan(defPlanLst, typ)
        
    sKeys = set(tps) & set(kwarg.keys())
    print '----- ..... %s getCanContain()-> %s - %s:' % (typ, tps, metaObj.getCanContain())
    print '----- ..... GetOrCreateMetaPlanObj sKeys, tps', sKeys, tps, kwarg
    #return
    
    if len(sKeys) > 0:
        tp = list(sKeys)[0]
        key = kwarg[tp]

        #   Если ключа нет, то создаем план с таким именем
        if not key in metaObj.keys():
            obj = metaObj.Add(key, tp)
            print '>>>>:::: Add metaobj cod, typ', key, tp,obj,typ
            
        else:
            obj = metaObj[key]
            #print '>>>>:::: Find metaobj cod, typ', key, tp

        try:
            descr = sprBuff[tp][key]
        except:
            descr = key
            print '### KEY ERROR SPRAV BUFF in CreateObj:', tp, key
            
        #   Функция инициализации объекта
        init_func(obj, descr)
        
        return GetOrCreateMetaPlanObj(obj, sprBuff, defPlanLst, init_func, **kwarg)
    else:
        return metaObj

def SetMetaPlan(metaObj, set_func, summa_, kol_, **kwarg):
    """
    Устанавливает сумму многофакторного плана по заданному списку ключей,
    одновременно вычисляя агрегированные суммы.
    """
    typ = metaObj.value.metatype
    tps = [cl.value.metatype for cl in metaObj.getMyContainerMetaItems()]
    sKeys = set(tps) & set(kwarg.keys())
    
    set_func(metaObj, summa_, kol_)
    
    if len(sKeys) > 0:
        tp = list(sKeys)[0]
        key = kwarg[tp]

        #   Если ключа нет, то создаем план с таким именем
        if not key in metaObj.keys():
            return metaObj
        else:
            obj = metaObj[key]
            #print '>>>>:::: Find metaobj cod, typ', key, tp
            
        #   Функция инициализации объекта
        #set_func(obj, summa_, kol_)
        
        return SetMetaPlan(obj, set_func, summa_, kol_, **kwarg)
    else:
        return metaObj

#--- Обнуление сумм-фактов ---
@ic_proccess_dlg.proccess2_noparent_deco
def MetaPlanZeroSum(metaTree,Year_,Month_,aggregate_ctrl=None):
    """
    Обнуление сумм-фактов в дереве планов.
    """
    ic_proccess_dlg.SetProccessBoxLabel('Обнуление сумм', 
        0,label2='Год: %s Месяц: %s Разнос сумм базового плана'%(Year_,Month_), value2=10)
    if not aggregate_ctrl:
        aggregate_ctrl=metaTree.value.aggregate_ctrl
        
    #Буферизируем справочники
    sprav_dict=getSpravBuffDict(metaTree)#{}
    
    #   Определям узел года
    if metaTree.has_key(str(Year_)):
        year_root=metaTree[str(Year_)]
    #   Если узла нет, то создаем
    else:
        year_root=metaTree.Add(str(Year_), 'mYear')
    #   Определям узел месяца
    month='m%02i'%(int(Month_))
    if year_root.has_key(month):
        month_root=year_root[month]
        month_root.BuildAll()
    #   Если узла нет, то создаем
    else:
        month_root=year_root.Add(month, 'mMonth')
        month_root.value.description=sprav_dict['mMonth'][month]
    
    #Начать транзакцию
    t1=time.clock()
    year_root.transact()
    
    #Перебрать таблицы-источники
    source_tabs=dict(map(lambda src_tab_name: (src_tab_name,ic_sqlobjtab.icSQLObjTabClass(src_tab_name)),
        aggregate_ctrl.keys()))
        
    for source_tab_name,source_tab in source_tabs.items():
        #Получить запрос преобразования
        src_query="""SELECT substr(dtoper, 1,4) as year,substr(dtoper, 6,2) as month,dtoper,substr(codt, 1,3) as vidprod, reg, substr(mens, 2, 4) as mens,sum(kolf) as kolf, sum(summa) as summa
    FROM %s WHERE substr(dtoper, 1,4)='%s' AND substr(dtoper, 6,2)='%s'
    group by year,month,dtoper,vidprod,reg,mens
    ORDER BY year,month,dtoper""" % (source_tab_name,Year_,Month_)
        ic_log.icToLog('SQL: '+src_query)
        
        #aggregate_ctrl[source_tab_name]['source_query']
        #Получиь путь разноса суммы
        summa_path=aggregate_ctrl[source_tab_name]['summa_path']
        #Получить список флагов разноса суммы по датам
        date_flags=aggregate_ctrl[source_tab_name]['date_flags']
        #Разносимые поля
        #aggregate_fields=aggregate_ctrl[source_tab_name]['aggregate_fields']
        #Поле даты
        date_field=aggregate_ctrl[source_tab_name]['date_field']
            
        #Перебор записей в таблице-источнике
        recs=source_tab.queryRecs(src_query)
        #print 'RECS COUNT>>>>',recs.count()
        #ic_dlg.icOpenProgressDlg(ic_user.icGetMainWin(),
        #    'Подождите пожалуйста','Обнуление сумм',0,recs.count())
        #t_progress.icOpenThreadedProgressDlg('Разнос сумм','Обнуление сумм',0,recs.count())
        #ic_proccess_dlg.SetProccessBoxLabel(label2='Разнос сумм', value2=10)
        #print 'ZERO SUMM',src_query, recs.count()
        i=0
        try:
            count_100=float(100.0/recs.count())
        except:
            count_100=0
        for rec in recs:
            #ic_dlg.icUpdateProgressDlg(i,'Обнуление сумм')
            #t_progress.icStepThreadedProgressDlg()
            #ic_proccess_dlg.SetProccessBoxLabel(label1='Обнуление сумм', value1=i)
            ic_proccess_dlg.SetProccessBoxLabel('Обнуление сумм '+source_tab_name,count_100*i)
            i+=1
            #Определить разносимые суммы
            #aggregate_values=dict(map(lambda field: (field,getattr(rec,field)),
            #    aggregate_fields))
            #Определить дату
            date_values=map(lambda flag: [None,getattr(rec,date_field)][int(flag)],date_flags)[1:]
            #Получить путь для разноса сумм
            value_path=map(lambda field: getattr(rec,field),summa_path)[1:]
            #Разнести суммы
            if not (None in value_path):
                #print date_values,value_path
                #установить имя у месяца с m
                value_path[0]='m'+value_path[0]
                SetZeroSum(year_root,source_tab_name,date_values,value_path,zeroSum)
            else:
                print summa_path,rec

        #Обнуление суммы у месяца
        #month_root.value.setProperty(**{source_tab_name:{'summa':[0,0]}})
        #Обнуление суммы у года
        year_root.value.setProperty(**{source_tab_name:{'summa':[0,0]}})

        #ic_dlg.icCloseProgressDlg()
        #t_progress.icCloseThreadedProgressDlg()

    #Закончить транзакцию
    t2=time.clock()
    month_root.commit()
    #month_root.SaveAllChildren()
    #year_root.savePropertyStorage()
    print ':::zero Summ commit()',t2-t1,time.clock()-t2

def SetZeroSum(parentMetaObj,src_tab,date_values,value_path,set_func):
    """
    Обнуление сумм-фактов.
    """
    if parentMetaObj is None:
        return False
        
    if value_path:
        if value_path[0] in parentMetaObj._children.keys():
            zeroAllSum(parentMetaObj._children[value_path[0]],['analitic','zayavki','pay'])
            set_func(parentMetaObj._children[value_path[0]],src_tab,date_values[0])
            return SetZeroSum(parentMetaObj._children[value_path[0]],
                src_tab,date_values[1:],value_path[1:],set_func)
        elif value_path[0]:
            #t_begin=time.clock()
            #Необходимо создать новый метаобъект
            container_metaitems=parentMetaObj.getMyContainerMetaItems()
            if container_metaitems:
                typ=container_metaitems[0].name
                new_metaobj=parentMetaObj.Add(value_path[0],typ)
                #t_end=time.clock()
                #print 'TIME:',t_end-t_begin #,new_metaobj.getPath()

                #Установка описания узла
                try:
                    typ_sprav=container_metaitems[0].value.sprav
                    description=spravfunc.FSpravBuffRepl(typ_sprav,value_path[0])
                    if description:
                        new_metaobj.value.description=description
                    else:
                        new_metaobj.value.description=value_path[0]
                except KeyError:
                    ic_log.icLogErr('ERROR '+container_metaitems[0].name)
                    #pass
                
                #print 'SetZeroSum:',value_path[0],typ
                zeroAllSum(new_metaobj,['analitic','zayavki','pay'])
                set_func(new_metaobj,src_tab,date_values[0])
                return SetZeroSum(new_metaobj,
                    src_tab,date_values[1:],value_path[1:],set_func)
            return True
        else:
            #print 'SetZeroSum:',value_path
            return False
    else:
        #print 'SetZeroSum:>',value_path
        return True

def zeroAllSum(metaObj,SrcTabs_):
    """
    Проставить полностью суммы-факты по всем параметрам в метаобъекте.
    """
    summa=None
    property=metaObj.value.getProperty()

    new_property={}
    for src_tab in SrcTabs_:
        if property.has_key(src_tab):
            summa=property[src_tab]
        else:
            summa={}
        summa['summa']=[0,0]
        new_property[src_tab]=summa
        
    metaObj.value.setProperty(**new_property)
    
def zeroSum(metaObj,SrcTab_,Date_):
    """
    Функция обнуления сумм-фактов в метаобъекте.
    """
    summa=None
    property=metaObj.value.getProperty()
    if property.has_key(SrcTab_):
        summa=property[SrcTab_]
    else:
        summa={}
    #summa['summa']=[0,0]
    if Date_:
        summa[Date_]=[0,0]
    metaObj.value.setProperty(**{SrcTab_:summa})
    
#--- Разнос сумм-фактов ---
#@ic_proccess_dlg.proccess2_deco
@ic_proccess_dlg.proccess2_noparent_deco
def MetaPlanDeliveSum(metaTree,Year_,Month_,aggregate_ctrl=None):
    """
    Разнесение сумм-фактов в дереве планов.
    """
    ic_proccess_dlg.SetProccessBoxLabel('Разнос сумм',
        0,label2='Год: %s Месяц: %s Разнос сумм базового плана'%(Year_,Month_), value2=50)
    if not aggregate_ctrl:
        aggregate_ctrl=metaTree.value.aggregate_ctrl
        
    #   Определям узел года
    if metaTree.has_key(str(Year_)):
        year_root=metaTree[str(Year_)]
    #   Если узла нет, то создаем
    else:
        year_root=metaTree.Add(str(Year_), 'mYear')
    #   Определям узел месяца
    month='m%02i'%(int(Month_))
    if year_root.has_key(month):
        month_root=year_root[month]
    #   Если узла нет, то создаем
    else:
        month_root=year_root.Add(month, 'mMonth')

    #Начать транзакцию
    t1=time.clock()
    year_root.transact()

    #Перебрать таблицы-источники
    source_tabs=dict(map(lambda src_tab_name: (src_tab_name,ic_sqlobjtab.icSQLObjTabClass(src_tab_name)),
        aggregate_ctrl.keys()))
    for source_tab_name,source_tab in source_tabs.items():
        #Получить запрос преобразования
        src_query="""SELECT substr(dtoper, 1,4) as year,substr(dtoper, 6,2) as month,dtoper,substr(codt, 1,3) as vidprod, reg, substr(mens, 2, 4) as mens,sum(kolf) as kolf, sum(summa) as summa
    FROM %s WHERE substr(dtoper, 1,4)='%s' AND substr(dtoper, 6,2)='%s'
    group by year,month,dtoper,vidprod,reg,mens
    ORDER BY year,month,dtoper""" % (source_tab_name,Year_,Month_)
        
        #aggregate_ctrl[source_tab_name]['source_query']
        #Получиь путь разноса суммы
        summa_path=aggregate_ctrl[source_tab_name]['summa_path']
        #Получить список флагов разноса суммы по датам
        date_flags=aggregate_ctrl[source_tab_name]['date_flags']
        #Разносимые поля
        #aggregate_fields=aggregate_ctrl[source_tab_name]['aggregate_fields']
        #Поле даты
        date_field=aggregate_ctrl[source_tab_name]['date_field']
            
        #Перебор записей в таблице-источнике
        recs=source_tab.queryRecs(src_query)

        #ic_dlg.icOpenProgressDlg(ic_user.icGetMainWin(),
        #    'Подождите пожалуйста','Разнос сумм',0,recs.count())
        #t_progress.icOpenThreadedProgressDlg('Разнос сумм','Разнос сумм',0,recs.count())
        #ic_proccess_dlg.SetProccessBoxLabel(label2='Разнос сумм', value2=10)
        
        i=0
        try:
            count_100=float(100.0/recs.count())
        except:
            count_100=0
        #print 'ZERO SUMM',src_query,recs.count()
        for rec in recs:
            #ic_dlg.icUpdateProgressDlg(i,'Обнуление сумм')
            #t_progress.icStepThreadedProgressDlg()
            #ic_proccess_dlg.SetProccessBoxLabel(label1='Разнос сумм', value1=i)
            ic_proccess_dlg.SetProccessBoxLabel('Разнос сумм '+source_tab_name,count_100*i)
            i+=1

            #Определить разносимые суммы
            #aggregate_values=dict(map(lambda field: (field,getattr(rec,field)),
            #    aggregate_fields))
            summa=(rec.summa,rec.kolf)
            #Определить дату
            date_values=map(lambda flag: [None,getattr(rec,date_field)][int(flag)],date_flags)[1:]
            #date_value=getattr(rec,date_field)
            #Получить путь для разноса сумм
            value_path=map(lambda field: getattr(rec,field),summa_path)[1:]
            #Разнести суммы
            if not (None in value_path):
                value_path[0]='m'+value_path[0]
                SetDeliveSum(year_root,source_tab_name,date_values,value_path,summa,deliveSum)

        #Подсчитать сумму
        #levelSum(month_root,source_tab_name)
        #Подсчитать сумму года
        levelSum(year_root,source_tab_name)
        
        #ic_dlg.icCloseProgressDlg()
        #t_progress.icCloseThreadedProgressDlg()

    #Закончить транзакцию
    #metaTree.SaveAllChildren()
    t2=time.clock()
    month_root.commit()
    #month_root.SaveAllChildren()
    #year_root.savePropertyStorage()
    print ':::delive Summ commit()',t2-t1,time.clock()-t2

def SetDeliveSum(parentMetaObj,src_tab,date_values,value_path,summa,set_func):
    """
    Разнесение сумм-фактов.
    """
    if parentMetaObj is None:
        return False
        
    if value_path:
        if value_path[0] in parentMetaObj._children.keys():
            set_func(parentMetaObj._children[value_path[0]],src_tab,date_values[0],summa)
            return SetDeliveSum(parentMetaObj._children[value_path[0]],
                src_tab,date_values[1:],value_path[1:],summa,set_func)
        elif value_path[0]:
            #Необходимо создать новый метаобъект
            container_metaitems=parentMetaObj.getMyContainerMetaItems()
            if container_metaitems:
                typ=container_metaitems[0].name
                new_metaobj=parentMetaObj.Add(value_path[0],typ)
                #print 'SetZeroSum:',value_path[0],typ
                #set_func(new_metaobj,src_tab,date_values[0])
                set_func(new_metaobj,src_tab,date_values[0],summa)
                return SetDeliveSum(new_metaobj,
                    src_tab,date_values[1:],value_path[1:],summa,set_func)
            return True
        else:
            #print 'SetZeroSum:',value_path
            return False
    else:
        #print 'SetZeroSum:>',value_path
        return True

def deliveSum(metaObj,SrcTab_,Date_,Summa_):
    """
    Функция разнесения сумм-фактов в метаобъекте.
    """
    summa=getattr(metaObj.value,SrcTab_)
    if summa is None:
        summa={}
        
    summa['summa'][0]+=Summa_[0]
    summa['summa'][1]+=Summa_[1]
    if Date_:
        summa[Date_][0]+=Summa_[0]
        summa[Date_][1]+=Summa_[1]
    metaObj.value.setProperty(**{SrcTab_:summa})

def levelSum(metaObj,SrcTab_):
    """
    Подсчитать сумму уровня.
    """
    try:
        summa=metaObj.value.getProperty()[SrcTab_]['summa']
    except KeyError:
        summa=[0,0]
    
    for child_name,child in metaObj.items():
        try:
            summa[0]+=child.value.getProperty()[SrcTab_]['summa'][0]
            summa[1]+=child.value.getProperty()[SrcTab_]['summa'][1]
        except KeyError:
            pass
        
    metaObj.value.setProperty(**{SrcTab_:{'summa':summa}})
    
def refreshSumm(metaTree=None,year=None,month=None):
    """
    Обноовление/разнос сумм в нашем деревер планов.
    """
    if None in (year,month):
        month_year=prs.ResultForm('MonthYearDlg',parent=ic_user.icGetMainWin())
        if month_year:
            month,year=month_year
        else:
            return None
    
    ic_log.icToLog('Разнос сумм за %s месяц %s года.'%(month,year))
    if metaTree is None:
        #metaTree=prs.icCreateObject('metadata_plan','mtd')
        metaTree=IMetaplan.IMetaplan().getObject()

    #Нормализация входных параметров
    year=str(year)
    month='%02d'%(int(month))
    
    MetaPlanZeroSum(metaTree,year,month)
    MetaPlanDeliveSum(metaTree,year,month)
    #metaTree.SaveAllChildren()
    ic_log.icToLog('Окончание разноса сумм за %s месяц %s года.'%(month,year))
    return (year,month)
    
def genPlanByFact():
    """
    Запускается диалог генерации месячного плана по накопленным фактам.
    """
    prs.ResultForm('GenMonthPlanDlg',parent=ic_user.icGetMainWin())
    
#---> Функции генерации модификаций планов ---
def planTreeToTable(metaObj, par=None, tableLst=None):
    """
    Преобразует дерево планов в табличное представление. Первый элемент кортеж
    идентификаторов (ключей) узлов, второй элемент картежа картеж суммы и количества.

    @type metaObj: C{icMetaItem}
    @param metaObj: Узел дерева плана.
    """
    if tableLst == None:
        tableLst = []
        
    if par == None:
        par = tuple()#('root',)
        
    for key, obj in metaObj.items():
        
        if obj.keys():
            tableLst = planTreeToTable(obj, par + (key,), tableLst)
        else:
            r = (par + (key,), (obj.value.summa, obj.value.kol))
            print '.....................>>>', r
            tableLst.append(r)
        
    return tableLst
    
def buildPlanTree(metaObj):
    """
    Строим дерево.
    """
    metaObj.BuildAll()

def buildStructByTable(mt, mMonthObj, modifLst, dict):
    """
    Создаем структуру модификации плана по подготовленной таблице.
    """
    #   Создаем структуру
    #ic_dlg.SetWaitBoxLabel('Прописываем суммы')
    
    kwarg = {}
    for r in mt:
        spar, (summa, kol) = r
        par = eval(spar)
        for i, el in enumerate(par):
            kwarg[modifLst[i+3]] = el
                
        fo = GetOrCreateMetaPlanObj(mMonthObj, dict, modifLst, init_plan_node_func, **kwarg)
    
    #   Прописываем суммы
    for r in mt:
        spar, (summa, kol) = r
        par = eval(spar)
        for i, el in enumerate(par):
            kwarg[modifLst[i+3]] = el
            
        fo = SetMetaPlan(mMonthObj, add_node_plan_sum, summa, kol, **kwarg)

def genModifPlan(parent, ibrows, id_modif, year=None, month=None):
    """
    Генерируется модификация плана по базовому плану.

    @type ibrows: C{icobjectinterface.icObjectInterface}
    @param ibrows: Указатель на интерфейс браузера ведения планов.
    @type id_modif: C{string}
    @param id_modif: Идентификатор модификации плана.
    """
    if None in (year, month):
        res = prs.ModalForm('MonthYearDlg', parent=parent)
        print '......... RES=', res
        if res == None:
            return
            
        month, year = res

    ic_proccess_dlg.SetProccessBoxLabel('Пересчет модификации плана за %s месяц %s года' %
                    (month, year), 0, 'Получаем дерево базового плана', 10)
    return _genModifPlan(parent, ibrows, id_modif, year, month)

def genModifPlanYear(parent, ibrows, id_modif, year=None):
    """
    Генерируется модификация плана по базовому плану за год.
    """

    if None in (year,):
        #res = prs.ModalForm('MonthYearDlg', parent=parent)
        year = prs.ModalForm('GetYearDlg', parent=parent)
        print '......... RES=', year
        if year == None:
            return
    
    return _genModifPlanYear(parent, ibrows, id_modif, int(year))
        
def genAllPlanMonth(parent, ibrows, modif_lst, month=None, year=None):
    """
    Генерируются модификации планов по базовому за выбранный месяц.
    """
    if None in (year, month):
        res = prs.ModalForm('MonthYearDlg', parent=parent)
        print '......... RES=', res
        if res == None:
            return
            
        month, year = res
    
    return _genAllPlanMonth(parent, ibrows, modif_lst, month, year)

@ic_proccess_dlg.proccess2_deco
def _genAllPlanMonth(parent, ibrows, modif_lst, month=None, year=None):
    """
    Генерируются модификации планов по базовому за выбранный месяц.
    """
    t1 = t2 = time.clock()
    for indx, id_modif in enumerate(modif_lst):
        tt = '%02i:%02i' % (int((t2-t1)/60), int(t2-t1) % 60)
        ic_proccess_dlg.SetProccessBoxLabel('Пересчет всех модификаций плана за %s месяц %s года  (%s)' %
                            (month, year, tt), int(100*indx/len(modif_lst)), 'Получаем дерево базового плана', 10)
        _genModifPlan(parent, ibrows, id_modif, year, month)
        t2 = time.clock()
        
@ic_proccess_dlg.proccess2_deco
def _genModifPlanYear(parent, ibrows, id_modif, year):
    """
    Генерируется модификация плана по базовому плану за год.
    """
    t1 = t2 = time.clock()
    for month in range(1, 13):
        tt = '%02i:%02i' % (int((t2-t1)/60), int(t2-t1) % 60)
        ic_proccess_dlg.SetProccessBoxLabel('Пересчет модификации плана за %s месяц %s года  (%s)' %
                    (month, year, tt), int(100*month/12), 'Получаем дерево базового плана', 10)
        _genModifPlan(parent, ibrows, id_modif, year, month)
        t2 = time.clock()
        
#@ic_dlg.wait_deco
@ic_proccess_dlg.proccess2_deco
def _genModifPlan(parent, ibrows, id_modif, year=None, month=None):
    """
    Генерируется модификация плана по базовому плану.

    @type ibrows: C{icobjectinterface.icObjectInterface}
    @param ibrows: Указатель на интерфейс браузера ведения планов.
    @type id_modif: C{string}
    @param id_modif: Идентификатор модификации плана.
    """
    result = None
    if None in (year, month):
        return
        
    base_plan_lst = ibrows.metaclass.plan_struct_lst[3:]
#    ic_proccess_dlg.SetProccessBoxLabel('Пересчет модификации плана за %s месяц %s года' %
#                    (str(month), year), None, 'Получаем дерево базового плана', 10)
    ic_proccess_dlg.SetProccessBoxLabel(label2='Получаем дерево базового плана', value2=10)

    ycod = str(year)
    if type(month)==type(0):
        mcod = 'm%02i' % month
    else:
        mcod = 'm%02i'%(int(month))

    #   Получаем талицу базового плана из буфера, если она там есть
    t = None
    
    if ic_cache.systemCache.hasObject('IManagePlans', mcod):
        t = ic_cache.systemCache.get('IManagePlans', mcod)

    tm1 = time.clock()
    if not t:
        metaObj = ibrows.setMetaplanById()
    
        #   Находим узел нужного месяца
        metaObj.getRoot().setCache(True)
        yearObj = None
        mnthObj = None
        
        try:
            metaObj.getRoot().BuildBranch([ycod, mcod], True)
            yearObj = metaObj[ycod]
            mnthObj = yearObj[mcod]
        except:
            ic_log.icLogErr()
            msgbox.MsgBox(parent, 'Элемент базового плана %s->%s не найден' % (mcod, ycod))
            return None

        t = planTreeToTable(mnthObj)
        ic_cache.systemCache.add('IManagePlans', mcod, t)

    #ic_dlg.SetWaitBoxLabel('Преобразуем таблицу данных')
    tm2 = time.clock()
    ic_proccess_dlg.SetProccessBoxLabel(label2='Преобразуем таблицу данных', value2=40)

    #   Получаем структуру модификации
    fullPlanLst = eval(IODBSprav.getModifPlanStructById(id_modif))
    modifLst = fullPlanLst[3:]

    #   Перебираем таблицу под структуру модификации плана, переставляем местами
    #   колонки
    #   1. Формируем словарь замен индексов колонок
    dictIndxRepl = {}
        
    for i, el in enumerate(base_plan_lst):
        try:
            n = modifLst.index(el)
            dictIndxRepl[i] = n
                
        except (ValueError, IndexError):
            dictIndxRepl[i] = -1
    
    #   2. Заменяем колонки
    mt = range(len(t))
    for indx, r in enumerate(t):
        p, val = r
        par = list(p)
        
        for i, j in dictIndxRepl.items():
            if j > -1:
                par[j] = p[i]
            else:
                par[j] = None
                
        par = filter(lambda x: x<>None, par)
        mt[indx] = (str(par), val)
    
    #   Сортируем таблицу
    ic_proccess_dlg.SetProccessBoxLabel(label2='Сортируем', value2=50)
    mt.sort()

    modif_metaplan = ibrows.setMetaplanById(id_modif)
    modif_metaplan.ReLoad()
    
    #   Определям узел года
    if modif_metaplan.has_key(ycod):
        mYearObj = modif_metaplan[str(year)]
    #   Если узла нет, то создаем
    else:
        mYearObj = modif_metaplan.Add(ycod, 'mYear')

    #   Определям узел месяца
    bCreateMnthNode = False
    if mYearObj.has_key(mcod):
        mMonthObj = mYearObj[mcod]
    #   Если узла нет, то создаем
    else:
        mMonthObj = mYearObj.Add(mcod, 'mMonth')
        mMonthObj.Save()
        bCreateMnthNode = True
        #mMonthObj.value.description = dict['mMonth'][mcod]

    #   Начинаем транзакцию
    mMonthObj.transact()

    mMonthObj.value.summa = 0
    mMonthObj.value.kol = 0
    mMonthObj.value.w = 0
    mMonthObj.value.w_kol = 0
    
    #   Чистим старую структуру модифивцированного плана
    for obj in mMonthObj.values():
        obj.Del()
        
    #   Строим дерево модифицированного плана по подготовленной таблице
    #   Буферезируем справочники
    ic_proccess_dlg.SetProccessBoxLabel(label2='Буферезируем справочники', value2=70)

    dict = getSpravBuffDict(mMonthObj)
    if bCreateMnthNode:
        mMonthObj.value.description = dict['mMonth'][mcod]
    
    tm2 = time.clock()
    ic_proccess_dlg.SetProccessBoxLabel(label2='Создаем структуру', value2=90)
    buildStructByTable(mt, mMonthObj, fullPlanLst, dict)

    #   Деламе пересчет коэфициентов по вычисленным суммам планов
    CountParPlan(mMonthObj)
    ieditpanel.CountWeightBySum(mMonthObj)
    ieditpanel.recount_prnt(mMonthObj, bSave=False)
    
    #   Завершаем транзакцию
    mMonthObj.commit()
    
#--- Функции разноса данных из базового плана в модифицированный ---
def planTree2Table(metaObj,par=None,tableLst=None):
    """
    Преобразует дерево планов в табличное представление.
        Первый элемент кортеж идентификаторов (ключей) узлов,
        второй элемент картежа картеж суммы и количества.

    @type metaObj: C{icMetaItem}
    @param metaObj: Узел дерева плана.
    """
    if tableLst == None:
        tableLst = []
        
    if par == None:
        par = tuple()#('root',)
        
    for key, obj in metaObj.items():
        
        if obj.keys():
            tableLst = planTree2Table(obj, par + (key,), tableLst)
        else:
            r = (par + (key,), copy.deepcopy(obj.value.getProperty()))
            #print '.....................>>>', r
            tableLst.append(r)
        
    return tableLst
    
def generateModifPlan(parent, metaclass, id_modif, year=None, month=None):
    """
    Генерируется модификация плана по базовому плану.

    @type id_modif: C{string}
    @param id_modif: Идентификатор модификации плана.
    """
    if None in (year, month):
        month, year = prs.ModalForm('MonthYearDlg', parent=parent)
    return _generateModifPlan(parent,metaclass,id_modif,year,month)
    
def _generateModifPlan(parent, metaclass, id_modif, year=None, month=None):
    """
    Генерируется модификация плана по базовому плану.

    @type id_modif: C{string}
    @param id_modif: Идентификатор модификации плана.
    """
    result = None
        
    ic_proccess_dlg.SetProccessBoxLabel('Получаем дерево базового плана '+id_modif,30)

    base_plan_lst = metaclass.plan_struct_lst[3:]
    
    #   Находим узел нужного месяца
    ycod = str(year)
    if type(month)==type(0):
        mcod = 'm%02i' % month
    else:
        mcod = 'm%02i'%(int(month))
        
    #   Получаем талицу базового плана из буфера, если она там есть
    base_plan_tab = None
    
    if ic_cache.systemCache.hasObject('IManagePlans', mcod):
        base_plan_tab = ic_cache.systemCache.get('IManagePlans', mcod)

    if not base_plan_tab:
        metaObj = metaclass.setMetaplanById()
    
        #   Находим узел нужного месяца
        metaObj.getRoot().setCache(True)
        yearObj = None
        mnthObj = None
        
        try:
            metaObj.getRoot().BuildBranch([ycod, mcod], True)
            yearObj = metaObj[ycod]
            mnthObj = yearObj[mcod]
        except:
            ic_log.icLogErr()
            msgbox.MsgBox(parent, 'Элемент базового плана %s->%s не найден' % (mcod, ycod))
            return None

        base_plan_tab = planTree2Table(mnthObj)
        ic_cache.systemCache.add('IManagePlans', mcod, base_plan_tab)
    
    #   Получаем структуру модификации
    modifLstFull=eval(IODBSprav.getModifPlanStructById(id_modif))
    modifLst = modifLstFull[3:]

    #   Перебираем таблицу под структуру модификации плана, переставляем местами
    #   колонки
    #   1. Формируем словарь замен индексов колонок
    dictIndxRepl = {}
    
    for i, el in enumerate(base_plan_lst):
        try:
            n = modifLst.index(el)
            dictIndxRepl[i] = n

        except (ValueError, IndexError):
            dictIndxRepl[i] = -1
    
    #ic_dlg.SetWaitBoxLabel('Преобразуем таблицу данных')
    ic_proccess_dlg.SetProccessBoxLabel('Генерация модификации плана '+id_modif,60)
    #   2. Заменяем колонки
    #print '.... dictIndxRepl=', dictIndxRepl
    mt = range(len(base_plan_tab))
    for indx, r in enumerate(base_plan_tab):
        p, val = r
        par = list(p)
        
        for i, j in dictIndxRepl.items():
            if j > -1:
                par[j] = p[i]
            else:
                par[j] = None
                
        par = filter(lambda x: x<>None, par)
        mt[indx] = (str(par), val)
    
    #   Сортируем таблицу
    mt.sort()

    modif_metaplan = metaclass.setMetaplanById(id_modif)
    modif_metaplan.ReLoad()
    #   Определям узел года
    if modif_metaplan.has_key(ycod):
        mYearObj = modif_metaplan[ycod]
    #   Если узла нет, то создаем
    else:
        mYearObj = modif_metaplan.Add(ycod, 'mYear')

    #   Определям узел месяца
    bCreateMnthNode = False
    if mYearObj.has_key(mcod):
        mMonthObj = mYearObj[mcod]
    #   Если узла нет, то создаем
    else:
        mMonthObj = mYearObj.Add(mcod, 'mMonth')
        bCreateMnthNode = True
        #mMonthObj.value.description = dict['mMonth'][mcod]
    
    ic_proccess_dlg.SetProccessBoxLabel('Строим дерево модифицированного плана '+id_modif,90)
    
    #   Начинаем транзакцию
    mMonthObj.transact()
    
    #init_value(mMonthObj,'')
    
    #   Чистим старую структуру модифивцированного плана
    #for obj in mMonthObj.values():
    #    obj.Del()
        
    #   Строим дерево модифицированного плана по подготовленной таблице
    
    #   Буферезируем справочники
    dict = getSpravBuffDict(mMonthObj)
    if bCreateMnthNode:
        mMonthObj.value.description = dict['mMonth'][mcod]
    
    buildModifPlanByTable(mt, mMonthObj, modifLstFull, dict)
    
    #   Деламе пересчет коэфициентов по вычисленным суммам
    #CountParPlan(mMonthObj)

    #chld_lst = mMonthObj.values()
    #if chld_lst:
    #    ieditpanel.recount_prnt(chld_lst[0], bSave=False)
    recount_fact(mMonthObj, bSave=True)

    #gen_month_date(mMonthObj)
    
    #   Заканчиваем транзакцию
    mMonthObj.commit()
    
def buildModifPlanByTable(mt, mMonthObj, modifLstFull, dict):
    """
    Создаем структуру модификации плана по подготовленной таблице.
    """
    #   Создаем структуру
    kwarg = {}
    for rec in mt:
        #spar, (summa, kol) = rec
        spar, val = rec
        par = eval(spar)
        #print '!!!!!!!!!!!!!',modifLst,par
        for i, el in enumerate(par):
            kwarg[modifLstFull[i+3]] = el
                
        fo = GetOrCreateMetaPlanObj(mMonthObj, dict, modifLstFull, init_value, **kwarg)
    
    #   Прописываем суммы
    for rec in mt:
        #spar, (summa, kol) = rec
        spar, val = rec
        par = eval(spar)
        #print '11111111111111',modifLst,par
        for i, el in enumerate(par):
            kwarg[modifLstFull[i+3]] = el
            
        fo = ValueMetaPlan(mMonthObj,modifLstFull,set_value, val, **kwarg)

def ValueMetaPlan(metaObj, modifLstFull,set_func, value_, **kwarg):
    """
    Устанавливает сумму многофакторного плана по заданному списку ключей,
        одновременно вычисляя агрегированные суммы.
    """
    typ = metaObj.value.metatype
    if not modifLstFull:
        tps = [cl.value.metatype for cl in metaObj.getMyContainerMetaItems()]
    else:
        tps = getChildTypesByStructPlan(modifLstFull, typ)
    sKeys = set(tps) & set(kwarg.keys())
    #print '!!!!!!!!!!!!!!!!',sKeys
    
    #   Функция инициализации объекта
    set_func(metaObj, value_)
    
    if len(sKeys) > 0:
        tp = list(sKeys)[0]
        key = kwarg[tp]

        #   Если ключа нет, то создаем план с таким именем
        if not key in metaObj.keys():
            return metaObj
        else:
            obj = metaObj[key]
            
        #   Функция инициализации объекта
        #set_func(obj, value_)
        
        return ValueMetaPlan(obj, modifLstFull, set_func, value_, **kwarg)
    else:
        return metaObj

def init_value(x, descr):
    """
    Функция инициализации элемента.
    """
    x.value.description = descr
    x.value.analitic={}
    x.value.zayavki={}
    x.value.pay={}
    
def set_value(metaObj,value):
    """
    Установление значения/свойств метаобъекта с разносом сумм.
    """
    #Планы
    #metaObj.value.summa += value['summa']
    #metaObj.value.kol += value['kol']

    #Факты
    for key,val in value['analitic'].items():
        if metaObj.value.analitic.has_key(key):
            metaObj.value.analitic[key]=[metaObj.value.analitic[key][0]+val[0],
                metaObj.value.analitic[key][1]+val[1]]
        else:
            metaObj.value.analitic[key]=val
            
    for key,val in value['zayavki'].items():
        if metaObj.value.zayavki.has_key(key):
            metaObj.value.zayavki[key]=[metaObj.value.zayavki[key][0]+val[0],
                metaObj.value.zayavki[key][1]+val[1]]
        else:
            metaObj.value.zayavki[key]=val

    for key,val in value['pay'].items():
        if metaObj.value.pay.has_key(key):
            metaObj.value.pay[key]=[metaObj.value.pay[key][0]+val[0],
                metaObj.value.pay[key][1]+val[1]]
        else:
            metaObj.value.pay[key]=val

def recount_fact(metaObj, bIndicator=True, bSave=True):
    """
    Пересчитывает суммы родительских фактов.
    """
    #parentObj = metaObj._Parent
    #print '......!!!',metaObj.name,len(metaObj.values())

    if not metaObj.isRoot():
        #   Вычисляем суммы
        analiticS=0
        analiticSk=0

        zayavkiS=0
        zayavkiSk=0
        
        payS=0
        paySk=0

        lst = metaObj.values()
            
        for el in lst:
            analiticS += el.value.analitic['summa'][0]
            analiticSk += el.value.analitic['summa'][1]

            zayavkiS += el.value.zayavki['summa'][0]
            zayavkiSk += el.value.zayavki['summa'][1]
            
            payS += el.value.pay['summa'][0]
            paySk += el.value.pay['summa'][1]
        

        metaObj.value.analitic['summa'] = [analiticS,analiticSk]
        metaObj.value.zayavki['summa'] = [zayavkiS,zayavkiSk]
        metaObj.value.pay['summa'] = [payS,paySk]
        print 'recount_fact::::',metaObj.name,\
            metaObj.value.analitic['summa'],\
            metaObj.value.zayavki['summa'],\
            metaObj.value.pay['summa']
            
        #   Рекурсивно вычисляем суммы в родительских элементах
        recount_fact(metaObj._Parent, False, bSave)
        
    #   У корневого элемента вызываем функцию синхронизации
    elif bSave:
        metaObj.SaveAllChildren()

def gen_month_date(MonthObj_):
    """
    Пересчет сум по дням для месячного плана.
    """
    children=MonthObj_.values()
    
    analiticD=copy.deepcopy(MonthObj_.value.analitic)
    zayavkiD=copy.deepcopy(MonthObj_.value.zayavki)
    payD=copy.deepcopy(MonthObj_.value.pay)
    
    for child in children:
    
        for date in child.value.analitic.keys():
            if date<>'summa':
                if analiticD.has_key(date):
                    analiticD[date][0]+=child.value.analitic[date][0]
                    analiticD[date][1]+=child.value.analitic[date][1]
                else:
                    analiticD[date]=child.value.analitic[date]
    
        for date in child.value.zayavki.keys():
            if date<>'summa':
                if zayavkiD.has_key(date):
                    zayavkiD[date][0]+=child.value.zayavki[date][0]
                    zayavkiD[date][1]+=child.value.zayavki[date][1]
                else:
                    zayavkiD[date]=child.value.zayavki[date]
                    
        for date in child.value.pay.keys():
            if date<>'summa':
                if payD.has_key(date):
                    payD[date][0]+=child.value.pay[date][0]
                    payD[date][1]+=child.value.pay[date][1]
                else:
                    payD[date]=child.value.pay[date]
                    
    MonthObj_.value.analitic.update(analiticD)
    MonthObj_.value.zayavki.update(zayavkiD)
    MonthObj_.value.pay.update(payD)
    
@ic_proccess_dlg.proccess2_noparent_deco
def loadDataPlanModif(metaclass,year,month):
    """
    Загрузка данных в дерево планов.
    @param metaclass: Метакласс базового метаплана.
    """
    #Сначала закачать данные в базовый план
    #result=refreshSumm(metaclass.getObject(),year,month)
    ic_cache.systemCache.clear()

    main_win=ic_user.icGetMainWin()
    #Обновить модификации
    modif_lst=IODBSprav.getModifLst()
    #print 'loadDataPlan:::',modif_lst,result

    if modif_lst:
        for i,modif_plan in enumerate(modif_lst):
            ic_proccess_dlg.SetProccessBoxLabel(label2='Год: %s Месяц: %s Генерация модификаций планов'%(year,month),
                value2=float(100.0/len(modif_lst))*i)
            generateModifPlan(main_win,metaclass,modif_plan[0],year,month)
