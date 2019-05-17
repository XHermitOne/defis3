#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Сервер движка Cubes OLAP Framework.
Исходники:
https://github.com/DataBrewery/cubes
Оффициальный сайт:
http://cubes.databrewery.org/

Основные данные и аналитические функции доступны через следующие запросы:
- /cube/<name>/aggregate – агрегация мер, предоставлять сводку, генерировать детализацию, фрагменты и кубы, ...
- /cube/<name>/members/<dim> – элементы измерения списка
- /cube/<name>/facts – список фактов внутри клетки
- /cube/<name>/fact – одиночный факт
- /cube/<name>/cell – описание ячейки

Параметры:
- cut - спецификация ячейки, например: cut=date:2004,1|category:2|entity:12345
- drilldown - измерение, который нужно "сверлить". Например drilldown=date даст строки для каждого значения
    следующий уровень даты измерения. Вы можете явно указать уровень для детализации в форме: dimension:level,
    таких как: drilldown=date:month. Чтобы указать иерархию используйте dimension@hierarchy как в
    drilldown=date@ywd для неявного уровня или drilldown=date@ywd:week явно указать уровень.
- aggregates – список агрегатов для расчета, разделяется с помошью |,
    например: aggergates=amount_sum|discount_avg|count
- measures – список мер, для которых будут рассчитаны их соответствующие агрегаты (см. ниже).
    Разделяется с помощью |, например: aggergates=proce|discount
- page - номер страницы для нумерации страниц
- pagesize - размер страницы для разбивки на страницы
- order - список атрибутов для заказа
- split – разделенная ячейка, тот же синтаксис, что и у вырезки, определяет виртуальное двоичное (флаговое) измерение, которое указывает, является ли ячейка
    принадлежит разделенному разрезу (true) или нет (false). Атрибут измерения называется __within_split__.
    Обратитесь к бэкэнду, который вы используете для получения дополнительной информации, поддерживается ли эта функция или нет.
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

