#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Сервер движка Cubes OLAP Framework.
https://github.com/DataBrewery/cubes
"""

import os.path

from .. import olap_server_interface
from ic.components import icwidget
from ic.utils import ic_file
from ic.log import log

from STD.json import json_manager

__version__ = (0, 1, 1, 1)

DEFAULT_SLICER_EXEC = 'slicer'
ALTER_SLICER_EXEC = os.path.join(ic_file.getHomeDir(), '.local', 'bin', 'slicer')

# Спецификация
SPC_IC_CUBESOLAPSERVER = {'source': None,    # Паспорт объекта БД хранения OLAP кубов
                          'ini_filename': None,     # Файл настройки OLAP сервера
                          'model_filename': None,   # JSON Файл описания кубов OLAP сервера
                          'exec': DEFAULT_SLICER_EXEC,  # Файл запуска OLAP сервера
                          'srv_path': None,     # Папка расположения файлов настроек OLAP сервера
                          '__parent__': icwidget.SPC_IC_SIMPLE,
                          '__attr_hlp__': {'source': u'Паспорт объекта БД хранения OLAP кубов',
                                           'ini_filename': u'Файл настройки OLAP сервера',
                                           'model_filename': u'JSON Файл описания кубов OLAP сервера',
                                           'exec': u'Файл запуска OLAP сервера',
                                           'srv_path': u'Папка расположения файлов настроек OLAP сервера',
                                           },
                          }


DEFAULT_INI_FILENAME = 'slicer.ini'
DEFAULT_MODEL_FILENAME = 'model.json'
START_COMMAND_FMT = '%s serve slicer.ini'

DEFAULT_OLAP_SERVER_DIRNAME = ic_file.getPrjProfilePath()


class icCubesOLAPServerProto(olap_server_interface.icOLAPServerInterface,
                             json_manager.icJSONManager):
    """
    OLAP Сервер движка Cubes OLAP Framework.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # БД хранения OLAP кубов
        self._db = None

        # Файл настройки OLAP сервера
        self._ini_filename = None

        # JSON Файл описания кубов OLAP сервера
        self._model_filename = None

    def run(self):
        """
        Запуск сервера.
        @return: True/False.
        """
        log.warning(u'Не определен метод запуска OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def stop(self):
        """
        Остановка сервера.
        @return: True/False.
        """
        log.warning(u'Не определен метод останова OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def is_running(self):
        """
        Проверка того что OLAP сервер запущен.
        @return: True - сервер запущен, False - нет.
        """
        log.warning(u'Не определен метод проверки запущенного OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def get(self, *args, **kwargs):
        """
        Запрос получения данных от сервера.
        Функция слишком общая.
        Поэтому реализация ее должна обрабатывать различные запросы в
        зависимости от входящих данных.
        @return: Запрашиваемые данные или None в случае ошибки.
        """
        log.warning(u'Не определен метод получения данных от OLAP сервера <%s>' % self.__class__.__name__)
        return None
