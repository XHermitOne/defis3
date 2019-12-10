#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции управления импортом модулей.
"""
import os
import sys
import importlib.util

from ic.log import log

__version__ = (0, 1, 1, 1)


def importModule(name):
    """
    Импортирование модуля. Пример: subsys.usercomponents.component
    :type name: C{string}
    :param name: Имя модуля.
    """
    mod = __import__(name, globals(), locals(), [], -1)
    # Поскольку __import__ возвращает родительский модуль
    # получаем доступ до нужного нам модуля через
    # рекурсивный getattr
    c = name.split('.')
    for x in c[1:]:
        mod = getattr(mod, x)
    return mod


def loadSource(name, path):
    """
    Возвращает загруженный модуль.
    :type name: C{string}
    :param name: Имя модуля.
    :type path: C{string}
    :param path: Полный путь до модуля.
    :return: Объект загруженного модуля или None в случае ошибки.
    """
    module = None
    try:
        module_spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    except ImportError:
        log.fatal(u'Ошибка загрузки модуля <%s>. Путь <%s>' % (name, path))
        log.warning(u'ВНИМАНИЕ! Возможно в корневой папке подсистемы находится __init__.py.')
        log.error(u'Системные пути (sys.path):')
        log.error(getSysPathStr())

    return module


def unloadSource(name):
    """
    Выгрузить модуль.
    :type name: C{string}
    :param name: Имя модуля.
    """
    if name in sys.modules:
        del sys.modules[name]
        return True
    return False


def reloadSource(name, path=None):
    """
    Перезагрузить модуль.
    :type name: C{string}
    :param name: Имя модуля.
    :type path: C{string}
    :param path: Полный путь до модуля.
    """
    if path is None:
        if name in sys.modules:
            try:
                py_file_name = sys.modules[name].__file__
                py_file_name = os.path.splitext(py_file_name)[0]+'.py'
                path = py_file_name
            except:
                log.error('Error')
                return None
        else:
            return None
    unloadSource(name)
    return loadSource(name, path)


def addImportPath(path):
    """
    Добавить путь для возможности импорта.
    Добавление происходит в sys.path.
    Также производится проверка на дублирование путей в sys.path
    :param path: Добавляемый путь для импорта.
    :return: Список путей sys.path.
    """
    if not isinstance(path, str):
        log.warning(u'Добавление пути для возможности импорта: ошибка типа <%s>' % type(path))
        return sys.path
    if not os.path.exists(path):
        log.warning(u'Добавление пути для возможности импорта: путь <%s> не существет' % path)
        return sys.path

    if path in sys.path:
        log.warning(u'Путь <%s> уже присутствует в списке sys.path' % path)
        return sys.path

    sys.path.append(path)

    # Проверить дублирование путей
    sys.path = [imp_path for i, imp_path in enumerate(sys.path) if imp_path not in sys.path[:i]]

    return sys.path


def getSysPathStr():
    """
    Список путей для sys.path в виде строки для вывода на экран (print).
    """
    return '\n'.join([u'\t%s' % pth for pth in sys.path])
