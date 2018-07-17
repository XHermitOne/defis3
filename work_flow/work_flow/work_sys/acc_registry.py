#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль реализации регистра накопления.
"""

import uuid
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# from services.ic_std.log import log
from ic.log import log

__version__ = (0, 0, 1, 31)


# Имя таблицы движения по умолчанию
DEFAULT_OPERATIONS_TABLE = 'operations'
# Имя таблицы итогов по умолчанию
DEFAULT_RESULT_TABLE = 'result'

# Параметры подключения к БД
DB_HOST = '10.0.0.3'
DB_PORT = 5432
DB_USER = 'xhermit'
DB_PASSWORD = 'xhermit'
DB_NAME = 'testing'

DEFAULT_DB_URL = 'postgres://%s:%s@%s:%d/%s' % (DB_USER, DB_PASSWORD,
                                                DB_HOST, DB_PORT, DB_NAME)

SQL_ROLLBACK = 'ROLLBACK'

# Типы реквизитов
INTEGER_REQUISITE_TYPE = 'int'
FLOAT_REQUISITE_TYPE = 'float'
TEXT_REQUISITE_TYPE = 'text'
DT_REQUISITE_TYPE = 'datetime'

# Коды операций движения
# Приход
RECEIPT_OPERATION_CODE = '+'
# Расход
EXPENSE_OPERATION_CODE = '-'

# Имена полей таблицы движения
CODE_OPERATION_FIELD = 'code'       # Поле кода операции
DT_OPERATION_FIELD = 'dt_oper'      # Поле даты-времени выполнения операции
OWNER_OPERATION_FIELD = 'owner'     # Поле идентификатора владельца операции


class icAccRegistry(object):
    """
    Класс регистра накопления.
    Общий вид работы регистра накопления:

    Событие 1-----+
    Событие 2---+ |
    Событие 3-+ | |
              | | |
    +---------| | |-------------------------+
    |         V V V   Регистр накопления    |
    | +===============+                     |
    | | Учет движений |                     |
    | +===============+                     |
    |       |                               |
    |       V                               |
    | +===============+                     |
    | | Учет итогов   |                     |
    | +===============+                     |
    +---------------------------------------+

    В  состав  регистра  накопления  как  объекта  входят  измерения и ресурсы.
    Ресурсы используются для хранения информации как о приращениях, так
    и о самих значениях показателей. По сути, каждый ресурс хранит данные
    одного показателя. Однако регистры могут быть не только одномерными.
    В  регистрах  накопления  разрезы  учета  реализуются  с  помощью
    измерений.
    В  состав  регистра  можно  включить  более  одного  измерения.
    В таблице операций движения присутствуют дополнительные поля:
    1. Код операции - <+> (приход) и <-> (расход)
    2. Дата-время выполнение операции (заполняется автоматически)
    3. Владелец операции - текстовое поле.
    В него можно писать номер документа или UUID
    какого-то объекта инициируемого операцию.
    """

    def __init__(self, db_url=None,
                 operation_table_name=DEFAULT_OPERATIONS_TABLE,
                 result_table_name=DEFAULT_RESULT_TABLE):
        """
        Конструктор.
        @param db_url: Параметры подключения к БД.
        @param operation_table_name: Имя таблицы движений.
        @param result_table_name: Имя итоговой таблицы.
        """
        self._db_url = DEFAULT_DB_URL if db_url is None else db_url
        self._connection = None

        self._operation_table_name = operation_table_name
        self._operation_table = None
        self._result_table_name = result_table_name
        self._result_table = None

        # Описания реквизитов регистра
        # Ресурсные реквизиты
        self._resource_requisites = list()
        # Реквизиты измерения
        self._dimension_requisites = list()

        # Дополнительные реквизиты
        # (просто присутствуют в итоговой таблице
        # и не учавствуют в таблице операций движения)
        self._extended_requisites = list()

    def get_operation_table(self):
        """
        Таблица sqlalchemy операций движения.
        """
        if not self.is_connected():
            self.connect()

        if self._operation_table is None:
            self.create_operation_table()
        return self._operation_table

    def get_result_table(self):
        """
        Таблица sqlalchemy итогов.
        """
        if not self.is_connected():
            self.connect()

        if self._result_table is None:
            self.create_result_table()
        return self._result_table

    def is_connected(self):
        """
        Установлена связь с БД?
        @return: True/False
        """
        return self._connection is not None

    def connect(self, db_url=None):
        """
        Установить связь с БД.
        @param db_url: URL связи с БД.
        @return: Объект связи с БД.
        """
        if db_url is None:
            db_url = self._db_url

        if self._connection:
            self.disconnect()

        self._connection = sqlalchemy.create_engine(db_url, echo=False)
        log.info(u'Установлена связь с БД <%s>' % db_url)
        return self._connection

    def disconnect(self):
        """
        Разорвать связь с БД.
        @return: True/False.
        """
        if self._connection:
            self._connection.dispose()
            self._connection = None
        return True

    def get_connection(self, auto_connect=True):
        """
        Объект связи с БД.
        @param auto_connect: Если не установлена связь,
            произвести автоматический коннект?
        """
        if self._connection is None and auto_connect:
            self.connect()
        return self._connection

    def sql_execute(self, connection=None, sql='', *args):
        """
        Выполнить SQL выражение.
        @connection: Объект связи с БД.
        @param sql: Текстовый формат SQL выражения.
        @param args: Параметры SQL выражения.
        @return: Рекордсет.
        """
        if connection is None:
            connection = self._connection

        result = None
        try:
            sql_txt = sql % args
        except TypeError:
            log.fatal(u'Ошибка формирования SQL выражения.')
            raise

        try:
            result = connection.execute(sql_txt)
        except:
            connection.execute(SQL_ROLLBACK)
            log.fatal(u'Ошибка выполнения SQL: %s' % sql_txt)
            raise
        return result

    def append_resource_requisite(self, requisite_name, requisite_type):
        """
        Добавление ресурса.
        @param requisite_name: Имя реквизита.
        @param requisite_type: Тип реквизита.
            Тип ресурсного реквизита
            м.б. только или целый ('int') или вещественный ('float').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._resource_requisites.append(requisite)

    def get_resource_requisite_names(self):
        """
        Имена реквизитов ресурсов.
        @return: Список имен реквизитов ресурсов.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._resource_requisites]
        return names

    def append_dimension_requisite(self, requisite_name, requisite_type):
        """
        Добавление измерения.
        @param requisite_name: Имя реквизита.
        @param requisite_type: Тип реквизита.
            Тип реквизита измерения
            м.б. только целый ('int'), дата-время('datetime')
            или текстовый ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._dimension_requisites.append(requisite)

    def get_dimension_requisite_names(self):
        """
        Имена реквизитов измерений.
        @return: Список имен реквизитов измерений.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._dimension_requisites]
        return names

    def append_extended_requisite(self, requisite_name, requisite_type):
        """
        Добавление дополнительного реквизита.
        @param requisite_name: Имя реквизита.
        @param requisite_type: Тип реквизита.
            Тип реквизита дополнительного реквизита
            м.б. целый ('int'), вещественный ('float'),
            дата-время('datetime') или текстовый ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._extended_requisites.append(requisite)

    def get_extended_requisite_names(self):
        """
        Имена дополнительных реквизитов.
        @return: Список имен дополнительных реквизитов.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._extended_requisites]
        return names

    def gen_column(self, requisite_name, requisite_type):
        """
        Генерация объекта колонки по описанию реквизита.
        @param requisite_name: Имя реквизита.
        @param requisite_type: Тип реквизита.
        @return: Объект колонки sqlalchemy или None в
            случае ошибки.
        """
        # Привести все имена к нижнему регистру
        requisite_name = requisite_name.strip().lower()
        requisite_type = requisite_type.strip().lower()
        column_type = sqlalchemy.UnicodeText
        if requisite_type == INTEGER_REQUISITE_TYPE:
            column_type = sqlalchemy.Integer
        elif requisite_type == FLOAT_REQUISITE_TYPE:
            column_type = sqlalchemy.Float
        elif requisite_type == TEXT_REQUISITE_TYPE:
            column_type = sqlalchemy.UnicodeText
        elif requisite_type == DT_REQUISITE_TYPE:
            column_type = sqlalchemy.DateTime

        column = sqlalchemy.Column(requisite_name, column_type)
        return column

    def gen_table(self, table_name, requisites):
        """
        Генерация объекта таблицы по описанию реквизитов.
        @param table_name: Имя таблицы.
        @param requisites: Список описаний реквизитов.
        @return: Объект таблицы sqlalchemy или None
            в случае ошибки.
        """
        metadata = sqlalchemy.MetaData(self._connection)
        # log.debug(u'gen_table <%s>' % requisites)
        columns = [self.gen_column(**requisite) for requisite in requisites]
        table = sqlalchemy.Table(table_name, metadata, *columns)
        return table

    def _get_operation_requisites(self):
        """
        Список реквизитов-полей таблицы движения
        @return: Список словарей описания полей:
            [{'requisite_name': <Имя поля>,
            'requisite_type': <Тип поля>}, ...]
        """
        code_requisite = dict(requisite_name=CODE_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)

        dt_requisite = dict(requisite_name=DT_OPERATION_FIELD,
                            requisite_type=DT_REQUISITE_TYPE)
        owner_requisite = dict(requisite_name=OWNER_OPERATION_FIELD,
                               requisite_type=TEXT_REQUISITE_TYPE)
        requisites = [code_requisite, dt_requisite,
                      owner_requisite] + self._dimension_requisites + self._resource_requisites
        return requisites

    def create_operation_table(self, operation_table_name=None):
        """
        Создание таблицы движений.
        ВНИМАНИЕ!
        Для таблицы движения надо завести поле кода операции.
        В это поле по сути пишеться только '+' или '-'
        '+' - это операция прихода.
        '-' - это операция расхода.
        А также поле даты-времени операции.
        @param operation_table_name: Имя таблицы движений.
        @return: Объект таблицы движений или None в случае ошибки.
        """
        if operation_table_name is None:
            operation_table_name = self._operation_table_name

        requisites = self._get_operation_requisites()
        self._operation_table = self.gen_table(operation_table_name, requisites)
        self._operation_table.create(checkfirst=True)
        return self._operation_table

    def _get_result_requisites(self):
        """
        Список реквизитов-полей итоговой таблицы.
        @return: Список словарей описания полей:
            [{'requisite_name': <Имя поля>,
            'requisite_type': <Тип поля>}, ...]
        """
        requisites = self._dimension_requisites + self._resource_requisites + self._extended_requisites
        return requisites

    def create_result_table(self, result_table_name=None):
        """
        Создание таблицы итогов.
        @param result_table_name: Имя итоговой таблицы.
        @return: Объект итоговой таблицы или None в случае ошибки.
        """
        if result_table_name is None:
            result_table_name = self._result_table_name

        requisites = self._get_result_requisites()
        self._result_table = self.gen_table(result_table_name, requisites)
        self._result_table.create(checkfirst=True)
        return self._result_table

    def is_receipt(self, **requisite_values):
        """
        Определить по значениям реквизитов какую операция
        осуществляется. Приход?
        @param requisite_values: Значения реквизитов.
        @return: True - приход. False - нет.
        """
        code = requisite_values.get(CODE_OPERATION_FIELD, None)
        return code == RECEIPT_OPERATION_CODE

    def is_expense(self, **requisite_values):
        """
        Определить по значениям реквизитов какую операция
        осуществляется. Расход?
        @param requisite_values: Значения реквизитов.
        @return: True - расход. False - нет.
        """
        code = requisite_values.get(CODE_OPERATION_FIELD, None)
        return code == EXPENSE_OPERATION_CODE

    def _is_uuid_field(self, table):
        """
        Проверить есть ли в таблице поле UUID.
        Это сделано потому что итоговая таблица м.б. таблица
        бизнес объекта. И при добавлении нового бизнесс объекта
        в таком случае необходимо инициализировать его уникальный
        идентификатор.
        @param table: Объект таблицы sqlalchemy.
        @return: True/False.
        """
        mapper = sqlalchemy.inspect(table)
        column_names = mapper.columns.keys()
        return 'uuid' in column_names

    def _do_operation(self, transaction,
                      operation_table, result_table,
                      requisite_values):
        """
        Выполнение операции движения. Внутреняя функция.
        @param transaction: Объект транзакции-сессии (sqlalchemy).
        @param operation_table: Объект таблицы операций движения (sqlalchemy).
        @param result_table: Объект итоговой таблицы (sqlalchemy).
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Дополнительные реквизиты (нужны только для итоговой таблицы)
        extended_requisite_names = self.get_extended_requisite_names()
        extended_requisites = dict([(name, requisite_values[name]) for name in extended_requisite_names if name in requisite_values])

        # Проверить есть ли в итоговой таблице запись
        # в соответствии с измерениями
        dimension_requisite_names = self.get_dimension_requisite_names()
        dimension_requisites = dict([(name, value) for name, value in requisite_values.items() if name in dimension_requisite_names])
        where = [getattr(result_table.c, name) == value for name, value in dimension_requisites.items()]
        find = result_table.select(sqlalchemy.and_(*where)).execute()
        if not find.rowcount:
            # Если такой записи нет, то создать ее
            resource_requisite_names = self.get_resource_requisite_names()
            resource_requisites = dict([(name, 0) for name in resource_requisite_names])
            requisites = dict()
            requisites.update(dimension_requisites)
            requisites.update(resource_requisites)
            requisites.update(extended_requisites)

            sql = result_table.insert().values(**requisites)
            transaction.execute(sql)

        # Обновить значения ресурсных реквизитов
        resource_requisite_names = self.get_resource_requisite_names()
        if self.is_receipt(**requisite_values):
            # Если операция прихода, то складываем
            resource_requisites = dict([(name, getattr(result_table.c, name)+requisite_values.get(name, 0)) for name in resource_requisite_names])
        elif self.is_expense(**requisite_values):
            # Если операция расхода, то отнимаем
            resource_requisites = dict([(name, getattr(result_table.c, name)-requisite_values.get(name, 0)) for name in resource_requisite_names])
        else:
            # Тип операции не поддерживается
            log.warning(u'Операция движения <%s> не поддерживается системой' % requisite_values.get(CODE_OPERATION_FIELD, None))
            transaction.rollback()
            return False

        requisites = dict()
        requisites.update(resource_requisites)
        requisites.update(extended_requisites)
        sql = result_table.update().where(sqlalchemy.and_(*where)).values(**requisites)
        transaction.execute(sql)

        # Взять только необходимые входные данные
        operation_requisite_values = self._get_operation_requisite_values(**requisite_values)
        # После того как поменяли значения в итоговой таблице
        # добавляем операцию в таблицу движения
        # Надо не забыть добавить поле даты-времени выполнения операции движения
        operation_requisite_values[DT_OPERATION_FIELD] = datetime.datetime.now()
        sql = operation_table.insert().values(**operation_requisite_values)
        transaction.execute(sql)
        return True

    def _get_operation_requisite_values(self, **requisite_values):
        """
        Отфильтровать только небходимые значения реквизитов
        для таблицы операций движения.
        @param requisite_values: Значения реквизитов.
        @return: Список реквизитов используемых в регистре.
        """
        used_requisite_names = [CODE_OPERATION_FIELD,
                                DT_OPERATION_FIELD,
                                OWNER_OPERATION_FIELD] + \
                               [requisite['requisite_name'] for requisite in self._dimension_requisites] + \
                               [requisite['requisite_name'] for requisite in self._resource_requisites]
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def _get_result_requisite_values(self, **requisite_values):
        """
        Отфильтровать только небходимые значения реквизитов
        для таблицы итогов.
        @param requisite_values: Значения реквизитов.
        @return: Список реквизитов используемых в регистре.
        """
        used_requisite_names = [requisite['requisite_name'] for requisite in self._dimension_requisites] + \
                               [requisite['requisite_name'] for requisite in self._resource_requisites] + \
                               [requisite['requisite_name'] for requisite in self._extended_requisites]
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def do_operation(self, **requisite_values):
        """
        Выполнение операции движения.
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        result_table = self.create_result_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = self._do_operation(transaction,
                                        operation_table, result_table,
                                        requisite_values)
            if result:
                # Закрытие транзакции
                transaction.commit()
            return result
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка выполнения операции движения <%s>' % requisite_values)
        return False

    def undo_operation(self, **requisite_values):
        """
        Отмена выполнения операции движения.
        @param requisite_values: Значения реквизитов.
        @return: True - Отмена операции прошла успешно.
            False - Отмена операции не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        result_table = self.create_result_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            # Найти операцию, соответствующую указанным реквизитам
            where = [getattr(operation_table.c, name) == value for name, value in requisite_values.items()]
            # ВНИМАНИЕ!
            # Здесь необходимо сделать ORDER_BY DESC по полю dt_oper
            # чтобы отмена операций производилась в строго обратном
            # хронологическом порядке
            find = operation_table.select().where(sqlalchemy.and_(*where)).order_by(operation_table.c.dt_oper.desc()).execute()
            if find.rowcount:
                # Есть такая операция движения
                for operation in find:
                    operation_code = operation[CODE_OPERATION_FIELD]
                    if operation_code == RECEIPT_OPERATION_CODE:
                        # Это приход, значит надо отнять из итоговой таблицы
                        log.debug(u'Вычитание из итоговой таблицы')
                        resource_requisite_names = self.get_resource_requisite_names()
                        resource_requisites = dict([(name, getattr(result_table.c, name)-operation[name]) for name in resource_requisite_names])
                        # Словарь значений рекзизитов для добавления позиции
                        init_resource_requisites = dict([(name, -operation[name]) for name in resource_requisite_names])
                    elif operation_code == EXPENSE_OPERATION_CODE:
                        # Это расход, значит надо прибавить в итоговой таблице
                        log.debug(u'Сложение в итоговой таблице')
                        resource_requisite_names = self.get_resource_requisite_names()
                        resource_requisites = dict([(name, getattr(result_table.c, name)+operation[name]) for name in resource_requisite_names])
                        # Словарь значений рекзизитов для добавления позиции
                        init_resource_requisites = dict([(name, operation[name]) for name in resource_requisite_names])
                    else:
                        # Не поддерживаемый тип операции движения
                        log.warning(u'Не поддерживаемый тип <%s> операции движения' % operation_code)
                        transaction.rollback()
                        return False

                    # Сделать обновление в итоговой таблице
                    dimension_requisite_names = self.get_dimension_requisite_names()
                    operation_values = dict(operation)
                    dimension_requisites = dict([(name, value) for name, value in operation_values.items() if name in dimension_requisite_names])
                    where = [getattr(result_table.c, name) == value for name, value in dimension_requisites.items()]
                    # Если не определена условие поиска в итоговой таблице,
                    # то нет возможности сделать обновление в итоговой таблице
                    if where:
                        # Есть условие поиска в итоговой таблице
                        log.debug(u'Выполнение отмены операции %s в итоговой таблице' % dimension_requisites)
                        # ВНИМАНИЕ! Если есть такая позиция, то сделать update
                        # если нет такой позиции то сделать insert
                        # т.к. значение из итоговой таблицы м.б. удалено
                        # При проверке на существование записи исполльзуется
                        # проверка на первую запись <first()>. Если возвращаемый рекордсет
                        # пустой, то функция возвращает None.
                        # В данном случае необходимо сначала выполнить <execute()>
                        # Получить ResultProxy и у него уже вызывать first()
                        if result_table.select().where(sqlalchemy.and_(*where)).execute().first() is not None:
                            sql = result_table.update().where(sqlalchemy.and_(*where)).values(**resource_requisites)
                            transaction.execute(sql)
                        else:
                            try:
                                requisites = dict()
                                requisites.update(init_resource_requisites)
                                requisites.update(dimension_requisites)
                                extended_requisite_names = self.get_extended_requisite_names()
                                extended_requisites = dict(
                                    [(name, value) for name, value in operation_values.items() if
                                     name in extended_requisite_names])
                                requisites.update(extended_requisites)
                                log.debug(u'Отмена операции. Добавление позиции в итоговую таблицу %s' % requisites)
                                sql = result_table.insert().values(**requisites)
                                transaction.execute(sql)
                            except:
                                log.fatal(u'Ошибка добавления отмененной позиции')
                                sql = None
                    else:
                        log.warning(u'Ошибка идентификации записей в итоговой таблице для обновления [%s]' % dimension_requisites)

                # Взять только необходимые входные данные
                operation_requisite_values = self._get_operation_requisite_values(**requisite_values)

                # Удалить операцию движения
                where = [getattr(operation_table.c, name) == value for name, value in operation_requisite_values.items()]
                sql = operation_table.delete().where(sqlalchemy.and_(*where))
                transaction.execute(sql)

            else:
                # Не найдена операция движения
                log.warning(u'Не найдена операция движения <%s> для отмены' % requisite_values)
                transaction.rollback()
                return False

            # Закрытие транзакции
            transaction.commit()

            return True
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка отмены операции движения <%s>' % requisite_values)
        return False

    def do_operations(self, requisite_values_list):
        """
        Групповое выполнение операций движения.
        @param requisite_values_list: Список словарей значений реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        result_table = self.create_result_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = True
            for requisite_values in requisite_values_list:
                result = result and self._do_operation(transaction,
                                                       operation_table, result_table,
                                                       requisite_values)

            if result:
                # Закрытие транзакции
                transaction.commit()
            return result
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка группового выполнения операций движения <%s>' % requisite_values_list)
        return False

    def receipt(self, **requisite_values):
        """
        Приход.
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        requisite_values[CODE_OPERATION_FIELD] = '+'
        return self.do_operation(**requisite_values)

    def expense(self, **requisite_values):
        """
        Расход.
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        requisite_values[CODE_OPERATION_FIELD] = '-'
        return self.do_operation(**requisite_values)

    def del_not_actual_operation(self, dt_actual=None):
        """
        Удаление старых(не актуальных) операций
        для уменьшения размера таблицы операций движения.
        Бывают задачи, в которых старые движения не нужны.
        @param dt_actual: Дата-время, с которой данные считаются
            актуальными. Если None, то берется сегодняшняя дата.
        @return: True/False.
        """
        if dt_actual is None:
            dt_actual = datetime.date.today()
        if isinstance(dt_actual, datetime.date):
            # ВНИМАНИЕ! Сравнивать date и datetime нельзя
            # Поэтому здесь необходимо сделать приведение типов
            dt_actual = datetime.datetime.combine(dt_actual,
                                                  datetime.datetime.min.time())
        if not isinstance(dt_actual, datetime.datetime):
            log.warning(u'Не корректный тип <%s> времени актуальности операций' % dt_actual.__class__.__name__)
            return False

        operation_tab = self.get_operation_table()
        if operation_tab is not None:
            try:
                # Удалить все записи где не определено время операции
                sql = operation_tab.delete().where(sqlalchemy.and_(operation_tab.c.dt_oper==None))
                sql.execute()
                sql = operation_tab.delete().where(sqlalchemy.and_(operation_tab.c.dt_oper < dt_actual))
                sql.execute()
            except:
                log.fatal(u'Ошибка удаления не актуальных операций движения')
            return True
        return False


def test():
    """
    Тестовая функция
    """
    from ic import config

    log.init(config)

    db_url = DEFAULT_DB_URL
    registry = icAccRegistry(db_url, 'test_oper', 'test_result')
    registry.connect()

    registry.append_dimension_requisite('test_dim1', 'text')
    registry.append_dimension_requisite('test_dim2', 'text')
    registry.append_resource_requisite('test_num', 'int')

    registry.do_operation(code='+',
                         test_dim1='zz',
                         test_dim2='z',
                         test_num=21)

    # registry.undo_operation(code='+',
    #                         test_dim1='q',
    #                         test_dim2='w',
    #                         test_num=21)

if __name__ == '__main__':
    test()
