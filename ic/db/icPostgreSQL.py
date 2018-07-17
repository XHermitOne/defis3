#!/usr/bin/env python
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

"""

from ic.components import icwidget

__version__ = (0, 0, 1, 2)

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
