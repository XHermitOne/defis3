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

В качестве внешнего редактора также могут использоваться Geany или Atom.
Выбор внешнего редактора программой производится в порядке
обнаружения установленной программы:
Atom, Geany, GEdit
"""

import os

from ic.interfaces import icideinterface
from ic.log import log

__version__ = (0, 1, 2, 1)

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

    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding=icideinterface.DEFAULT_ENCODINT_STR, bReadonly=False):
        """
        Загружает нужный файл в IDE.

        :type filename: C{string}
        :param filename: Имя загружаемого файла.
        :type bOpenInNewTab: C{bool}
        :param bOpenInNewTab: Признак загрузки файла на новой закладке.
        :type bEditRecentFiles: C{bool}
        :param bEditRecentFiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        :type encoding: C{string}
        :param encoding: Кодировка файла.
        :type bReadonly: C{bool}
        :param bReadonly: Указание, что файл откроется только для чтения.
        :rtype: C{bool}
        :return: Признак успешной загрузки.
        """
        try:
            # Параметры кодировки
            encoding_param = ''
            if GEDIT_EXT_ENCODING_PARAM_FMT:
                if encoding != icideinterface.DEFAULT_ENCODINT_STR:
                    encoding_param = GEDIT_EXT_ENCODING_PARAM_FMT % encoding

            # Формирование командной строки запуска внешнего редактора
            cmd = GEDIT_EXT_PYTHON_EDITOR_FMT % (encoding_param, filename)
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)

    def openFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.

        :param res: Ресурсное описание.
        :param res_editor: Указатель на редактор ресурсов.
        """
        log.error(u'Не реализован дизайнер форм в IDE <%s>' % self.__class__.__name__)

    def goToLine(self, filename, n_line=0):
        """
        Выполнить переход на линию модуля.

        :param filename: Имя файла модуля.
        :param n_line: Номер линии для перехода.
        :return: True - выполнен переход / False - переход не выполнен.
        """
        try:
            # Формирование командной строки запуска внешнего редактора
            cmd = GEDIT_EXT_PYTHON_EDITOR_FMT % (filename, u'+%d' % n_line)
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s : %s> в IDE' % (filename, n_line))
        return False


GEANY_EXEC_FILENAME = '/usr/bin/geany'
GEANY_EXT_PYTHON_EDITOR_FMT = 'geany --no-msgwin %s %s &'


class icGeanyPythonEditor(icideinterface.icIDEInterface):
    """
    Geany как внешний редактор модулей Python.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icideinterface.icIDEInterface.__init__(self, *args, **kwargs)

    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding=icideinterface.DEFAULT_ENCODINT_STR, bReadonly=False):
        """
        Загружает нужный файл в IDE.

        :type filename: C{string}
        :param filename: Имя загружаемого файла.
        :type bOpenInNewTab: C{bool}
        :param bOpenInNewTab: Признак загрузки файла на новой закладке.
        :type bEditRecentFiles: C{bool}
        :param bEditRecentFiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        :type encoding: C{string}
        :param encoding: Кодировка файла.
        :type bReadonly: C{bool}
        :param bReadonly: Указание, что файл откроется только для чтения.
        :rtype: C{bool}
        :return: Признак успешной загрузки.
        """
        try:
            # Формирование командной строки запуска внешнего редактора
            cmd = GEANY_EXT_PYTHON_EDITOR_FMT % ('--read-only' if bReadonly else '',
                                                 filename)
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)

    def getAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        pass

    def isOpenedFile(self, filename):
        """
        Проверить открыт файл или нет.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        pass

    def openFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.

        :param res: Ресурсное описание.
        :param res_editor: Указатель на редактор ресурсов.
        """
        log.error(u'Не реализован дизайнер форм в IDE <%s>' % self.__class__.__name__)

    def goToLine(self, filename, n_line=0):
        """
        Выпонить переход на линию модуля.

        :param filename: Имя файла модуля.
        :param n_line: Номер линии для перехода.
        :return: True - выполнен переход / False - переход не выполнен.
        """
        try:
            # Формирование командной строки запуска внешнего редактора
            cmd = GEANY_EXT_PYTHON_EDITOR_FMT % (filename, u'--line=%d' % n_line)
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s : %s> в IDE' % (filename, n_line))
        return False


ATOM_EXEC_FILENAME = '/usr/bin/atom'
ATOM_EXT_PYTHON_EDITOR_FMT = 'atom %s%s &'


class icAtomPythonEditor(icideinterface.icIDEInterface):
    """
    Atom (https://atom.io/) как внешний редактор модулей Python.

    Для использования Atom как редактора Python устанавливаются
    следующие плагины:
        1. atom-i18n (для руссификации)
        2. linter (для PEP8)
        3. atom-autocomplete-python (поддержка автозаполнения Python)
        4. minimap (миникарта кода)
        5. symbols-tree-view (простой браузер кода)
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icideinterface.icIDEInterface.__init__(self, *args, **kwargs)

    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding=icideinterface.DEFAULT_ENCODINT_STR, bReadonly=False):
        """
        Загружает нужный файл в IDE.

        :type filename: C{string}
        :param filename: Имя загружаемого файла.
        :type bOpenInNewTab: C{bool}
        :param bOpenInNewTab: Признак загрузки файла на новой закладке.
        :type bEditRecentFiles: C{bool}
        :param bEditRecentFiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        :type encoding: C{string}
        :param encoding: Кодировка файла.
        :type bReadonly: C{bool}
        :param bReadonly: Указание, что файл откроется только для чтения.
        :rtype: C{bool}
        :return: Признак успешной загрузки.
        """
        try:
            # Формирование командной строки запуска внешнего редактора
            cmd = ATOM_EXT_PYTHON_EDITOR_FMT % (filename, u'')
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s> в IDE' % filename)

    def getAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        pass

    def isOpenedFile(self, filename):
        """
        Проверить открыт файл или нет.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        pass

    def openFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.

        :param res: Ресурсное описание.
        :param res_editor: Указатель на редактор ресурсов.
        """
        log.error(u'Не реализован дизайнер форм в IDE <%s>' % self.__class__.__name__)

    def goToLine(self, filename, n_line=0):
        """
        Выпонить переход на линию модуля.

        :param filename: Имя файла модуля.
        :param n_line: Номер линии для перехода.
        :return: True - выполнен переход / False - переход не выполнен.
        """
        try:
            # Формирование командной строки запуска внешнего редактора
            cmd = ATOM_EXT_PYTHON_EDITOR_FMT % (filename, u':%d' % n_line)
            log.info(u'Запуск команды <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка открытия файла <%s : %s> в IDE' % (filename, n_line))
        return False


# Выбор внешнего редактора программой производится в порядке
# обнаружения установленной программы:
# Atom, Geany, GEdit
if os.path.exists(ATOM_EXEC_FILENAME):
    icExtPythonEditor = icAtomPythonEditor
elif os.path.exists(GEANY_EXEC_FILENAME):
    icExtPythonEditor = icGeanyPythonEditor
elif os.path.exists(GEDIT_EXEC_FILENAME):
    icExtPythonEditor = icGEditPythonEditor
else:
    log.error(u'Не определен внешний редактор модулей Python')
