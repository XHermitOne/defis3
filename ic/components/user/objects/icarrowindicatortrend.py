#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
try:
    import ic.components.icResourceParser as prs
except:
    print('import error icResourceParser')
    
import ic.utils.util as util
import ic.components.icwidget as icwidget
import datetime, time, calendar

import ic.components.user.icArrowIndDef as indDef
import ic.interfaces.icobjectinterface as icobjectinterface

try:
    import matplotlib
    from matplotlib import pylab
    from matplotlib.dates import DayLocator, YearLocator, MonthLocator, HourLocator, MinuteLocator,\
        drange, date2num, timezone, num2date, DateFormatter
    import matplotlib.numerix as numerix
except:
    print('import error matplotlib')
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0414\u0438\u043d\u0430\u043c\u0438\u043a\u0430 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u0430', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'f48916d18ad8e6e3727e7ff38131a9f1', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'f62f8511d5d55f82c368d51a94d2a962', 'proportion': 1, 'name': u'DefaultName_1489', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (500, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'1a40bbf93f76ddf2429e242ec8085add', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(34, 46), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'1e00e20382ffe41544838d5c3108e50e', 'proportion': 0, 'name': u'DefaultName_1120', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'borderRightColor': None, 'child': [], 'refresh': None, 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, 44), 'moveAfterInTabOrder': u'', 'foregroundColor': (10, 83, 220), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u043e\u0434\u043f\u0438\u0441\u044c', 'source': None, 'backgroundColor': (245, 245, 245), 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'', '_uuid': u'c2a34f2008f57e15caf401e2ed1fdf80', 'style': 0, 'flag': 8192, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 1, 'borderLeftColor': None, 'name': u'titleCtrl', 'borderBottomColor': (10, 83, 220), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'refresh': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Trend', '_uuid': u'febc0ec6c3076101ae5fb3e3bf7813df', 'onDrawCursor': u"a=''", 'style': 0, 'wxAgg': 3, 'flag': 8192, 'recount': None, 'onMouseLeftDown': u'WrapperObj.OnCursorClick(evt)', 'name': u'trendCtrl', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(45, 49)}, {'activate': u'1', 'show': 1, 'borderRightColor': (250, 250, 250), 'child': [{'activate': u'0', 'show': 1, 'keyDown': None, 'border': 0, 'size': wx.Size(90, 21), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', '_uuid': u'37c85bbae953953a189b8cab5a9c027c', 'style': 2, 'flag': 0, 'recount': None, 'name': u'begTimeCtrl', 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(7, 11), 'onInit': None, 'refresh': None}, {'activate': u'0', 'show': 1, 'keyDown': None, 'border': 0, 'size': wx.Size(90, 21), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', '_uuid': u'f1006483a7192838fdbf72198a87e0c9', 'style': 2, 'flag': 0, 'recount': None, 'name': u'endTimeCtrl', 'value': u'', 'alias': None, 'init_expr': None, 'position': (110, 10), 'onInit': None, 'refresh': None}, {'activate': u'0', 'show': 1, 'mouseClick': u'WrapperObj.OnRefresh(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'8cb90fb7ebf995f3a519fd173d7cfec3', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'refreshBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(211, 10), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, 30), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'67dedc0c74eaafe7f4482554a56723f0', 'style': 0, 'flag': 8192, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_1227', 'borderBottomColor': (250, 250, 250), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 393), 'borderStyle': None, 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, 20)}], 'name': u'trendIndPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'TrendDialog', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 2, 3)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'ArrowIndicatorTrend'

#   Типы планов
DAY_PLAN_TYPE = 0
MONTH_PLAN_TYPE = 1
QUARTER_PLAN_TYPE = 2
YEAR_PLAN_TYPE = 3

AsscColorDict = {0: 'r',
                 1: 'y',
                 2: 'g',
                 3: 'y',
                 4: 'r'}

plan_example = [18, 19, 21, 20, 20, 18, 17, 20, 25, 25, 20, 21]


def _get_plan(tm, cod, typPlan=DAY_PLAN_TYPE):
    """
    """
    return None
    
    if typPlan == DAY_PLAN_TYPE:
        if cod < len(plan_example):
            return plan_example[cod]*100000
        return 2000000
    elif typPlan == MONTH_PLAN_TYPE:
        return 2000000 * 30
    elif typPlan == QWARTER_PLAN_TYPE:
        return 2000000 * 30 * 3
    else:
        return 2000000 * 365

