#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Модуль подсистемы управления мониторами.
Автор(ы): Колчанов Шурик.

Мониторы - это запись в объектной БД,
    у каждого элемента которого следующая структура:
    cod - код запроса;
    description - описание запроса;
    edit_form - указание формы-визарда заполнения тела запроса;
    view_form - указание формы-монитора отображения запроса;
    query - тело запроса.
    monitor_link - серилизованный словарь ссылок на другие мониторы
        формат:
            {'monitor alias1':'monitor cod1',...}
            
При работе с мониторами экземпляр класса icMonitorNode
    передается в каждый монитор в пространство имен
    в виде объекта MonitorNode.
    MonitorNode - объект управления монитором,
    которого он описывает.
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение модулей ---
import wx

#import NSI.spravfunc
from ic.log import ic_log
from ic.engine import ic_user
from ic.components import icResourceParser
from ic.utils import util
from ic.utils import resource
#from ic.db import tabclass
#from ic.db import ic_sqlobjtab

#--- Константы ---
#Тип справочника мониторов по умолчанию
MONITOR_SPRAV_TYPE_DEFAULT='Monitors'
#Имя объекта управления монитора в форме монитора
MONITOR_OBJ_NAME='MonitorNode'

#Режимы навигатора
IC_VIEW_MODE=0
IC_WIZARD_MODE=1

#Режим просмотра
IC_NEW_MONITOR=0 #Кажды раз открывать новую страницу
IC_ONE_MONITOR=1 #Перед открытием новой страницы закрывать старую

#--- Функции ---

