#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Формирование окружения для работы редактора критериев выборки коллекций.
Окружение редактора фильтров - словарно списковая структура формата:
{
    'requisites': Список возможных для выбора реквизитов
    'logic':Стандартные логические операции
    'funcs':Стандартные функции
}

Представление реквизита в редакторе критериев выборки коллекций:
{
    'name':Англоязычное имя реквизита
    'description':Рускоязычное описание реквизита
    'field':Имя поля хранения реквизита
    'type':Тип значения реквизита
    'funcs':Список функций 
}

Типы значений реквизитов:
REQUISITE_TYPE_STR='str' - Строка
REQUISITE_TYPE_INT='int' - Целое
REQUISITE_TYPE_FLOAT='float' - С плавающей точкой
REQUISITE_TYPE_NUM='number' - Число
REQUISITE_TYPE_DATETIME='datetime' - Дата/время в строковом представлении
REQUISITE_TYPE_NSI='NSI' - Справочник

Оформление функций:
    Все функции должны возвращать кортеж элементов
    проверки в понятиях SQL
    Например: ('cost','>=','2300.00') или
              ('name','ILIKE(%s)','\'%рога и копыта%\'')

Регистрация уже существующей функции:
1. Зарегистрировать структуру функции в словаре DEFAULT_ENV_..._FUNCS.
    Например: DEFAULT_ENV_NSI_FUNCS
2. Зарегистрировать имя функции в списке DEFAULT_..._FUNCS.
    Например: DEFAULT_NSI_FUNCS
3. Зарегистрировать питоновский аналог функции в словаре PY_..._FUNCS.
    Например: PY_NSI_FUNCS
Все делать по аналогии с другими функциями.
"""

# Imports
import wx

from ic.kernel import io_prnt
from . import filter_py_funcs as pyf
from . import filter_ext_funcs as exf

# Образы
from ic.imglib import logic_img as img_lib

# Version
__version__ = (0, 0, 3, 4)


# Constants
# Типы значений реквизитов
REQUISITE_TYPE_STR = 'str'  # Строка
REQUISITE_TYPE_INT = 'int'  # Целое
REQUISITE_TYPE_FLOAT = 'float'  # С плавающей точкой
REQUISITE_TYPE_NUM = 'number'   # Число
REQUISITE_TYPE_D = 'd_text'  # Дата/время в строковом представлении
REQUISITE_TYPE_DATETIME = 'datetime'  # Дата/время в представлении datetime
REQUISITE_TYPE_NSI = 'NSI'  # Справочник

# Словарь преобразования типов полей БД в типы значений реквизитов
DB_FLD_TYPE2REQUISITE_TYPE = {'T': REQUISITE_TYPE_STR,
                              'I': REQUISITE_TYPE_INT,
                              'F': REQUISITE_TYPE_FLOAT,
                              'D': REQUISITE_TYPE_D,
                              'DateTime': REQUISITE_TYPE_DATETIME,
                              'NSI': REQUISITE_TYPE_NSI,
                              }
    
# Functions
# Все функции должны возвращать кортеж элементов
# проверки в понятиях SQL
# Например: ('cost','>=','2300.00') или
#       ('name','ILIKE(%s)','\'%рога и копыта%\'')

DEFAULT_DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'


def _get_requisite_field(requisite):
    """
    Определить поле хранения реквизита.
    """
    if ('field' not in requisite) or (not requisite['field']):
        if ('name' not in requisite) or (not requisite['name']):
            io_prnt.outLog(u'Не определено поле хранения для реквизита <%s>' % requisite)
            return None
        field = requisite['name'].lower()
    else:
        field = requisite['field']
    return field


def num_equal(requisite, value):
    """
    Функция сравнения значения числового реквизита со значением.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '=', value


