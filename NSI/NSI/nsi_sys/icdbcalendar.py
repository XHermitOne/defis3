#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Класс календаря/календарного графика.
"""

# --- Подключение библиотек ---
from ic.dlg import dlgfunc
from ic.dlg import ic_proccess_dlg
from ic.utils import datetimefunc
from ic.log import log

from ic.components import iccalendar
from . import icsprav

# --- Версия ---
__version__ = (0, 1, 1, 2)


# --- Спецификация ---
SPC_IC_DBCALENDAR = {'type': 'DBCalendar',
                     'name': 'default',
                     'description': '',     # Описание
                     '__parent__': icsprav.SPC_IC_SPRAV,
                     }


class icDBCalendarProto(icsprav.icSpravProto):
    """
    Класс календаря/календарного графика.
    """
    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.
        @param sprav_manager: Объект менеджера справочника.
        @param name: Имя в списке менеджера справочников.
        """
        icsprav.icSpravProto.__init__(self, sprav_manager, name)
    
    def getMonthNameByNum(self, n_month):
        """
        Получить имя месяца по его номеру 1..12.
        """
        month_list = iccalendar.GetMonthList()
        try:
            return month_list[int(n_month) - 1]
        except IndexError:
            log.fatal(u'Ошибка параметров DBCalendar <%s>' % n_month)
            return None

    def getFullDateTxt(self, str_date, fmt=datetimefunc.DEFAULT_DATETIME_FMT):
        """
        Получить полную дату с указанием дня недели.
        """
        date_tuple = datetimefunc.DateTimeTuple(str_date, fmt)
        if date_tuple:
            day = date_tuple[2]
            month = self.getMonthNameByNum(date_tuple[1])
            year = date_tuple[0]
            week_day = datetimefunc.getWeekList()[date_tuple[6]]
            return '%d %s %d года %s' % (day, month, year, week_day)
        return ''

    def loadData(self, str_date, fmt=datetimefunc.DEFAULT_DATETIME_FMT):
        """
        Прочитать данные за день.
        @param str_date: День в виде строки.
        @param fmt: Формат строки.
        """
        date_tuple = datetimefunc.DateTimeTuple(str_date, fmt)
        year_str = '%04d' % date_tuple[0]
        month_str = '%02d' % (date_tuple[1]+1)
        day_str = '%02d' % (date_tuple[2]+1)
        cod = self.ListCode2StrCode((year_str, month_str, day_str))
        storage = self.getStorage()
        if storage:
            return storage.getRecByCod(cod)
        return None

    def saveData(self, record_dict, str_date, fmt=datetimefunc.DEFAULT_DATETIME_FMT):
        """
        Сохранить данные на день.
        @param record_dict: Заполненный словарь записи.
        @param str_date: День в виде строки.
        @param fmt: Формат строки.
        """
        date_tuple = datetimefunc.DateTimeTuple(str_date, fmt)
        year_str = '%04d' % date_tuple[0]
        month_str = '%02d' % (date_tuple[1] + 1)
        day_str = '%02d' % (date_tuple[2] + 1)
        cod = self.ListCode2StrCode((year_str, month_str, day_str))
        storage = self.getStorage()
        if storage:
            return storage.updateRecByCod(cod, record_dict)
        return None
        
    def checkYear(self, year):
        """
        Проверка календарного графика на год, если нет, то создать.
        """
        if not self.isYear(year):
            self.genYear(year)
        
    def genYear(self, year):
        """
        Генерация календарного графика на год с опросом пользователя.
        """
        if dlgfunc.openAskBox(u'ВНИМАНИЕ!', u'Создать календарный график на %s год?' % str(year)):
            if self._delYearRec(year):
                self.generateYear(year)
        
    def isYear(self, year):
        """
        Проверить есть ли календарный график на год.
        """
        storage = self.getStorage()
        if storage:
            cod = self.ListCode2StrCode((str(year),))
            return storage.isCod(cod)
        return None
        
    @ic_proccess_dlg.proccess2_noparent_deco
    def generateYear(self, year):
        """
        Генерация календарного графика на год.
        @param year: Указание года, за который нужно сгенерировать календарный график.
        """
        self._genYearRec(year)
        # Перебор по месяцам
        for month in range(12):
            self._genMonthRec(year, month + 1)
            # Опрделить сколько дней в месяце
            days = datetimefunc.getMonthDaysCount(month + 1, year)
            for day in range(days):
                ic_proccess_dlg.setProccessBoxLabel(u'Календарный график на %s год. Месяц: %s' % (str(year),
                                                                                                  self.getMonthNameByNum(month+1)),
                                                    100.0 / 12.0 * (month + 1), u'День: ' + str(day+1),
                                                    100.0 / days * (day+1))
                self._genDayRec(year, month + 1, day + 1)
    
    def _delYearRec(self, year):
        """
        Удалить год.
        """
        if self.isYear(year):
            if dlgfunc.openAskBox(u'ВНИМАНИЕ!', u'Календарный график на %s год уже существует. Удалить?' % str(year)):
                storage = self.getStorage()
                if storage:
                    cod = self.ListCode2StrCode((str(year),))
                    return storage.delRecByCod(cod)
                return True
            else:
                return False
        return True
        
    def _genYearRec(self, year):
        """
        Генерация записи года.
        """
        cod = self.ListCode2StrCode((str(year),))
        name = 'Календарный график на %s год' % str(year)
        self.addRec(cod, {'name': name})
        
    def _genMonthRec(self, year, month):
        """
        Генерация записи месяца.
        """
        month_str = '%02d' % int(month)
        cod = self.ListCode2StrCode((str(year), month_str))
        name = self.getMonthNameByNum(month)
        self.addRec(cod, {'name': name})

    def _genDayRec(self, year, month, day):
        """
        Генерация записи на день.
        """
        month_str = '%02d' % int(month)
        day_str = '%02d' % int(day)
        cod = self.ListCode2StrCode((str(year), month_str, day_str))
        name = '%s.%s.%s' % (day_str, month_str, str(year))
        # Проверка на нерабочие дни
        week_day = datetimefunc.getWeekDay(day, month, year)
        if week_day == 7 or week_day == 6:
            dontWork = 1
        else:
            dontWork = 0
        self.addRec(cod, {'name': name, 'n1': week_day, 'n2': dontWork, 'n3': 0,
                          'f1': 1.0, 'f2': 1.0, 'f3': 1.0})