#--- Классы ---
class icMonitorNode:
    """
    Узел монитора в гипер графе мониторов.
    """
    def __init__(self,Cod_,Parent_=None):
        """
        Конструктор.
        """
        #Тип справочника запросов
        self.sprav_type=MONITOR_SPRAV_TYPE_DEFAULT
        self.cod=Cod_
        self.parent_win=Parent_
        self.view_mode=IC_NEW_MONITOR
        self.work_mode=IC_VIEW_MODE
        self.body=None

    def getViewMode(self):
        return self.view_mode
        
    def setViewMode(self,Mode_):
        self.view_mode=Mode_
        
    def getWorkMode(self):
        return self.work_mode
        
    def setWorkMode(self,Mode_):
        self.work_mode=Mode_
        
    def view(self, bIndicator=False):
        """
        Запуск монитора на просмотр.
        """
        monitor_dict=NSI.spravfunc.FSprav(self.sprav_type,
            self.cod,['name','s1','s2','s3'])
        print '>>>viewMonitor',monitor_dict
        #Инициализировать тело монитора
        self.body=self.loadBody()
        
        if monitor_dict['s2']:
            if issubclass(self.parent_win.__class__,wx.Notebook):
                monitor_form=icResourceParser.CreateForm(monitor_dict['s2'],
                    parent=self.parent_win, bIndicator = bIndicator,
                    evalSpace=util.InitEvalSpace({MONITOR_OBJ_NAME:self}))
                self.parent_win.AddPage(monitor_form,
                    monitor_dict['name'],select=True)
                self.parent_win.Refresh()
                monitor_form.Refresh()
                return monitor_form
            elif self.parent_win:
                monitor_form=icResourceParser.CreateForm(monitor_dict['s2'],
                    parent=self.parent_win, bIndicator = bIndicator,
                    evalSpace=util.InitEvalSpace({MONITOR_OBJ_NAME:self}))
                return monitor_form
            else:
                return ic_user.icAddMainOrgPage(monitor_dict['s2'],
                    monitor_dict['name'])

    def wizard(self, bIndicator=False):
        """
        Запуск визарда монитора.
        """
        monitor_dict=NSI.spravfunc.FSprav(self.sprav_type,
            self.cod,['name','s1','s2','s3'])
        print '>>>wizardMonitor',monitor_dict
        #Инициализировать тело монитора
        self.body=self.loadBody()
        if monitor_dict['s1']:
            if issubclass(self.parent_win.__class__,wx.Notebook):
                monitor_form=icResourceParser.CreateForm(monitor_dict['s1'],
                    parent=self.parent_win, bIndicator = bIndicator,
                    evalSpace=util.InitEvalSpace({MONITOR_OBJ_NAME:self}))
                self.parent_win.AddPage(monitor_form,
                    monitor_dict['name'],select=True)
                self.parent_win.Refresh()
                return monitor_form
            elif self.parent_win:
                monitor_form=icResourceParser.CreateForm(monitor_dict['s1'],
                    parent=self.parent_win, bIndicator = bIndicator,
                    evalSpace=util.InitEvalSpace({MONITOR_OBJ_NAME:self}))
                return monitor_form
            else:
                return ic_user.icAddMainOrgPage(monitor_dict['s1'],
                    monitor_dict['name'])

    def edit(self):
        """
        Редактирование мониторов.
            Редактирование производится стандартным
            образом ч/з справочную систему.
        """
        #   Вызываем редактирование справочника
        #   1. Определяем размер первого уровня и структурный фильтр для справочника
        monitors_id=NSI.spravfunc.getSpravId(self.sprav_type)
        flt = {"NsiStd":{"id_nsi_list":monitors_id}}
    
        #   2. Вызываем форму для редактирования
        icResourceParser.ResultForm(NSI.spravfunc.NsiEdtFormName(self.sprav_type),
            filter=flt, parent=ic_user.icGetMainWin())
    
    def viewLink(self,LinkAlias_):
        """
        Запуск просмотра монитора по ссылке.
        @param LinkAlias_: Алиас ссылаемого монитора.
        """
        monitor_dict=NSI.spravfunc.FSprav(self.sprav_type,
            self.cod,['name','s4'])
        print '>>>viewLinkMonitor',monitor_dict
        if monitor_dict['s4'].strip():
            links=dict(monitor_dict['s4'])
            if links.has_key(LinkAlias_):
                monitor_node=icMonitorNode(links[LinkAlias_],
                    self.parent_win)
                monitor_node.setWorkMode(IC_VIEW_MODE)
                monitor_node.setViewMode(self.view_mode)
                return monitor_node.view()

    def wisardLink(self,LinkAlias_):
        """
        Запуск визарда монитора по ссылке.
        @param LinkAlias_: Алиас ссылаемого монитора.
        """
        monitor_dict=NSI.spravfunc.FSprav(self.sprav_type,
            self.cod,['name','s4'])
        print '>>> wizardLinkMonitor',monitor_dict
        if monitor_dict['s4'].strip():
            links=dict(monitor_dict['s4'])
            if links.has_key(LinkAlias_):
                monitor_node=icMonitorNode(links[LinkAlias_],
                    self.parent_win)
                monitor_node.setWorkMode(IC_WIZARD_MODE)
                monitor_node.setViewMode(self.view_mode)
                return monitor_node.wizard()

    def loadBody(self):
        """
        Загрузить тело монитора.
        """
        monitor_dict=NSI.spravfunc.FSprav(self.sprav_type,
            self.cod,['name','s3'])
        try:
            return eval(monitor_dict['s3'])
        except:
            return monitor_dict['s3']

    def getCurrentBody(self):
        if self.body:
            return self.body
        self.body=self.loadBody()
        return self.body
        
    def saveBody(self,Body_=None):
        """
        Сохранить тело монитора/запроса.
        @param Body_: Тело монитора.
            В основном это словарно-списковая структура.
        @return: Результат выполнения операции True/False.
        """
        #nsi_std=tabclass.CreateTabClass('NsiStd')
        nsi_std=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
                    nameRes='NsiStd'))
        monitor_id=NSI.spravfunc.getSpravCodeId(self.sprav_type,
            self.cod)
        if monitor_id:
            #monitor_rec=nsi_std.get(monitor_id)
            #monitor_rec.set(s3=str(Body_))
            monitor_rec.update(monitor_id,s3=str(Body_))
            return True
        return False

    def _genMonitorCode(self,NSIStd_,ParentCode_=''):
        """
        Генерация кода для нового монитора.
        @param NSIStd_: SQLObject класс данных.
        @param ParentCode_: Код монитора родительского уровня.
        @return: Возвращает сгенерированный код.
        """
        nsi_std=NSIStd_
        for i_cur_cod in range(100):
            cur_cod=ParentCode_+'%02d'%(i_cur_cod)
            #Если запись с таким кодом уже существует,
            #то продолжить генерацию
            if nsi_std.select(nsi_std.q.cod==cur_cod).count():
                continue
            else:
                return cur_cod
        return ParentCode_+'XX'
        
    def newMonitor(self,ViewForm_=None,
        WizardForm_=None,Body_=None):
        """
        Создать новый монитор.
        @param ViewForm_: Форма просмотра монитора.
        @param WizardForm_: Форма визарда монитора.
        @param Body_: Тело монитора/запроса.
        @return: Функция возвращает код справочника нового
            монитора или None в случае ошибки.
        """
        try:
            #nsi_std=tabclass.CreateTabClass('NsiStd')
            nsi_std=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
                nameRes='NsiStd'))
            new_cod=self._genMonitorCode(nsi_std,self.cod)
            rec=nsi_std.add(type=self.sprav_type,cod=new_cod,
                name='NewMonitor '+new_cod,
                s1=WizardForm_,s2=ViewForm_,s3=Body_)
            return new_cod
        except:
            ic_log.icLogErr('Ошмбка создания монитора')
            return None