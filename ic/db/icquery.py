#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций работы с таблицами запросов. 
"""

# Подключение библиотек
import copy
from . import icsqlalchemydataset

import ic.utils.ic_util
from ic.utils import resource
from ic.log import log
from ic.utils import txtgen
from ic.utils import ic_str

import ic.interfaces.icdataclassinterface as icdataclassinterface

__version__ = (0, 0, 2, 3)

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
        if type(Query_) in (str, unicode):
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
        if type(Query_) in (str, unicode):
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
                                 ic.utils.ic_util.getStrInQuotes(PostFilter_[fld])) for fld in PostFilter_.keys()]
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

    def getDataSource(self):
        """
        Источник данных.
        """
        return self.data_source
        
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
        @return: Возвращает список кортежей.
        """
        result = None
        data_src = self.getDataSource()
        if data_src:
            cursor = data_src.createCursor()
            sql_txt = self.getSQLTxt(**kwargs)
            try:
                cursor.execute(sql_txt)
                result = cursor.fetchall()
            except:
                log.fatal(u'QUERY: Ошибка выполнения запроса: %s' % sql_txt)
            data_src.closeCursor()
        return result
        
    def fetchOneRec(self):
        """
        Получить одну запись результата запроса.
        @return: Возвращает кортеж значений.
        """
        result = None
        data_src = self.getDataSource()
        if data_src:
            cursor = data_src.getCursor()
            if cursor:
                result = cursor.fetchone()
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
            #    new_data = [dict([(fields[i][0], val) for i, val in enumerate(rec)]) for rec in data]
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
