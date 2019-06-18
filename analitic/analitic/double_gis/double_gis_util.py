#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительные функции.
Функции взяты из проекта folium.
"""

import math
import numpy
import pandas


def validate_location(location):
    """
    Проверка одной пары координат широта / долгота и преобразование в список

     Проверьте это местоположение:
     * является переменной размера
     * с размером 2
     * позволяет индексировать (т.е. имеет порядок)
     * где оба значения являются плавающими (или конвертируемыми в плавающие)
     * и оба значения не являются NaN
    @return: list[float, float]
    """
    if isinstance(location, numpy.ndarray) \
            or (pandas is not None and isinstance(location, pandas.DataFrame)):
        location = numpy.squeeze(location).tolist()
    if not hasattr(location, '__len__'):
        raise TypeError('Location should be a sized variable, '
                        'for example a list or a tuple, instead got '
                        '{!r} of type {}.'.format(location, type(location)))
    if len(location) != 2:
        raise ValueError('Expected two (lat, lon) values for location, '
                         'instead got: {!r}.'.format(location))
    try:
        coords = (location[0], location[1])
    except (TypeError, KeyError):
        raise TypeError('Location should support indexing, like a list or '
                        'a tuple does, instead got {!r} of type {}.'
                        .format(location, type(location)))
    for coord in coords:
        try:
            float(coord)
        except (TypeError, ValueError):
            raise ValueError('Location should consist of two numerical values, '
                             'but {!r} of type {} is not convertible to float.'
                             .format(coord, type(coord)))
        if math.isnan(float(coord)):
            raise ValueError('Location values cannot contain NaNs.')
    return [float(x) for x in coords]


def validate_locations(locations):
    """
    Проверьте итерацию с несколькими парами координат широта / долгота.
    @return: list[list[float, float]] or list[list[list[float, float]]]
    """
    locations = if_pandas_df_convert_to_numpy(locations)
    try:
        iter(locations)
    except TypeError:
        raise TypeError('Locations should be an iterable with coordinate pairs,'
                        ' but instead got {!r}.'.format(locations))
    try:
        next(iter(locations))
    except StopIteration:
        raise ValueError('Locations is empty.')
    try:
        float(next(iter(next(iter(next(iter(locations)))))))
    except (TypeError, StopIteration):
        # locations is a list of coordinate pairs
        return [validate_location(coord_pair) for coord_pair in locations]
    else:
        # locations is a list of a list of coordinate pairs, recurse
        return [validate_locations(lst) for lst in locations]


def if_pandas_df_convert_to_numpy(obj):
    """
    Вернуть массив Numpy из фрейма данных Pandas.

    Итерации по DataFrame имеют странные побочные эффекты, такие как первый
    строка, являющаяся именами столбцов. Преобразование в Numpy более безопасно.
    """
    if pandas is not None and isinstance(obj, pandas.DataFrame):
        return obj.values
    else:
        return obj


def parse_size(value):
    try:
        if isinstance(value, str) and value.endswith('px'):
            value_type = 'px'
            value = int(value.strip('px'))
            assert value > 0
        elif isinstance(value, (int, float)):
            value_type = 'px'
            value = int(value)
            assert value > 0
        else:
            value_type = '%'
            value = int(value.strip('%'))
            assert 0 <= value <= 100
    except Exception:
        msg = 'Cannot parse value {!r} as {!r}'.format
        raise ValueError(msg(value, value_type))
    return value, value_type
