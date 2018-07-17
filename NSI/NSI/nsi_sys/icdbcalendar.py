#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Класс календаря/календарного графика.
Автор(ы): Колчанов А.В.
"""

#--- Версия ---
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---
from ic.dlg import ic_dlg
from ic.dlg import ic_proccess_dlg
from ic.utils import ic_time

from ic.components import iccalendar
from . import icsprav

#--- Спецификация ---
SPC_IC_DBCALENDAR={
    'type': 'DBCalendar',
    'name': 'default',
    'description':'',    #Описание
    '__parent__':icsprav.SPC_IC_SPRAV,
    }

#--- Константы ---
#--- Функции ---
#--- Классы ---
class icDBCalendarPrototype(icsprav.icSpravPrototype):
    """
    Класс календаря/календарного графика.
    """
    def __init__(self,SpravManager_=None,Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя в списке менеджера справочников.
        """
        icsprav.icSpravPrototype.__init__(self,SpravManager_,Name_)
    
    def getMonthNameByNum(self,MonthNum_):
        """
        Получить имя месяца по его номеру 1..12.
        """
        month_list=iccalendar.GetMonthList()
        try:
            return month_list[int(MonthNum_)-1]
        except IndexError:
            print('ERROR PARAMETER DBCalendar',MonthNum_)
            return None

    def getFullDateTxt(self,Date_,Fmt_=ic_time.DEFAULT_DATETIME_FMT):
        """
        Получить полную дату с указанием дня недели.
        """
        date_tuple=ic_time.DateTimeTuple(Date_,Fmt_)
        if date_tuple:
            day=date_tuple[2]
            month=self.getMonthNameByNum(date_tuple[1])
            year=date_tuple[0]
            week_day=ic_time.getWeekList()[date_tuple[6]]
            return '%d %s %d года %s'%(day,month,year,week_day)
        return ''

    def loadData(self,Date_,Fmt_=ic_time.DEFAULT_DATETIME_FMT):
        """
        Прочитать данные за день.
        @param Date_: День в виде строки.
        @param Fmt_: Формат строки.
        """
        date_tuple=ic_time.DateTimeTuple(Date_,Fmt_)
        year_str='%04d'%(date_tuple[0])
        month_str='%02d'%(date_tuple[1]+1)
        day_str='%02d'%(date_tuple[2]+1)
        cod=self.ListCode2StrCode((year_str,month_str,day_str))
        storage=self.getStorage()
        if storage:
            return storage.getRecByCod(cod)
        return None

    def saveData(self,RecDict_,Date_,Fmt_=ic_time.DEFAULT_DATETIME_FMT):
        """
        Сохранить данные на день.
        @param RecDict_: Заполненный словарь записи.
        @param Date_: День в виде строки.
        @param Fmt_: Формат строки.
        """
        date_tuple=ic_time.DateTimeTuple(Date_,Fmt_)
        year_str='%04d'%(date_tuple[0])
        month_str='%02d'%(date_tuple[1]+1)
        day_str='%02d'%(date_tuple[2]+1)
        cod=self.ListCode2StrCode((year_str,month_str,day_str))
        storage=self.getStorage()
        if storage:
            return storage.updateRecByCod(cod,RecDict_)
        return None
        
    def checkYear(self,Year_):
        """
        Проверка календарного графика на год, если нет, то создать.
        """
        if self.isYear(Year_)==False:
            self.genYear(Year_)
        
    def genYear(self,Year_):
        """
        Генерация календарного графика на год с опросом пользователя.
        """
        if ic_dlg.icAskBox(u'ВНИМАНИЕ!',u'Создать календарный график на %s год?'%(str(Year_))):
            if self._delYearRec(Year_):
                self.generateYear(Year_)
        
    def isYear(self,Year_):
        """
        Проверить есть ли календарный график на год.
        """
        storage=self.getStorage()
        if storage:
            cod=self.ListCode2StrCode((str(Year_),))
            return storage.isCod(cod)
        return None
        
    @ic_proccess_dlg.proccess2_noparent_deco
    def generateYear(self,Year_):
        """
        Генерация календарного графика на год.
        @param Year_: Указание года, за который нужно сгенерировать календарный график.
        """
        self._genYearRec(Year_)
        #Перебор по месяцам
        for month in range(12):
            self._genMonthRec(Year_,month+1)
            #Опрделить сколько дней в месяце
            days=ic_time.getMonthDaysCount(month+1,Year_)
            for day in range(days):
                ic_proccess_dlg.SetProccessBoxLabel(u'Календарный график на %s год. Месяц: %s'%(str(Year_),self.getMonthNameByNum(month+1)), 
                    100.0/12.0*(month+1),u'День: '+str(day+1),
                    100.0/days*(day+1))
                self._genDayRec(Year_,month+1,day+1)
    
    def _delYearRec(self,Year_):
        """
        Удалить год.
        """
        if self.isYear(Year_)==True:
            if ic_dlg.icAskBox(u'ВНИМАНИЕ!',u'Календарный график на %s год уже существует. Удалить?'%(str(Year_))):
                storage=self.getStorage()
                if storage:
                    cod=self.ListCode2StrCode((str(Year_),))
                    return storage.delRecByCod(cod)
                return True
            else:
                return False
        return True
        
    def _genYearRec(self,Year_):
        """
        Генерация записи года.
        """
        cod=self.ListCode2StrCode((str(Year_),))
        name='Календарный график на %s год'%(str(Year_))
        print('gen Year',cod)
        self.addRec(cod,{'name':name})
        
    def _genMonthRec(self,Year_,Month_):
        """
        Генерация записи месяца.
        """
        month_str='%02d'%(int(Month_))
        cod=self.ListCode2StrCode((str(Year_),month_str))
        name=self.getMonthNameByNum(Month_)
        print('gen Month',cod)
        self.addRec(cod,{'name':name})

    def _genDayRec(self,Year_,Month_,Day_):
        """
        Генерация записи на день.
        """
        month_str='%02d'%(int(Month_))
        day_str='%02d'%(int(Day_))
        cod=self.ListCode2StrCode((str(Year_),month_str,day_str))
        name='%s.%s.%s'%(day_str,month_str,str(Year_))
        #Проверка на нерабочие дни
        week_day=ic_time.getWeekDay(Day_,Month_,Year_)
        if week_day==7 or week_day==6:
            dontWork=1
        else:
            dontWork=0
        print('gen Day',cod)
        self.addRec(cod,{'name':name,'n1':week_day,'n2':dontWork,'n3':0,
            'f1':1.0,'f2':1.0,'f3':1.0})
        
