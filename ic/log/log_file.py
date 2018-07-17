#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции чтения сообщений из log файлов.

Журнал сообщений программы сохраняется в файле *.log
Формат журнала:
2016-11-18 08:22:11 INFO Сообщение
    ^         ^      ^      ^
    |         |      |      +-- Текст сообщения
    |         |      +--------- Тип сообщения
    |         +---------------- Время регистрации
    +-------------------------- Дата регистрации
Текст сообщения может быть многострочным. В основном для критических ошибок.
"""

import os
import os.path
import datetime

import log

__version__ = (0, 0, 1, 6)

# Типы сообщений
INFO_LOG_TYPE = 'INFO'
WARNING_LOG_TYPE = 'WARNING'
ERROR_LOG_TYPE = 'ERROR'
FATAL_LOG_TYPE = 'FATAL'
DEBUG_LOG_TYPE = 'DEBUG'
SERVICE_LOG_TYPE = 'SERVICE'
DEBUG_SERVICE_LOG_TYPE = 'DEBUG SERVICE.'

LOG_TYPES = (DEBUG_SERVICE_LOG_TYPE,    # Не основные типы должны стоять первыми для обнаружения
             SERVICE_LOG_TYPE,
             INFO_LOG_TYPE,
             WARNING_LOG_TYPE,
             ERROR_LOG_TYPE,
             FATAL_LOG_TYPE,
             DEBUG_LOG_TYPE,
             )

AND_FILTER_LOGIC = 'AND'
OR_FILTER_LOGIC = 'OR'

MSG_LEN_LIMIT = 100

DATETIME_LOG_FMT = '%Y-%m-%d %H:%M:%S'

DEFAULT_ENCODING = 'utf-8'

LINE_SEPARATOR = os.linesep


def get_records_log_file(sLogFileName, tLogTypes=LOG_TYPES,
                         dtStartFilter=None, dtStopFilter=None,
                         tFilters=(), sFilterLogic=AND_FILTER_LOGIC,
                         encoding=DEFAULT_ENCODING):
    """
    Прочитать из файла журнала сообщений программы сообщения указанных типов.
    @param sLogFileName: Полное имя log файла.
    @param tLogTypes: Кортеж/список типов сообщений.
    @param dtStartFilter: Начальная дата/время фильтра по времени.
        Если не определено, то выбор происходит с начала файла.
    @param dtStopFilter: Конечная дата/время фильтра по времени.
        Если не определено, то выбор происходит до конца файла.
    @param tFilters: Кортеж/список дополнительных методов фильтрации.
        Методы фильтрации задаются как lambda или функции, которые принимают
        Словарь записи, а возвращают True-запись попадает в выбор/False - не попадает.
    @param sFilterLogic: Комманда способа обработки дополнительных фильтров
        AND - Чтобы запись попала в выбор необходимо положительное выполнение всех фильтров,
        OR - Чтобы запись попала в выбор достаточно положительное выполнение одного фильтра.
    @param encoding: Кодировка файла журнала.
    @return: Список словарей формата:
        [{'dt': Время регистрации в datetime.datetime,
          'type': Тип сообщения INFO, WARNING и т.п.,
          'text': Текст сообщения,
          'short': Краткий текст сообщения ограниченный MSG_LEN_LIMIT}, ...]
    """
    if not sLogFileName:
        log.warning(u'Не определен файл журнала сообщений программы для чтения')
        return list()

    if not os.path.exists(sLogFileName):
        log.warning(u'Файл журнала сообщений программы <%s> не найден' % sLogFileName)
        return list()

    log_file = None
    try:
        records = list()

        record = dict()
        log_file = open(sLogFileName, 'r')
        for line in log_file:
            # Определяем является ли текущая линия началом нового сообщения или продолжением предыдущего
            if is_new_msg(line):
                record = parse_msg_record(line, encoding=encoding)
                if check_filter_record(record, tLogTypes, dtStartFilter, dtStopFilter, tFilters, sFilterLogic):
                    records.append(record)
            else:
                if isinstance(line, str):
                    line = unicode(line, encoding)
                # record['text'] = record.get('text', u'') + LINE_SEPARATOR + line
                record['text'] = record.get('text', u'') + line
                record['short'] += (u'...' if not record.get('short', u'').endswith(u'...') else u'')

        log_file.close()
        return records
    except:
        if log_file:
            log_file.close()
        log.fatal(u'Ошибка чтения записей журнала сообщений программы <%s>' % sLogFileName)
    return list()


def is_new_msg(line):
    """
    Определяем является ли текущая линия началом нового сообщения или продолжением предыдущего
    @param line: Текущая обрабатываемая линия файла журнала сообщений программы.
    @return: True - Новое сообщение / False - продолжение предыдущего сообщения.
    """
    if not line or len(line) < 20:
        return False
    try:
        msg_type = line[20:][:line[20:].index(' ')]
    except ValueError:
        return False
    return msg_type in LOG_TYPES


def get_msg_log_type(line):
    """
    Определить тип лога сообщения.
    @param line:
    @return:
    """
    for log_type in LOG_TYPES:
        if line[20:].startswith(log_type):
            return log_type
    return None


def parse_msg_record(line, encoding=DEFAULT_ENCODING):
    """
    Распарсить строку файла журнала сообщений программы.
    @param line: Текущая обрабатываемая линия файла журнала сообщений программы.
    @return: {'dt': Время регистрации в datetime.datetime,
              'type': Тип сообщения INFO, WARNING и т.п.,
              'text': Текст сообщения,
              'short': Краткий текст сообщения ограниченный MSG_LEN_LIMIT}
    """
    dt_txt = line[:20].strip()
    # log.debug('Data: %s' % dt_txt)
    try:
        dt = datetime.datetime.strptime(dt_txt, DATETIME_LOG_FMT)
    except:
        log.fatal(u'Ошибка парсинга времени лога <%s>' % dt_txt)
        raise

    msg_type = get_msg_log_type(line)
    msg = line[21+len(msg_type):].strip()
    short_msg = u''
    # Переведем все в unicode
    try:
        if isinstance(msg, str):
            msg = unicode(msg, encoding)
    except:
        log.fatal(u'Ошибка перевода строки в unicode')
        msg = u''
    try:
        if isinstance(msg, unicode):
            short_msg = msg[:MSG_LEN_LIMIT] + (u'...' if len(msg) > MSG_LEN_LIMIT else u'')
    except:
        log.fatal(u'Ошибка перевода строки в unicode')
    return dict(dt=dt, type=msg_type, text=msg, short=short_msg)


def check_filter_record(record, tLogTypes=LOG_TYPES,
                        dtStartFilter=None, dtStopFilter=None,
                        tFilters=(), sFilterLogic=AND_FILTER_LOGIC):
    """
    Проверка соответствия записи фильтрам.
    @param record: Текущая проверяемая запись.
    @param tLogTypes: Кортеж/список типов сообщений.
    @param dtStartFilter: Начальная дата/время фильтра по времени.
        Если не определено, то выбор происходит с начала файла.
    @param dtStopFilter: Конечная дата/время фильтра по времени.
        Если не определено, то выбор происходит до конца файла.
    @param tFilters: Кортеж/список дополнительных методов фильтрации.
        Методы фильтрации задаются как lambda или функции, которые принимают
        Словарь записи, а возвращают True-запись попадает в выбор/False - не попадает.
    @param sFilterLogic: Комманда способа обработки дополнительных фильтров
        AND - Чтобы запись попала в выбор необходимо положительное выполнение всех фильтров,
        OR - Чтобы запись попала в выбор достаточно положительное выполнение одного фильтра.
    @return: True - Запись соответствует всем фильтрам и должна быть добавлена в выбор/
        False - Запись не соответствует какому либо фильтру.
    """
    msg_type = record.get('type', '')
    if msg_type not in tLogTypes:
        return False

    result = True
    dt = record.get('dt', None)
    if dtStartFilter:
        if dt:
            result = result and (dt >= dtStartFilter)
        else:
            log.warning(u'Ошибка определения даты записи %s' % str(record))
            return False
    if dtStopFilter:
        if dt:
            result = result and (dt <= dtStopFilter)
        else:
            log.warning(u'Ошибка определения даты записи %s' % str(record))
            return False

    # Дополнительные фильтры
    if tFilters:
        try:
            filter_result = [fltr(record) for fltr in tFilters]
        except:
            log.fatal(u'Ошибка проверки фильтров')
            return False

        if sFilterLogic == AND_FILTER_LOGIC:
            result = result and all(filter_result)
        elif sFilterLogic == OR_FILTER_LOGIC:
            result = result and any(filter_result)

    return result