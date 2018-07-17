#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль прикладной системы.
Автор(ы): 
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---
import ic.interfaces.icobjectinterface as icobjectinterface


#--- Интерфейсы ---
#   Имя класса
ic_class_name = 'INSIInterface'

class INSIInterface(icobjectinterface.icObjectInterface):
    """
    Интерфейс к подсистеме НСИ.
    """
    def __init__(self, MetaTree_=None):
        """
        Конструктор интерфейса.
        @param MetaTree_: Метадерево описания справочной подсистемы.
        """
        self.meta_tree=MetaTree_

    def HlpSprav(self,typSprav,ParentCode=(None,),field=None,datatime=None,rec=None,parentForm=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного справочника.
        @type typSprav: C{string}
        @param typSprav: Код типа (номер) справочника.
        @type ParentCode: C{...}
        @param ParentCode: Код более верхнего уровня.
        @param field: Задает поле или группу полей, которые надо вернуть.
        @type datatime: C{string}
        @param datatime: Время актуальности кода.
        @param rec: Текущая запись справочника.
        @param parentForm: Родительская форма.
        """
        pass
        
    def FSprav(self,typSprav, cod, field='name', datatime=None):
        """
        Поиск по коду.
    
        @type typeSprav: C{...}
        @param typeSprav: Тип справочника.
        @type cod: C{...}
        @param cod: Код строки справочника.
        @type field: C{string | list }
        @param field: Имя поля или список полей.
        @type datatime: C{string}
        @param datatime: Время актуальности справочной информации.
        @rtype: C{dictionary}
        @return: Значение либо словарь значений (если поле field задает список полей).
            None, если строка с заданным кодом не найдена.
        """
        pass
        