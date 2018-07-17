#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Регистры.

РЕГИСТР НАКОПЛЕНИЯ.
Объект позволяющий накапливать значения реквизитов.
Аналог объекта накопления это виртуальный склад или
регистр накополения в 1С.

РЕГИСТР БИЗНЕС ОБЪЕКТА
Объект позволяющий отслеживать изменение состояния
и реквизитов бизнес объекта.

@type SPC_IC_REGISTER: C{dictionary}
@var SPC_IC_REGISTER: Спецификация на ресурсное описание регистра.
Описание ключей SPC_IC_REGISTER:

    - B{name = 'default'}: Имя.
    - B{type = 'Register'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{db = None}: БД - хранилище объекта.
    - B{prototype = None}: Регистр, у которого наследуются измерения и ресурсы.
"""

# --- Imports ---

from ic.components import icwidget

from . import acc_registry
from . import obj_registry


# Версия
__version__ = (0, 0, 0, 4)

# --- Specifications ---

SPC_IC_ACCUMULATE_REGISTRY = {'type': 'AccumulateRegistry',

                              # БД хранения данных
                              'db': None,

                              # Список имен реквизитов измерений
                              'dimension_requisites': [],
                              # Список имен реквизитов ресурсов
                              'resource_requisites': [],

                              # Имя таблицы операций движения
                              'operation_table': 'operation_tab',

                              # Имя таблицы итогов
                              'result_table': 'result_tab',

                              '__parent__': icwidget.SPC_IC_SIMPLE,
                              }

SPC_IC_OBJECT_REGISTRY = {'type': 'ObjectRegistry',

                          # БД хранения данных
                          'db': None,

                          # Имя таблицы операций движения
                          'operation_table': 'operation_object',

                          # Имя таблицы объектов
                          'obj_table': 'object_tab',

                          '__parent__': icwidget.SPC_IC_SIMPLE,
                          }


class icAccumulateRegistryProto(acc_registry.icAccRegistry):
    """
    НАКОПИТЕЛЬНЫЙ РЕГИСТР.
    Аналог объекта накопления это виртуальный склад или
    регистр накополения в 1С.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        acc_registry.icAccRegistry.__init__(self, *args, **kwargs)


class icObjectRegistryProto(obj_registry.icObjRegistry):
    """
    РЕГИСТР БИЗНЕС ОБЪЕКТА.
    Объект позволяющий отслеживать изменение состояния
    и реквизитов бизнес объекта.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        obj_registry.icObjRegistry.__init__(self, *args, **kwargs)
