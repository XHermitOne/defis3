#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с MSSQL.
"""

from ic.components import icwidget

# Константы
# Тип БД
MSSQL_DB_TYPE = 'MSSQLDB'

# Спецификация БД
SPC_IC_MSSQL = {'type': MSSQL_DB_TYPE,
                'user': '',
                'dbname': '',
                'password': '',
                'host': '',
                'encoding': 'UTF-8',

                '__parent__': icwidget.SPC_IC_SIMPLE,
                }
