#!/usr/bin/env python
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

__version__ = (0, 0, 0, 1)

EXT_ENCODING_PARAM_FMT = '--encoding=%s'
EXT_PYTHON_EDITOR_FMT = 'gedit %s %s &'


class icExtPythonEditor(icideinterface.icIDEInterface):
    """
    Внешний редактор модулей Python.
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
            if EXT_ENCODING_PARAM_FMT:
                if encoding != icideinterface.DEFAULT_ENCODINT_STR:
                    encoding_param = EXT_ENCODING_PARAM_FMT % encoding

            # Формирование коммандной строки запуска внешнего редактора
            cmd = EXT_PYTHON_EDITOR_FMT % (encoding_param, filename)
            log.info(u'Запуск комманды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)

