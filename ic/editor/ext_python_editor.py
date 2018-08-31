#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Внешний редактор модулей Python.

В нашем случае используется gEdit.
Т.к. он кросплатформенный, поддерживает плагины и
подсвечивает синтаксис Python.

Установка плагинов:
sudo apt install gedit-plugins

Для gEdit есть плагин PythonChecker:
https://github.com/rdunklau/Gedit-checkpython.git
"""

import os

from ic.interfaces import icideinterface
from ic.log import log

__version__ = (0, 1, 1, 1)

GEDIT_EXEC_FILENAME = '/usr/bin/gedit'
GEDIT_EXT_ENCODING_PARAM_FMT = '--encoding=%s'
GEDIT_EXT_PYTHON_EDITOR_FMT = 'gedit %s %s &'


class icGEditPythonEditor(icideinterface.icIDEInterface):
    """
    GEdit как внешний редактор модулей Python.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icideinterface.icIDEInterface.__init__(self, *args, **kwargs)

    def OpenFile(self, filename, OpenInNewTab=True,
                 editrecentfiles=True, encoding=icideinterface.DEFAULT_ENCODINT_STR, readonly=False):
        """
        Загружает нужный файл в IDE.

        @type filename: C{string}
        @param filename: Имя загружаемого файла.
        @type OpenInNewTab: C{bool}
        @param OpenInNewTab: Признак загрузки файла на новой закладке.
        @type editrecentfiles: C{bool}
        @param editrecentfiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        @type encoding: C{string}
        @param encoding: Кодировка файла.
        @type readonly: C{bool}
        @param readonly: Указание, что файл откроется только для чтения.
        @rtype: C{bool}
        @return: Признак успешной загрузки.
        """
        try:
            # Параметры кодировки
            encoding_param = ''
            if GEDIT_EXT_ENCODING_PARAM_FMT:
                if encoding != icideinterface.DEFAULT_ENCODINT_STR:
                    encoding_param = GEDIT_EXT_ENCODING_PARAM_FMT % encoding

            # Формирование коммандной строки запуска внешнего редактора
            cmd = GEDIT_EXT_PYTHON_EDITOR_FMT % (encoding_param, filename)
            log.info(u'Запуск комманды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)


GEANY_EXEC_FILENAME = '/usr/bin/geany'
GEANY_EXT_PYTHON_EDITOR_FMT = 'geany %s %s &'


class icGeanyPythonEditor(icideinterface.icIDEInterface):
    """
    Geany как внешний редактор модулей Python.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icideinterface.icIDEInterface.__init__(self, *args, **kwargs)

    def OpenFile(self, filename, OpenInNewTab=True,
                 editrecentfiles=True, encoding=icideinterface.DEFAULT_ENCODINT_STR, readonly=False):
        """
        Загружает нужный файл в IDE.

        @type filename: C{string}
        @param filename: Имя загружаемого файла.
        @type OpenInNewTab: C{bool}
        @param OpenInNewTab: Признак загрузки файла на новой закладке.
        @type editrecentfiles: C{bool}
        @param editrecentfiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        @type encoding: C{string}
        @param encoding: Кодировка файла.
        @type readonly: C{bool}
        @param readonly: Указание, что файл откроется только для чтения.
        @rtype: C{bool}
        @return: Признак успешной загрузки.
        """
        try:
            # Формирование коммандной строки запуска внешнего редактора
            cmd = GEANY_EXT_PYTHON_EDITOR_FMT % ('--read-only' if readonly else '',
                                                 filename)
            log.info(u'Запуск комманды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)

    def GetAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        pass

    def IsOpenedFile(self, fileName):
        """
        Проверить открыт файл или нет.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        pass


if os.path.exists(GEANY_EXEC_FILENAME):
    icExtPythonEditor = icGeanyPythonEditor
elif os.path.exists(GEDIT_EXEC_FILENAME):
    icExtPythonEditor = icGEditPythonEditor
else:
    log.error(u'Не определен внешний редактор модулей Python')
