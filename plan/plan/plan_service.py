#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль сервисных функций системы планирования.
"""

# --- Подключение библиотек ---
from ic.utils import ic_util
from ic.dlg import ic_dlg
from . import calc_plan

# Версия
__version__ = (0, 1, 1, 1)

#   Кодировка имен файлов для разных месяцев
monthFileNameDict = {'m01': u'Январь',
                     'm02': u'Февраль',
                     'm03': u'Март',
                     'm04': u'Апрель',
                     'm05': u'Май',
                     'm06': u'Июнь',
                     'm07': u'Июль',
                     'm08': u'Август',
                     'm09': u'Сентябрь',
                     'm10': u'Октябрь',
                     'm11': u'Ноябрь',
                     'm12': u'Декабрь'}


# --- Функции ---
def getPlanMethodChoice(PlanModule_=None):
    """
    Получение списка выбора методов расчетов планов.
    @param PlanModule_: Модуль, в котором находятся функции
        расчета плановых значений.
    @return: Возвращает список строк в формате
        'имя функции-метода  описание'.
    """
    func_list = ic_util.getFuncListInModule(PlanModule_)
    if func_list:
        return map(lambda func: func[0]+' '+func[1].splitlines()[1],
                   func_list)
    return []


def PlanMethodChoiceDlg(Parent_=None):
    """
    Диалог выбора метода расчета плановых значений.
    """
    method_str = ic_dlg.getSingleChoiceDlg(Parent_,
                                          u'Выберите метод',
                                          u'Методы расчета плановых значений',
                                           getPlanMethodChoice(calc_plan))
    if method_str:
        method_str = method_str[:method_str.find(' ')]
        return calc_plan.__dict__[method_str]
    return None


def runPlanMethod(PlanMethod_,*Args_,**KWArgs_):
    """
    Запуск метода расчета плановых значений.
    """
    if PlanMethod_:
        PlanMethod_(*Args_, **KWArgs_)