try:
    matplotlib.rcParams['timezone'] = 'US/Pacific'
    tz = timezone('US/Pacific')
except:
    pass


def _day_buff_aggr(rs, indicator):
    """
    Собираем буфера значений, которые будут отображеться в графике.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type indicator: C{icarrowindicator.icArrowIndicator}
    @param indicator: Указатель на идикатор, к которому прикреплен тренд.
    """

    fld_time = indicator.attrTime
    fld_val = indicator.attrVal
    fld_plan = indicator.attrPlan
    factor = indicator.factor
    clrRgn = indicator.colorRegions
    min = indicator.GetMinValue()
    
    # --- Подготавливаем данные для отображения графика
    buff_values = range(rs.count())
    buff_plans = range(rs.count())
    buff_times = range(rs.count())
            
    #   Буфер для цветовых зон
    regLst = [range(rs.count()) for x in range(6)]
    #   Заполняем границу нижней зоны
    for i in xrange(rs.count()):
        regLst[0][i] = min
        
    for i, r in enumerate(rs):
        p_date = getattr(r, fld_time)
        year, month, day = p_date.split('.')
        tt = datetime.datetime(int(year), int(month), int(day), tzinfo=tz)

        buff_values[i] = getattr(r, fld_val)/factor
        buff_plans[i] = getattr(r, fld_plan)
        
        if buff_plans[i]:
            buff_plans[i] = buff_plans[i]/factor
            max = buff_plans[i]*2
        else:
            #   Если определена функция определения планов, то используем ее;
            #   В противном случае используем заглушку
            if not indicator.cod in (None, '', 'None') and indicator.GetDayPlanFunc():
                pl = indicator.GetDayPlanFunc()(indicator.cod, int(day), int(month), int(year))
            else:
                pl = _get_plan(p_date, i)
            
            if pl is not None:
                buff_plans[i] = pl/factor
                max = buff_plans[i]*2
            else:
                buff_plans[i] = indicator.GetMaxValue()/2
                max = indicator.GetMaxValue()
            
        #   Вычисляем значение для зон
        for indx, obj in enumerate(clrRgn):
            procent, clr = obj
            val = min + float(int(procent.replace('%', '')))/100.0*(max-min)
            regLst[indx+1][i] = val
            
        buff_times[i] = date2num(tt)

    return buff_times, buff_values, buff_plans, regLst


def _day_list_aggr(data, indicator):
    """
    Собираем буфера значений, которые будут отображеться в графике.
    
    @type data: C{list}
    @param data: Список картежей записей.
    @type indicator: C{icarrowindicator.icArrowIndicator}
    @param indicator: Указатель на идикатор, к которому прикреплен тренд.
    """
    factor = indicator.factor
    clrRgn = indicator.colorRegions
    min = indicator.GetMinValue()
    
    # --- Подготавливаем данные для отображения графика
    buff_values = range(len(data))
    buff_plans = range(len(data))
    buff_times = range(len(data))
            
    #   Буфер для цветовых зон
    regLst = [range(len(data)) for x in range(6)]
    
    #   Заполняем границу нижней зоны
    for i in xrange(len(data)):
        regLst[0][i] = min
        
    #
    for i, r in enumerate(data):
        p_date, value, plan = r
        year, month, day = p_date.split('.')
        tt = datetime.datetime(int(year), int(month), int(day), tzinfo=tz)

        buff_values[i] = value/factor
        buff_plans[i] = plan/factor
        max = plan*2/factor
            
        #   Вычисляем значение для зон
        for indx, obj in enumerate(clrRgn):
            procent, clr = obj
            val = min + float(int(procent.replace('%', '')))/100.0*(max-min)
            regLst[indx+1][i] = val
            
        buff_times[i] = date2num(tt)

    return buff_times, buff_values, buff_plans, regLst


