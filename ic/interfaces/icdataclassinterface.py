#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс классов данных системы.
"""

from ic.log import log


__version__ = (0, 0, 2, 3)


class icDataClassInterface:
    """
    Интерфейс классов данных системы.
    """
    def __init__(self, TabRes_=None):
        """
        Конструктор.
        @param TabRes_: Ресурс таблицы.
        """
        self.res = TabRes_
        #   Указатель на класс провайдера
        self._class = None

    def getResource(self):
        """
        Ресурс.
        """
        return self.res
            
    def getConnection(self):
        """
        Возвращает объект соединения с базой данных, который поддерживает DB API 2.0. Внутренний
        счетчик пользователей увеличивается на 1. После использования объекта надо вызвать функцию
        releaseConnection - счетчик пользователей уменьшится на 1.
        """
        pass
        
    def releaseConnection(self):
        """
        Уменьшает счетчик пользователей соединения на 1. Когда кольчеств пользователей <= 0. Соединение может
        быть безопасно уничтожено.
        """
        pass
        
    def getProvider(self):
        """
        Возвращает указатель на класс данных, который реально работает с базой данных
        (Например класс, наследованный от SQLObject).
        """
        return self._class
        
    def getClassName(self):
        """
        Возвращает имя класса данных.
        """
        pass
        
    def delete(self, id):
        """
        Удаления объекта класса данных.
        
        @type id: C{int}
        @param id: Идентификатор объекта.
        """
        pass
        
    def add(self, *args, **kwargs):
        """
        Добавить объект.
        """
        pass
        
    def update(self, *args, **kwargs):
        """
        Изменить объект.
        """
        pass
        
    def get(self, id):
        """
        Получить объект.
        """
        pass

    def select(self, *args, **kwargs):
        """
        Выбрать список объектов из класса данных.
        @return: Возвражает объект SelectResults.
        """
        pass
        
    def queryAll(self, *args, **kwargs):
        """
        Выполнить запрос класса данных.
        @return: Возвращает список кортежей.
        """
        pass
        
    def queryRecs(self, SQLQuery_):
        """
        Выполнить запрос класса данных.
        @param SQLQuery_: Строка запроса.
        @return: Возвражает список объектов icSQLRecord.
        """
        pass
        
    def txtClassToDB(self, text):
        """
        Функция конвертации имен полей из предствления класса в представление базы данных.
        """
        pass

    def txtDBToClass(self, text):
        """
        Функция конвертации имен полей из предствления класса в представление базы данных.
        """
        pass
        
    def convQueryToSQL(self, text):
        """
        Конвертация запроса в терминах класса в SQL запрос.
        """
        pass

    def Lock(self):
        """
        Блокирует таблицу.
        """
        pass
        
    def unLock(self):
        """
        Разблокирует таблицу.
        """
        pass
        
    def LockObject(self, id):
        """
        Блокировка изменения объекта.
        """
        pass
        
    def unLockObject(self, id):
        """
        Разблокирует объект.
        """
        pass
        
    def IsLock(self):
        """
        Возвращает признак блокировки класса данных.
        """
        pass
        
    def IsLockObject(self, id):
        """
        Возвращает признак блокировки объекта класса данных.
        """
        pass

    def clear(self):
        """
        Очистить таблицу.
        """
        pass

    def get_normalized(self, query_result=None):
        """
        Произвести нормализацию результата запроса.
        @param query_result: Абстрактный результат запроса.
        @return: Функция возвращает результат запроса
        представляется в словарно-списковом представлении:
            {'__fields__': (), - Описание полей - кортеж кортежей
             '__data__': [],   - Данные - список кортежей
            }
        """
        return None

    def find_record(self, normal_data=None, field_name=None, value=None):
        """
        Поиск записи в нормализованных данных по значению поля
        @param normal_data: Нормализованные данные
            в словарно-списковом представлении:
            {'__fields__': (), - Описание полей - кортеж кортежей
             '__data__': [],   - Данные - список кортежей
            }
        @param field_name: Наименование поля по которому происходит поиск.
        @param value: Искомое значение.
        @return: Словарь записи в формате:
            { 'имя поля': значение поля, ...}
            или None если запись не найдена.
        """
        if normal_data is None:
            normal_data = self.get_normalized()

        if normal_data:
            try:
                field_names = [field[0] for field in normal_data.get('__fields__', [])]
                field_idx = field_names.index(field_name)
                find_record = None
                for rec in normal_data.get('__data__', []):
                    if rec[field_idx] == value:
                        find_record = dict([(fld_name, rec[i]) for i, fld_name in enumerate(field_names)])
                        break
                return find_record
            except:
                log.fatal(u'Ошибка поиска записи по значению поля <%s> : <%s>' % (field_name, str(value)))
        else:
            log.warning(u'Не определены данные табличного объекта для поиска записи по значению поля <%s> : <%s>' % (field_name, str(value)))
        return None

    def get_record_dict(self, normal_data=None, record=None):
        """
        Преобразовать строковую запись в запись в виде словаря.
        @param normal_data: Нормализованные данные
            в словарно-списковом представлении:
            {'__fields__': (), - Описание полей - кортеж кортежей
             '__data__': [],   - Данные - список кортежей
            }
        @param record: Запись в виде списка или кортежа.
        @return: Словарь записи в формате:
            { 'имя поля': значение поля, ...}
            или None если запись не найдена.
        """
        field_names = [field[0] for field in normal_data.get('__fields__', [])]
        rec_count = len(record)
        record_dict = dict([(fld_name, record[i] if i < rec_count else None) for i, fld_name in enumerate(field_names)])
        return record_dict

    def get_recordset_dict(self, normal_data=None):
        """
        Преобразовать табличные данные в список словарей.
        @param normal_data: Нормализованные данные
            в словарно-списковом представлении:
            {'__fields__': (), - Описание полей - кортеж кортежей
             '__data__': [],   - Данные - список кортежей
            }
        @return: Список словарей записей.
            Словарь записи в формате:
            { 'имя поля': значение поля, ...}
            или None если запись не найдена.
        """
        if normal_data is None:
            normal_data = self.get_normalized()

        recordset = list()
        field_names = [field[0] for field in normal_data.get('__fields__', [])]
        for rec in normal_data.get('__data__', []):
            rec_count = len(rec)
            record_dict = dict([(fld_name, rec[i] if i < rec_count else None) for i, fld_name in enumerate(field_names)])
            recordset.append(record_dict)
        return recordset

    def set_recordset_dict(self, normal_data=None, recordset=None):
        """
        И обратная операция
        Преобразовать список словарей в табличные данные.
        @param normal_data: Нормализованные данные
            в словарно-списковом представлении:
            {'__fields__': (), - Описание полей - кортеж кортежей
             '__data__': [],   - Данные - список кортежей
            }
        @param recordset: Список словарей записей.
            Словарь записи в формате:
            { 'имя поля': значение поля, ...}
            или None если запись не найдена.
        @return: Заполненнные нормализованные данные.
        """
        if normal_data is None:
            normal_data = self.get_normalized()

        if recordset is None:
            # Нечего преобразовывать
            log.warning(u'Не определен рекорсет')
            return normal_data

        field_names = [field[0] for field in normal_data.get('__fields__', [])]

        data = list()
        for record_dict in recordset:
            rec = [record_dict.get(field_name, None) for field_name in field_names]
            data.append(rec)
        normal_data['__data__'] = data
        return normal_data