def str_equal(requisite, value):
    """
    Функция сравнения значения строкового реквизита со значением.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '=', u'\''+value+u'\''


def datetime_equal(requisite, value):
    """
    Функция сравнения значения datetime реквизита со значением.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def equal(requisite, value):
    """
    Функция сравнения значения реквизита с указанным значением.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_equal(requisite, value)

    # По умолчанию сравнивать строки
    return str_equal(requisite, value)


def num_not_equal(requisite, value):
    """
    Функция сравнения значения числового реквизина с указанным значением на неравенство.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<>', value


def str_not_equal(requisite, value):
    """
    Функция сравнения значения строкового реквизита с указанным значением на неравенство.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<>', u'\''+value+u'\''


def datetime_not_equal(requisite, value):
    """
    Функция сравнения значения datetime реквизита с указанным значением на неравенство.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<>', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def not_equal(requisite, value):
    """
    Функция сравнения значения реквизита с указанным значением на неравенство.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_not_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_not_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_not_equal(requisite, value)

    # По умолчанию сравнивать строки
    return str_not_equal(requisite, value)


def num_great(requisite, value):
    """
    Функция сравнения числового значения реквизита на > (больше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>', value


def str_great(requisite, value):
    """
    Функция сравнения строкового значения реквизита на > (больше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>', u'\''+value+u'\''


def datetime_great(requisite, value):
    """
    Функция сравнения строкового значения реквизита на > (больше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def great(requisite, value):
    """
    Функция сравнения значения реквизита на > (больше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_great(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_great(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_great(requisite, value)

    # По умолчанию сравнивать числа
    return num_great(requisite, value)


def num_great_or_equal(requisite, value):
    """
    Функция сравнения числового значения реквизита на >= (больше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>=', value


def str_great_or_equal(requisite, value):
    """
    Функция сравнения строкового значения реквизита на >= (больше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>=', u'\''+value+u'\''


def datetime_great_or_equal(requisite, value):
    """
    Функция сравнения datetime значения реквизита на >= (больше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '>=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def great_or_equal(requisite, value):
    """
    Функция сравнения значения реквизита на >= (больше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_great_or_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_great_or_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_great_or_equal(requisite, value)

    # По умолчанию сравнивать числа
    return num_great_or_equal(requisite, value)


def num_lesser(requisite, value):
    """
    Функция сравнения числового значения реквизита на < (меньше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<', value


def str_lesser(requisite, value):
    """
    Функция сравнения строкового значения реквизита на < (меньше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<', u'\''+value+u'\''


def datetime_lesser(requisite, value):
    """
    Функция сравнения строкового значения реквизита на < (меньше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def lesser(requisite, value):
    """
    Функция сравнения значения реквизита на < (меньше).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_lesser(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_lesser(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_lesser(requisite, value)

    # По умолчанию сравнивать числа
    return num_lesser(requisite, value)


def num_lesser_or_equal(requisite, value):
    """
    Функция сравнения числового значения реквизита на <= (меньше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<=', value


def str_lesser_or_equal(requisite, value):
    """
    Функция сравнения строкового значения реквизита на <= (меньше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<=', u'\''+value+u'\''


def datetime_lesser_or_equal(requisite, value):
    """
    Функция сравнения datetime значения реквизита на <= (меньше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, '<=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def lesser_or_equal(requisite, value):
    """
    Функция сравнения значения реквизита на <= (меньше или равно).
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_lesser_or_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_lesser_or_equal(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_lesser_or_equal(requisite, value)

    # По умолчанию сравнивать числа
    return num_lesser_or_equal(requisite, value)


def num_between(requisite, minimum, maximum):
    """
    Функция сравнения числового значения реквизита на между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return field, 'BETWEEN ', minimum, ' AND ', maximum


def str_between(requisite, minimum, maximum):
    """
    Функция сравнения строкового значения реквизита на между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return field, 'BETWEEN ', u'\''+minimum+u'\'', ' AND ', u'\''+maximum+u'\''


def datetime_between(requisite, minimum, maximum):
    """
    Функция сравнения datetime значения реквизита на между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return field, 'BETWEEN ', \
           '\'%s\'' % minimum.strftime(DEFAULT_DATETIME_FORMAT), ' AND ', \
           '\'%s\'' % maximum.strftime(DEFAULT_DATETIME_FORMAT)


def between(requisite, minimum, maximum):
    """
    Функция сравнения значения реквизита на между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_between(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_between(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_between(requisite, minimum, maximum)

    # По умолчанию сравнивать строки
    return str_between(requisite, minimum, maximum)


def num_not_between(requisite, minimum, maximum):
    """
    Функция сравнения числового значения реквизита на не между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, 'BETWEEN ', minimum, ' AND ', maximum, ')'


def str_not_between(requisite, minimum, maximum):
    """
    Функция сравнения строкового значения реквизита на не между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, 'BETWEEN ', u'\''+minimum+u'\'', ' AND ', u'\''+maximum+u'\'', ')'


def datetime_not_between(requisite, minimum, maximum):
    """
    Функция сравнения datetime значения реквизита на не между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, 'BETWEEN ', \
           '\'%s\'' % minimum.strftime(DEFAULT_DATETIME_FORMAT), ' AND ', \
           '\'%s\'' % maximum.strftime(DEFAULT_DATETIME_FORMAT), ')'


def not_between(requisite, minimum, maximum):
    """
    Функция сравнения значения реквизита на не между.
    @param requisite: Описание реквизита из окружения.
    @param minimum: Минимальное значение диапазона.
    @param maximum: Максимальное значение диапазона.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return num_not_between(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_not_between(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return datetime_not_between(requisite, minimum, maximum)

    # По умолчанию сравнивать строки
    return str_not_between(requisite, minimum, maximum)


def str_contain(requisite, value):
    """
    Функция сравнения строкового значения реквизита на содержание в нем подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, 'ILIKE(', '\'%'+value+'%\'', ')'


def contain(requisite, value):
    """
    Функция сравнения значения реквизита на содержание в нем подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_contain(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_contain(requisite, value)


def str_not_contain(requisite, value):
    """ 
    Функция сравнения строкового значения реквизита на отсутствие в нем подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, 'ILIKE(', '\'%'+value+'%\'', '))'


def not_contain(requisite, value):
    """ 
    Функция сравнения значения реквизита на отсутствие в нем подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_not_contain(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_not_contain(requisite, value)


def str_left_equal(requisite, value):
    """ 
    Функция сравнения строкового значения реквизита на начало с подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, 'ILIKE(', '\''+value+'%\'', ')'


def left_equal(requisite, value):
    """ 
    Функция сравнения значения реквизита на начало с подстроки.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_left_equal(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_left_equal(requisite, value)


def str_right_equal(requisite, value):
    """ 
    Функция сравнения строкового значения реквизита на окончание подстрокой.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, 'ILIKE(', '\'%'+value+'\'', ')'


def right_equal(requisite, value):
    """
    Функция сравнения значения реквизита на окончание подстрокой.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_right_equal(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_right_equal(requisite, value)


def str_mask(requisite, value):
    """
    Функция сравнения строкового значения реквизита на соответствие маске.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return field, 'ILIKE(', '\''+value+'\'', ')'


def mask(requisite, value):
    """
    Функция сравнения значения реквизита на соответствие маске.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_mask(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_mask(requisite, value)


def str_not_mask(requisite, value):
    """
    Функция сравнения строкового значения реквизита на не соответствие маске.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, 'ILIKE(', '\''+value+'\'', '))'


def not_mask(requisite, value):
    """
    Функция сравнения значения реквизита на не соответствие маске.
    @param requisite: Описание реквизита из окружения.
    @param value: Сравневаемое значение.
    """
    if 'type' in requisite and requisite['type']:
        # Если тип значения реквизита определен, то сравнить по типу
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return str_not_mask(requisite, value)
        
    # По умолчанию сравнивать строки
    return str_not_mask(requisite, value)


def is_null(requisite):
    """
    Функция сравнения значения реквизита на пустое значение.
    @param requisite: Описание реквизита из окружения.
    """
    field = _get_requisite_field(requisite)
    return field, ' IS NULL'


def is_not_null(requisite):
    """
    Функция сравнения значения реквизита на не пустое значение.
    @param requisite: Описание реквизита из окружения.
    """
    field = _get_requisite_field(requisite)
    return field, ' IS NOT NULL'


def into(requisite, values):
    """
    Функция сравнения значения реквизита на принадлежность набору.
    @param requisite: Описание реквизита из окружения.
    @param values: Список значений.
    """
    field = _get_requisite_field(requisite)
    return field, ' IN ', tuple(values)


def not_into(requisite, values):
    """
    Функция сравнения значения реквизита на не принадлежность набору.
    @param requisite: Описание реквизита из окружения.
    @param values: Список значений.
    """
    field = _get_requisite_field(requisite)
    return 'NOT (', field, ' IN ', tuple(values), ')'


# Constants
# Логическое операции
LOGIC_OPERATION = {'name': 'AND',  # Английское название логической операции
                   'description': u'И',  # Русское название
                   }

# Представление функции в редакторе критериев выборки коллекций
FILTER_FUNC = {'func': None,         # Объект функции
               'description': None,  # Рускоязычное описание функции
               'args': [],           # Список аргументов функции
               }

# Представление аргумента функции в редакторе критериев выборки коллекций
FILTER_ARG = {'name': None,         # Англоязычное наименование аргумента
              'description': None,  # Рускоязычное описание аргумента
              'ext_edit': None,     # Класс расширенного редактора значения аргумента
              'ext_args': None,     # Аргументы конструктора класса расширенного редактора
              'ext_kwargs': None,   # Аргументы конструктора класса расширенного редактора
              }
    
# Представление реквизита в редакторе критериев выборки коллекций
FILTER_REQUISITE = {'name': None,         # Англоязычное имя реквизита
                    'description': None,  # Рускоязычное описание реквизита
                    'field': None,        # Имя поля хранения реквизита
                    'type': None,         # Тип значения реквизита
                    'funcs': [],          # Список функций
                    }

# Стандартные используемые логические операции
DEFAULT_ENV_LOGIC_OPERATIONS = [
    {'name': 'AND', 'description': u'И', 'img': img_lib.logic_and},
    {'name': 'OR', 'description': u'ИЛИ', 'img': img_lib.logic_or},
    {'name': 'NOT', 'description': u'НЕ', 'img': img_lib.logic_not_and},
    {'name': 'NOT OR', 'description': u'НЕ ИЛИ', 'img': img_lib.logic_not_or},
    ]
    
# Стандартные используемые функции
DEFAULT_ENV_FUNCS = {
    'equal': {
        'name': 'equal',
        'func': equal,
        'description': u'Равно',
        'args': [
                {'name': 'value',
                 'description': u'Значение'}],
        'img': img_lib.logic_equal,
        },
        
    'not_equal': {
        'name': 'not_equal',
        'func': not_equal,
        'description': u'Не равно',
        'args': [
                 {'name': 'value',
                  'description': u'Значение'}],
        'img': img_lib.logic_not_equal,
        },
        
    'great': {
        'name': 'great',
        'func': great,
        'description': u'Больше',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_great,
        },
        
    'great_or_equal': {
        'name': 'great_or_equal',
        'func': great_or_equal,
        'description': u'Больше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_great_or_equal,
        },
        
    'lesser': {
        'name': 'lesser',
        'func': lesser,
        'description': u'Меньше',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_lesser,
        },
        
    'lesser_or_equal': {
        'name': 'lesser_or_equal',
        'func': lesser_or_equal,
        'description': u'Меньше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_lesser_or_equal,
        },
        
    'between': {
        'name': 'between',
        'func': between,
        'description': u'Между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение'},
            {'name': 'maximum',
             'description': u'Максимальное значение'},
            ],
        'img': img_lib.logic_between,
        },
    
    'not_between': {
        'name': 'not_between',
        'func': not_between,
        'description': u'Не между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение'},
            {'name': 'maximum',
             'description': u'Максимальное значение'},
            ],
        'img': img_lib.logic_not_between,
        },
        
    'contain': {
        'name': 'contain',
        'func': contain,
        'description': u'Содержит',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_contain,
        },

    'not_contain': {
        'name': 'not_contain',
        'func': not_contain,
        'description': u'Не содержит',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_not_contain,
        },
        
    'left_equal': {
        'name': 'left_equal',
        'func': left_equal,
        'description': u'Начинается с',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_left_equal,
        },

    'right_equal': {
        'name': 'right_equal',
        'func': right_equal,
        'description': u'Заканчивается на',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_right_equal,
        },

    'startswith': {
        'name': 'startswith',
        'func': left_equal,
        'description': u'Начало строки с',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_left_equal,
    },

    'endswith': {
        'name': 'endswith',
        'func': right_equal,
        'description': u'Окончание строки на',
        'args': [
            {'name': 'value',
             'description': u'Значение'}],
        'img': img_lib.logic_right_equal,
    },

    'mask': {
        'name': 'mask',
        'func': mask,
        'description': u'Соответствует маске',
        'args': [
            {'name': 'value',
             'description': u'Маска'}],
        'img': img_lib.logic_mask,
        },
        
    'not_mask': {
        'name': 'not_mask',
        'func': not_mask,
        'description': u'Не соответствует маске',
        'args': [
            {'name': 'value',
             'description': u'Маска'}],
        'img': img_lib.logic_not_mask,
        },
        
    'is_null': {
        'name': 'is_null',
        'func': is_null,
        'description': u'Пусто',
        'args': [],
        'img': img_lib.logic_is_null,
        },
        
    'is_not_null': {
        'name': 'is_not_null',
        'func': is_not_null,
        'description': u'Не пусто',
        'args': [],
        'img': img_lib.logic_is_not_null,
        },
        
    'into': {
        'name': 'into',
        'func': into,
        'description': u'Любое из',
        'args': [
            {'name': 'values',
             'description': u'Список значений'}],
        'img': img_lib.logic_into,
        },
        
    'not_into': {
        'name': 'not_into',
        'func': not_into,
        'description': u'Не одно из',
        'args': [
            {'name': 'values',
             'description': u'Список значений'}],
        'img': img_lib.logic_not_into,
        },
        
    }
    
DEFAULT_STRING_FUNCS = ('equal', 'not_equal', 'contain', 'not_contain',
                        'left_equal', 'right_equal',
                        # 'mask','not_mask',
                        'is_null', 'is_not_null', 'into', 'not_into')
    
PY_STRING_FUNCS = {
    'equal': pyf.py_equal,
    'not_equal': pyf.py_not_equal,
    'contain': pyf.py_contain,
    'not_contain': pyf.py_not_contain,
    'left_equal': pyf.py_left_equal,
    'right_equal': pyf.py_right_equal,
    'mask': pyf.py_mask,
    'not_mask': pyf.py_not_mask,
    'is_null': pyf.py_is_null,
    'is_not_null': pyf.py_not_null,
    'into': pyf.py_into,
    'not_into': pyf.py_not_into,
}
    
DEFAULT_NUMBER_FUNCS = ('equal', 'not_equal', 'lesser', 'lesser_or_equal',
                        'great', 'great_or_equal', 'between', 'not_between',
                        'is_null', 'is_not_null')

PY_NUMBER_FUNCS = {
    'equal': pyf.py_equal,
    'not_equal': pyf.py_not_equal,
    'lesser': pyf.py_lesser,
    'lesser_or_equal': pyf.py_lesser_or_equal,
    'great': pyf.py_great,
    'great_or_equal': pyf.py_great_or_equal,
    'between': pyf.py_between,
    'not_between': pyf.py_not_between,
    'is_null': pyf.py_is_null,
    'is_not_null': pyf.py_not_null,
    }


DEFAULT_DATE_FUNCS = ('date_equal', 'date_not_equal', 'date_lesser', 'date_lesser_or_equal',
                      'date_great', 'date_great_or_equal', 'date_between', 'date_not_between',
                      'is_null', 'is_not_null',
                      # Дополнительные функции
                      'sys_date',   # В текущем(системном) дне
                      'sys_month',  # В текущем(системном) месяце
                      'sys_year',   # В текущем(системном) году
                      'choice_date',    # Указанная дата
                      'choice_month',   # Указанный месяц
                      'choice_year',    # Указанный год
                      'choice_date_range',    # Указанный диапазон дат
                      'choice_month_range',   # Указанный диапазон масяцев
                      )

PY_DATE_FUNCS = {
    'equal': pyf.py_equal,
    'not_equal': pyf.py_not_equal,
    'lesser': pyf.py_lesser,
    'lesser_or_equal': pyf.py_lesser_or_equal,
    'great': pyf.py_great,
    'great_or_equal': pyf.py_great_or_equal,
    'between': pyf.py_between,
    'not_between': pyf.py_not_between,
    'left_equal': pyf.py_left_equal,
    'right_equal': pyf.py_right_equal,
    'is_null': pyf.py_is_null,
    'is_not_null': pyf.py_not_null,
    }


DEFAULT_DATETIME_FUNCS = ('datetime_equal', 'datetime_not_equal', 'datetime_lesser', 'datetime_lesser_or_equal',
                          'datetime_great', 'datetime_great_or_equal', 'datetime_between', 'datetime_not_between',
                          'is_null', 'is_not_null',
                          # Дополнительные функции
                          'datetime_sys_date',   # В текущем(системном) дне
                          'datetime_yesterday',   # Во вчерашнем дне
                          'datetime_two_days_ago',   # В позавчерашнем дне
                          'datetime_sys_month',  # В текущем(системном) месяце
                          'datetime_sys_year',   # В текущем(системном) году
                          'datetime_oper_year',   # В текущем(операционном) году
                          'datetime_choice_date',    # Указанная дата
                          'datetime_choice_month',   # Указанный месяц
                          'datetime_choice_year',    # Указанный год
                          'datetime_choice_date_range',    # Указанный диапазон дат
                          'datetime_choice_month_range',   # Указанный диапазон масяцев
                          )

PY_DATETIME_FUNCS = {
    'equal': pyf.py_datetime_equal,
    'not_equal': pyf.py_datetime_not_equal,
    'lesser': pyf.py_datetime_lesser,
    'lesser_or_equal': pyf.py_datetime_lesser_or_equal,
    'great': pyf.py_datetime_great,
    'great_or_equal': pyf.py_datetime_great_or_equal,
    'between': pyf.py_datetime_between,
    'not_between': pyf.py_datetime_not_between,
    'is_null': pyf.py_datetime_is_null,
    'is_not_null': pyf.py_datetime_not_null,
    }


DEFAULT_NSI_FUNCS = ('nsi_equal', 'nsi_not_equal', 'nsi_left_equal',)


PY_NSI_FUNCS = {
    'nsi_equal': pyf.py_equal,
    'nsi_not_equal': pyf.py_not_equal,
    'nsi_left_equal': pyf.py_left_equal,
    }


PY_FUNCS = {
    REQUISITE_TYPE_STR: PY_STRING_FUNCS,
    REQUISITE_TYPE_INT: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_FLOAT: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_NUM: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_D: PY_DATE_FUNCS,
    REQUISITE_TYPE_DATETIME: PY_DATETIME_FUNCS,
    REQUISITE_TYPE_NSI: PY_NSI_FUNCS,
}
    
   
# Окружение редактора критериев выборки коллекций
FILTER_ENVIRONMENT = {
    'requisites': [],  # Список возможных для выбора реквизитов
    'logic': DEFAULT_ENV_LOGIC_OPERATIONS,  # Стандартные логические операции
    'funcs': DEFAULT_ENV_FUNCS,  # Стандартные функции
    }

from . import filter_builder_ctrl

# Стандартные используемые функции для реквизитов даты
DEFAULT_ENV_DATE_FUNCS = {
    'date_equal': {
        'name': 'equal',
        'func': equal,
        'description': u'Равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_equal,
        },
        
    'date_not_equal': {
        'name': 'not_equal',
        'func': not_equal,
        'description': u'Не равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_not_equal,
        },
        
    'date_great': {
        'name': 'great',
        'func': great,
        'description': u'Больше',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_great,
        },
        
    'date_great_or_equal': {
        'name': 'great_or_equal',
        'func': great_or_equal,
        'description': u'Больше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_great_or_equal,
        },
        
    'date_lesser': {
        'name': 'lesser',
        'func': lesser,
        'description': u'Меньше',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_lesser,
        },
        
    'date_lesser_or_equal': {
        'name': 'lesser_or_equal',
        'func': lesser_or_equal,
        'description': u'Меньше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_lesser_or_equal,
        },
        
    'date_between': {
        'name': 'between',
        'func': between,
        'description': u'Между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': u'Максимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            ],
        'img': img_lib.logic_between,
        },
    
    'date_not_between': {
        'name': 'not_between',
        'func': not_between,
        'description': u'Не между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': u'Максимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            ],
        'img': img_lib.logic_not_between,
        },

    # --- Дополнительные функции ---

    'sys_date': {
        'name': 'equal',
        'func': equal,
        'description': u'Текущая дата',
        'args': [],
        'get_args': exf.get_args_sys_date,
        'img': img_lib.logic_equal,
        },

    'sys_month': {
        'name': 'between',
        'func': between,
        'description': u'Текущий месяц',
        'args': [],
        'get_args': exf.get_args_sys_month,
        'img': img_lib.logic_equal,
        },

    'sys_year': {
        'name': 'between',
        'func': between,
        'description': u'Текущий год',
        'args': [],
        'get_args': exf.get_args_sys_year,
        'img': img_lib.logic_equal,
        },

    'choice_date': {
        'name': 'equal',
        'func': equal,
        'description': u'Указанная дата',
        'args': [],
        'get_args': exf.get_args_choice_date,
        'img': img_lib.logic_equal,
        },

    'choice_month': {
        'name': 'between',
        'func': between,
        'description': u'Указанный месяц',
        'args': [],
        'get_args': exf.get_args_choice_month,
        'img': img_lib.logic_equal,
        },

    'choice_year': {
        'name': 'between',
        'func': between,
        'description': u'Указанный год',
        'args': [],
        'get_args': exf.get_args_choice_year,
        'img': img_lib.logic_equal,
        },

    'choice_date_range': {
        'name': 'between',
        'func': between,
        'description': u'Указанный период дат',
        'args': [],
        'get_args': exf.get_args_choice_date_range,
        'img': img_lib.logic_equal,
        },

    'choice_month_range': {
        'name': 'between',
        'func': between,
        'description': u'Указанный период масяцев',
        'args': [],
        'get_args': exf.get_args_choice_month_range,
        'img': img_lib.logic_equal,
        },

    }

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_DATE_FUNCS)

# Стандартные используемые функции для реквизитов даты/времени
DEFAULT_ENV_DATETIME_FUNCS = {
    'datetime_equal': {
        'name': 'equal',
        'func': equal,
        'description': u'Равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_equal,
    },

    'datetime_not_equal': {
        'name': 'not_equal',
        'func': not_equal,
        'description': u'Не равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_not_equal,
    },

    'datetime_great': {
        'name': 'great',
        'func': great,
        'description': u'Больше',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_great,
    },

    'datetime_great_or_equal': {
        'name': 'great_or_equal',
        'func': great_or_equal,
        'description': u'Больше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_great_or_equal,
    },

    'datetime_lesser': {
        'name': 'lesser',
        'func': lesser,
        'description': u'Меньше',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_lesser,
    },

    'datetime_lesser_or_equal': {
        'name': 'lesser_or_equal',
        'func': lesser_or_equal,
        'description': u'Меньше или равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             }],
        'img': img_lib.logic_lesser_or_equal,
    },

    'datetime_between': {
        'name': 'between',
        'func': between,
        'description': u'Между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': u'Максимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
        ],
        'img': img_lib.logic_between,
    },

    'datetime_not_between': {
        'name': 'not_between',
        'func': not_between,
        'description': u'Не между',
        'args': [
            {'name': 'minimum',
             'description': u'Минимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': u'Максимальное значение',
             'ext_edit': filter_builder_ctrl.icDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.DP_DROPDOWN}}
             },
        ],
        'img': img_lib.logic_not_between,
    },

    # --- Дополнительные функции ---

    'datetime_sys_date': {
        'name': 'between',
        'func': between,
        'description': u'Текущая системная дата',
        'args': [],
        'get_args': exf.get_args_sys_date_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_yesterday': {
        'name': 'between',
        'func': between,
        'description': u'Вчерашняя дата',
        'args': [],
        'get_args': exf.get_args_yesterday_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_two_days_ago': {
        'name': 'between',
        'func': between,
        'description': u'Позавчерашняя дата',
        'args': [],
        'get_args': exf.get_args_two_days_ago_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_sys_month': {
        'name': 'between',
        'func': between,
        'description': u'Текущий системный месяц',
        'args': [],
        'get_args': exf.get_args_sys_month_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_sys_year': {
        'name': 'between',
        'func': between,
        'description': u'Текущий системный год',
        'args': [],
        'get_args': exf.get_args_sys_year_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_oper_year': {
        'name': 'between',
        'func': between,
        'description': u'Текущий операционный год',
        'args': [],
        'get_args': exf.get_args_oper_year_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_choice_date': {
        'name': 'between',
        'func': between,
        'description': u'Указанная дата',
        'args': [],
        'get_args': exf.get_args_choice_date_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_choice_month': {
        'name': 'between',
        'func': between,
        'description': u'Указанный месяц',
        'args': [],
        'get_args': exf.get_args_choice_month_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_choice_year': {
        'name': 'between',
        'func': between,
        'description': u'Указанный год',
        'args': [],
        'get_args': exf.get_args_choice_year_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_choice_date_range': {
        'name': 'between',
        'func': between,
        'description': u'Указанный период дат',
        'args': [],
        'get_args': exf.get_args_choice_date_range_datetime,
        'img': img_lib.logic_equal,
    },

    'datetime_choice_month_range': {
        'name': 'between',
        'func': between,
        'description': u'Указанный период масяцев',
        'args': [],
        'get_args': exf.get_args_choice_month_range_datetime,
        'img': img_lib.logic_equal,
    },

}

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_DATETIME_FUNCS)

