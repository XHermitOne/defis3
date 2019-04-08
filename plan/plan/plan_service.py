# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль сервисных функций системы планирования.
Автор(ы):
"""

#--- Подключение библиотек ---
from ic.utils import ic_util
from ic.dlg import ic_dlg
import calc_plan

# Версия
__version__ = (0, 0, 0, 1)

#   Кодировка имен файлов для разных месяцев
monthFileNameDict = {'m01':'Январь',
                    'm02':'Февраль',
                    'm03':'Март',
                    'm04':'Апрель',
                    'm05':'Май',
                    'm06':'Июнь',
                    'm07':'Июль',
                    'm08':'Август',
                    'm09':'Сентябрь',
                    'm10':'Октябрь',
                    'm11':'Ноябрь',
                    'm12':'Декабрь'}

#--- Функции ---
def getPlanMethodChoice(PlanModule_=None):
    """
    Получение списка выбора методов расчетов планов.
    @param PlanModule_: Модуль, в котором находятся функции
        расчета плановых значений.
    @return: Возвращает список строк в формате
        'имя функции-метода  описание'.
    """
    func_list=ic_util.getFuncListInModule(PlanModule_)
    if func_list:
        return map(lambda func: func[0]+' '+func[1].splitlines()[1],
            func_list)
    return []
    
def PlanMethodChoiceDlg(Parent_=None):
    """
    Диалог выбора метода расчета плановых значений.
    """
    method_str=ic_dlg.icSingleChoiceDlg(Parent_,
        'Выбирите метод',
        'Методы расчета плановых значений',
        getPlanMethodChoice(calc_plan))
    if method_str:
        method_str=method_str[:method_str.find(' ')]
        return calc_plan.__dict__[method_str]
    return None

def runPlanMethod(PlanMethod_,*Args_,**KWArgs_):
    """
    Запуск метода расчета плановых значений.
    """
    if PlanMethod_:
        PlanMethod_(*Args_,**KWArgs_)