def _month_buff_aggr(rs, indicator, beg, end):
    """
    По месячная агрегация данных из буфера.

    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type indicator: C{icarrowindicator.icArrowIndicator}
    @param indicator: Указатель на идикатор, к которому прикреплен тренд.
    @type beg: C{string}
    @param beg: Начало периода тренда.
    @type end: C{string}
    @param end: Конец периода тренда.
    """
    fld_time = indicator.attrTime
    fld_val = indicator.attrVal
    fld_plan = indicator.attrPlan
    factor = indicator.factor
    clrRgn = indicator.colorRegions
    min = indicator.GetMinValue()
    
    # --- Подготавливаем данные для отображения графика
    year, mnth1, day = [int(x) for x in beg.split('.')]
    year, mnth, day = [int(x) for x in end.split('.')]
    
    buff_values = [0 for x in range(mnth)]
    buff_plans = [0 for x in range(mnth)]
    buff_times = [0 for x in range(mnth)]
            
    #   Буфер для цветовых зон
    regLst = [range(mnth) for x in range(6)]
    
    #   Заполняем границу нижней зоны
    for i in xrange(mnth):
        regLst[0][i] = min

    rss = [r for r in rs]
    
    #   Заполняем массив дат
    for n in range(mnth):
        fd, ld = calendar.monthrange(year, n+1)
        t1 = '%s.%s.01' % (year, ('00'+str(n+1))[-2:])
        t2 = '%s.%s.%s' % (year, ('00'+str(n+1))[-2:], str(ld))
        tt = date2num(datetime.datetime(year, n+1, ld, tzinfo=tz))
        buff_times[n] = tt
        
        val, plan = indicator.aggregatePar(rss, t1, t2)

        if val:
            val = val/factor
        else:
            val = 0
        
        buff_values[n] = val
        
        if not plan:
            max = indicator.GetMaxValue()
            plan = max/2
        else:
            max = 2*plan/factor
            buff_plans[n] = plan/factor

        #   Вычисляем значение для зон
        for indx, obj in enumerate(clrRgn):
            procent, clr = obj
            val = min + float(int(procent.replace('%', '')))/100.0*(max-min)
            regLst[indx+1][n] = val
        
    return buff_times, buff_values, buff_plans, regLst


def _qwarter_buff_aggr(rs, indicator, beg, end):
    """
    По квартальная агрегация данных из буфера.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type indicator: C{icarrowindicator.icArrowIndicator}
    @param indicator: Указатель на идикатор, к которому прикреплен тренд.
    @type beg: C{string}
    @param beg: Начало периода тренда.
    @type end: C{string}
    @param end: Конец периода тренда.
    """
    fld_time = indicator.attrTime
    fld_val = indicator.attrVal
    fld_plan = indicator.attrPlan
    factor = indicator.factor
    clrRgn = indicator.colorRegions
    min = indicator.GetMinValue()
    
    # --- Подготавливаем данные для отображения графика
    year, mnth1, day = [int(x) for x in beg.split('.')]
    year, mnth, day = [int(x) for x in end.split('.')]
    qwart = indDef.ic_month_qwart_indx[mnth]
    
    buff_values = [0 for x in range(qwart)]
    buff_plans = [0 for x in range(qwart)]
    buff_times = [0 for x in range(qwart)]
            
    #   Буфер для цветовых зон
    regLst = [range(qwart) for x in range(6)]
    
    #   Заполняем границу нижней зоны
    for i in xrange(qwart):
        regLst[0][i] = min

    #   Буферизируем записи
    rss = [r for r in rs]
    
    #   Заполняем массив дат
    for n in range(qwart):
        
        if n == 0:
            t1 = '%s.01.01' % year
            t2 = '%s.03.31' % year
            tt = date2num(datetime.datetime(year, 1, 1, tzinfo=tz))
        elif n == 1:
            t1 = '%s.04.01' % year
            t2 = '%s.06.30' % year
            tt = date2num(datetime.datetime(year, 4, 1, tzinfo=tz))
        elif n == 2:
            t1 = '%s.07.01' % year
            t2 = '%s.09.30' % year
            tt = date2num(datetime.datetime(year, 7, 1, tzinfo=tz))
        else:
            t1 = '%s.10.01' % year
            t2 = '%s.12.31' % year
            tt = date2num(datetime.datetime(year, 10, 1, tzinfo=tz))
            
        buff_times[n] = n
        
        val, plan = indicator.aggregatePar(rss, t1, t2)

        if val:
            val = val/factor
        else:
            val = 0
        
        buff_values[n] = val
        
        if not plan:
            max = indicator.GetMaxValue()
            plan = max/2
        else:
            max = 2*plan/factor
            buff_plans[n] = plan/factor

        #   Вычисляем значение для зон
        for indx, obj in enumerate(clrRgn):
            procent, clr = obj
            val = min + float(int(procent.replace('%', '')))/100.0*(max-min)
            regLst[indx+1][n] = val
        
    return buff_times, buff_values, buff_plans, regLst