# Поддержка справочников в фильтрах
try:
    from NSI.usercomponents.spravtreecomboctrl import icSpravTreeComboCtrl
except ImportError:
    io_prnt.outWarning(u'Не подключен редактор НСИ аргумента в конструкторе фильтров')
    icSpravTreeComboCtrl = None

DEFAULT_ENV_NSI_FUNCS = {
    'nsi_equal': {
        'name': 'equal',
        'func': equal,
        'description': u'Равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': icSpravTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': img_lib.logic_equal,
        },
        
    'nsi_not_equal': {
        'name': 'not_equal',
        'func': not_equal,
        'description': u'Не равно',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': icSpravTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': img_lib.logic_not_equal,
        },

    'nsi_left_equal': {
        'name': 'left_equal',
        'func': left_equal,
        'description': u'Группа',
        'args': [
            {'name': 'value',
             'description': u'Значение',
             'ext_edit': icSpravTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': img_lib.logic_left_equal,
        },
    }

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_NSI_FUNCS)

DEFAULT_FUNCS = {
    REQUISITE_TYPE_STR: DEFAULT_STRING_FUNCS,
    REQUISITE_TYPE_INT: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_FLOAT: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_NUM: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_D: DEFAULT_DATE_FUNCS,
    REQUISITE_TYPE_DATETIME: DEFAULT_DATETIME_FUNCS,
    REQUISITE_TYPE_NSI: DEFAULT_NSI_FUNCS,
}

DEFAULT_ALL_FUNCS = tuple(DEFAULT_ENV_FUNCS.keys())