OLAP_SERVER_URL_FMT = 'http://%s:%d/%s'


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

    def get_request_url(self, request_url):
        """
        Получить полный запрос получения данных от сервера по URL.
        @param request_url: URL запроса к OLAP серверу.
        @return: Полный сгенерированный запрос.
        """
        url = OLAP_SERVER_URL_FMT % (self.getHost(), self.getPort(),
                                     request_url)
        if self.isPrettyPrint():
            url += '&prettyprint=true' if '?' in url else '?prettyprint=true'
        return url

    def get_response(self, request_url):
        """
        Запрос получения данных от сервера по URL.
        @param request_url: URL запроса к OLAP серверу.
        @return: Запрашиваемые данные или None в случае ошибки.
        """
        url = self.get_request_url(request_url)
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
            cube_content = self._get_model_cube(cube)
            json_content['cubes'].append(cube_content)

            dimensions = cube.getDimensions()
            for dimension in dimensions:
                dimension_content = self._get_model_dimension(dimension)
                json_content['dimensions'].append(dimension_content)

        return self.save_dict_as_json(model_filename, json_content, bReWrite)

    def _get_model_cube(self, cube):
        """
        Содержимое модели куба.
        @param cube: Объект куба.
        @return: Словарь содержимого модели, соответствующей кубу.
        """
        dimensions = cube.getDimensions()
        cube_content = dict(name=cube.getTableName(),
                            dimensions=[dimension.getName() for dimension in dimensions])

        label = cube.getLabel()
        if label:
            cube_content['label'] = label

        # Заполнение фактов
        measures = cube.getMeasures()
        if measures:
            if 'measures' not in cube_content:
                cube_content['measures'] = list()
            for measure in measures:
                measure_content = self._get_model_measure(measure)
                cube_content['measures'].append(measure_content)

        # Заполнение измерений
        for dimension in dimensions:
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
                aggregate_content = self._get_model_aggregate(aggregate)
                cube_content['aggregates'].append(aggregate_content)
        return cube_content

    def _get_model_measure(self, measure):
        """
        Содержимое модели меры/фактических данных.
        @param measure: Объект меры.
        @return: Словарь содержимого модели, соответствующей мере.
        """
        measure_content = dict(name=measure.getFieldName())
        measure_label = measure.getLabel()
        if measure_label:
            measure_content['label'] = measure_label
        return measure_content

    def _get_model_aggregate(self, aggregate):
        """
        Содержимое модели агрегации данных.
        @param aggregate: Объект агрегации данных.
        @return: Словарь содержимого модели, соответствующей агрегации данных.
        """
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
        return aggregate_content

    def _get_model_dimension(self, dimension):
        """
        Содержимое модели измерения.
        @param dimension: Объект измерения.
        @return: Словарь содержимого модели, соответствующей измерению.
        """
        dimension_content = dict(name=dimension.getName())
        label = dimension.getLabel()
        if label:
            dimension_content['label'] = label
        dimension_attributes = dimension.getAttributes()
        if dimension_attributes:
            dimension_content['attributes'] = dimension_attributes
        dimension_levels = dimension.getLevels()
        if dimension_levels:
            dimension_content['levels'] = [self._get_model_dimension_level(level) for level in dimension_levels]
        dimension_hierarchies = dimension.getHierarchies()
        if dimension_hierarchies:
            dimension_content['hierarchies'] = [self._get_model_dimension_hierarchy(hierarchy) for hierarchy in dimension_hierarchies]
            # ВНИМАНИЕ! По умолчанию считаем первую иерархию
            dimension_content['default_hierarchy_name'] = dimension_hierarchies[0].getName()
        return dimension_content

    def _get_model_dimension_level(self, level):
        """
        Содержимое модели уровня измерения.
        @param level: Объект уровня.
        @return: Словарь содержимого модели, соответствующей уровню измерения.
        """
        level_content = dict(name=level.getName())
        level_attributes = level.getAttributes()
        if level_attributes:
            level_content['attribites'] = level_attributes
        return level_content

    def _get_model_dimension_hierarchy(self, hierarchy):
        """
        Содержимое модели иерархии уровней измерения.
        @param hierarchy: Объект иерархии.
        @return: Словарь содержимого модели, соответствующей иерархии.
        """
        hierarchy_content = dict(name=hierarchy.getName())
        hierarchy_levels = hierarchy.getLevelNames()
        if hierarchy_levels:
            hierarchy_content['levels'] = hierarchy_levels
        return hierarchy_content

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

    def _to_spreadsheet(self, json_dict, cube=None):
        """
        Преобразование результатов запроса к OLAP серверу к структуре SpreadSheet.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @param cube: Куб. Если не определен, то берется первый.
        @return: Словарь структуры SpreadSheet.
        """
        if cube is None:
            cubes = self.getCubes()
            cube = cubes[0] if cubes else None
            if cube is None:
                log.warning(u'Конвертация в структуру SpreadSheet. Не определен куб.')
                return None

        # Объект управления структурой SpreadSheet
        spreadsheet_mngr = spreadsheet_manager.icSpreadSheetManager()
        # Создаем книгу
        workbook = spreadsheet_mngr.createWorkbook()
        # Создаем лист в книге
        worksheet = workbook.createWorksheet()
        # Создаем стили
        styles = workbook.createStyles()
        # Добавляем стили
        for default_style_attr in spreadsheet_manager.DEFAULT_STYLES:
            style = styles.createStyle()
            style_id = default_style_attr.get('ID', None)
            if style_id:
                style.setID(style_id)
            # log.debug(u'1. Style %s' % str(style.get_attributes()))
            style.update_attributes(default_style_attr)
            # log.debug(u'2. Style %s' % str(style.get_attributes()))

        # Создаем таблицу
        row_count = self._get_row_count(json_dict)
        col_count = self._get_col_count(json_dict)
        table = self._create_spreadsheet_table(spreadsheet_mngr, worksheet, row_count, col_count)

        # Заполнение заголовка
        self._create_spreadsheet_header(table, json_dict, cube)
        # Создаем строки
        self._create_spreadsheet_detail(table, json_dict)
        # Заполнение подвала
        self._create_spreadsheet_footer(table, json_dict)

        return spreadsheet_mngr.getData()

    def _get_row_count(self, json_dict):
        """
        Количество строк.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @return: Количество строк.
        """
        cells = json_dict.get('cells', dict())
        # Учитываем строку заголовка и строку итогов
        #                        V
        row_count = len(cells) + 2
        return row_count

    def _get_col_count(self, json_dict):
        """
        Количество колонок.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @return: Количество колонок.
        """
        col_count = self._get_level_count(json_dict) + self._get_aggregate_count(json_dict)
        return col_count

    def _get_level_count(self, json_dict):
        """
        Количество уровней измерений.
        @return: Количество уровней измерений.
        """
        attributes = json_dict.get('attributes', list())
        return len(attributes)

    def _get_aggregate_count(self, json_dict):
        """
        Количество уровней измерений.
        @return: Количество уровней измерений.
        """
        aggregates = json_dict.get('aggregates', list())
        return len(aggregates)

    def _create_spreadsheet_table(self, spreadsheet_mngr, worksheet, row_count, col_count):
        """
        Создать таблицу SpreadSheet.
        @param spreadsheet_mngr: Менеджер управления структурой SpreadSheet.
        @param worksheet: Объект листа.
        @param row_count: Количество строк.
        @param col_count: Количество столбцов.
        @return: Объект таблицы
        """
        # Создаем таблицу
        table = worksheet.createTable()
        # Создаем колонки
        spreadsheet_mngr.createDefaultColumns(table, count=col_count)
        spreadsheet_mngr.createDefaultRows(table, count=row_count)
        return table

    def _get_level_name(self, json_dict, level_idx):
        """
        Получить имя уровня по индексу.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @param level_idx: Индекс уровня.
        @return: Имя уровня.
        """
        attributes = json_dict.get('attributes', list())
        return attributes[level_idx]

    def _get_aggregate_name(self, json_dict, aggregate_idx):
        """
        Получить имя агрегации по индексу.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @param aggregate_idx: Индекс агрегации.
        @return: Имя агрегации.
        """
        aggregates = json_dict.get('aggregates', list())
        return aggregates[aggregate_idx]

    def _create_spreadsheet_header(self, table, json_dict, cube):
        """
        Создать заголовок данных структуры SpreadSheet.
        @param table: Объект таблицы.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @param cube: Объект куба.
        @return: True/False
        """
        # Заполнение части уровней измерения строк
        level_count = self._get_level_count(json_dict)
        for i in range(level_count):
            cell = table.getCell(1, i + 1)
            cell.setStyleID('GROUP')
            dimension = cube.findDimension(self._get_level_name(json_dict, i))
            cell.setValue(dimension.getLabel() if dimension else u'')
            if level_count > 1:
                cell.setMerge(level_count - 1, 0)

        # Заполнение колонок агрегаций
        aggregate_count = self._get_aggregate_count(json_dict)
        for i in range(aggregate_count):
            cell = table.getCell(1, level_count + i + 1)
            cell.setStyleID('HEADER')
            aggregate = cube.findAggregate(self._get_aggregate_name(json_dict, i))
            cell.setValue(aggregate.getLabel() if aggregate else u'')
        return True

    def _create_spreadsheet_detail(self, table, json_dict):
        """
        Создать тело табличной части данных структуры SpreadSheet.
        @param table: Объект таблицы.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @return: True/False
        """
        attributes = json_dict.get('attributes', list())
        aggregates = json_dict.get('aggregates', list())
        records = json_dict.get('cells', list())
        for i_row, record in enumerate(records):
            # Затем расставляем значения по своим местам
            last_idx = 0
            for name, value in record.items():
                style_id = None
                if name in attributes:
                    idx = attributes.index(name)
                    last_idx += 1
                    style_id = 'GROUP'
                elif name in aggregates:
                    idx = last_idx + aggregates.index(name)
                    style_id = 'CELL'
                else:
                    log.warning(u'Не определено имя колонки <%s>' % name)
                    continue

                # log.debug(u'Ячейка <%d x %d>' % (i_row + 1, idx + 1))
                # Учет строки заголовка------V
                cell = table.getCell(i_row + 2, idx + 1)
                if style_id:
                    cell.setStyleID(style_id)
                cell.setValue(value if value is not None else u'')
        return True

    def _create_spreadsheet_footer(self, table, json_dict):
        """
        Создать подвал/итоговую строку данных структуры SpreadSheet.
        @param table: Объект таблицы.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @return: True/False
        """
        summary = json_dict.get('summary', dict())
        aggregates = json_dict.get('aggregates', list())
        level_count = self._get_level_count(json_dict)
        last_rec_idx = self._get_row_count(json_dict) - 1

        # Затем расставляем значения по своим местам
        for i, name in enumerate(aggregates):
            idx = level_count + i
            i_row = last_rec_idx + 1
            i_col = idx + 1
            cell = table.getCell(i_row, i_col)
            cell.setStyleID('FOOTER')
            value = summary.get(name, None)
            cell.setValue(value if value is not None else u'')
        return True

    def to_spreadsheet(self, json_dict, cube=None):
        """
        Преобразование результатов запроса к OLAP серверу к структуре SpreadSheet.
        @param json_dict: Результаты запроса к OLAP серверу в виде словаря JSON.
        @param cube: Куб. Если не определен, то берется первый.
        @return: Словарь структуры SpreadSheet.
        """
        try:
            spreadsheet = self._to_spreadsheet(json_dict=json_dict, cube=cube)
            # log.debug(u'SpreadSheet %s' % str(spreadsheet))
            return spreadsheet
        except:
            log.fatal(u'Ошибка конвертации результатов запроса к OLAP серверу к структуре SpreadSheet.')
        return None
