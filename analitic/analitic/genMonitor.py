#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Функции генерации мониторов.
"""


# --- Подключение библиотек ---
from ic.prj import ctrlPrj
from ic.dlg import ic_dlg

# import NSI.spravfunc

# Версия
__version__ = (0, 1, 1, 1)


# --- Функции ---
def genViewZayavkiName(Type_, Cod_):
    """
    Генерация имен представлений по заявкам.
    """
    return 'vz'+str(Type_)+str(Cod_)


def genViewRealizeName(Type_, Cod_):
    """
    Генерация имен представлений по реализации.
    """
    return 'vr'+str(Type_)+str(Cod_)


def genViewPayName(Type_, Cod_):
    """
    Генерация имен представлений по оплате.
    """
    return 'vp'+str(Type_)+str(Cod_)


_SpravType2SQLWhere = {'Product': 'SUBSTR(codt,1,3)',
                       'Menager': 'mens',
                       'Region': 'reg',
                       }


def genViewZayavki(Type_, Cod_, PrototypeName_='zayavki_sum'):
    """
    Генерация представлений по заявкам.
    """
    view_name = genViewZayavkiName(Type_,Cod_)
 
    prj_res_ctrl = ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    # Проверка на добавление нового ресурса
    if not prj_res_ctrl.isRes(view_name, 'vid'):
        view_res = prj_res_ctrl.loadResClone(PrototypeName_,'vid')
        # Установка свойств
        view_res['name'] = view_name
        view_res['table'] = view_name.lower()
        view_res['prototype'] = 'zayavki'
        view_res['query'] = '''
SELECT 
    dtoper,
    NULL as grup,
    NULL AS codt,
    NULL AS ei,
    SUM(kolf) AS kolf,
    NULL AS cena,
    SUM(summa) AS summa,
    NULL AS reg,
    NULL AS mens,
    NULL AS plan_kol,
    NULL AS plan_sum 
FROM zayavki 
    WHERE %s LIKE('%s')
    GROUP BY dtoper
    ''' % (_SpravType2SQLWhere[Type_], Cod_)
        prj_res_ctrl.saveRes(view_name, 'vid', view_res)
    return view_name


def genViewRealize(Type_, Cod_, PrototypeName_='realize_sum'):
    """
    Генерация представлений по реализации.
    """
    view_name = genViewRealizeName(Type_, Cod_)
 
    prj_res_ctrl = ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    # Проверка на добавление нового ресурса
    if not prj_res_ctrl.isRes(view_name, 'vid'):
        view_res = prj_res_ctrl.loadResClone(PrototypeName_, 'vid')
        # Установка свойств
        view_res['name'] = view_name
        view_res['table'] = view_name.lower()
        view_res['prototype'] = 'analitic'
        view_res['query'] = '''
SELECT 
    dtoper,
    NULL as grup,
    NULL AS codt,
    NULL AS ei,
    SUM(kolf) AS kolf,
    NULL AS cena,
    SUM(summa) AS summa,
    NULL AS reg,
    NULL AS mens,
    NULL AS plan_kol,
    NULL AS plan_sum 
FROM analitic 
WHERE %s LIKE('%s')
GROUP BY dtoper
    ''' % (_SpravType2SQLWhere[Type_], Cod_)
        prj_res_ctrl.saveRes(view_name, 'vid', view_res)
    return view_name


def genViewPay(Type_, Cod_, PrototypeName_='pay_sum'):
    """
    Генерация представлений по оплате.
    """
    view_name = genViewPayName(Type_, Cod_)
 
    prj_res_ctrl = ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    # Проверка на добавление нового ресурса
    if not prj_res_ctrl.isRes(view_name, 'vid'):
        view_res = prj_res_ctrl.loadResClone(PrototypeName_, 'vid')
        # Установка свойств
        view_res['name'] = view_name
        view_res['table'] = view_name.lower()
        view_res['prototype'] = 'pay'
        view_res['query'] = '''
SELECT 
    dtoper,
    NULL as grup,
    NULL AS codt,
    NULL AS ei,
    SUM(kolf) AS kolf,
    NULL AS cena,
    SUM(summa) AS summa,
    NULL AS reg,
    NULL AS mens,
    NULL AS plan_kol,
    NULL AS plan_sum 
FROM pay 
WHERE %s LIKE('%s')
GROUP BY dtoper
    ''' % (_SpravType2SQLWhere[Type_], Cod_)
        prj_res_ctrl.saveRes(view_name, 'vid', view_res)
    return view_name


# --- Генерация имен полей аналитики ---
_SpravType2AnaliticFieldName = {'Product': 'codt',
                                'Region': 'reg',
                                'Menager': 'mens'}


def genFieldName(Type_):
    """
    Сгенерировать имя поля аналитики по видам продукции.
    """
    return _SpravType2AnaliticFieldName.setdefault(Type_, 'dtoper')
    

# --- Создание монитора в системе ---
_SpravType2MonitorCode = {'Product': 'ПР',
                          'Region': 'РГ',
                          'Menager': 'МН'}


def genMonitorCode(Type_, Cod_):
    """
    Генерация кода монитора.
    """
    cod_dir = _SpravType2MonitorCode.setdefault(Type_,'ПЧ')
    _NsiStd = ic_sqlobjtab.icSQLObjTabClass(NSI.spravfunc.getNsiStdClassName())
    max_cod=_NsiStd.execute("""SELECT MAX(SUBSTR(cod,3,LENGTH(cod)-2)) 
        FROM nsi_std 
        WHERE type='Monitors' AND SUBSTR(cod,1,2) LIKE('%s')"""%(cod_dir))[0][0]
    #print 'genMonitorCode',max_cod,cod_dir+'%02d'%(int(max_cod)+1)
    if not max_cod:
        max_cod='00'
    return cod_dir+('%02d'%(int(max_cod)+1))[:2]
    
def createMonitor(Name_,Type_,Cod_):
    """
    Создание монитора в системе.
    """
    #Создать представления
    genViewZayavki(Type_,Cod_)
    genViewRealize(Type_,Cod_)
    genViewPay(Type_,Cod_)
    
    #Прописать монитор в справочнике мониторов
    monitor_cod=genMonitorCode(Type_,Cod_)
    monitor_lst_id=NSI.spravfunc.getSpravId('Monitors')
    _NsiStd=ic_sqlobjtab.icSQLObjTabClass(NSI.spravfunc.getNsiStdClassName())
    _NsiStd.add(type='Monitors',id_nsi_list=monitor_lst_id,
        cod=monitor_cod,name=Name_,
        count=0,access='',
        s1='',s2='',s3='(\'%s\',\'%s\')'%(Type_,Cod_),s4='',s5='',
        n1=0,n2=0,n3=0,n4=0,n5=0,
        f1=0.0,f2=0.0,f3=0.0)
        
    if ic_dlg.icAskDlg('?','Произвести обновление данных'):
        refreshAllView(Type_,Cod_)

def refreshAllView(Type_,Cod_):
    """
    Обновление всех представлений.
    """
    name=genViewZayavkiName(Type_,Cod_)
    view=ic_tabview.icSQLObjTabView(name)
    view.refreshView()
    name=genViewRealizeName(Type_,Cod_)
    view=ic_tabview.icSQLObjTabView(name)
    view.refreshView()
    name=genViewPayName(Type_,Cod_)
    view=ic_tabview.icSQLObjTabView(name)
    view.refreshView()
    
#--- Удаление мониторов из системы ---
def delViewZayavki(Type_,Cod_):
    """
    Удалить представление монитора по заявкам.
    """
    view_name=genViewZayavkiName(Type_,Cod_)
 
    prj_res_ctrl=ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    #удаление ресурса
    prj_res_ctrl.delRes(view_name,'vid')
    return view_name
    
def delViewRealize(Type_,Cod_):
    """
    Удалить представление монитора по реализации.
    """
    view_name=genViewRealizeName(Type_,Cod_)
 
    prj_res_ctrl=ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    #удаление ресурса
    prj_res_ctrl.delRes(view_name,'vid')
    return view_name
    
def delViewPay(Type_,Cod_):
    """
    Удалить представление монитора по оплате.
    """
    view_name=genViewPayName(Type_,Cod_)
 
    prj_res_ctrl=ctrlPrj.icProjectResManager()
    prj_res_ctrl.openPrj()
    
    #удаление ресурса
    prj_res_ctrl.delRes(view_name,'vid')
    return view_name
    
def delMonitor(MonitorCode_):
    """
    Удалить монитор из системы.
    """
    #Нельзя удалять верхний уровень!!!
    if len(MonitorCode_)<=2:
        return
        
    #Взять монитор из справочника мониторов.
    monitor_dict=NSI.spravfunc.FSprav('Monitors',MonitorCode_,
        ['cod','name','s1','s2','s3'])
    #Удалить в справочнике
    ok=NSI.spravfunc.DelSprav('Monitors',MonitorCode_)
    #Удалить представления
    if monitor_dict['s3'] and ok:
        typ,cod=eval(monitor_dict['s3'])
        delViewZayavki(typ,cod)
        delViewRealize(typ,cod)
        delViewPay(typ,cod)
