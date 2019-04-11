#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль прикладной системы МОНИТОРИНГ.
Управление просмотром и редактированием мониторов.
"""

from ic.components.user.objects import icmetatreebrows as browser
from ic.engine import ic_user
from analitic.metadatainterfaces import IMetaplan
from plan import browsers as brws
from analitic import planUtils

# Версия
__version__ = (0, 1, 1, 1)


# --- Функции ---
def showTextMonitorBrowser():
    """
    Вывод на экран формы редактирования мониторов.
    """
    frm = {'mYear': 'analitic.interfaces.IAnaliticBrows.IAnaliticBrows',
           'mMonth': 'analitic.interfaces.IAnaliticBrows.IAnaliticBrows',
           'mVidProd': 'analitic.interfaces.IAnaliticBrows.IAnaliticBrows',
           'mReg': 'analitic.interfaces.IAnaliticBrows.IAnaliticBrows',
           'mMenager': 'analitic.interfaces.IAnaliticBrows.IAnaliticBrows'
           }
    metaclass = IMetaplan.IMetaplan(forms=frm)
#    metaObj = metaclass.getObject()

#    brows=browser.MetaTreeBrows(ic_user.icGetMainWin(), metaObj=metaObj,
#                                treeRootTitle='Классификация мониторов',
#                                treeLabels=['Мониторы'])
    brows = brws.icMonitoringBrows(ic_user.icGetMainWin(), 'metadata_plan',
                                   metaclass=metaclass,
                                   treeRootTitle=u'Классификация мониторов',
                                   treeLabels=[u'Мониторы'])

    # Отключить режим редактирования
    brows.SetEditMode(False)

    # Устанавливает у метадерева режим мониторинга и указатель на браузер.
    metaclass.SetUserData({'mode': 'monitoring', 'browserInterface': brows})
    obj = brows.getObject()
    ic_user.icAddMainOrgPage(obj, u'Табличные мониторы')


def showMonitorBrowser():
    """
    Вывод на экран формы редактирования мониторов.
    """
    frm = {'mYear': 'analitic.interfaces.IYearTrendPanel.IYearTrendPanel',
           'mMonth': 'analitic.interfaces.IStdIndicatorPanel.IStdIndicatorPanel',
           'mVidProd': 'analitic.interfaces.IStdIndicatorPanel.IStdIndicatorPanel',
           'mReg': 'analitic.interfaces.IStdIndicatorPanel.IStdIndicatorPanel',
           'mMenager': 'analitic.interfaces.IStdIndicatorPanel.IStdIndicatorPanel'
           }
    metaclass = IMetaplan.IMetaplan(forms=frm)
#    metaObj = metaclass.getObject()

#    brows=browser.MetaTreeBrows(ic_user.icGetMainWin(), metaObj=metaObj,
#                                treeRootTitle='Классификация мониторов',
#                                treeLabels=['Мониторы'])
    brows = brws.icMonitoringBrows(ic_user.icGetMainWin(), 'metadata_plan',
                                   metaclass=metaclass,
                                   treeRootTitle=u'Классификация мониторов',
                                   treeLabels=[u'Мониторы'])

    # Отключить режим редактирования
    brows.SetEditMode(False)
    # Устанавливает у метадерева режим мониторинга и указатель на браузер.
    metaclass.SetUserData({'mode': 'monitoring', 'browserInterface': brows})
    obj = brows.getObject()
    # obj.Show(True)
    ic_user.icAddMainOrgPage(obj, u'Просмотр индикаторов')


def showPlanBrowser():
    """
    Вывод формы редактирования планов.
    """
    metaclass = IMetaplan.IMetaplan()
    metaObj = metaclass.getObject()
#    cls=browser.MetaTreeBrows(None, 'metadata_plan',
#                            metaObj=metaObj,
#                            treeRootTitle='Структура планов',
#                            treeLabels=['Планы'])
    brows = brws.icPlanBrows(None, 'metadata_plan',
                             metaclass=metaclass,
                             treeRootTitle=u'Структура планов',
                             treeLabels=[u'Планы'])

    #   Определяем функции пересчета модифицированных планов по базовому
    brows.recountFunc = planUtils.genModifPlan
    brows.recountModifPlanYear = planUtils.genModifPlanYear
    brows.recountAllModifPlanMnth = planUtils.genAllPlanMonth

    # Устанавливает у метадерева указатель на браузер.
    metaclass.SetUserData({'mode': 'planning', 'browserInterface': brows})
    obj = brows.getObject()
    obj.Show(True)


def loadData():
    """
    Загрузка данных-фактов.
    """
    metaclass = IMetaplan.IMetaplan()
    plan_manager = brws.icPlanMenager(metaclass)

    planUtils.loadDataPlan(metaclass)
