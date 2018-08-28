#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль прототипа компонента менеджера управления фильтрацией и сортировкой документов.

Менеджер фильтра документов расширяет возможности менеджера навигации документа.
В него входят функции управления фильтрами, привязки реквизитов к контролам управления
фильтрами и т.п.
"""

import wx

from ic.log import log
from ic.engine import panel_manager

from . import document_navigator_manager

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_DOCUMENT_FILTER_MANAGER = {'__parent__': document_navigator_manager.SPC_IC_DOCUMENT_NAVIGATOR_MANAGER,
                                  }

# Наименования внутренних атрибутов менеджера
DOC_FILTER_LIST_NAME = '__document_filter_list'
DOC_FILTER_ASSOCIATE_NAME = '__document_filter_associate'


class icDocumentFilterManagerProto(document_navigator_manager.icDocumentNavigatorManagerProto,
                                   panel_manager.icPanelManager):
    """
    Прототип компонента менеджера управления фитрами и сортировкой документов.
    """
    def setFilters(self, *filter_list):
        """
        Установить список фильтра документов.
        @param filter_list: Список фильтра.
        """
        setattr(self, DOC_FILTER_LIST_NAME, list(filter_list))

    def getFilters(self):
        """
        Получить список фильтра документов.
        @return: Список фильтра документов.
        """
        try:
            return getattr(self, DOC_FILTER_LIST_NAME)
        except:
            log.fatal(u'Ошибка получения списка фильтра документов')
        return list()

    def addFilter(self, filter_func):
        """
        Добавить фильтр в список.
        @param filter_func: Функция фильтрации.
        @return: Заполненнный список фильтра документов.
        """
        new_filter = self.getFilters()
        new_filter.append(filter_func)
        self.setFilters(*new_filter)
        return new_filter

    def filterDocs(self, filter_list=None, bRefresh=True):
        """
        Запуск фильтрации документов.
        @param filter_list: Список фильтрации.
            Если не определен, то берется текущий внутренний.
        @param bRefresh: Признак автоматического обновления списка документов.
        @return:
        """
        if filter_list is None:
            filter_list = self.getFilters()
        document_navigator_manager.icDocumentNavigatorManagerProto.filterDocs(self,
                                                                              doc_filter=filter_list,
                                                                              bRefresh=bRefresh)

    def setAssociates(self, **associate_dict):
        """
        Установить словарь ассоциаций.
        @param associate_dict: Словарь ассоциаций.
        """
        setattr(self, DOC_FILTER_ASSOCIATE_NAME, associate_dict)

    def getAssociates(self):
        """
        Получить словарь ассоциаций.
        @return: Словарь ассоциаций.
        """
        try:
            return getattr(self, DOC_FILTER_ASSOCIATE_NAME)
        except:
            log.fatal(u'Ошибка получения словаря ассоциаций')
        return list()

    def addAssociate(self, **associate):
        """
        Добавить ассоциацию.
        @param associate: Ассоциация.
            Ассоциация представляет из себя словарь.
            Главным атрибутом является type - тип реквизита.
            Тип реквизита необходим для определения функции фильтрации.
        @return: Заполненнный словарь ассоциации.
        """
        associate_dict = self.getAssociates()
        associate_dict[associate.get('name', None)] = associate
        self.setAssociates(**associate_dict)
        return associate_dict

    def associateDateRangeFilter(self, requisite_name,
                                 enable_check_box=None,
                                 begin_date_ctrl=None,
                                 end_date_ctrl=None,
                                 one_check_box=None):
        """
        Ассоциировать реквизит с контролами выбора фильтра диапазона дат.
        @param requisite_name: Наименование реквизита.
        @param enable_check_box: Чекбокс включения в фильтрацию контролов управления фильтра.
        @param begin_date_ctrl: Контрол выбора начальной даты фильтра.
        @param end_date_ctrl: Контрол выбора конечной даты фильтра.
        @param one_check_box: Чекбокс выбора выбора на конкретную дату.
        @return: True/False.
        """
        try:
            associate = dict(name=requisite_name,
                             type='DateTime',
                             enable_check_box=enable_check_box,
                             begin_date_ctrl=begin_date_ctrl,
                             end_date_ctrl=end_date_ctrl,
                             one_check_box=one_check_box)
            # Блок логики управления контролами
            # ...
            self.addAssociate(**associate)
            return True
        except:
            log.fatal(u'Ошибка установки ассоциации')
        return False

    def associateTextFilter(self, requisite_name,
                            enable_check_box=None,
                            text_ctrl=None,
                            contain_radiobox=None):
        """
        Ассоциировать реквизит с контролами выбора фильтра поиска в текстовом реквизите.
        @param requisite_name: Наименование реквизита.
        @param enable_check_box: Чекбокс включения в фильтрацию контролов управления фильтра.
        @param text_ctrl: Контрол ввода текстового фильтра.
        @param contain_radiobox: Радиобокс переключения поиска содержания.
            (*) В начале () Содержит () В конце () Точное совпадение
        @return: True/False.
        """
        try:
            associate = dict(name=requisite_name,
                             type='Text',
                             enable_check_box=enable_check_box,
                             text_ctrl=text_ctrl,
                             contain_radiobox=contain_radiobox)
            # Блок логики управления контролами
            # ...
            self.addAssociate(**associate)
            return True
        except:
            log.fatal(u'Ошибка установки ассоциации')
        return False

    def associateSpravFilter(self, requisite_name,
                             enable_check_box=None,
                             sprav_ctrl=None):
        """
        Ассоциировать реквизит с контролами выбора фильтра поиска в реквизите справочника.
        @param requisite_name: Наименование реквизита.
        @param enable_check_box: Чекбокс включения в фильтрацию контролов управления фильтра.
        @param sprav_ctrl: Контрол выбора фильтра по коду справочника.
        @return: True/False.
        """
        try:
            associate = dict(name=requisite_name,
                             type='Sprav',
                             enable_check_box=enable_check_box,
                             sprav_ctrl=sprav_ctrl)
            # Блок логики управления контролами
            # ...
            self.addAssociate(**associate)
            return True
        except:
            log.fatal(u'Ошибка установки ассоциации')
        return False

    def associateMultiSpravFilter(self, requisite_name,
                                  enable_check_box=None,
                                  sprav_ctrl=None):
        """
        Ассоциировать реквизит с контролами выбора фильтра поиска в реквизите справочника по нескольким кодам.
        @param requisite_name: Наименование реквизита.
        @param enable_check_box: Чекбокс включения в фильтрацию контролов управления фильтра.
        @param sprav_ctrl: Контрол выбора фильтра по ескольким кодам справочника.
        @return: True/False.
        """
        try:
            associate = dict(name=requisite_name,
                             type='MultiSprav',
                             enable_check_box=enable_check_box,
                             sprav_ctrl=sprav_ctrl)
            # Блок логики управления контролами
            # ...
            self.addAssociate(**associate)
            return True
        except:
            log.fatal(u'Ошибка установки ассоциации')
        return False

    def buildFilter(self, logic='AND'):
        """
        Построить фильтр документов по логике выбора в контролах.
        @param logic: Связующая логика фильтра.
            М.б. AND - связь по И / OR - связь по ИЛИ.
        @return: Заполненный фильтр.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        """
        pass

    def refreshFilter(self):
        """
        Обновить список документов в соответствии с выбранными фильтрами.
        @return: True/False.
        """
        try:
            return True
        except:
            log.fatal(u'Ошибка обновления списка документов по фильтру')
        return False