def _year_buff_aggr(rs, indicator, beg, end):
    """
    По годовая агрегация данных из буфера.
    
    @type rs: C{SQLObject.main.SelectResult}
    @param rs: Набор отобранных записей.
    @type indicator: C{icarrowindicator.icArrowIndicator}
    @param indicator: Указатель на идикатор, к которому прикреплен тренд.
    @type beg: C{string}
    @param beg: Начало периода тренда.
    @type end: C{string}
    @param end: Конец периода тренда.
    """
    fld_time = indicator.attrTime
    fld_val = indicator.attrVal
    fld_plan = indicator.attrPlan
    factor = indicator.factor
    clrRgn = indicator.colorRegions
    min = indicator.GetMinValue()
    
    # --- Подготавливаем данные для отображения графика
    year1, mnth1, day = [int(x) for x in beg.split('.')]
    year2, mnth2, day2 = [int(x) for x in end.split('.')]
    year_end = year2
    
    if year1 == year2:
        year2 += 1

    ny = year2 - year1
    
    buff_values = [0 for x in range(ny)]
    buff_plans = [0 for x in range(ny)]
    buff_times = [0 for x in range(ny)]
            
    #   Буфер для цветовых зон
    regLst = [range(ny) for x in range(6)]
    
    #   Заполняем границу нижней зоны
    for i in xrange(ny):
        regLst[0][i] = min

    #   Буферизируем записи
    rss = [r for r in rs]
    
    #   Заполняем массив дат
    for n in range(ny):
        t1 = '%s.01.01' % str(n+year1)
        
        if n+year1 < year_end:
            t2 = '%s.12.31' % str(n+year1)
        else:
            t2 = end
            
        tt = date2num(datetime.datetime(n+year1, 12, 31, tzinfo=tz))
        buff_times[n] = tt
        
        val, plan = indicator.aggregatePar(rss, t1, t2)
        
        if val:
            val = val/factor
        else:
            val = 0
        
        buff_values[n] = val

        if not plan:
            max = indicator.GetMaxValue()
            plan = max/2
        else:
            max = 2*plan/factor
            buff_plans[n] = plan/factor

        #   Вычисляем значение для зон
        for indx, obj in enumerate(clrRgn):
            procent, clr = obj
            val = min + float(int(procent.replace('%', '')))/100.0*(max-min)
            regLst[indx+1][n] = val
        
    return buff_times, buff_values, buff_plans, regLst


def fcmpTm(x,y):
    """
    Функция сравнения для сортировки списка в порядке увеличения времени.
    """
    if x[0] < y[0]:
        return -1
    elif x[0] > y[0]:
        return 1
    else:
        return 0


