#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль ресурса <C:/defis/NSI/NSI/calendarEditFrm.frm>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/calendarEditFrm.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/calendarEditFrm_frm.py
# Purpose:     Модуль ресурса.
#
# Author:      <...>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0,0,0,1)

#--- Подключение библиотек ---
from ic.utils import datetimefunc

#--- Общие переменные ---
#Признак изменения справочника
#is_changed=False

#from NSI.spravEditDlg2_frm import *

#--- Функции-обработчики событий ---
def onInitDateChoiceCtrl(self,DBCalendar_,FullDateTxtCtrl_):
    """
    Инициализация компонента календаря.
    """
    date_txt=self.GetStrDate()
    full_date_txt=DBCalendar_.getFullDateTxt(date_txt,'%Y.%m.%d')
    FullDateTxtCtrl_.SetLabel(full_date_txt)
    year=int(datetimefunc.convertDateTimeFmt(date_txt, '%Y.%m.%d', '%Y'))
    DBCalendar_.checkYear(year)
    rec=DBCalendar_.loadData(date_txt,'%Y.%m.%d')
    print('@@@',rec,year)
    
def onDateChangedDateChoiceCtrl(self,DBCalendar_,FullDateTxtCtrl_):
    """
    Изменение даты в календаре.
    """
    print('OnDateChanged START',self.GetStrDate())
    onInitDateChoiceCtrl(self,DBCalendar_,FullDateTxtCtrl_)
    
    
