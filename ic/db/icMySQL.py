#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Специфакация соединение к MySQL. 

Необходимо установить пакет MySQLdb/pymysql:

**********************************************
sudo apt install python-pymysql
**********************************************

ВНИМАНИЕ! Для MySQL необходимо указывать charset в атрибуте query.
    Иначе русский текст получается как ????????.
    Например 'query' = {'charset': 'utf8'}
    !!! Обращаю внимание что charset указывается только как utf8.
    !!! Нельзя использовать utf-8 или utf_8.
"""

import MySQLdb

from ic.components import icwidget

from ic.log import log

from . import field_types

__version__ = (0, 1, 1, 1)

# Константы
# Тип БД
MYSQL_DB_TYPE = 'MySQLDB'

# Спецификация БД
SPC_IC_MYSQL = {'type': MYSQL_DB_TYPE,
                'user': '',
                'dbname': '',
                'password': '',
                'host': '',
                'port': '3306',
                'options': '',
                'encoding': 'utf_8',
                'query': {},

                '__parent__': icwidget.SPC_IC_SIMPLE,
                }


_MYSQLDB_COLUMN_TYPES2FIELD_TYPE = {MySQLdb.FIELD_TYPE.STRING: field_types.TEXT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.VAR_STRING: field_types.TEXT_FIELD_TYPE,
                                    # MySQLdb.FIELD_TYPE.: field_types.INT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.DECIMAL: field_types.INT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.FLOAT: field_types.FLOAT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.DATE: field_types.DATE_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.DATETIME: field_types.DATETIME_FIELD_TYPE,
                                    # MySQLdb.FIELD_TYPE.: field_types.DATETIME_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.BIT: field_types.BOOLEAN_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.LONGLONG: field_types.BIGINT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.INT24: field_types.BIGINT_FIELD_TYPE,
                                    MySQLdb.FIELD_TYPE.BLOB: field_types.BINARY_FIELD_TYPE}


def mysqldb_description2fields(*field_description):
    """
    Преобразовать описания полей DBAPI2 mysqldb во внутренний вариан описаний.

    :param field_description: Список описаний полей DBAPI2.
        Описания полей ожидаются как описания колонок.
    :return: Список описаний полей во внутреннем формате:
        [
        ('Имя поля', 'Тип поля (T, I, F, DateTime, Boolean и т.п)', Длина поля),
        ...
        ]
    """
    new_fields = list()
    try:
        new_fields = [(column[0],
                       _MYSQLDB_COLUMN_TYPES2FIELD_TYPE.get(column[1], field_types.TEXT_FIELD_TYPE),
                       column[2]) for column in field_description]
    except:
        log.fatal(u'Ошибка преобразования описания полей из mysqldb')

    return new_fields
