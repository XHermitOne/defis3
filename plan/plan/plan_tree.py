# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль прикладной системы планирования 
    для организации дерева планов.
Автор(ы): 
"""

#--- Подключение библиотек ---
import copy

from ic.storage import objstore
from ic.storage import storesrc

# Версия
__version__ = (0, 0, 0, 1)

#--- Спецификации ---
#Данные узла о планировании
PlanRec={'koeff':0.0, #Коэффициент расчета плана
    'summa':0.0, #Расчитываемое число плана
    'cost':0.0, #Цена продукта за 1
    'amount':0.0 #Запланированное количество
    }
#--- Функции ---

#--- Классы ---
class icPlanNode:
    """
    Абстрактный узел дерева планирования.
    """
    def __init__(self):
        """
        Конструктор.
        """
        #Привязать данные планирования к узлу
        self._plan=copy.deepcopy(PlanRec)
        self['plan']=self._plan

    def __getitem__(self,item):
        if item in self._plan.keys():
            return self['plan'][item]
        return self.__dict__[item]
        
    def __setitem__(self,item,value):
        if item in self._plan.keys():
            self._plan[item]=value
            self['plan']=self._plan
        self.__dict__[item]=value
        
class icPlanRootStorage(icPlanNode,objstore.icObjectStorage):
    """
    Корень плановой системы.
    """
    def __init__(self,Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания объекта.
        """
        icPlanNode.__init__(self)
        objstore.icObjectStorage.__init__(self,Resource_)

class icYearPlan(icPlanNode,storesrc.icDirStorage):
    """
    Узел годового планирования.
    """
    def __init__(self):
        """
        Конструктор.
        """
        icPlanNode.__init__(self)
        storesrc.icDirStorage.__init__(self)
        self._property=storesrc.icFileStorage()
        self['property']=self._property
        
class icMonthPlan(icPlanNode,storesrc.icFileStorage):
    """
    Узел месячного планирования.
    """
    def __init__(self):
        """
        Конструктор.
        """
        icPlanNode.__init__(self)
        storesrc.icFileStorage.__init__(self)

#--- Тестовые функции ---
def test():
    from ic.utils import resource
    res=resource.icGetRes('plans_storage','odb',nameRes='plans_storage')
    plan_root=icPlanRootStorage(res)
    
if __name__=='__main__':
    test()