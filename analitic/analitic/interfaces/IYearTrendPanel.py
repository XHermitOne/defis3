#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль прикладной системы.
"""

import wx

import analitic.indicators.icarrowindicatortrend as trendInd
import ic.interfaces.icBrPnlInterface as icBrPnlInterface
import analitic.interfaces.IStdIndicatorPanel as stdPanel
import analitic.indicators.icarrowindicator as icarrowindicator

# Версия
__version__ = (0, 1, 1, 1)


# --- Классы
class IYearTrendPanel(trendInd.ArrowIndicatorTrend, icBrPnlInterface.icBrowsPanelInterface):
    def __init__(self, parent, metaObj=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на дерево планов.
        """
        self.table = 'analitic'
        
        # Выдираем нужный кусок ресурса графика
        res = self.GetObjectResource('trendIndPanel', resource=trendInd.resource)
        
        # Создаем индикатор, по которому строится график
        indicator_res = self.GetObjectResource('dayRealiz', resource=stdPanel.resource)
        self.indicator = icarrowindicator.icArrowIndicator(parent, -1, indicator_res)

        trendInd.ArrowIndicatorTrend.__init__(self, parent, self.indicator, newRes=res)
        icBrPnlInterface.icBrowsPanelInterface.__init__(self, metaObj)
        
    def LoadData(self):
        """
        """
        if self.metaObj and not self.metaObj.isRoot():
            year = int(self.metaObj.getPath()[0])
            
            lstDays = ['%s.%02d.%s' % (year, month+1,
                                       wx.DateTime.GetNumberOfDaysInMonth(month, year))
                                       for month in range(12)]
            # print '... lst=', lstDays
            self.LoadIndicator(year)
            data = stdPanel._getStatisticYearSumma(self.metaObj, self.table, lstDays)
            self.SetGraphFromData(data)
            print('... lst=', lstDays)
            
            for r in data:
                print(r)
    
    def LoadIndicator(self, year):
        """
        Функция загружает заданый индикатор.
        """
        tdate = '%s.12.31' % year
        summa, kol = stdPanel._getYearSumma(tdate, self.metaObj, self.table)
        plan = stdPanel._getYearPlan(tdate, self.metaObj)
        
#        mnthPlan = stdPanel._getMonthPlan('2005.01.31', self.metaObj)
#        print '++++++ mnthPlan=', mnthPlan, self.metaObj.getPath()
#        plan = 0
#        summa = 0
        obj = self.indicator

        if obj and self.metaObj:
            
            # По необходимости устанавливаем заголовок индикатора
            # if ei:
            #     obj.SetLabel('%s (%s)' % (label, ei))
            #     obj.ei = ei
            # else:
            #     obj.SetLabel('%s (%s)' % (label, obj.ei))

            obj.SetLabel('Реализация по месяцам (руб.) на %d год' % year)
            factor = stdPanel._getTypeFactor(self.metaObj, 2*plan)
            print('------- factor=', factor)
            obj.colorRegions = self.metaObj.value.color_zones
            obj.SetState(summa, plan, factor=factor)
            return True

        return False
