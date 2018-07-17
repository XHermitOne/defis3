#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции журналирования в БД PostgreSQL.
    Функции сделаны для организации просмора панели аварийных тревог.

В конфигурационном файле д.б. опеределены следующие переменные:
ALARM_MODE - Вкл/Выкл режима регистрации тревог
DB_URL или DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD -
    Параметры подключения к БД.
ALARM_ACTUAL_DAYS - Количество дней актуальности тревог
ALARM_TABLENAME - Имя таблицы регистрации тревог

Формат таблицы тревог:
    Источник/уровень тревоги (source)
    Дата/Время регистрации сигнала тревоги (alarm_dt)
    Вид тревоги (alarm_type)
    Сообщение (msg)
"""

import traceback
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker

__version__ = (0, 0, 0, 5)

# Модуль конфигурации
CONFIG = None

# Имя таблицы регистрации тревог по умолчанию
DEFAULT_ALARM_TABLENAME = 'alarms'


def connect(mConfig=None, db_url=None,
            db_host=None, db_port=None, db_name=None,
            db_user=None, db_password=None):
    """
    Создание связи с БД.
    @param mConfig: Модуль конфигурации.
    @param db_url: URL БД. Соединение может задаваться URL,
        а может задаваться параметрами соединения.
    @param db_host: Параметр соединения с БД. Сервер БД.
    @param db_port: Параметр соединения с БД. Порт БД.
    @param db_name: Параметр соединения с БД. Имя БД.
    @param db_user: Параметр соединения с БД. Имя пользователя БД.
    @param db_password: Параметр соединения с БД. Пароль пользователя БД.
    """
    global CONFIG

    if db_url is None:
        # Сначала проверить возможность задания связи с БД
        # при помощи URL
        db_url = CONFIG.DB_URL if hasattr(CONFIG, 'DB_URL') else None
    if db_url is None:
        # Если все таки URL БД не определен, то надо пробовать
        # определить параметры подключения
        if db_host:
            db_host = CONFIG.DB_HOST
        if db_port:
            db_port = CONFIG.DB_PORT
        if db_name:
            db_name = CONFIG.DB_NAME
        if db_user:
            db_user = CONFIG.DB_USER
        if db_password:
            db_password = CONFIG.DB_PASSWORD

        db_url = 'postgres://%s:%s@%s:%d/%s' % (db_user, db_password,
                                                db_host, db_port, db_name)
    connection = None
    try:
        connection = sqlalchemy.create_engine(db_url, echo=True)
    except:
        disconnect(connection)
    return connection


def disconnect(connection):
    """
    Разорвать соединение с БД.
    @param connection: Объект связи с БД.
    """
    if connection:
        connection.dispose()
        connection = None


def create_alarm_table(connection):
    """
    Функция создания объекта таблицы тревог.
    @param connection: Объект связи с БД.
    @return: Объект таблицы реггистрации тревог.
    """
    global CONFIG
    table_name = CONFIG.ALARM_TABLENAME if hasattr(CONFIG, 'ALARM_TABLENAME') else None
    table_name = DEFAULT_ALARM_TABLENAME if table_name is None else table_name

    metadata = sqlalchemy.MetaData(connection)
    columns = [sqlalchemy.Column('source', sqlalchemy.UnicodeText),
               sqlalchemy.Column('alarm_dt', sqlalchemy.DateTime),
               sqlalchemy.Column('alarm_type', sqlalchemy.UnicodeText),
               sqlalchemy.Column('msg', sqlalchemy.UnicodeText)]
    table = sqlalchemy.Table(table_name, metadata, *columns)
    # Создание таблицы в БД
    metadata.create_all(connection)
    return table


def delete_not_actual(connection=None, table=None, actual_dt=None):
    """
    Удаление неактуальных данных тревог.
    @param connection: Объект связи с БД.
    @param table: Объект таблицы .
    @param actual_dt: Указание даты актуальности.
        Все записи произведенные ранее считаются не актуальными.
        Если не определено, то считается начало сегодняшнего дня.
    @return: True/False.
    """
    global CONFIG

    if actual_dt is None:
        actual_dt = datetime.date.today()
    if isinstance(actual_dt, datetime.date):
        actual_dt = datetime.datetime.combine(actual_dt,
                                              datetime.datetime.min.time())

    if connection is None:
        connection = connect(CONFIG)
    if table is None:
        table = create_alarm_table(connection)

    # Начало транзакции
    session = sessionmaker(bind=connection)
    transaction = session()

    try:
        sql = table.delete().where(table.c.alarm_dt < actual_dt)
        transaction.execute(sql)
        transaction.commit()
    except:
        # Откат транзакции
        transaction.rollback()
        # disconnect(connection)
        # raise

    disconnect(connection)


def init(mConfig=None):
    """
    Инициализация файла лога.
    @param mConfig: Модуль конфигурации.
    """
    global CONFIG
    CONFIG = mConfig

    if not CONFIG.ALARM_MODE:
        # В конфигурации не предусмотрен режим сигнализации тревог
        return

    # Удалить не актуальную информацию
    actual_days = CONFIG.ALARM_ACTUAL_DAYS if hasattr(CONFIG, 'ALARM_ACTUAL_DAYS') else 0
    actual_dt = datetime.date.today() - datetime.timedelta(days=actual_days)
    delete_not_actual(actual_dt=actual_dt)


def alarm(sMsg, source=None, alarm_type=None, alarm_dt=None):
    """
    Зарегистрировать тревогу.
    @param sMsg: Текстовое сообщение.
    @param source: Указания источника тревоги.
        Если не указано, то определяется как <Общий уровень>.
    @param alarm_type: Вид тревоги.
        Если не указано, то имеется ввиду ИНФОРМАЦИОННЫЙ вид.
    @param alarm_dt: Дата/Время регистрации.
        Если не указывается то берется системное.
    """
    global CONFIG

    if alarm_dt is None:
        alarm_dt = datetime.datetime.now()
    if alarm_type is None:
        alarm_type = 'INFO'
    # Сообщение привести к юникоду
    if not isinstance(sMsg, unicode):
        sMsg = unicode(str(sMsg), CONFIG.DEFAULT_ENCODING)

    connection = connect(CONFIG)
    table = create_alarm_table(connection)

    # Начало транзакции
    session = sessionmaker(bind=connection)
    transaction = session()

    try:
        record = dict(source=source,
                      alarm_dt=alarm_dt,
                      alarm_type=alarm_type,
                      msg=sMsg)
        sql = table.insert().values(**record)
        transaction.execute(sql)
        transaction.commit()
    except:
        # Откат транзакции
        transaction.rollback()
        # disconnect(connection)
        # raise

    disconnect(connection)


def debug(sMsg, source=None):
    """
    Вывести ОТЛАДОЧНУЮ информацию.
    @param sMsg: Текстовое сообщение.
    @param source: Указания источника тревоги.
        Если не указано, то определяется как <Общий уровень>.
    """
    if source is None:
        source = u'Общий уровень'
    return alarm(sMsg, source, u'DEBUG')


def info(sMsg, source=None):
    """
    Вывести ОБЩУЮ информацию.
    @param sMsg: Текстовое сообщение.
    @param source: Указания источника тревоги.
        Если не указано, то определяется как <Общий уровень>.
    """
    if source is None:
        source = u'Общий уровень'
    return alarm(sMsg, source, u'INFO')


def warning(sMsg, source=None):
    """
    Вывести информацию ОБ ПРЕДУПРЕЖДЕНИИ.
    @param sMsg: Текстовое сообщение.
    @param source: Указания источника тревоги.
        Если не указано, то определяется как <Общий уровень>.
    """
    if source is None:
        source = u'Общий уровень'
    return alarm(sMsg, source, u'WARNING')


def fatal(sMsg, source=None):
    """
    Вывести информацию ОБ ОШИБКЕ.
    @param sMsg: Текстовое сообщение.
    @param source: Указания источника тревоги.
        Если не указано, то определяется как <Общий уровень>.
    """
    global CONFIG

    if source is None:
        source = u'Общий уровень'

    trace_txt = traceback.format_exc()

    try:
        msg = sMsg+u'\n'+trace_txt
    except UnicodeDecodeError:
        if not isinstance(sMsg, unicode):
            sMsg = unicode(sMsg, CONFIG.DEFAULT_ENCODING)
        if not isinstance(trace_txt, unicode):
            trace_txt = unicode(trace_txt, CONFIG.DEFAULT_ENCODING)
        msg = sMsg+u'\n'+trace_txt

    return alarm(msg, source, u'FATAL')
