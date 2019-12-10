#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции манипулирования DBF таблицами.
"""

import os
import os.path
import jaydebeapi

from ic.log import log

try:
    import dbfpy3.dbf
except ImportError:
    log.error(u'Ошибка импорта dbfpy3.dbf')

__version__ = (0, 1, 1, 2)

#
DBF_DB_URL_FMT = 'jdbc:dbf:///%s?charSet=%s'
JDBC_DBF_DRIVER = os.path.join(os.path.dirname(__file__), 'JDBC', 'DBF_JDBC42.jar')

DEFAULT_DBF_ENCODING = 'cp1251'


def get_dbf_field_names(tab_filename):
    """
    Получить имена полей таблицы DBF.

    :param tab_filename: Имя файла таблицы DBF.
    :return: Список имен полей таблицы DBF.
    """
    tab_dbf = None
    field_names = list()
    try:
        log.info(u'Открытие таблицы <%s>' % tab_filename)
        tab_dbf = dbfpy3.dbf.Dbf(tab_filename, new=False)
        field_names = tab_dbf.fieldNames
        tab_dbf.close()
    except:
        if tab_dbf:
            tab_dbf.close()
        log.fatal(u'Ошибка получения списка имен колонок в таблице <%s>' % tab_filename)
    return field_names


def check_exists_columns(tab_filename, columns, auto_create=True):
    """
    Проверка существования колонок в таблице.

    :param tab_filename: Имя файла таблицы DBF.
    :param columns: Список колонок.
        [(Имя колонки, Тип колонки, Длина, Значение по умолчанию)]
    :param auto_create: Автоматически создать коолнки, если не существует.
    :return: True - все колонки существуют. False - колонки не найдены.
    """
    results = list()
    try:
        fields = get_dbf_field_names(tab_filename)

        results = [column[0] in fields for column in columns]
        for column in columns:
            column_name = column[0]
            if column_name not in fields:
                if auto_create:
                    column_type = column[1]
                    column_len = column[2] if len(column) > 2 else 0
                    column_default = column[3] if len(column) > 3 else None

                    append_dbf_new_field(tab_filename, column_name, column_type, column_len, default=column_default)
    except:
        log.fatal(u'Ошибка проверки наличия колонок в таблице')
    return all(results)


def append_dbf_new_field(dbf_filename,
                         new_fieldname, field_type, field_length, default=None):
    """
    Добавить новое поле в DBF файл.

    :param dbf_filename: Имя DBF файла.
    :param new_fieldname: Имя нового поля.
    :param field_type: Тип поля (C-символьное).
    :param field_length: Длина поля.
    :param default: Значение по умолчанию.
    :return: Объект DBF таблицы.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log.warning(u'Добавление нового поля в DBF файл. Файл <%s> не найден' % dbf_filename)
        return None

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        # Добавление нового поля
        if field_type == 'C':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s VARCHAR(%d)' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                         new_fieldname, field_length)
            if default is not None:
                sql += ' DEFAULT \'%s\'' % str(default)
            log.debug(u'Выполнение SQL <%s>' % sql)
            db_cursor.execute(sql)
        elif field_type == 'L':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s BOOLEAN' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                     new_fieldname)
            if default is not None:
                sql += ' DEFAULT %s' % str(default)
            db_cursor.execute(sql)
        elif field_type == 'D':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s DATE' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                  new_fieldname)
            if default is not None:
                sql += ' DEFAULT \'%s\'' % str(default)
            db_cursor.execute(sql)
        else:
            log.warning(u'Добавление нового поля в DBF файл. Тип <%s> добавляемого поля не поддерживается' % field_type)
        dbf_connection.close()
    except:
        if dbf_connection:
            dbf_connection.close()
        log.fatal(u'Ошибка добавления нового поля в DBF файл <%s>' % dbf_filename)
    return None


def append_dbf_new_fields(dbf_filename, *field_defs):
    """
    Добавить новые поля в DBF файл.

    :param dbf_filename: Имя DBF файла.
    :param field_defs: Описания полей (Имя поля, Тип, Длина, Значение по умолчанию).
    :return: Объект DBF таблицы.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log.warning(u'Добавление нового поля в DBF файл. Файл <%s> не найден' % dbf_filename)
        return None

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        for new_fieldname, field_type, field_length, default in field_defs:
            # Добавление нового поля
            if field_type == 'C':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s VARCHAR(%d)' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                             new_fieldname, field_length)
                if default is not None:
                    sql += ' DEFAULT \'%s\'' % str(default)
                # log.debug(u'Выполнение SQL <%s>' % sql)
                db_cursor.execute(sql)
            elif field_type == 'L':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s BOOLEAN' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                         new_fieldname)
                if default is not None:
                    sql += ' DEFAULT %s' % str(default)
                db_cursor.execute(sql)
            elif field_type == 'D':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s DATE' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                      new_fieldname)
                if default is not None:
                    sql += ' DEFAULT \'%s\'' % str(default)
                db_cursor.execute(sql)
            else:
                log.warning(u'Добавление нового поля в DBF файл. Тип <%s> добавляемого поля не поддерживается' % field_type)
                continue
        dbf_connection.close()
    except:
        if dbf_connection:
            dbf_connection.close()
        log.fatal(u'Ошибка добавления новый полей в DBF файл <%s>' % dbf_filename)


def set_dbf_field_value(dbf_filename, field_name, value, field_type='C'):
    """
    Установить значение поля DBF таблицы.

    :param dbf_filename: Имя DBF файла.
    :param field_name: Наименование поля DBF таблицы.
    :param value: Значение.
    :param field_type: Тип поля.
    :return: True - все ок / False - ошибка.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log.warning(u'Установка значения поля в DBF файл. Файл <%s> не найден' % dbf_filename)
        return False

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        # Добавление нового поля
        db_cursor = dbf_connection.cursor()

        # Строковые типы обрамляются кавычками
        if field_type in ('C', 'D'):
            value = '\'%s\'' % str(value)

        sql = 'UPDATE %s SET %s=%s' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                       field_name, value)
        db_cursor.execute(sql)
        dbf_connection.close()
        return True
    except:
        if dbf_connection:
            dbf_connection.close()
        log.fatal(u'Ошибка установки значения поля в DBF файле <%s>' % dbf_filename)
    return False
