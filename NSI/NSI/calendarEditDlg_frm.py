#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль ресурса <C:/defis/NSI/NSI/calendarEditDlg_frm.py>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/calendarEditDlg_frm.py
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/calendarEditDlg_frm.py
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

#--- Функции-обработчики событий ---
from NSI.spravEditDlg2_frm import *

def onMouseClickYearGenTool(Year_,DBCalendar_,TreeCtrl_,evalSpace):
    """
    Генерация календарного графика на год.
    """
    print('onMouseClickYearGenTool START',Year_)
    DBCalendar_.genYear(Year_)
    #TreeCtrl_.reFresh()
    onInitSpravTree(evalSpace)
    
