#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с PostgreSQL.

В качестве драйвера используется psycopg2:

***********************************************************
sudo apt install python-psycopg2
***********************************************************

Памятка по PostgreSQL:

1. Смена типа поля (при условии совместимасти старого и нового типа)
***********************************************************
ALTER TABLE tab_name ALTER COLUMN field_name TYPE bigint;
***********************************************************

2. Полностью копия таблицы с созданием:
***********************************************************
CREATE TABLE tab_name_dest AS TABLE tab_name_source;
***********************************************************

3. Создание индексов
*******************************************************************
CREATE INDEX index_name_idx ON table_name (field1, field2, field3)
*******************************************************************

Список активных соединений:

*******************************************************************
SELECT * FROM pg_stat_activity;
*******************************************************************
"""

import psycopg2.extensions
import sqlalchemy

from ic.components import icwidget

from ic.log import log

from . import field_types

__version__ = (0, 1, 2, 1)

# Константы
# Тип БД
POSTGRES_DB_TYPE = 'PostgreSQLDB'

# Спецификация БД
SPC_IC_POSTGRESQL = {'type': POSTGRES_DB_TYPE,
                     'user': '',
                     'dbname': '',
                     'password': '',
                     'host': 'localhost',
                     'port': '5432',
                     'options': '',
                     'encoding': 'UTF-8',

                     '__parent__': icwidget.SPC_IC_SIMPLE,
                     }


def getActiveConnectionsPostgreSQL(db_url=None):
    """
    Список активных связей с БД PostgreSQL.
    :param db_url: URL связи с БД.
    :return: Список словарей записей активных связей или None в случае ошибки.
    """
    if db_url is None:
        # Не определена URL БД, тогда и проверять нечего
        log.warning(u'Не определено URL БД при получении списка активных связей')
        return None

    engine = sqlalchemy.create_engine(db_url, echo=False)

    if engine:
        connection = None
        try:
            connection = engine.connect()
            records = connection.execute('SELECT * FROM pg_stat_activity').fetchall()
            connection.close()
            records = [dict(record) for record in records]
            return records
        except:
            log.fatal(u'Ошибка определения активных связей с БД PostgreSQL')
            if connection:
                connection.close()
    return None


def countActiveConnectionsPostgreSQL(db_url=None):
    """
    Колчество активных связей с БД PostgreSQL.
    :param db_url: URL связи с БД.
    :return: Количество активных связей или -1 в случае ошибки.
    """
    records = getActiveConnectionsPostgreSQL(db_url=db_url)
    if records is None:
        return -1
    return len(records)


_PSYCOPG2_COLUMN_TYPES2FIELD_TYPE = {'STRING': field_types.TEXT_FIELD_TYPE,
                                     'INTEGER': field_types.INT_FIELD_TYPE,
                                     'DECIMAL': field_types.INT_FIELD_TYPE,
                                     'FLOAT': field_types.FLOAT_FIELD_TYPE,
                                     'DATE': field_types.DATE_FIELD_TYPE,
                                     'DATETIME': field_types.DATETIME_FIELD_TYPE,
                                     'DATETIMETZ': field_types.DATETIME_FIELD_TYPE,
                                     'BOOLEAN': field_types.BOOLEAN_FIELD_TYPE,
                                     'LONGINTEGER': field_types.BIGINT_FIELD_TYPE,
                                     'BINARYARRAY': field_types.BINARY_FIELD_TYPE}


def psycopg2_field_description2fields(*field_description):
    """
    Преобразовать описания полей DBAPI2 psycopg2 во внутренний вариан описаний.
    :param field_description: Список описаний полей DBAPI2.
        Описания полей ожидаются как описания колонок psycopg2.
    :return: Список описаний полей во внутреннем формате:
        [
        ('Имя поля', 'Тип поля (T, I, F, DateTime, Boolean и т.п)', Длина поля),
        ...
        ]
    """
    new_fields = list()
    if field_description and isinstance(field_description[0], psycopg2.extensions.Column):
        # Простой случай
        try:
            new_fields = [(column.name,
                           _PSYCOPG2_COLUMN_TYPES2FIELD_TYPE[psycopg2.extensions.string_types[column.type_code].name if column.type_code in psycopg2.extensions.string_types else 'STRING'],
                           column.internal_size,
                           column.precision) for column in field_description]
        except:
            log.fatal(u'Ошибка преобразования описания полей из psycopg2')
            log.error(u'Исходное описание:')
            for column in field_description:
                column_type = psycopg2.extensions.string_types.get(column.type_code, None)
                log.error(u'\t%s\tТип: %s' % (str(column), column_type.name if column_type else str(column_type)))
    elif field_description and len(field_description) == 1 and isinstance(field_description[0], tuple):
        try:
            # В некоторых сложных запросах результат получения описания полей может быть сложным
            new_fields = [(column.name,
                           _PSYCOPG2_COLUMN_TYPES2FIELD_TYPE[psycopg2.extensions.string_types[column.type_code].name if column.type_code in psycopg2.extensions.string_types else 'STRING'],
                           column.internal_size,
                           column.precision) for column in field_description[0]]
        except:
            log.fatal(u'Ошибка преобразования описания полей из psycopg2')
            log.error(u'Исходное описание:')
            for column in field_description[0]:
                column_type = psycopg2.extensions.string_types.get(column.type_code, None)
                log.error(u'\t%s\tТип: %s' % (str(column),  column_type.name if column_type else str(column_type)))
    else:
        log.warning(u'Не обрабатываемый случай преобразования описания полей из psycopg2\n\t%s' % str(field_description))

    return new_fields
