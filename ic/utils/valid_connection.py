#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции проверки связи.
"""

import sys
import os
import os.path
import traceback

try:
    import pyodbc
except ImportError:
    pass

try:
    import jaydebeapi
except ImportError:
    pass

try:
    import urllib.request
except ImportError:
    pass

try:
    import sqlalchemy
except:
    pass

__version__ = (0, 1, 2, 1)


def validPingHost(host_name):
    """
    Проверка связи с хостом по пингу (ping).
    @param host_name: Имя хоста.
    @return: True - связь с хостом есть. False - сбой связи.
    """
    if sys.platform.startswith('win'):
        response = os.system('ping -n 1 %s' % host_name)
    elif sys.platform.startswith('linux'):
        response = os.system('ping -c 1 %s' % host_name)
    else:
        return False
    return response == 0


# --- Проверка связи через ODBC ---
def validDBConnectODBC(connection_str=None):
    """
    Проверка связи с БД ODBC.
    @param connection_str: Connection string связи с БД.
    @return: True - есть связь. False - связь не установлена.
    """
    if connection_str is None:
        # Не определена связь с БД, тогда и проверять нечего
        return False

    try:
        connection = pyodbc.connect(connection_str)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return False

    is_connect = False
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()

            if result:
                is_connect = True
            cursor.close()
        except:
            if cursor:
                cursor.close()
            is_connect = False
        connection.close()
    return is_connect


def getNotValidDBConnectODBCErrTxt(connection_str=None):
    """
    Получить сообщение об ошибке в случае не доступности связи с БД ODBC.
    @param connection_str: Connection string связи с БД.
    @return: Текст ошибки или пустая строка в случае отсутствия ошибки.
    """
    if connection_str is None:
        # Не определена связь с БД, тогда и проверять нечего
        return u'Не определена связь с БД'

    try:
        connection = pyodbc.connect(connection_str)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return u'Ошибка связи с сервером БД\n<%s>\n%s' % (connection_str, traceback.format_exc())

    error_txt = u''
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()
            if not result:
                error_txt = u'Не корректный результат тестового запроса к БД <%s>' % connection_str
            cursor.close()
        except:
            if cursor:
                cursor.close()
            error_txt = u'Ошибка выполнения тестового запроса к БД \n<%s>\n%s' % (connection_str, traceback.format_exc())
        connection.close()
    else:
        error_txt = u'Не определен объект связи для доступа к БД \n<%s>' % connection_str

    return error_txt


def validURL(url):
    """
    Проверка доступности URL.
    @param url: URL. Например http://localhost:8080
    @return: True/False.
    """
    try:
        response = urllib.request.urlopen(url)
        return response.getcode() == 200
    except:
        error_txt = traceback.format_exc()
    return False


def getNotValidURLErrTxt(url):
    """
    Получить сообщение об ошибке в случае не доступности URL.
    @param url: URL. Например http://localhost:8080
    @return: Текст ошибки или пустая строка в случае отсутствия ошибки.
    """
    error_txt = u''
    try:
        response = urllib.request.urlopen(url)
        response_code = response.getcode()
        if response_code == 200:
            pass
        else:
            error_txt = u'Результат проверки доступности адреса <%s>. Код <%d>' % (url, response_code)
    except:
        error_txt = u'Ошибка проверки доступности адреса <%s>\n%s' % (url, traceback.format_exc())
    return error_txt


# --- Проверка связи через JDBC ---
# Поддерживаемые типы JDBC драйверов
JDBC_TYPES = ('DBF', 'MSSQL', 'POSTGRESQL')
JAVA_DRIVER_CLASS = {'DBF': 'com.hxtt.sql.dbf.DBFDriver',
                     'MSSQL': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
                     'POSTGRESQL': 'org.postgresql.Driver',
                     }

JDBC_DRIVER_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'JDBC')
JDBC_DRIVER_FILENAME = {'DBF': os.path.join(JDBC_DRIVER_DIR, 'DBF_JDBC40.jar'),
                        'MSSQL': os.path.join(JDBC_DRIVER_DIR, 'sqljdbc4.jar'),
                        'POSTGRESQL': os.path.join(JDBC_DRIVER_DIR, 'postgresql-42.2.5.jar'),
                        }


def validDBConnectJDBC(connection_url=None, jdbc_type=None):
    """
    Проверка связи с БД JDBC.
    @param connection_url: Connection string связи с БД.
    @param jdbc_type: Тип JDBC драйвера.
        Поддерживаются следующие типы:
        DBF, MSSQL, POSTGRESQL
    ВНИМАНИЕ! При создании связи JDBC необходимо указывать все используемые
    драйвера JDBC. Используемы драйвера регистрируются при первом connect.
    Последующие подключения ищут драйвера среди зарегистрированных.
    @return: True - есть связь. False - связь не установлена.
    """
    if jdbc_type is None or jdbc_type not in JDBC_TYPES:
        # Не определен драйвер JDBC
        return False
    java_driver_class = JAVA_DRIVER_CLASS.get(jdbc_type, None)
    if not java_driver_class:
        # Ошибка определения класса драйвера Java
        return False

    # ВНИМАНИЕ! При создании связи JDBC необходимо указывать все используемые
    # драйвера JDBC. Используемы драйвера регистрируются при первом connect.
    # Последующие подключения ищут драйвера среди зарегистрированных.
    jdbc_drivers = list(JDBC_DRIVER_FILENAME.values())
    if not jdbc_drivers or not all([os.path.exists(jdbc_driver) for jdbc_driver in jdbc_drivers]):
        # Ошибка определения драйвера JDBC
        return False

    if connection_url is None:
        # Не определена связь с БД, тогда и проверять нечего
        return False

    try:
        connection = jaydebeapi.connect(java_driver_class, [connection_url], jdbc_drivers)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return False

    is_connect = False
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()

            if result:
                is_connect = True
            cursor.close()
        except:
            if cursor:
                cursor.close()
            is_connect = False
        connection.close()
    return is_connect


def getNotValidDBConnectJDBCErrTxt(connection_url=None, jdbc_type=None):
    """
    Получить сообщение об ошибке в случае не доступности связи с БД JDBC.
    @param connection_url: Connection string связи с БД.
    @param jdbc_type: Тип JDBC драйвера.
        Поддерживаются следующие типы:
        DBF, MSSQL, POSTGRESQL
    ВНИМАНИЕ! При создании связи JDBC необходимо указывать все используемые
    драйвера JDBC. Используемы драйвера регистрируются при первом connect.
    Последующие подключения ищут драйвера среди зарегистрированных.
    @return: Текст ошибки или пустая строка в случае отсутствия ошибки.
    """
    if jdbc_type is None or jdbc_type not in JDBC_TYPES:
        # Не определен драйвер JDBC
        return u'Не определен драйвер JDBC'
    java_driver_class = JAVA_DRIVER_CLASS.get(jdbc_type, None)
    if not java_driver_class:
        # Ошибка определения класса драйвера Java
        return u'Ошибка определения класса драйвера Java'

    # ВНИМАНИЕ! При создании связи JDBC необходимо указывать все используемые
    # драйвера JDBC. Используемы драйвера регистрируются при первом connect.
    # Последующие подключения ищут драйвера среди зарегистрированных.
    jdbc_drivers = list(JDBC_DRIVER_FILENAME.values())
    if not jdbc_drivers or not all([os.path.exists(jdbc_driver) for jdbc_driver in jdbc_drivers]):
        # Ошибка определения драйвера JDBC
        return u'Ошибка определения драйверов JDBC <%s>' % jdbc_drivers

    if connection_url is None:
        # Не определена связь с БД, тогда и проверять нечего
        return u'Не определена связь с БД'

    try:
        connection = jaydebeapi.connect(java_driver_class, [connection_url], jdbc_drivers)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return u'Ошибка связи с сервером БД\n<%s>\n%s' % (connection_url, traceback.format_exc())

    error_txt = u''
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            cursor.execute('SELECT 1')
            result = cursor.fetchall()
            if not result:
                error_txt = u'Не корректный результат тестового запроса к БД <%s>' % connection_url
            cursor.close()
        except:
            if cursor:
                cursor.close()
            error_txt = u'Ошибка выполнения тестового запроса к БД \n<%s>\n%s' % (connection_url, traceback.format_exc())
        connection.close()
    else:
        error_txt = u'Не определен объект связи для доступа к БД \n<%s>' % connection_url

    return error_txt


# --- Проверка связи через SQLAlchemy ---
def validDBConnectSQLAlchemy(connection_str=None):
    """
    Проверка связи с БД через SQLAlchemy.
    @param connection_str: Connection string связи с БД.
    @return: True - есть связь. False - связь не установлена.
    """
    if connection_str is None:
        # Не определена связь с БД, тогда и проверять нечего
        return False

    try:
        engine = sqlalchemy.create_engine(connection_str, echo=False)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return False

    is_connect = False
    if engine:
        connection = None
        try:
            connection = engine.connect()
            result = connection.execute('SELECT 1').fetchall()
            if result:
                is_connect = True
            connection.close()
        except:
            if connection:
                connection.close()
            is_connect = False
    return is_connect


def getNotValidDBConnectSQLAlchemyErrTxt(connection_str=None):
    """
    Получить сообщение об ошибке в случае не доступности связи с БД через SQLAlchemy.
    @param connection_str: Connection string связи с БД.
    @return: Текст ошибки или пустая строка в случае отсутствия ошибки.
    """
    if connection_str is None:
        # Не определена связь с БД, тогда и проверять нечего
        return u'Не определена связь с БД'

    try:
        engine = sqlalchemy.create_engine(connection_str, echo=False)
    except:
        # Если сединение не можем сделать, то нет связи с сервером
        return u'Ошибка связи с сервером БД\n<%s>\n%s' % (connection_str, traceback.format_exc())

    error_txt = u''
    if engine:
        connection = None
        try:
            connection = engine.connect()

            result = connection.execute('SELECT 1').fetchall()
            if not result:
                error_txt = u'Не корректный результат тестового запроса к БД <%s>' % connection_str
            connection.close()
        except:
            if connection:
                connection.close()
            error_txt = u'Ошибка выполнения тестового запроса к БД \n<%s>\n%s' % (connection_str, traceback.format_exc())
        connection.close()
    else:
        error_txt = u'Не определен объект связи для доступа к БД \n<%s>' % connection_str

    return error_txt
