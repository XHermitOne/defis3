#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль стандартных диалогов.
Автор(ы): Колчанов. А.В.
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---
import wx

from ic.components import icResourceParser
from ic.utils import util
from ic.log import ic_log

#--- Функции ---

def icDateRangeSTDDlg(parent=None,DefaultDateRange_=None):
    """
    Стандартный диалог выбора диапазона дат.
    """
    result=None
    
    #Подготовить пространство имен
    evsp=util.InitEvalSpace({'default': DefaultDateRange_})
    
    #Создать форму
    is_new_parent=False
    if parent is None:
        #Если необходимо то создать родительское окно
        parent=wx.Frame(None,-1,'')
        is_new_parent=True
    try:
        result=icResourceParser.ResultForm('date_range_dlg',parent=parent,evalSpace=evsp,bBuff=False)
    except:
        ic_log.icLogErr(u'Ошибка стандартного диалога выбора диапазона дат.')
        
    #Если необходимо то удалить родительское окно
    if is_new_parent:
        parent.Destroy()
        parent=None
        
    return result

def test():
    """
    Тестовая функция.
    """
    app=wx.PySimpleApp()
    print(icDateRangeSTDDlg())
    app.MainLoop()
    
if __name__=='__main__':
    test()