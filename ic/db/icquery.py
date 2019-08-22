#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций работы с таблицами запросов.

Запрос может использоваться для сохранения результатов в таблицу.
Сохранение в таблицу производиться с помошью метода <to_table>.
"""

# Подключение библиотек
import copy
from . import icsqlalchemydataset

from ic.utils import toolfunc
from ic.utils import resource
from ic.log import log
from ic.utils import txtgen
from ic.engine import glob_functions
from ic.utils import util


import ic.interfaces.icdataclassinterface as icdataclassinterface

__version__ = (0, 1, 4, 1)

# Спецификации
# Результат запроса (словарно-списковое представление)
QUERY_TABLE_RESULT = {'__fields__': (),     # Описание полей - кортеж кортежей
                      '__data__': [],       # Данные - список кортежей
                      }


def getQueryTableFields(Query_):
    """
    Получить описания полей таблицы запроса.
    @param Query_: Имя запроса/dataset объект.
    """
    try:
        if isinstance(Query_, str):
            # Сначала получить dataset
            dataset = icsqlalchemydataset.getDataset(Query_)
        else:
            dataset = Query_
        # Заполнить поля
        fields = []
        for field_name in dataset.getFieldList():
            field_info = dataset.getFieldInfo(field_name)
            fields.append(tuple([field_name,
                                _fieldType.setdefault(field_info['type_val'], 6)]))
        return fields
    except:
        # Вывести сообщение об ошибке в лог
        log.fatal(u'Ошибка получения описаний полей таблицы запроса <%s>.' % str(Query_))
        return None


_fieldType = {'T': 6,   # Код текстового поля
              'I': 0,   # Код целого поля
              'F': 1,   # Код вещественного поля
              }


def getQueryTable(Query_, PostFilter_=None):
    """
    Получить таблицу запроса.
    @param Query_: Имя запроса/dataset объект.
    @param PostFilter_: Дополнительный фильтр для дополнительной фильтрации 
        данных таблицы запроса. Структура такая же как у структурного 
        фильтра Dataset'а.
    @return: Функция возвращает словарь -
            ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ 
            {'__fields__':описания полей таблицы,'__data__':данные таблицы}
    """
    try:
        log.info(u'getQueryTable: НАЧАЛО')
        if isinstance(Query_, str):
            # Сначала получить dataset
            dataset = icsqlalchemydataset.getDataset(Query_)
            dataset.clearChangeRowBuff(-1)
        else:
            dataset = Query_
        
        # Установить буфер на полную таблицу
        dataset.buffAllData() 
        # Заполнить поля
        fields = []
        for field_name in dataset.getFieldList():
            field_info = dataset.getFieldInfo(field_name)
            fields.append(tuple([field_name,
                                _fieldType.setdefault(field_info['type_val'], 6)]))
        # Инициализация данных
        data = []
        # Перейти на первую запись
        dataset.Move()
        while not dataset.IsEOF():
            # Заполнить текущую запись значениями полей
            rec = [dataset.getNameValue(x[0]) for x in fields]
            # Добавить текущую запись в выходную таблицу
            data.append(tuple(rec))
            # Перейти на следующую запись
            dataset.Skip()

        # Корректно освободить буфер
        dataset.clearPageBuff()

        str_print = '|'.join([', '.join([str(f) for f in list(rec)]) for rec in data])
        log.debug(u'getQueryTable: ДО ФИЛЬТРАЦИИ ' + str_print)

        # Дополнительная фильтрация
        if PostFilter_ and isinstance(PostFilter_, dict):
            # Заполниь соответчтвие имен и индексов полей
            field_name2idx = {}
            field_names = [fld[0] for fld in fields]
            for field_name in field_names:
                field_name2idx[field_name] = field_names.index(field_name)
            # Фильтрация
            filter_if_str_lst = ['r[%d]==%s' % (field_name2idx[fld],
                                                toolfunc.getStrInQuotes(PostFilter_[fld])) for fld in PostFilter_.keys()]
            filter_if_str = 'lambda r: '+' and '.join(filter_if_str_lst)
            log.debug(u'getQueryTable PostFilter: ' + filter_if_str)
            filter_if = eval(filter_if_str)
            log.debug(u'getQueryTable PostFilter eval OK' + str(filter_if) + str(field_name2idx))
            data = list(filter(filter_if, data))

        str_print = '|'.join([', '.join([str(f) for f in list(rec)]) for rec in data])
        log.info(u'getQueryTable: КОНЕЦ ' + str_print)
        return {'__fields__': fields, '__data__': data}
    except:
        # Вывести сообщение об ошибке в лог
        log.fatal(u'Ошибка получения таблицы запроса %s.' % str(Query_))
        return None


# --- Спецификаци ---
QUERY_TYPE = 'Query'

SPC_IC_QUERY = {'type': QUERY_TYPE,     # Тип запроса
                'name': 'default',      # Имя запроса

                'sql_txt': None,    # Текст прямого SQL запроса
                'description': '',  # Описание
                'child': [],        # Поля запроса
                'source': None,     # Имя источника данных/БД
                }

# Символы перевода коретки.
# Используются в генераторе SQL выражения
UNIX_CR = '\n'
WIN_CR = '\r\n'


# --- Классы ---
class icQueryPrototype(icdataclassinterface.icDataClassInterface):
    """
    SQL Запрос к источнику данных в табличном представлении.
    """
    
    def __init__(self, Resource_):
        """
        Конструктор.
        @param Resource_: Ресурсное описание запроса.
        """
        icdataclassinterface.icDataClassInterface.__init__(self, Resource_)
        
        self._data_src = Resource_['source']
        self._sql_txt = Resource_['sql_txt']
        
        self.data_source = None

        # Объект управления проектом.
        # Необходим для генерации ресурса таблицы
        self._prj_res_manager = None

    def getDataSource(self):
        """
        Источник данных.
        """
        return self.data_source
        
    def checkOnlineConnect(self):
        """
        Проверка связи с источником данных.
        @return: True - связь установлена / False - связь разорвана по какой либо причине.
        """
        return self.data_source.checkOnline() if self.data_source else False

    def getSQLTxt(self, **kwargs):
        """
        Текст SQL запроса.
        @param kwargs: Параметры SQL запроса для генерации исполняемого текста
            SQL запроса.
        """
        # Необходимо заменить перевод кареток
        sql_txt = self._sql_txt.replace('\\n', UNIX_CR)

        # Сгенерировать запрос для последующего использования
        sql_txt = txtgen.gen(sql_txt, kwargs)

        return sql_txt

    def setSQLTxt(self, SQLTxt_):
        """
        Установить текст SQL запроса.
        """
        self._sql_txt = SQLTxt_
        
    def queryAll(self, **kwargs):
        """
        Выполнить SQL запрос и вернуть результат в виде QUERY_TABLE_RESULT.
        @param kwargs: Параметры SQL запроса для генерации исполняемого текста
            SQL запроса.
        """
        data_src = self.getDataSource()
        if data_src:
            return data_src.executeSQL(self.getSQLTxt(**kwargs))
        return None
        
    def execute(self):
        """
        Выполнить запрос независимо от его конфигурирования.
        """
        recordset = self.fetchAllRecs()
        return recordset
   
    def execSQL(self, **kwargs):
        """
        Выполнить SQL запрос.
        @param kwargs: Параметры SQL запроса для генерации исполняемого текста
            SQL запроса.
        """
        result = None
        data_src = self.getDataSource()
        if data_src:
            cursor = data_src.createCursor()
            sql_txt = self.getSQLTxt(**kwargs)
            try:
                cursor.execute(sql_txt)
            except:
                log.fatal(u'QUERY: Ошибка выполнения запроса <%s>' % sql_txt)
        return result
            
    def closeSQL(self):
        """
        Закрыть SQL запрос.
        """
        data_src = self.getDataSource()
        if data_src:
            data_src.closeCursor()
        
    def fetchAllRecs(self, **kwargs):
        """
        Получить все записи результата запроса.
        @param kwargs: Параметры SQL запроса для генерации исполняемого текста
            SQL запроса.
        @return: Возвращает список словарей записей.
        """
        dataset = tuple()
        data_src = self.getDataSource()
        if data_src:
            sql_txt = self.getSQLTxt(**kwargs)
            try:
                result = data_src.executeSQL(sql_txt)
                records = result.get('__data__', tuple())
                fields = result.get('__fields__', tuple())
                field_names = [field[0] for field in fields]
                dataset = [dict([(fld_name, record[i]) for i, fld_name in enumerate(field_names)]) for record in records]
                return dataset
            except:
                log.fatal(u'QUERY: Ошибка выполнения запроса: %s' % sql_txt)
        return dataset
        
    def fetchOneRec(self, **kwargs):
        """
        Получить одну запись результата запроса.
        @param kwargs: Параметры SQL запроса для генерации исполняемого текста
            SQL запроса.
        @return: Возвращает структуру таблицы результата запроса.
        """
        result = None
        data_src = self.getDataSource()
        if data_src:
            sql_txt = self.getSQLTxt(**kwargs)
            try:
                result = data_src.executeSQLOne(sql_txt)
            except:
                log.fatal(u'QUERY: Ошибка выполнения запроса: %s' % sql_txt)
        return result

    def get_normalized(self, query_result=None):
        """
        Произвести нормализацию результата запроса.
        @param query_result: Абстрактный результат запроса.
        @return: Функция возвращает результат запроса
        представляется в словарно-списковом представлении:
        QUERY_TABLE_RESULT = {'__fields__': (), - Описание полей - кортеж кортежей
                              '__data__': [],   - Данные - список кортежей
                              }
        """
        if query_result is None:
            sql_params = dict([(name, u'') for name in txtgen.get_raplace_names(self._sql_txt)])
            return self.queryAll(**sql_params)
        try:
            # if data and to_dict:
            #    new_data = [dict([(fields[idx][0], val) for idx, val in enumerate(rec)]) for rec in data]
            #    data = new_data
            data = list(query_result)
            if data:
                fields = [(col.name, col.type.name,
                           col.type.length if getattr(col.type, 'length') else 0) for col in query_result]
            else:
                fields = ()
            result = copy.deepcopy({'__fields__': fields, '__data__': data})
            return result
        except:
            log.fatal(u'Ошибка нормализации результата запроса')
        return None

    def getName(self):
        """
        Имя объекта.
        """
        return u'query'

    def _get_prj_res_manager(self, bOpenPrj=True):
        """
        Менеджер управления ресурсами проекта.
        @param bOpenPrj: Автоматически открыть текущий проект?
        """
        if self._prj_res_manager is None:
            self._prj_res_manager = glob_functions.getKernel().getProjectResManager()
            if bOpenPrj:
                self._prj_res_manager.openPrj()
        return self._prj_res_manager

    def _isTableRes(self, tab_resname=None):
        """
        Проверить есть ли ресурсное описание результирующей таблицы.
        @param tab_resname: Имя ресурсного описание результирующей таблицы.
            Если None, тогда имя берется из ресурсного описания этого компонента.
        @return: True - такой ресурс есть / False - ресурса таблицы с таким именем нет.
        """
        if tab_resname is None:
            tab_resname = self.getName()

        prj_res_manager = self._get_prj_res_manager()
        return prj_res_manager.isRes(tab_resname, 'tab')

    def to_table(self, table=None, bReCreateRes=False, bData=True, bClear=False, bTransact=True):
        """
        Преобразовать результат запроса в таблицу.
        В результате работы функции создается ресурс таблицы,
        если он не существует.
        @param table: Таблица.
            Таблица может задаваться именем, паспортом или передаваться в виде объекта.
            Если None, то таблица создается с таким же именем как и запрос.
        @param bReCreateRes: Пересоздать ресурс если он уже существует?
        @param bData: Заполнить таблицу данными автоматически?
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @param bTransact: Сделать сохранение данных одной транзакцией?
        @return: True/False.
        """
        if isinstance(table, str) or table is None:
            return self._to_table_by_name(table, bReCreateRes=bReCreateRes, bData=bData,
                                          bClear=bClear, bTransact=bTransact)
        elif toolfunc.is_pasport(table):
            kernel = glob_functions.getKernel()
            tab = kernel.Create(passport=table)
            return self._to_table(tab, bReCreateRes=bReCreateRes, bData=bData,
                                  bClear=bClear, bTransact=bTransact)
        return self._to_table(table, bReCreateRes=bReCreateRes, bData=bData,
                              bClear=bClear, bTransact=bTransact)

    def _to_table(self, table, bReCreateRes=False, bData=True, bClear=False, bTransact=True):
        """
        Преобразовать результат запроса в таблицу.
        В результате работы функции создается ресурс таблицы,
        если он не существует.
        @param table: Таблица.
        @param bReCreateRes: Пересоздать ресурс если он уже существует?
        @param bData: Заполнить таблицу данными автоматически?
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @param bTransact: Сделать сохранение данных одной транзакцией?
        @return: True/False.
        """
        if table is None:
            log.warning(u'Не определен объект таблицы для заполнения результатом выполнения запроса <%s>' % self.getName())
            return None

        result = False
        if bReCreateRes:
            table_name = table.getName()
            # Если необходимо пересоздать ресурс,
            # то сначала удаляем его а затем вновь создаем
            prj_res_manager = self._get_prj_res_manager()
            prj_res_manager.delRes(table_name, 'tab')

            # Создаем ресурс заново
            result = self.createTableResource(table_name=table_name)

            # Проверяем есть ли ресурс таблицы для выгрузки
            # Если его нет то выгрузка не возможна
            if not self._isTableRes(table_name):
                log.warning(u'Ресурс таблицы <%s> не найден' % table_name)
                log.warning(u'Выгрузка результатов запроса <%s> в таблицу не возможна' % self.getName())
                return False

        if bData:
            data = self.execute()
            # Заполнить таблицу данными
            result = self.saveData(table, dataset=data, bClear=bClear, bTransact=bTransact)

        return result

    def _to_table_by_name(self, table_name=None, bReCreateRes=False, bData=True, bClear=False, bTransact=True):
        """
        Преобразовать результат запроса в таблицу.
        В результате работы функции создается ресурс таблицы,
        если он не существует.
        @param table_name: Имя таблицы.
            Если None, то таблица создается с таким же именем как и запрос.
        @param bReCreateRes: Пересоздать ресурс если он уже существует?
        @param bData: Заполнить таблицу данными автоматически?
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @param bTransact: Сделать сохранение данных одной транзакцией?
        @return: True/False.
        """
        if table_name is None:
            table_name = self.getName()

        result = False
        if bReCreateRes:
            # Если необходимо пересоздать ресурс,
            # то сначала удаляем его а затем вновь создаем
            prj_res_manager = self._get_prj_res_manager()
            prj_res_manager.delRes(table_name, 'tab')

            # Создаем ресурс заново
            result = self.createTableResource(table_name=table_name)

        # Проверяем есть ли ресурс таблицы для выгрузки
        # Если его нет то выгрузка не возможна
        if not self._isTableRes(table_name):
            log.warning(u'Ресурс таблицы <%s> не найден' % table_name)
            log.warning(u'Выгрузка результатов запроса <%s> в таблицу не возможна' % self.getName())
            return False

        if bData:
            data = self.execute()
            # Заполнить таблицу данными
            result = self.saveData(table_name, dataset=data, bClear=bClear, bTransact=bTransact)

        return result

    def createTableResource(self, table_name=None):
        """
        Построить ресурсное описание по этому компоненту.
        @return: True - ресурс таблицы создан / False - ресур таблицы не создан.
        """
        if table_name is None:
            table_name = self.getName()
            
        if not self._isTableRes(table_name):
            log.warning(u'ВНИМАНИЕ! Создается ресурс таблицы <%s>' % table_name)
            tab_res = self._createTabSpc()

            children_fld = self._getFields()
            for child_fld in children_fld:
                fld_spc = self._createFieldSpc(**child_fld)
                tab_res['child'].append(fld_spc)

            return self._saveTabRes(tab_res)
        return False

    def _saveTabRes(self, tab_res):
        """
        Сохранить ресурс результирующей таблицы.
        @param tab_res: Сгенерированный ресурс таблицы.
        @return: True/False.
        """
        table_name = tab_res['name']
        # Сохранить ресурс
        prj_res_manager = self._get_prj_res_manager()
        prj_res_manager.saveRes(table_name, 'tab', tab_res)

        # И сразу удалить за ненадобностью
        self._prj_res_manager = None
        return True

    def _getFields(self):
        """
        Описание дочерних полей.
        """
        query_result = self.fetchOneRec()
        # rec_dict = self.get_normalized(record)

        return [dict(name=field[0], type_val=field[1], length=field[2]) for field in query_result['__fields__']]

    def _createTabSpc(self, table_name=None):
        """
        Создать спецификацию результирующей таблицы.
        @param table_name: Имя результирующей таблицы.
        """
        from ic.components.user import ic_tab_wrp
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)

        # Установить свойства таблицы
        if table_name is None:
            table_name = self.getName()
        tab_spc['name'] = table_name
        tab_spc['description'] = self.resource['description']
        tab_spc['table'] = table_name
        tab_spc['source'] = self._data_src

        return tab_spc

    def _createFieldSpc(self, name, type_val='T', length=0, default=None):
        """
        Создать спецификацию поля результирующей таблицы из поля конвертации.
        @param name: Имя поля.
        @param type_val: Тип значения поля.
        @param length: Длина поля.
        @param default: Значение по умолчанию.
        """
        from ic.components.user import ic_field_wrp
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        field_spc['name'] = name
        field_spc['description'] = name
        # field_spc['field'] = ConvertFieldSpc_['field']
        field_spc['type_val'] = type_val
        field_spc['len'] = length
        # field_spc['attr'] = ConvertFieldSpc_['attr']
        field_spc['default'] = default

        return field_spc

    def saveData(self, table=None, dataset=(), bClear=False, bTransact=True):
        """
        Сохранить результат запроса в таблице.
        @param table: Таблица.
            Таблица может задаваться именем, паспортом или передаваться в виде объекта.
        @param dataset: Набор записей-результата запроса.
            Список словарей.
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @param bTransact: Сделать сохранение данных одной транзакцией?
        @return: True/False.
        """
        if table is None:
            table = self.getName()

        if isinstance(table, str):
            # Таблица задается именем
            kernel = glob_functions.getKernel()
            table = kernel.createObjByRes(table, table, 'tab')
        elif toolfunc.is_pasport(table):
            # Таблица задается паспортом
            kernel = glob_functions.getKernel()
            table = kernel.Create(table)
        else:
            # Таблица задается объектом
            pass

        if table is None:
            log.warning(u'Не определена таблица для сохранения данных запроса <%s>' % self.getName())
            return False

        try:
            if bTransact:
                return self._saveDataTransact(table=table, dataset=dataset, bClear=bClear)
            return self._saveData(table=table, dataset=dataset, bClear=bClear)
        except:
            log.fatal(u'Ошибка сохранения данных запроса <%s> в таблице <%s>' % (self.getName(), table_name))
        return False

    def _saveData(self, table=None, dataset=(), bClear=False):
        """
        Сохранить результат запроса в таблице.
        @param table: Таблица.
        @param dataset: Набор записей-результата запроса.
            Список словарей.
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @return: True/False.
        """
        # Очистить данные таблицы
        if bClear:
            table.clear()

        # Заполнить таблицу данными
        for record in dataset:
            # log.debug(u'Добавление записи %s в таблицу <%s>' % (str(record), table_name))
            table.add(**record)

        return True

    def _saveDataTransact(self, table=None, dataset=(), bClear=False):
        """
        Сохранить результат запроса в таблице.
        ВНИМАНИЕ! Сохранение производим одной транзакцией.
        @param table: Таблица.
        @param dataset: Набор записей-результата запроса.
            Список словарей.
        @param bClear: Произвести предварительную очистку данных при заполнении?
        @return: True/False.
        """
        transaction = table.db.session(autoflush=False, autocommit=False)
        try:
            # Очистить данные таблицы
            if bClear:
                table.clear(transaction=transaction)

            # Заполнить таблицу данными
            for record in dataset:
                # log.debug(u'Добавление записи %s в таблицу <%s>' % (str(record), table_name))
                table.add_rec_transact(rec=record, transaction=transaction)

            # --- Закончить транзакцию ---
            transaction.commit()
            log.debug(u'Заполнения таблицы <%s> результатом запроса <%s> завершено' % (table.getName(), self.getName()))

            return True
        except:
            # Вернуть транзакцию
            transaction.rollback()
            log.fatal(u'Ошибка заполнения таблицы <%s> результатом запроса <%s>' % (table_name, self.getName()))
        return False


class icNamedQueryPrototype(icQueryPrototype):
    """
    Именованный запрос (Создание объекта по имени).
    """

    def __init__(self, QueryName_):
        """
        Конструктор.
        @param QueryName_: Имя запроса.
        """
        icQueryPrototype.__init__(self,
                                  resource.icGetRes(QueryName_, 'mtd',
                                                    nameRes=QueryName_))
