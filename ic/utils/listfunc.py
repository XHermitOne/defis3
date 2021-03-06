#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительные функции обработки списков.
"""

import operator
import functools

__version__ = (0, 1, 1, 3)


def sort_multi_key(items, keys):
    """
    Сложная сортировка списка словарей.
    Взято с
        https://wiki.python.org/moin/SortingListsOfDictionaries
    Примеры использования:
        result = sort_multi_key(undecorated, ['key1', 'key2', 'key3'])
        result = sort_multi_key(undecorated, ['-key1', '-key2', '-key3'])

    :param items: Список словарей.
    :param keys: Порядок сортировки по ключам.
    :return: ОТсортированный список.
    """
    comparers = [((operator.itemgetter(key[1:].strip()), -1) if key.startswith('-') else (operator.itemgetter(key.strip()), 1)) for key in
                 keys]

    def comparer(left, right):
        """
        Функция сравнения.

        :param left: Левое значение для сравнения
        :param right:
        :return:
        """
        for fn, mult in comparers:
            fn_left = fn(left)
            fn_right = fn(right)
            # Это выражение для замены функции cmp из Python2
            #                        V
            result = (fn_left > fn_right) - (fn_left < fn_right)

            if result:
                return mult * result
        else:
            return 0

    return sorted(items, key=functools.cmp_to_key(comparer))


AND_COMPARE_SIGNATURE = 'AND'
OR_COMPARE_SIGNATURE = 'OR'


def filter_multi_key(items, finds, compare=AND_COMPARE_SIGNATURE):
    """
    Фильтрация списка словарей по значениям нескольких ключей.

    :param items: Список словарей.
    :param finds: Словарь значений ключей.
    :param compare: Метод сравнения И/AND или ИЛИ/OR.
    :return: Список отфильтрованных словарей.
    """
    result = list()
    if compare == AND_COMPARE_SIGNATURE:
        result = [item for item in items if all([item.get(key, None) == value for key, value in finds.items()])]
    elif compare == OR_COMPARE_SIGNATURE:
        result = [item for item in items if any([item.get(key, None) == value for key, value in finds.items()])]
    else:
        pass
    return result


def find_multi_key(items, find_keys, compare=AND_COMPARE_SIGNATURE):
    """
    Поиск в списке словарей по значениям нескольких ключей.

    :param items: Список словарей.
    :param find_keys: Словарь значений ключей.
    :param compare: Метод сравнения И/AND или ИЛИ/OR.
    :return: Найденный словарь или None если ничего не найдено.
    """
    filter_items = filter_multi_key(items, find_keys, compare)
    return filter_items[0] if filter_items else None
