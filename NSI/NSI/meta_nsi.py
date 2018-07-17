#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль прикладной системы.
Автор(ы): 
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Импортирование библиотек ---
from ic.components import icwidget
#--- Функции ---

#--- Классы ---
class icMetaNSI(icwidget.icSimple):
    """
    Интерфейс справочной системы.
    """
    def __init__(self, parent, id=-1, component=None, logType = 0, evalSpace = None,
                        bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        icwidget.icSimple.__init__(self,parent,id,component,logType,evalSpace, bGenUUID=False)

        self._meta_tree=icMetaTree(parent,id,component,logType,evalSpace, bGenUUID=False)