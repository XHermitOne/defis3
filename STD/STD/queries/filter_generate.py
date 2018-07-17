#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции генерации фильтров для вызова из функций прикладного уровня.
Использование:
    create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))

Фильтр представляет собой словарно-списковую структуру, состоящую из
структур двух типов объектов: группа и реквизит.

Группа - структура, описывающая группировку связанных скобками элементов и
соединяемых одним логическим операндом (И, ИЛИ, НЕ).

Группа:
{
 'name': Наименование группы. Обычно соответствует логическому операнду.
 'type': Тип группы. Строка <group>.
 'logic': Логический операнд. AND или OR или NOT.
 'children': Список реквизитов - элементов группы.
}

Реквизит - структура, описывающая элемент группы, соответствует
полю таблицы. Кроме указания поля включает в себя оператор сравнения
и аргументы оператора сравнения.

Реквизит:

{
 'requisite': Наименование реквизита. Обычно соответствует имени поля таблицы.
 'type': Тип. Слово <compare>.
 'arg_1': Значение аргумента 1.
 'arg_2': Значение аргумента 2.
 'get_args': Дополнительная функция получения аргументов.
 'func': Имя функции сравнения. Функция сравнения выбирается по имени из
            словаря функций сравнения DEFAULT_ENV_FUNCS, определенного
            в модуле filter_builder_env.
 '__sql__': Кортеж элментов sql выражения соответствующего данному реквизиту.
            Поэтому генерация WHERE секции SQL заключается в правильном
            соединении нужных строк этого ключа.
}
"""

# Version
__version__ = (0, 0, 1, 1)


def create_filter_group(logic='AND', *compare_requisites):
    """
    Создать группу фильтра
    @param logic: Логический операнд группы.
    @param compare_requisites: Список реквизитов фильтра.
    @return: Сгенерированные/Заполненный словарь группы.
        {
        'name': Наименование группы. Обычно соответствует логическому операнду.
        'type': Тип группы. Строка <group>.
        'logic': Логический операнд. AND или OR или NOT.
        'children': Список реквизитов - элементов группы.
        }
    """
    compare_requisites = [requisite for requisite in compare_requisites if requisite]
    filter_grp = dict(name=logic, type='group',
                      logic=logic, children=compare_requisites)
    return filter_grp


def create_filter_group_AND(*compare_requisites):
    """
    Создать группу фильтра с логическим операндом <И>.
    @param compare_requisites: Список реквизитов фильтра.
    """
    return create_filter_group('AND', *compare_requisites)


def create_filter_group_OR(*compare_requisites):
    """
    Создать группу фильтра с логическим операндом <ИЛИ>.
    @param compare_requisites: Список реквизитов фильтра.
    """
    return create_filter_group('OR', *compare_requisites)


def create_filter_group_NOT(*compare_requisites):
    """
    Создать группу фильтра с логическим операндом <НЕ>.
    @param compare_requisites: Список реквизитов фильтра.
    """
    return create_filter_group('NOT', *compare_requisites)


# --- Операции сравнения ---
# Замена операций сравнения на их имена
COMPARE_OPERATION_TRANSLATE = {'==': 'equal',
                               '<>': 'not_equal',
                               '<=': 'lesser_or_equal',
                               '>=': 'great_or_equal',
                               '>': 'great',
                               '<': 'leser',
                               '>..<': 'between',
                               '.<>.': 'not_between',
                               'N': 'null',

                               '..)': 'startswith',
                               '(..': 'endswith',
                               '(..)': 'contain',
                               }

DEFAULT_COMPARE_OPERATE = '=='


def create_filter_compare_requisite(name, compare_operate=DEFAULT_COMPARE_OPERATE,
                                    arg_1=None, arg_2=None):
    """
    Создать реквизит фильтра.
    @param name: Наименование реквизита. Обычно соответствует имени поля таблицы.
    @param compare_operate: Операция сравнения.
    @param arg_1: Значение аргумента 1.
    @param arg_2: Значение аргумента 2.
    @return: Реквизит:
        {
        'requisite': Наименование реквизита. Обычно соответствует имени поля таблицы.
        'type': Тип. Слово <compare>.
        'arg_1': Значение аргумента 1.
        'arg_2': Значение аргумента 2.
        'get_args': Дополнительная функция получения аргументов.
        'func': Имя функции сравнения. Функция сравнения выбирается по имени из
                словаря функций сравнения DEFAULT_ENV_FUNCS, определенного
                в модуле filter_builder_env.
        '__sql__': Кортеж элментов sql выражения соответствующего данному реквизиту.
                   Поэтому генерация WHERE секции SQL заключается в правильном
                   соединении нужных строк этого ключа.
        }
    """
    compare_func = COMPARE_OPERATION_TRANSLATE.get(compare_operate, compare_operate)
    filter_compare = dict(requisite=name, type='compare',
                          arg_1=arg_1, arg_2=arg_2,
                          func=compare_func)
    return filter_compare
