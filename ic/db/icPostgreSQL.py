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

import sqlalchemy

from ic.components import icwidget

from ic.log import log

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
    @param db_url: URL связи с БД.
    @return: Список словарей записей активных связей или None в случае ошибки.
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
    @param db_url: URL связи с БД.
    @return: Количество активных связей или -1 в случае ошибки.
    """
    records = getActiveConnectionsPostgreSQL(db_url=db_url)
    if records is None:
        return -1
    return len(records)

