#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль методов расчетов планов.
"""

# --- Подключение библиотек ---
import time
import wx

from plan.interfaces import IODBSprav
from . import plans

# Версия
__version__ = (0, 1, 1, 1)


# --- Функции ---
def calcKoeffPlan1(Type_,BasisSumm_=None):
    """
    Метод1. Расчет планов в соответствии с весовыми коэффициентами.
    @param Type_: Тип параметра наблюдения. Код справочника.
    @param BasisSumm_: Значение основной расчетной суммы.
        Если она None, то эта сумма расчитывается
        стандартной функцией.
    """
    if BasisSumm_ is None:
        BasisSumm_ = plans.getPlanSumm()
        
    sql_txt = '''UPDATE plan
                 SET p_val=%f*koeff
                 WHERE typ_param=\'%s\';
                 SELECT * FROM plan;
                ''' % (BasisSumm_, Type_)
    print('calcKoeffPlan1 SQL:', sql_txt)
    
    plan_tab = ic_sqlobjtab.icSQLObjTabClass('plan')
    plan_tab.execute(sql_txt)


# --- Функции возвращает плановые значения из дерева планов
def SearchObj(metaObj, **kwarg):
    """
    Поиск по дереву нужного значенич.
    """
    typ = metaObj.value.metatype
    print(' .... before getMyContainerMetaItems()', typ)
    print(' ... metaObj.getMyContainerMetaItems()=', metaObj.getMyContainerMetaItems())
    tps = [cl.value.metatype for cl in metaObj.getMyContainerMetaItems()]
    sKeys = set(tps) & set(kwarg.keys())
    # print '<SearchObj in Meta Type=>', typ, metaObj.keys(), sKeys
    
    if not metaObj.keys():
        return metaObj
    elif len(sKeys) > 0:
        key = kwarg[list(sKeys)[0]]
        # print '<key=>:', key, metaObj[key]
        if key in metaObj:
            return SearchObj(metaObj[key], **kwarg)
        else:
            print('### Search object in <%s> KEY_ERROR: invalid key=%s' % (metaObj.value.metatype, key))
            raise Exception
    else:
        return metaObj


def getDayPlanValue(date, metaObj, **kwarg):
    """
    Вычисляет дневной план.
    
    @type date: C{string}
    @param date: Дата планового значения в виде гггг.мм.чч.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    codYear = date[:4]
    codMonth = 'm%s' % date[5:7]
    kwarg['mYear'] = codYear
    kwarg['mMonth'] = codMonth
    obj = SearchObj(metaObj, **kwarg)
    #   Если нужный элемент плана найден
    if obj:
        #   Используем месячные декадные параметры
        decadWeight = metaObj.getRoot()[codYear][codMonth].value.decadWeight
        if day <= 10:
            idec = 0
            decdays = 10
        elif day <= 20:
            idec = 1
            decdays = 10
        else:
            idec = 2
            decdays = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)-20

        S = reduce(lambda x,y: x+y, decadWeight)
        kwart_par = decadWeight[idec]
        return obj.value.summa/decdays*kwart_par/S


def getDayPlanKol(date, metaObj, **kwarg):
    """
    Вычисляет дневной план по количеству.
    
    @type date: C{string}
    @param date: Дата планового значения в виде гггг.мм.чч.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    codYear = date[:4]
    codMonth = 'm%s' % date[5:7]
    kwarg['mYear'] = codYear
    kwarg['mMonth'] = codMonth
    obj = SearchObj(metaObj, **kwarg)

    #   Если нужный элемент плана найден
    if obj:
        #   Используем месячные декадные параметры
        decadWeight = metaObj.getRoot()[codYear][codMonth].value.decadWeightKol
        if day <= 10:
            idec = 0
            decdays = 10
        elif day <= 20:
            idec = 1
            decdays = 10
        else:
            idec = 2
            decdays = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)-20

        S = reduce(lambda x,y: x+y, decadWeight)
        kwart_par = decadWeight[idec]
        return obj.value.kol/decdays*kwart_par/S


def getPlanMarja(metaObj):
    """
    Возвращает маржу текущего элемента плана. Если маржинальный коэфициент не
    определен, то наследуем родительский коэфициент.
    """
    if metaObj.value.marja:
        return metaObj.value.marja
    
    elif metaObj.getItemParent():
        return getPlanMarja(metaObj.getItemParent())


def getDayPlanMarja(date, metaObj, **kwarg):
    """
    Возвращает планируемую маржу за день.
    """
    marja_par = getPlanMarja(metaObj)
    
    if marja_par:
        return getDayPlanValue(date, metaObj, **kwarg)*marja_par
