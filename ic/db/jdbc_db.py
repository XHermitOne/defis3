#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции поддержки работы с источниками данных JDBC.
"""

import os
import os.path
import jaydebeapi

# Типы поддерживаемых БД
JDBC_TYPES = ('DBF', 'MSSQL', 'POSTGRESQL')

#
JAVA_DRIVER_CLASS = {'DBF': 'com.hxtt.sql.dbf.DBFDriver',
                     'MSSQL': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
                     }

# Путь к папке с драйверами JDBC
JDBC_DRIVER_DIR = os.path.join(os.path.dirname(__file__), 'JDBC')

# Файлы драйверов JDBC
JDBC_DRIVER_FILENAME = {'DBF': os.path.join(JDBC_DRIVER_DIR, 'DBF_JDBC40.jar'),
                        'MSSQL': os.path.join(JDBC_DRIVER_DIR, 'sqljdbc4.jar')}


class icJDBC():
    """
    Класс поддержки доступа к данным через JDBC.
    """
    pass
