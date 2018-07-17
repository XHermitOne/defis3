#!/usr/bin/env python
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

from ic.components import icwidget

__version__ = (0, 0, 1, 3)

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
