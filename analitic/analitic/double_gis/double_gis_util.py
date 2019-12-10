#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительные функции.
Функции взяты из проекта folium.
"""

import math
import numpy
import pandas

__version__ = (0, 1, 1, 1)


def validate_location(location):
    """
    Проверка одной пары координат широта / долгота и преобразование в список

     Проверьте это местоположение:
     * является переменной размера
     * с размером 2
     * позволяет индексировать (т.е. имеет порядок)
     * где оба значения являются плавающими (или конвертируемыми в плавающие)
     * и оба значения не являются NaN
    :return: list[float, float]
    """
    if isinstance(location, numpy.ndarray) \
            or (pandas is not None and isinstance(location, pandas.DataFrame)):
        location = numpy.squeeze(location).tolist()
    if not hasattr(location, '__len__'):
        raise TypeError(u'Расположение должно быть переменной размера, '
                        u'например список или кортеж, вместо этого получено '
                        '{!r} типа {}.'.format(location, type(location)))
    if len(location) != 2:
        raise ValueError(u'Ожидаемые два (широта, долгота) значения для местоположения, '
                         u'вместо этого получено: {!r}.'.format(location))
    try:
        coords = (location[0], location[1])
    except (TypeError, KeyError):
        raise TypeError(u'Местоположение должно поддерживать индексацию, например, список или '
                        u'кортеж, вместо этого получено {!r} тип {}.'
                        .format(location, type(location)))
    for coord in coords:
        try:
            float(coord)
        except (TypeError, ValueError):
            raise ValueError(u'Местоположение должно состоять из двух числовых значений, '
                             u'но {!r} тип {} не конвертируется в float.'
                             .format(coord, type(coord)))
        if math.isnan(float(coord)):
            raise ValueError(u'Значения местоположения не могут содержать NaN. Координаты <%s>' % str(coords))
    return [float(x) for x in coords]


def validate_locations(locations):
    """
    Проверьте итерацию с несколькими парами координат широта / долгота.
    :return: list[list[float, float]] or list[list[list[float, float]]]
    """
    locations = if_pandas_df_convert_to_numpy(locations)
    try:
        iter(locations)
    except TypeError:
        raise TypeError(u'Местоположения должны быть итерируемыми с парами координат,'
                        u' но вместо этого получено {!r}.'.format(locations))
    try:
        next(iter(locations))
    except StopIteration:
        raise ValueError(u'Пустая локация')
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
