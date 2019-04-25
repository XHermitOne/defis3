#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Сервер движка Cubes OLAP Framework.
Исходники:
https://github.com/DataBrewery/cubes
Оффициальный сайт:
http://cubes.databrewery.org/
"""

import os.path

from .. import olap_server_interface
from ic.components import icwidget
from ic.utils import ic_file
from ic.log import log
from ic.utils import ini
from ic.utils import system

from STD.json import json_manager
from STD.spreadsheet import spreadsheet_manager

__version__ = (0, 1, 1, 1)

DEFAULT_SLICER_EXEC = 'slicer'
ALTER_SLICER_EXEC = os.path.join(ic_file.getHomeDir(), '.local', 'bin', 'slicer')

# Спецификация
SPC_IC_CUBESOLAPSERVER = {'source': None,    # Паспорт объекта БД хранения OLAP кубов
                          'ini_filename': None,     # Файл настройки OLAP сервера
                          'model_filename': None,   # JSON Файл описания кубов OLAP сервера
                          'exec': DEFAULT_SLICER_EXEC,  # Файл запуска OLAP сервера
                          'srv_path': None,     # Папка расположения файлов настроек OLAP сервера

                          'log_filename': None,     # Путь до файла журнала
                          'log_level': 'info',  # Уровень журналирования
                          'host': 'localhost',  # Хост сервера
                          'port': 5000,         # Порт сервера
                          'reload': True,       #
                          'prettyprint': True,  # Демонстрационные цели
                          'allow_cors_origin': '*',  # Заголовок совместного использования ресурсов. Другие связанные заголовки также добавляются, если эта опция присутствует.

                          '__parent__': icwidget.SPC_IC_SIMPLE,
                          '__attr_hlp__': {'source': u'Паспорт объекта БД хранения OLAP кубов',
                                           'ini_filename': u'Файл настройки OLAP сервера',
                                           'model_filename': u'JSON Файл описания кубов OLAP сервера',
                                           'exec': u'Файл запуска OLAP сервера',
                                           'srv_path': u'Папка расположения файлов настроек OLAP сервера',

                                           'log_filename': u'Путь до файла журнала',
                                           'log_level': u'Уровень журналирования',
                                           'host': u'Хост сервера',
                                           'port': u'Порт сервера',
                                           'reload': u'',
                                           'prettyprint': u'Демонстрационные цели',
                                           'allow_cors_origin': u'Заголовок совместного использования ресурсов. Другие связанные заголовки также добавляются, если эта опция присутствует.',
                                           },
                          }


DEFAULT_INI_FILENAME = 'slicer.ini'
DEFAULT_MODEL_FILENAME = 'model.json'
START_COMMAND_FMT = '%s serve %s &'

DEFAULT_OLAP_SERVER_DIRNAME = ic_file.getPrjProfilePath()

LOG_LEVELS = ('info', 'debug', 'warn', 'error')

OLAP_SERVER_URL_FMT = 'http://%s:%d/cube/%s/%s'
OLAP_SERVER_URL_DIMENSION_FMT = '?drilldown=%s'
OLAP_SERVER_URL_VALUE_FMT = '?cut=%s:%s'


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

    def getExec(self):
        """
        Файл запуска OLAP сервера.
        """
        return DEFAULT_SLICER_EXEC

    def getRunCommand(self):
        """
        Команда запуска OLAP сервера.
        """
        exec_file = self.getExec()
        ini_filename = self.getINIFileName()

        command = START_COMMAND_FMT % (exec_file, ini_filename)
        return command

    def run(self):
        """
        Запуск сервера.
        @return: True/False.
        """
        if self.is_running():
            # Если сервер уже запущен, то запуск производить не надо
            log.info(u'OLAP Сервер <%s> уже запущен' % self.getName())
            return True

        self.save_ini()
        self.save_model()

        run_command = self.getRunCommand()

        try:
            os.system(run_command)
            log.info(u'Выполнена комманда <%s>' % run_command)
            return True
        except:
            log.fatal(u'Ошибка выполнения комманды <%s>' % run_command)
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
        exec_filename = self.getExec()
        log.info(u'Проверка запущенного OLAP сервера по <%s>' % exec_filename)
        return system.isActiveProcess(exec_filename)

    def get_response(self, *args, **kwargs):
        """
        Запрос получения данных от сервера.
        Функция слишком общая.
        Поэтому реализация ее должна обрабатывать различные запросы в
        зависимости от входящих данных.
        @return: Запрашиваемые данные или None в случае ошибки.
        """
        cube_name = kwargs.get('cube_name',  self.getCubes()[0].getTableName() if self.getCubesCount() else None)
        func_name = kwargs.get('method_name',  'aggregate')
        dimension_name = kwargs.get('dimension_name',  None)
        dimension_value = kwargs.get('dimension_value',  None)

        url = OLAP_SERVER_URL_FMT % (self.getHost(), self.getPort(),
                                     cube_name, func_name)
        if dimension_name:
            url += OLAP_SERVER_URL_DIMENSION_FMT % dimension_name
            if dimension_value:
                url += OLAP_SERVER_URL_VALUE_FMT % (dimension_name, dimension_value)

        # url = 'http://%s:%d/cubes' % (self.getHost(), self.getPort())
        log.debug(u'Определение JSON по URL <%s>' % url)
        return self.get_json_as_dict_by_url(url)

    def getName(self):
        """
        Имя объекта.
        """
        return u''

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return None

    def getDB(self):
        """
        Объект БД.
        """
        return self._db

    def getINIFileName(self):
        """
        Имя настроечного файла.
        """
        return self._ini_filename

    def getModelFileName(self):
        """
        Имя файла описания кубов.
        """
        return self._model_filename

    def getLogFileName(self):
        """
        Путь до файла журнала.
        """
        return None

    def getLogLevel(self):
        """
        Уровень журналирования.
        """
        return None

    def getHost(self):
        """
        Хост сервера.
        """
        return None

    def getPort(self):
        """
        Порт сервера.
        """
        return None

    def isReload(self):
        """
        """
        return True

    def isPrettyPrint(self):
        """
        Демонстрационные цели.
        """
        return True

    def getAllowCorsOrigin(self):
        """
        Заголовок совместного использования ресурсов.
        Другие связанные заголовки также добавляются,
        если эта опция присутствует.
        """
        return '*'

    def _save_ini(self, ini_filename=None, bReWrite=True):
        """
        Сохранить файл настройки OLAP сервера.
        @param ini_filename: Полное имя INI файла настроек OLAP сервера.
            Если не определено, то берем имя файла из описания объекта.
        @param bReWrite: Перезаписать существующий файл?
        @return: True/False.
        """
        if ini_filename is None:
            ini_filename = self.getINIFileName()

        ini_content = dict(workspace=dict(),
                           server=dict(),
                           store=dict(type='sql'),
                           models=dict())

        log_filename = self.getLogFileName()
        if log_filename:
            ini_content['workspace']['log'] = log_filename
        log_level = self.getLogLevel()
        if log_level:
            ini_content['workspace']['log_level'] = log_level

        # Настройки сервера
        host = self.getHost()
        if host:
            ini_content['server']['host'] = host
        port = self.getPort()
        if port:
            ini_content['server']['port'] = port
        reload = self.isReload()
        if reload:
            ini_content['server']['reload'] = reload
        prettyprint = self.isPrettyPrint()
        if prettyprint:
            ini_content['server']['prettyprint'] = prettyprint
        allow_cors_origin = self.getAllowCorsOrigin()
        if allow_cors_origin:
            ini_content['server']['allow_cors_origin'] = allow_cors_origin

        # Настройки БД
        db = self.getDB()
        if db:
            db_url = db.getDBUrl()
            ini_content['store']['url'] = db_url
        else:
            log.warning(u'Не определена БД хранения таблицы OLAP куба <%s>' % self.getName())

        #
        model_filename = self.getModelFileName()
        if model_filename:
            ini_content['models']['main'] = model_filename
        else:
            log.warning(u'Не определен файл описания кубов OLAP сервера <%s>' % self.getName())

        return ini.Dict2INI(ini_content, ini_filename, rewrite=bReWrite)

    def save_ini(self, ini_filename=None, bReWrite=True):
        """
        Сохранить файл настройки OLAP сервера.
        @param ini_filename: Полное имя INI файла настроек OLAP сервера.
            Если не определено, то берем имя файла из описания объекта.
        @param bReWrite: Перезаписать существующий файл?
        @return: True/False.
        """
        try:
            return self._save_ini(ini_filename=ini_filename, bReWrite=bReWrite)
        except:
            log.fatal(u'Ошибка сохранения файла настройки OLAP сервера <%s>' % ini_filename)
        return False

    def _save_model(self, model_filename=None, bReWrite=True):
        """
        Сохранить файл описания кубов OLAP сервера.
        @param model_filename: Полное имя JSON файла описания кубов OLAP сервера.
            Если не определено, то берем имя файла из описания объекта.
        @param bReWrite: Перезаписать существующий файл?
        @return: True/False.
        """
        if model_filename is None:
            model_filename = self.getModelFileName()

        json_content = dict(cubes=list(),
                            dimensions=list())

        # Заполнение кубов
        for cube in self.getCubes():
            dimensions = cube.getDimensions()
            cube_content = dict(name=cube.getTableName(),
                                dimensions=[dimension.getName() for dimension in dimensions])

            # Заполнение фактов
            measures = cube.getMeasures()
            if measures:
                if 'measures' not in cube_content:
                    cube_content['measures'] = list()
                for measure in measures:
                    measure_content = dict(name=measure.getFieldName())
                    measure_label = measure.getLabel()
                    if measure_label:
                        measure_content['label'] = measure_label

                    cube_content['measures'].append(measure_content)

            # Заполнение измерений
            for dimension in dimensions:
                dimension_content = dict(name=dimension.getName())
                dimension_attributes = dimension.getAttributes()
                if dimension_attributes:
                    dimension_content['attributes'] = dimension_attributes
                json_content['dimensions'].append(dimension_content)

                dimension_detail_tabname = dimension.getDetailTableName()
                if dimension_detail_tabname:
                    dimension_detail_fldname = dimension.getDetailFieldName()
                    if dimension_detail_fldname:
                        if 'joins' not in cube_content:
                            cube_content['joins'] = list()

                        # Настроить связь
                        dimension_fld_name = dimension.getFieldName()
                        dimension_join = dict(master=dimension_fld_name,
                                              detail='%s.%s' % (dimension_detail_tabname,
                                                                dimension_detail_fldname))
                        cube_content['joins'].append(dimension_join)

            # Заполнение агрегаций
            aggregates = cube.getAggregates()
            if aggregates:
                if 'aggregates' not in cube_content:
                    cube_content['aggregates'] = list()
                for aggregate in aggregates:
                    aggregate_content = dict(name=aggregate.getName())
                    aggregate_function = aggregate.getFunctionName()
                    if aggregate_function:
                        aggregate_content['function'] = aggregate_function
                    aggregate_measure = aggregate.getMeasureName()
                    if aggregate_measure:
                        aggregate_content['measure'] = aggregate_measure
                    aggregate_expression = aggregate.getExpressionCode()
                    if aggregate_expression:
                        aggregate_content['expression'] = aggregate_expression

                    cube_content['aggregates'].append(aggregate_content)

            json_content['cubes'].append(cube_content)

        return self.save_dict_as_json(model_filename, json_content, bReWrite)

    def save_model(self, model_filename=None, bReWrite=True):
        """
        Сохранить файл описания кубов OLAP сервера.
        @param model_filename: Полное имя JSON файла описания кубов OLAP сервера.
            Если не определено, то берем имя файла из описания объекта.
        @param bReWrite: Перезаписать существующий файл?
        @return: True/False.
        """
        try:
            return self._save_model(model_filename=model_filename, bReWrite=bReWrite)
        except:
            log.fatal(u'Ошибка сохранения файла описания кубов OLAP сервера <%s>' % model_filename)
        return False

    def getCubes(self):
        """
        Список объектов кубов OLAP сервера.
        """
        return list()

    def getCubesCount(self):
        """
        Количество кубов OLAP сервера.
        """
        return len(self.getCubes())

    def to_spreadsheet(self, json_dict):
        """
        Преобразование результатов запроса к OLAP серверу к структуре SpreadSheet.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @return: Словарь структуры SpreadSheet.
        """
        # Объект управления структурой SpreadSheet
        spreadsheet_mngr = spreadsheet_manager.icSpreadSheetManager()
        # Создаем книгу
        workbook = spreadsheet_mngr.createWorkbook()
        # Создаем лист в книге
        worksheet = workbook.createWorksheet()
        # Создаем стили
        styles = workbook.createStyles()
        # Добавляем стили
        for default_style_attr in spreadsheet_mngr.DEFAULT_STYLES:
            style = styles.createStyle()
            style.set_attributes(default_style_attr)

        # Создаем таблицу
        table = worksheet.createTable()
        # Заполнение заголовка
        # Создаем колонки
        levels = json_dict.get('levels', dict())
        aggregates = json_dict.get('aggregates', dict())
        for level_name, level_content in levels.items():
            first_column = spreadsheet_mngr.createDefaultColumn(table)
            col_count = len(level_content) - 1 + len(aggregates)
            spreadsheet_mngr.createDefaultColumns(table, count=col_count)

        # Создаем строки

        return spreadsheet_mngr.getData()