class ArrowIndicatorTrend(icobjectinterface.icObjectInterface):
    def __init__(self, parent, indicator=None, newRes = None):
        """
        Конструктор инерфейса - 'динамика изменения показаний финансового индикатора'.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type indicator: C{ic.components.user.icarrowindicator.icArrowIndicator}
        @param indicator: Указатель на индикатор свойства, которого настраиваем.
        """
        #   Указатель на индикатор
        self._indicator = indicator
        #   Буфер отсортированных параметров
        self._buff_par = None
        #   Указатель на окно подсказки
        self._helpWin = None
    
        if newRes:
            res = newRes
        else:
            res = resource
            
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, res)
        
    def AnalogSortLst(self, analogLst, lstLst):
        """
        Функция сортирует списки по отсортированному списку, который содержит
        старый индекс.
        
        @param lstLst: Список списков, которые надо отсортировать.
        """
        newLst = [range(len(analogLst)) for x in range(len(lstLst))]
        
        for n, lst in enumerate(lstLst):
            for i, obj in enumerate(analogLst):
                ob, oi = obj
                newLst[n][i] = lst[oi]
                
        return newLst
        
    def GetIDataclass(self):
        """
        Возвращает интерфейс на класс данных.
        """
        if self.GetIndicator():
            return self.GetIndicator().GetIDataclass()
        
        return None
        
    def GetIndicator(self):
        """
        Возвращает указатель на индикатор.
        """
        return self._indicator
        
    def GetRecordset(self):
        """
        Возвращает набор записей отобранных из класса данных по заданному периоду.
        
        @rtype: C{SQLObject.main.SelectResults}
        @return: Возвращаем список отобранных записей.
        """
        if self.GetIndicator():
            fld = self.GetIndicator().GetTimeField()
            t1 = self.GetNameObj('begTimeCtrl').GetStrDate()
            t2 = self.GetNameObj('endTimeCtrl').GetStrDate()
            return self.GetIndicator().GetRecordset(t1, t2)
            
    def OnCursorClick(self, evt):
        """
        Обрабатываем нажатие левой кнопки на графике.
        """
        dct = {0: u'I кв.', 1: u'II кв.', 2: u'III кв.', 3: u'IV кв.'}
        aggrTyp = self.GetIndicator().GetAggregationType()
        trend = self.GetNameObj('trendCtrl')
        ret = trend.GetStaticCursor()
        t, v = ret
        
        if aggrTyp == indDef.AGR_TYPE_QUARTER:
            if t < 0:
                t = 0
                
            tm = dct[int(t)]
        else:
            tm = str(num2date(t))[:10]

        v = v * self.GetIndicator().factor

        #   Рисуем подсказку
        sx, sy = trend.GetSize()
        
        #   График генерирует свое событие
        px, py = p = evt.x, evt.y
        figheight = trend.canvas.figure.bbox.height()
        py = figheight - py
        d = 5
        r = wx.Rect(d, d, sx-2*d, sy-2*d)

        #   Создаем окно подсказки
        if r.Inside(p):
            msg = '%s: %s' % (tm, str(v))

            if self._helpWin:
                self._helpWin.Show(False)
                self._helpWin.Destroy()

            self._helpWin = icwidget.icShortHelpString(trend, msg, (px, py-15), 2000)
            self._helpWin.SetBackgroundColour(wx.Colour(255, 255, 200))
    
    def SetGraphFromData(self, data):
        """
        Обновляет представления графика.
        """
        
        subplot = None
        trend = self.GetNameObj('trendCtrl')
        
        factor = self.GetIndicator().factor
        clrRgn = self.GetIndicator().colorRegions
        fig = trend.fig
        formatter, majorTick = None, None

        if data > 0:
            buff_times, buff_values, buff_plans, regLst = _day_list_aggr(data, self.GetIndicator())
            formatter = DateFormatter('%d/%m')
            majorTick = None
            
            # --- Создаем график
            self._buff_par = (buff_times, buff_values, buff_plans)
            fig = trend.fig
            fig.clear()
            subplot = fig.add_subplot(111)

            # --- Рисуем зоны
            x = numerix.concatenate((buff_times, buff_times[::-1]))
            clrRgn = self.GetIndicator().colorRegions
            for i in range(len(clrRgn)):
                y = numerix.concatenate((regLst[i+1], regLst[i][::-1]))
                clr = AsscColorDict[i]
                p = subplot.fill(x, y, facecolor=clr, alpha=0.2)

            # В зависимости от типа агрегации создаем график
            subplot.plot_date(buff_times, buff_values, 'b-s', tz=tz)
            subplot.plot_date(buff_times, buff_plans, 'g', tz=tz)

        if not subplot:
            fig.clear()
            subplot = fig.add_subplot(111)
            
        subplot.grid(True)
        self.GetNameObj('titleCtrl').SetLabel(self.GetIndicator().GetLabel())
        
        if factor > 1:
            subplot.set_ylabel('x'+str(factor)+'\n')
            labels = subplot.get_yticklabels()
            pylab.setp(labels, size=10)
            
        if majorTick:
            subplot.xaxis.set_major_locator(majorTick)
            
        if formatter:
            subplot.xaxis.set_major_formatter(formatter)
            labels = subplot.get_xticklabels()
            pylab.setp(labels, 'rotation', 45, size=10)

        trend.toolbar.update()
        trend.canvas.draw()
        
    def OnRefresh(self, evt=None):
        """
        Обрабатываем нажатие кнопки обновить представление.
        """
        rs = self.GetRecordset()
        subplot = None
        trend = self.GetNameObj('trendCtrl')
        
        fld_time = self.GetIndicator().attrTime
        fld_val = self.GetIndicator().attrVal
        fld_plan = self.GetIndicator().attrPlan
        factor = self.GetIndicator().factor
        clrRgn = self.GetIndicator().colorRegions
        fig = trend.fig
        formatter, majorTick = None, None

        beg = self.GetNameObj('begTimeCtrl').GetStrDate()
        end = self.GetNameObj('endTimeCtrl').GetStrDate()
        
        if rs and rs.count() > 0:
            # --- Подготавливаем данные для отображения графика
            aggrTyp = self.GetIndicator().GetAggregationType()
            
            #   Агрегированное значение пишем на последнее число месяца
            if aggrTyp in (indDef.AGR_TYPE_DAY, indDef.AGR_TYPE_USUAL, indDef.AGR_TYPE_PERIOD):
                buff_times, buff_values, buff_plans, regLst = _day_buff_aggr(rs, self.GetIndicator())
                formatter = DateFormatter('%d-%m')
                majorTick = None
                
            elif aggrTyp == indDef.AGR_TYPE_MONTH:
                buff_times, buff_values, buff_plans, regLst = _month_buff_aggr(rs, self.GetIndicator(), beg, end)
                formatter = DateFormatter('%m')
                majorTick = MonthLocator()
                
            elif aggrTyp == indDef.AGR_TYPE_QUARTER:
                buff_times, buff_values, buff_plans, regLst = _qwarter_buff_aggr(rs, self.GetIndicator(), beg, end)
                
            elif aggrTyp == indDef.AGR_TYPE_YEAR:
                buff_times, buff_values, buff_plans, regLst = _year_buff_aggr(rs, self.GetIndicator(), beg, end)
                formatter = DateFormatter('%Y')
                majorTick = YearLocator()
            
            # --- Создаем график
            self._buff_par = (buff_times, buff_values, buff_plans)
            fig = trend.fig
            fig.clear()
            subplot = fig.add_subplot(111)

            # --- Рисуем зоны
            x = numerix.concatenate((buff_times, buff_times[::-1]))
            for i in range(5):
                y = numerix.concatenate((regLst[i+1], regLst[i][::-1]))
                clr = AsscColorDict[i]
                p = subplot.fill(x, y, facecolor=clr, alpha=0.2)

            # В зависимости от типа агрегации создаем график
            if aggrTyp == indDef.AGR_TYPE_QUARTER:
                ind = numerix.arange(4)
                width = 0.25
                subplot.bar(buff_times, buff_values, width, color='b')
                subplot.plot(buff_times, buff_plans, 'g')
                
                subplot.set_xticks(ind+width/2)
                subplot.set_xticklabels(['I', 'II', 'III', 'IV'])
                
            else:
                subplot.plot_date(buff_times, buff_values, 'b-s', tz=tz)
                subplot.plot_date(buff_times, buff_plans, 'g', tz=tz)

        if not subplot:
            fig.clear()
            subplot = fig.add_subplot(111)
            
        subplot.grid(True)
        self.GetNameObj('titleCtrl').SetLabel(self.GetIndicator().GetLabel())
        
        if factor > 1:
            subplot.set_ylabel('x'+str(factor)+'\n')

        if majorTick:
            subplot.xaxis.set_major_locator(majorTick)
            
        if formatter:
            subplot.xaxis.set_major_formatter(formatter)
            for i, tick in enumerate(subplot.xaxis.get_major_ticks()):
                tick.label1.update({'rotation': 45, 'size': 10})

        trend.toolbar.update()
        trend.canvas.draw()


def test(par=0):
    """
    Тестируем класс ArrowIndicatorTrend.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = ArrowIndicatorTrend(frame)
    
    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
