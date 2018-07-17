#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Некоторые опрделения и функции стрелочного индикатора.
"""

#   Типы планов
DAY_PLAN_TYPE = 0
MONTH_PLAN_TYPE = 1
QUARTER_PLAN_TYPE = 2
YEAR_PLAN_TYPE = 3

#   Описания типов накопления
AGR_TYPE_USUAL = 0
AGR_TYPE_DAY = 1
AGR_TYPE_MONTH = 2
AGR_TYPE_QUARTER = 3
AGR_TYPE_YEAR = 4
AGR_TYPE_PERIOD = 5

#   Описание функций накопления
AGR_FUNC_SUM = 0
AGR_FUNC_MIN = 1
AGR_FUNC_MAX = 2
AGR_FUNC_AVRG = 3
AGR_FUNC_DISP = 4

aggregationTypeDict ={'USUAL': AGR_TYPE_USUAL,
                      'DAY': AGR_TYPE_DAY,
                      'MONTH': AGR_TYPE_MONTH,
                      'QUARTER': AGR_TYPE_QUARTER,
                      'YEAR': AGR_TYPE_YEAR,
                      'PERIOD': AGR_TYPE_PERIOD,
                      'Обычный': AGR_TYPE_USUAL,
                      'День': AGR_TYPE_DAY,
                      'Месяц': AGR_TYPE_MONTH,
                      'Квартал': AGR_TYPE_QUARTER,
                      'Год': AGR_TYPE_YEAR,
                      'Период': AGR_TYPE_PERIOD}

aggregationFuncDict = {'SUM': AGR_FUNC_SUM,
                       'MIN': AGR_FUNC_MIN,
                       'MAX': AGR_FUNC_MAX,
                       'AVRG': AGR_FUNC_AVRG,
                       'DISP': AGR_FUNC_DISP,
                       'Сумма': AGR_FUNC_SUM,
                       'Минимум': AGR_FUNC_MIN,
                       'Максимум': AGR_FUNC_MAX,
                       'Среднее': AGR_FUNC_AVRG,
                       'Дисперсия': AGR_FUNC_DISP}


_buff_last_value = {}

__version__ = (0, 0, 0, 2)


# --- Функции агрегации
def _get_day_plan(date, cod):
    """
    """
    global _buff_last_value
    ret = None
    
    if cod == 'plan_sum':
        ret = 2000000.0
    elif cod == 'plan_kol':
        ret = 20000.0
    
    if ret is not None and cod is not None:
        _buff_last_value[cod] = ret
        return ret
    elif cod in _buff_last_value:
        return _buff_last_value[cod]


def _sum_func_agr(rs, parTime, par, parPlan=None, t1=None, t2=None,
                  cod=None, funcPlan=None):
    """
    Функция суммирования параметра.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type par: C{string}
    @param par: Имя накапливаемого параметра.
    @type parPlan: C{string}
    @param parPlan: Имя накапливаемого параметра плана.
    @type t1: C{string}
    @param t1: Начало периода агрегации ('2005.10.10').
    @type t2: C{string}
    @param t2: Конец периода агрегации ('2005.12.31').
    @type cod: C{string}
    @param cod: Код наблюдаемого параметра.
    @type funcPlan: C{function}
    @param funcPlan: Функция, вычисляющая плановые значения за день.
    """
    sum = 0.0
    plan = 0.0

    for r in rs:
        tm = getattr(r, parTime)
        
        if (t1 is None and t2 is None) or (t1 <= tm <= t2):
            try:
                sum += float(getattr(r, par))
            except TypeError:
                print(u'### TYPE ERROR par = %s' % par)
                print(u'### getattr(r, par) = %s' % getattr(r, par))
                
            if parPlan:
                v = getattr(r, parPlan)
                
                #   Если план определен
                if v is not None:
                    plan += float(v)
                    
                #   Если плановое значение не определено
                else:
                    if funcPlan:
                        yy, mm, dd = [int(x) for x in tm.split('.')]
                        _val = funcPlan(cod, dd, mm, yy)
                    else:
                        _val = _get_day_plan(tm, parPlan)
                    
                    if _val is not None:
                        plan += _val

    if parPlan:
        return sum, plan
    else:
        return sum, None


def _min_func_agr(rs, parTime, par, parPlan=None, t1=None, t2=None,
                  cod=None, funcPlan=None):
    """
    Функция находим минимальное значение параметра.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type par: C{string}
    @param par: Имя накапливаемого параметра.
    @type parPlan: C{string}
    @param parPlan: Имя накапливаемого параметра плана.
    @type t1: C{string}
    @param t1: Начало периода агрегации ('2005.10.10').
    @type t2: C{string}
    @param t2: Конец периода агрегации ('2005.12.31').
    @type cod: C{string}
    @param cod: Код наблюдаемого параметра.
    @type funcPlan: C{function}
    @param funcPlan: Функция, вычисляющая плановые значения за день.
    """
    min = None
    plan = None
    
    for r in rs:
        tm = getattr(r, parTime)
        
        if (t1 is None and t2 is None) or (t1 <= tm <= t2):
            v = float(getattr(r, par))
            
            if min is None or min > v:
                min = v
    
            if parPlan:
                vp = getattr(r, parPlan)
                if vp is not None:
                    vp = float(vp)
                else:
                    vp = _get_day_plan(tm, parPlan)
                    
                if vp is not None and (plan is None or plan > vp):
                    plan = vp

    return min, plan


def _max_func_agr(rs, parTime, par, parPlan=None, t1=None, t2=None,
                  cod=None, funcPlan=None):
    """
    Функция находим максимальнове значение параметра.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type par: C{string}
    @param par: Имя накапливаемого параметра.
    @type parPlan: C{string}
    @param parPlan: Имя накапливаемого параметра плана.
    @type t1: C{string}
    @param t1: Начало периода агрегации ('2005.10.10').
    @type t2: C{string}
    @param t2: Конец периода агрегации ('2005.12.31').
    @type cod: C{string}
    @param cod: Код наблюдаемого параметра.
    @type funcPlan: C{function}
    @param funcPlan: Функция, вычисляющая плановые значения за день.
    """
    max = None
    plan = None
    
    for r in rs:
        tm = getattr(r, parTime)
        
        if (t1 is None and t2 is None) or (t1 <= tm <= t2):
            v = float(getattr(r, par))
            
            if max is None or max < v:
                max = v
    
            if parPlan:
                vp = getattr(r, parPlan)
                if vp is not None:
                    vp = float(vp)
                else:
                    vp = _get_day_plan(tm, parPlan)
            
                if vp is not None and (plan is None or plan < vp):
                    plan = vp

    return max, plan


def _avrg_func_agr(rs, parTime, par, parPlan=None, t1=None, t2=None,
                   cod=None, funcPlan=None):
    """
    Функция находим среднее значение параметра.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type par: C{string}
    @param par: Имя накапливаемого параметра.
    @type parPlan: C{string}
    @param parPlan: Имя накапливаемого параметра плана.
    @type t1: C{string}
    @param t1: Начало периода агрегации ('2005.10.10').
    @type t2: C{string}
    @param t2: Конец периода агрегации ('2005.12.31').
    @type cod: C{string}
    @param cod: Код наблюдаемого параметра.
    @type funcPlan: C{function}
    @param funcPlan: Функция, вычисляющая плановые значения за день.
    """
    sum = 0
    plan = 0
    count = 0
    
    for r in rs:
        tm = getattr(r, parTime)
        
        if (t1 is None and t2 is None) or (t1 <= tm <= t2):
            sum += float(getattr(r, par))
            count += 1
            
            if parPlan:
                v = getattr(r, parPlan)
                
                #   Если план определен
                if v is not None:
                    plan += float(v)
                    
                #   Если плановое значение не определено
                else:
                    vp = _get_day_plan(tm, parPlan)
                    if vp is not None:
                        plan += vp
            
    if count > 0:
        sum = sum / count
        
        if parPlan:
            plan = plan/count
            
    if parPlan:
        return sum, plan
    else:
        return sum, None


def _disp_func_agr(rs, parTime, par, parPlan=None, t1=None, t2=None,
                   cod=None, funcPlan=None):
    """
    Функция находит дисперсию значение параметра.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type par: C{string}
    @param par: Имя накапливаемого параметра.
    @type parPlan: C{string}
    @param parPlan: Имя накапливаемого параметра плана.
    @type t1: C{string}
    @param t1: Начало периода агрегации ('2005.10.10').
    @type t2: C{string}
    @param t2: Конец периода агрегации ('2005.12.31').
    @type cod: C{string}
    @param cod: Код наблюдаемого параметра.
    @type funcPlan: C{function}
    @param funcPlan: Функция, вычисляющая плановые значения за день.
    """
    sum = 0
    n = rs.count()
    
    if n > 0:
        buff = range(n)
        buffPlan = range(n)
        
    avrg = None
    plan = 0
    count = 0
    
    #   Находим среднее значение и заодно буферизируем значения параметра.
    for i, r in enumerate(rs):
        tm = getattr(r, parTime)
        
        if (t1 is None and t2 is None) or (t1 <= tm <= t2):
            v = float(getattr(r, par))
            sum += v
            buff[count] = v
            
            if parPlan:
                vp = getattr(r, parPlan)
                
                #   Если план определен
                if vp is not None:
                    vp = float(vp)
                    
                #   Если плановое значение не определено
                else:
                    vp = _get_day_plan(tm, parPlan)
                
                if vp is not None:
                    plan += vp
                    
                buffPlan[count] = vp
                
            count += 1
            
    if count > 0:
        #   Считаем среднее
        avrg = sum / count
        buff = buff[:count]
        
        if parPlan:
            plan = plan / count
    
        #   Считаем дисперсию
        dsp = 0
        dspPlan = 0
        
        for i, v in enumerate(buff):
            dsp += (v - avrg)**2
            if parPlan:
                vp = buffPlan[i]
                
                if vp is not None:
                    dspPlan += (vp - plan)**2
                
        if parPlan:
            print(u'DISPERSION = (%s, %s)' % (dsp/count, dspPlan/count))
            return dsp/count, dspPlan/count
        else:
            return dsp/count, None
        
    return None


aggregationFuncMap = {AGR_FUNC_SUM: _sum_func_agr,
                      AGR_FUNC_MIN: _min_func_agr,
                      AGR_FUNC_MAX: _max_func_agr,
                      AGR_FUNC_AVRG: _avrg_func_agr,
                      AGR_FUNC_DISP: _disp_func_agr}


#   Словарь соответствий месяцов определенному кварталу
ic_month_qwart_indx = {1: 1, 2: 1, 3: 1,
                       4: 2, 5: 2, 6: 2,
                       7: 3, 8: 3, 9: 3,
                       10: 4, 11: 4, 12: 4}
