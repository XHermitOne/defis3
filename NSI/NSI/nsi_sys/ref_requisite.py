#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Реквизит.
Реквизит определяет атрибут объекта, указывает его тип,
описывает поля редактирования/просмотра этого атрибута,
поле хранения атрибута и т.п.
"""

from ic.components import icwidget

from ic.log import log

# Версия
__version__ = (0, 1, 1, 1)

SPC_IC_REFREQUISITE = {'type': 'RefRequisite',
                       'name': 'default',
                       'description': '',  # Описание

                       # --- Свойства генерации поля хранения ---
                       'type_val': 'T',  # Тип значения реквизита
                       'len': None,  # Длина значения реквизита
                       'field': None,  # Поле таблицы родительского компонента,
                                       # в котором храниться значение реквизита
                       'default': None,  # Значение по умолчанию

                       'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                       'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                       # --- Свойства генерации контролов редактирования/просмотра ---
                       'label': u'',  # Надпись реквизита
                                      # Если надпись пустая, то берется вместо надписи описание (description)

                       '__parent__': icwidget.SPC_IC_SIMPLE,
                       '__attr_hlp__': {'type_val': u'Тип значения реквизита',
                                        'len': u'Длина значения реквизита',
                                        'field': u'Поле таблицы родительского компонента, в котором храниться значение реквизита',
                                        'default': u'Значение по умолчанию',

                                        'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                        'get_value': u'Функционал, исполняемый при получениии значения реквизита',

                                        'label': u'Надпись реквизита',
                                        },
                       }

SPC_IC_REFNSIREQUISITE = {'type': 'RefNSIRequisite',
                          'name': 'default',
                          'description': '',  # Описание

                          # --- Свойства генерации контролов редактирования/просмотра ---
                          'label': u'',  # Надпись реквизита
                                         # Если надпись пустая, то берется вместо надписи описание (description)

                          # --- Свойства генерации полей хранения ---
                          'field': None,  # Поле кода справочника

                          'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                          'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                          # --- Ссылка на объект справочника ---
                          'nsi_psp': None,  # Справочник NSI
                          'auto_set': True,  # Признак автоматического заполнения полей при редактировании

                          '__parent__': icwidget.SPC_IC_SIMPLE,
                          '__attr_hlp__': {'label': u'Надпись реквизита',

                                           'field': u'Поле кода справочника',

                                           'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                           'get_value': u'Функционал, исполняемый при получениии значения реквизита',

                                           'nsi_psp': u'Справочник NSI',
                                           'auto_set': u'Признак автоматического заполнения полей при редактировании',
                                           },
                          }


class icRefRequisiteInterface(object):
    """
    Общий интерфейс реквизитов.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        # Родительский объект
        self.parent = parent


class icRefRequisiteProto(icRefRequisiteInterface):
    """
    Реквизит.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        icRefRequisiteInterface.__init__(self, parent)

        # Имя реквизита
        self.name = None

        # Имя поля
        self.field = None
        # Описание
        self.description = ''
        # Тип поля
        self.type_val = 'T'
        # Длина поля
        self.len = None

    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        return self.type_val

    def getLabel(self):
        """
        Надпись реквизита.
        """
        return u''


class icRefNSIRequisiteProto(icRefRequisiteInterface):
    """
    Реквизит связи со справочником системы NSI.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        icRefRequisiteInterface.__init__(self, parent)

        # Текущее значение реквизита - код справочника
        self.value = None

        # Объект справочника
        self.sprav = None

    def getSprav(self):
        """
        Объект справочника.
        """
        return self.sprav
