#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции формирования стандартных фильтров.
ВНИМАНИЕ! У всех фильтров корневым элементом д.б. группа.
"""


def get_date_between_filter(requisite_name, min_date, max_date):
    """
    Фильтр диапазона дат.
    @param requisite_name: Имя реквизита даты.
    @param min_date: Минимальная дата.
    @param max_date: Максимальная дата.
    @return: Заполненный фильтр.
    """
    filter_dict = dict()
    filter_dict['requisite'] = requisite_name
    filter_dict['type'] = 'compare'
    filter_dict['arg_1'] = min_date
    filter_dict['arg_2'] = max_date
    filter_dict['func'] = 'between'
    group_dict = dict()
    group_dict['name'] = 'grp'
    group_dict['type'] = 'group'
    group_dict['logic'] = 'AND'
    group_dict['children'] = [filter_dict]
    return group_dict
