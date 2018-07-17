#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с SQLite.
"""

from ic.components import icwidget

# Константы
# Тип БД
SQLITE_DB_TYPE = 'SQLiteDB'

# Спецификация БД
SPC_IC_SQLITEDB = {'type': SQLITE_DB_TYPE,
                   'name': 'sqlite_db_default',
                   'path': '',
                   'filename': '',
                   'encoding': 'UTF-8',

                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   }

