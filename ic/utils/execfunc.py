#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций выполнения запросов и методов пользователя.
"""

import os
import sys
# import imp
import subprocess
import locale

from ic.log import log
try:
    from . import util
except ImportError:
    import util

__versiom__ = (0, 1, 1, 2)


def unLoadSource(name):
    """
    Выгрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    """
    if name in sys.modules:
        del sys.modules[name]
        return True
    return False


def reLoadSource(name, path=None):
    """
    Перезагрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    @type path: C{string}
    @param path: Полный путь до модуля.
    """
    if path is None:
        if name in sys.modules:
            py_file_name = sys.modules[name].__file__
            py_file_name = os.path.splitext(py_file_name)[0]+'.py'
            path = py_file_name
        else:
            log.warning(u'Модуль <%s> не загружен' % name)
            return None
    unLoadSource(name)
    return util.icLoadSource(name, path)


def exec_code(sCode='', bReImport=False, name_space=None, kwargs=None):
    """
    Выполнить блок кода.
    @type sCode: C{string}
    @param sCode: Блок кода.
        Блок кода - строка в формате:
            ИмяПакета.ИмяМодуля.ИмяФункции(аргументы).
    @type bReImport: C{bool}
    @param bReImport: Переимпортировать модуль функции?
    @type name_space: C{dictionary}
    @param name_space: Пространство имен.
    @type kwargs: C{dictionary}
    @param kwargs: Дополнительные аргументы функции.
    """
    result = None

    # Подготовить пространство имен
    if name_space is None or not isinstance(name_space, dict):
        name_space = {}

    # Определяем флаг что блок кода производит вызов функции
    is_exec_func = '(' in sCode and ')' in sCode
    # Элементы импорта
    func_import = sCode.split('(')[0].split('.')
    # Имя модуля или функции для работы с импортированным объектом
    func_mod = '.'.join(func_import[:-1])

    if bReImport:
        unLoadSource(func_mod)

    # Импортирование модуля
    if func_mod:
        import_str = 'import ' + func_mod
        try:
            exec(import_str)
            log.info(u'Импорт функции/модуля <%s>' % import_str)
        except:
            log.fatal(u'Ошибка импорта <%s>' % import_str)
            raise

    # Добавить локальное пространство имен
    name_space.update(locals())

    if kwargs:
        if isinstance(kwargs, dict):
            name_space.update(kwargs)
        else:
            log.warning(u'Не поддерживаемый тип <%s> дополнительных аргументов функции <%s>' % (type(kwargs), sCode))

    # Выполнение функции
    if is_exec_func:
        try:
            result = eval(sCode, globals(), name_space)
        except:
            log.fatal(u'Ошибка выполнения выражения <%s>' % sCode)
            raise
    else:
        log.warning(u'Не определен вызов функции в блоке кода <%s>' % sCode)

    return result


def exec_sys_cmd(command, split_lines=False):
    """
    Выполнить системную комманду и получить результат ее выполнения.
    @param command: Системная комманда.
    @param split_lines: Произвести разделение на линии?
    @return: Если нет разделения по линиям, то возвращается текст который
        отображается в консоли.
        При разбитии по линиям возвращается список выводимых строк.
        В случае ошибки возвращается None.
    """
    try:
        cmd = command.strip().split(' ')
        console_encoding = locale.getpreferredencoding()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        if split_lines:
            b_lines = process.stdout.readlines()
            lines = [line.decode(console_encoding).strip() for line in b_lines]
            return lines
        else:
            b_text = process.stdout.read()
            text = b_text.decode(console_encoding)
            return text
    except:
        log.fatal(u'Ошибка выполнения системной комманды <%s>' % command)
    return None
