#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции поддержки работы с источниками данных JDBC.
"""

import os
import os.path
import jaydebeapi

from ic.interfaces import icsourceinterface
from ic.log import log

# Поддерживаемые типы JDBC драйверов
JDBC_TYPES = ('DBF', 'MSSQL', 'POSTGRESQL')
JAVA_DRIVER_CLASS = {'DBF': 'com.hxtt.sql.dbf.DBFDriver',
                     'MSSQL': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
                     'POSTGRESQL': 'org.postgresql.Driver',
                     }

JDBC_DRIVER_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'JDBC')
JDBC_DRIVER_FILENAME = {'DBF': os.path.join(JDBC_DRIVER_DIR, 'DBF_JDBC42.jar'),
                        'MSSQL': os.path.join(JDBC_DRIVER_DIR, 'sqljdbc4.jar'),
                        'POSTGRESQL': os.path.join(JDBC_DRIVER_DIR, 'postgresql-42.2.5.jar'),
                        }


class icJDBC(icsourceinterface.icSourceInterface):
    """
    Класс поддержки доступа к данным через JDBC.
    """
    pass
