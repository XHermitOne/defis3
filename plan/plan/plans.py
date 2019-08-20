#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль управления планами.
"""

import wx
import time

from NSI import spravfunc
# from ic.db import ic_tabview
# import ic.db.ic_sqlobjtab as ic_sqlobjtab
# from sqlobject import AND

# Версия
__version__ = (0, 1, 1, 1)

# --- Константы ---
# Имя таблицы планов
PLAN_TAB_NAME_DEFAULT = 'plan'

#   Буфера значений весовых коэфициентов
WBuffValueDictF1 = {'000': 1}
WBuffValueDictF2 = {'000': 1}

SumPlanValueDict = {}
KolPlanValueDict = {}


def ClearWBuff():
    """
    Чистит буфера весовых коэфициентов.
    """
    global WBuffValueDictF1
    global WBuffValueDictF2

    WBuffValueDictF1 = {'000': 1}
    WBuffValueDictF2 = {'000': 1}


def ClearPlanBuff():
    """
    Чистит буфера плановых значений.
    """
    global SumPlanValueDict
    global KolPlanValueDict

    SumPlanValueDict = {}
    KolPlanValueDict = {}


# --- Функции ---
def getPlanTabName():
    """
    Имя таблицы планов.
    """
    return PLAN_TAB_NAME_DEFAULT


def getPlanByDate(Date_, Param_, Type_):
    """
    План по параметру на определенную дату.
    @param Date_: Указание даты в строковом формате.
    @param Param_: Имя параметра.
    @param Type_: Тип плана.
    """
    return None


# --- Функции генерации информации о планах
def countPlanTableWeight(month=None, year=None, table='analitic',
                         view='realize_sum'):
    """
    Функция вычисляет относительную долю каждого вида продукции в сумме и в массе
    за месяц (поля f1 и f2 справочника <Product>). Вычисленные доли прописываются в
    справочнике видов продукции и в последствии используются для генерации планов
    по общим месячным планам.

    @type month: C{int}
    @param month: Номер месяца, по которому вычисляются параметры.
    @type year: C{string}
    @param year: Номер года.
    @type table: C{string}
    @param table: Имя таблицы, по которой вычисляются долевые параметры.
    @type view: C{string}
    @param view: Имя таблицы из которой берется общая сумма.
    """
    tm = wx.DefaultDateTime
    if not month:
        month = tm.GetMonth()+1
    if not year:
        year = tm.GetYear()
    
    dt = '%s.%s' % (str(year), ('00'+str(month))[-2:])

    print('--->>> countPlanTableWeight')
    print('..... dt=', dt)
    
    # --- Вычисляем общую сумму
    view = ic_tabview.icSQLObjTabView(view)
    rs = view.select(view.q.dtoper.startswith(dt))
    sum = 0
    kol = 0
    
    if rs.count() > 0:
        for r in rs:
            sum += r.summa
            kol += r.kolf
    
    # --- Для каждого вида продукции вычисляем сумму
    if sum and kol:
        # print '..... Optional Sum=', sum
        t1 = time.clock()
        tab = ic_sqlobjtab.icSQLObjTabClass(table)

        #   Буферизируем отобранные строки
        tab_rs = tab.select(tab.q.dtoper.startswith(dt))
        # tab_buff = ic_sqlobjtab.getRecBuffList(tab_rs, ('codt', fld,))
        
        # spr_buff = ic_sqlobjtab.getRecBuffList(spr_rs, ('cod',))
        spr_dict = spravfunc.getReplDict('Product', 'cod', 'f2')
        spr = ic_sqlobjtab.icSQLObjTabClass(spravfunc.getNsiStdClassName())
        spr_rs = spr.select(spr.q.type == 'Product')
        spr_dict = {}
        
        if spr_rs.count() > 0:
            for r in spr_rs:
                spr_dict[r.cod] = [0, 0]
                
        spr_dict['000'] = 0
        dictkeys = spr_dict.keys()
        
        for r in tab_rs:
            cod = r.codt.strip()
            r_sum = r.summa
            r_kol = r.kolf
            
            if cod in dictkeys:
                spr_dict[cod][0] += r_sum
                spr_dict[cod[:3]][0] += r_sum
                spr_dict[cod][1] += r_kol
                spr_dict[cod[:3]][1] += r_kol
            else:
                print('-->>> UNKNOWN COD=<%s> in table=<%s>' % (cod, table))
        
        if spr_rs.count() > 0:  # and tab_buff:
            for r in spr_rs:
                cod = r.cod
                cod_sum, kol_sum = spr_dict[cod]
                r.f1 = val = cod_sum/sum
                r.f2 = kol_sum/kol
                
                # print '.....  %s.f1=%function' % (cod, val)
        t7 = time.clock()
        
    print('.....End Update Sum=', sum, t7-t1)


def countSumMonthPlan(cod, month=None, year=None, view='realize_sum'):
    """
    Генерируется месячный план по виду продукции в денежном эквиваленте.

    @type cod: C{string}
    @param cod: Код вида продукции.
    @type month: C{int}
    @param month: Номер месяца, по которому вычисляются параметры.
    @type year: C{string}
    @param year: Номер года.
    @type view: C{string}
    @param view: Имя таблицы из которой берется общая сумма.
    """
    tm = wx.DefaultDateTime
    
    if not month:
        month = tm.GetMonth()+1
    
    if not year:
        year = tm.GetYear()
        
    dt = '%s.%s' % (str(year), ('00'+str(month))[-2:])
    
    #   Получаем относительную долю вклада данного вида продукции в общую сумму
    if cod in WBuffValueDictF1:
        w = WBuffValueDictF1[cod]
    else:
        w = spravfunc.FSprav('Product', cod, 'f1')
        WBuffValueDictF1[cod] = w
        
    # print '...weight=', w
    #   Определяем общую сумму плана из таблицы планов
    #   Если план не определен, то берем общую сумму за предыдущий период
    try:
        return w * SumPlanValueDict['000'][dt]
    except:
        if '000' not in SumPlanValueDict:
            SumPlanValueDict['000'] = {}
            
        if dt not in SumPlanValueDict['000']:
            SumPlanValueDict['000'][dt] = None
        
        tab = ic_sqlobjtab.icSQLObjTabClass('plan')
        rs = tab.select(AND(tab.q.typ_plan == 'P3', tab.q.do_date.startswith(dt),
                        tab.q.param.startswith('000')))
        
        if rs.count() > 0:
            print('....>>> w, summa=', w, rs[0].p_val)
            SumPlanValueDict['000'][dt] = w*rs[0].p_val
            return SumPlanValueDict['000'][dt]
            
        #   Если план не найден берем общую сумму за за последний месяц
        else:
            view = ic_tabview.icSQLObjTabView(view)
            if month > 1:
                dtl = '%s.%s' % (str(year), ('00'+str(month-1))[-2:])
            else:
                dtl = '%s.12' % (str(year-1),)
                
            rs = view.select(view.q.dtoper.startswith(dtl))
            if rs.count() > 0:
                sum = 0
                for r in rs:
                    sum += r.summa
            
                print('....>>> w, summa=', w, sum)
                SumPlanValueDict['000'][dt] = w*sum
                return w*sum
        
    return None


def countKolMonthPlan(cod, month=None, year=None, view='realize_sum'):
    """
    Вычисляется месячный план по виду продукции в натуральном выражении (в кг.).

    @type cod: C{string}
    @param cod: Код вида продукции.
    @type month: C{int}
    @param month: Номер месяца, по которому вычисляются параметры.
    @type year: C{string}
    @param year: Номер года.
    @type view: C{string}
    @param view: Имя таблицы из которой берется общая сумма.
    """
    tm = wx.DefaultDateTime
    
    if not month:
        month = tm.GetMonth()+1
    
    if not year:
        year = tm.GetYear()
        
    dt = '%s.%s' % (str(year), ('00'+str(month))[-2:])
    
    #   Получаем относительную долю вклада данного вида продукции в общую сумму
    if cod in WBuffValueDictF2:
        w = WBuffValueDictF2[cod]
    else:
        w = spravfunc.FSprav('Product', cod, 'f2')
        WBuffValueDictF2[cod] = w
        
    #   Определяем общую сумму плана из таблицы планов
    #   Если план не определен, то берем общую сумму за предыдущий период
    try:
        return w*KolPlanValueDict['000'][dt]
    except:
        if '000' not in KolPlanValueDict:
            KolPlanValueDict['000'] = {}
            
        if dt not in KolPlanValueDict['000']:
            KolPlanValueDict['000'][dt] = None

        tab = ic_sqlobjtab.icSQLObjTabClass('plan')
        rs = tab.select(AND(tab.q.typ_plan == 'K3', tab.q.do_date.startswith(dt),
                        tab.q.param.startswith('000')))
        
        if rs.count() > 0:
            # print '....>>> w, plan K3 =', w, rs[0].p_val
            KolPlanValueDict['000'][dt] = w*rs[0].p_val
            return KolPlanValueDict['000'][dt]
            
        #   Если план не найден берем общую сумму за за предыдущий месяц
        else:
            view = ic_tabview.icSQLObjTabView(view)
            if month > 1:
                dtl = '%s.%s' % (str(year), ('00'+str(month-1))[-2:])
            else:
                dtl = '%s.12' % (str(year-1),)
                
            rs = view.select(view.q.dtoper.startswith(dtl))
            if rs.count() > 0:
                kol = 0
                for r in rs:
                    kol += r.kolf
    
                print('....>>> w, summa=', w, kol)
                KolPlanValueDict['000'][dt] = w*kol
                return w*kol
        
    return None


def countSumDayPlan(cod, day=None, month=None, year=None, view='realize_sum'):
    """
    Вычисляется суточный план по виду продукции в натуральном выражении (в кг.).

    @type cod: C{string}
    @param cod: Код вида продукции.
    @type day: C{int}
    @param day: День месяца.
    @type month: C{int}
    @param month: Номер месяца, по которому вычисляются параметры.
    @type year: C{string}
    @param year: Номер года.
    @type view: C{string}
    @param view: Имя таблицы из которой берется общая сумма.
    """
    #   Планируется, что можно посмотреть дневной план, но только кто его будет
    #   заполнять, поэтому эта возможность пока не реализована
    
    #   Находим значение месячного плана и делим на количество календарных дней
    #   в заданном месяце
    result = countSumMonthPlan(cod, month, year, view)
    if result is None:
        return None

    tm = wx.DefaultDateTime

    if not month:
        month = tm.GetMonth()+1
    if not year:
        year = tm.GetYear()
    
    nd = wx.DateTime.GetNumberOfDaysInMonth(month, year)
    return result/nd


def countKolDayPlan(cod, day=None, month=None, year=None, view='realize_sum'):
    """
    Вычисляется суточный план по виду продукции в натуральном выражении (в кг.).

    @type cod: C{string}
    @param cod: Код вида продукции.
    @type day: C{int}
    @param day: День месяца.
    @type month: C{int}
    @param month: Номер месяца, по которому вычисляются параметры.
    @type year: C{string}
    @param year: Номер года.
    @type view: C{string}
    @param view: Имя таблицы из которой берется общая сумма.
    """
    #   Планируется, что можно посмотреть дневной план, но только кто его будет
    #   заполнять, поэтому эта возможность пока не реализована
    
    #   Находим значение месячного плана и делим на количество календарных дней
    #   в заданном месяце
    result = countKolMonthPlan(cod, month, year, view)
    if result is None:
        return None
        
    tm = wx.DefaultDateTime

    if not month:
        month = tm.GetMonth()+1
    if not year:
        year = tm.GetYear()
    
    nd = wx.DateTime.GetNumberOfDaysInMonth(month, year)

    return result/nd


# --- Дополнительные функции ---
def getPlanSumm(Type_='Product'):
    """
    Получение/расчет базисной суммы для расчетов планов.
    """
    plan_tab = ic_sqlobjtab.icSQLObjTabClass('plan')
    sql_txt = 'SELECT SUM(p_val) FROM plan WHERE typ_param=\'%s\'' % Type_
    print('getPlanSumm SQL:', sql_txt)
    plan_sum = plan_tab.execute(sql_txt)[0][0]
    return plan_sum
