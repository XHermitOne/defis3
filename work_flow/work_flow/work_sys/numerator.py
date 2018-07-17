#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль реализации нумераторов.
Формат кода нумератора может содержать все временные форматы,
а также
    <%N> - номер счетчика строки таблицы нумератора.
    <%E> - дополнительные параметры, передаваемые функции
           генерации кода в качестве дополнительных аргументов.
"""

import re
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoping
from sqlalchemy.sql import func

from ic.log import log

__version__ = (0, 0, 0, 2)

# Формат номера строки в качестве подкода
N_RECORD_PATTERN = r'(\%.[0-9]N)'

# Формат дополнительных строк в качестве подкода
EXT_STR_PATTERN = '%E'

# Формат номера-кода по умолчанию
DEFAULT_NUM_CODE_FMT = 'N-%05N'

# Типы реквизитов
INTEGER_REQUISITE_TYPE = 'int'
FLOAT_REQUISITE_TYPE = 'float'
TEXT_REQUISITE_TYPE = 'text'
DT_REQUISITE_TYPE = 'datetime'

# Имя таблицы нумератора по умолчанию
DEFAULT_NUMERATOR_TABLE = 'numerator'

# Имена полей таблицы нумератора
NUMBER_CODE_FIELD = 'number_code'   # Поле кода номера
DT_NUMBER_FIELD = 'dt_num'          # Поле даты-времени выдачи номера
CUR_COUNT_FIELD = 'cur_count'       # Поле счетчика


class icNumerator(object):
    """
    Класс нумератора.
    """

    def __init__(self, db_url=None,
                 numerator_table_name=DEFAULT_NUMERATOR_TABLE,
                 num_code_format=DEFAULT_NUM_CODE_FMT,
                 check_unique=False):
        """
        Конструктор.
        @param db_url: Параметры подключения к БД.
        @param numerator_table_name: Имя таблицы нумератора.
        @param num_code_format: Формат номер-кода нумератра.
        @param check_unique: Производить проверку уникальности
            генерируемого номер-кода?
        """
        self._db_url = db_url
        self._connection = None

        # Таблица нумератора
        self._numerator_table_name = numerator_table_name
        self._numerator_table = None

        # Формат номера-кода нумератора
        self._num_code_format = num_code_format

        # Автоматическая проверка на уникальность номер-кода
        self._check_unique = check_unique

        # Текущий номер-код
        self._num_code = None

    def set_check_unique(self, check_unique=True):
        """
        Автоматическая проверка на уникальность номер-кода.
        Установить.
        """
        self._check_unique = check_unique

    def get_check_unique(self):
        """
        Автоматическая проверка на уникальность номер-кода.
        """
        return self._check_unique

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

    def get_numerator_table(self):
        """
        Таблица sqlalchemy нумератора.
        """
        if not self.is_connected():
            self.connect()

        if self._numerator_table is None:
            self.create_numerator_table()
        return self._numerator_table

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
        columns = [self.gen_column(**requisite) for requisite in requisites]
        table = sqlalchemy.Table(table_name, metadata, *columns)
        return table

    def _get_numerator_requisites(self):
        """
        Список реквизитов-полей таблицы нумератора.
        @return: Список словарей описания полей:
            [{'requisite_name': <Имя поля>,
            'requisite_type': <Тип поля>}, ...]
        """
        num_code_requisite = dict(requisite_name=NUMBER_CODE_FIELD,
                                  requisite_type=TEXT_REQUISITE_TYPE)

        dt_num_requisite = dict(requisite_name=DT_NUMBER_FIELD,
                                requisite_type=DT_REQUISITE_TYPE)

        cur_count_requisite = dict(requisite_name=CUR_COUNT_FIELD,
                                   requisite_type=INTEGER_REQUISITE_TYPE)
        requisites = [num_code_requisite,
                      dt_num_requisite,
                      cur_count_requisite]
        return requisites

    def create_numerator_table(self, numerator_table_name=None):
        """
        Создание таблицы нумератора.
        ВНИМАНИЕ!
        Таблица нумератора состоит из полей:
            1. Выданный нумератором номер-код (number_code)
            2. Дата-время выдачи номера (dt_num)
            3. Счетчик выдачи номера (cur_count)
        @param numerator_table_name: Имя таблицы нумератора.
        @return: Объект таблицы нумератора или None в случае ошибки.
        """
        if numerator_table_name is None:
            numerator_table_name = self._numerator_table_name

        requisites = self._get_numerator_requisites()
        self._numerator_table = self.gen_table(numerator_table_name, requisites)
        self._numerator_table.create(checkfirst=True)
        return self._numerator_table

    def _gen_new_num_code(self, fmt=None, n_count=0, *args):
        """
        Сгенерировать новый номер-код.
        @param fmt: Формат кода.
        @param n_count: Дополнительнвй идентификатор генерирумой
            строки таблицы нумератора.
        @param args: Дополнительные параметры кода.
        @return: Сгененрированный номер-код.
        """
        if fmt is None:
            fmt = self._num_code_format

        # Заменить в формате временные параметры
        # ВНИМАНИЕ! При замене с помощью strftime
        # необходимо заменить <%> на <%%> иначе замена
        # происходит не корректно
        now = datetime.datetime.now()
        fmt = now.strftime(fmt.replace('%', '%%'))

        fmt_args = list()

        # Заменить значение счетчика
        replaces = [(element, element.replace('N', 'd')) for element in re.findall(N_RECORD_PATTERN, fmt)]
        if replaces:
            for src, dst in replaces:
                # log.debug(u'Замена <%s> на <%s> <%s>' % (src, dst, fmt))
                fmt = fmt.replace(src, dst)
                fmt_args.append(n_count)

        # Заменить дополнительные строковые параметры
        if EXT_STR_PATTERN in fmt:
            fmt = fmt.replace(EXT_STR_PATTERN, '%s')
            fmt_args += [str(arg) for arg in args]

        if fmt_args:
            # Если есть дополнительные параметры
            # то сгененрировать код
            log.debug(u'Генерация номер-кода по формату <%s> аргументы %s' % (fmt, fmt_args))
            fmt = fmt % tuple(fmt_args)

        # Все считаем что код сгененирован
        return fmt

    def get_actual_year(self):
        """
        Актуальнй год для определения максимального счетчика.
        Но метод можно переопределить.
        @return: Значение года системы.
        """
        return datetime.date.today().year

    def get_max_count(self, session, numerator_table, cur_year=None):
        """
        Определить максимальное значение счетчика нумератора.
        Максимальное значение счетчика необходимо производить
        с учетом текущего программного года.
        @param session: Сессия обработки SQLAlchemy.
        @param numerator_table: Таблица нумератора.
        @param cur_year: Текущий год.
            Если не определяется, то берется системный год.
        @return: Максимальное значение счетчика нумератора.
        """
        if cur_year is None:
            cur_year = self.get_actual_year()
        min_date = datetime.date(cur_year, 1, 1)
        max_date = datetime.date(cur_year, 12, 31)

        session_query = scoping.scoped_session(session)
        max_count = session_query.query(func.max(numerator_table.c.cur_count).label('max_count')).filter(sqlalchemy.between(numerator_table.c.dt_num, min_date, max_date)).one()[0]
        return max_count

    def do_gen_num_code(self, check_unique=None, *args):
        """
        Сгенерировать новый номер-код.
        Кроме того что генерируется номер-код,
        он регистрируется(записывается) в таблице нумератора
        и указывается время выдачи номер-кода.
        @param check_unique: Произвести контроль уникальности кода?
        @param args: Дополнительные параметры кода.
        @return: Сгененрированный номер-код или None
            в случае ошибки.
        """
        if check_unique is None:
            check_unique = self.get_check_unique()

        # Сначала создать таблицы (вдруг их нет)
        numerator_table = self.create_numerator_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        # В начале генерации сбросить текущий номер-код
        self._num_code = None
        try:
            # Определение максимального значения счетчика
            max_count = self.get_max_count(session, numerator_table)
            max_count = max_count + 1 if max_count else 1
            log.debug(u'New max count <%s>' % max_count)

            # Т.к. актуальный год можно заменить, то и дату выставить
            # актуального года
            now = datetime.datetime.now()
            now = now.replace(year=self.get_actual_year())

            sql = numerator_table.insert().values(number_code=None,
                                                  dt_num=now,
                                                  cur_count=max_count)
            transaction.execute(sql)

            new_num_code = self._gen_new_num_code(n_count=max_count, *args)
            if check_unique:
                # Необходимо произвести контроль уникальности номер-кода
                find = numerator_table.select(numerator_table.c.number_code == new_num_code).execute()
                if find.rowcount:
                    log.warning(u'Такой код <%s> уже существует в нумераторе' % new_num_code)
                    transaction.rollback()
                    return None

            # Поле даты-времени и поле счетчика являются уникальными идентификаторами записи
            sql = numerator_table.update().where(sqlalchemy.and_(numerator_table.c.dt_num == now,
                                                                 numerator_table.c.cur_count == max_count)).values(number_code=new_num_code)
            transaction.execute(sql)

            # Закрытие транзакции
            transaction.commit()
            # Все прошло успешно надо запомнить номер-код который сгенерировали
            self._num_code = new_num_code
            return self._num_code
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка генерации нового номер-кода нумератором')
        return None

    def undo_gen_num_code(self):
        """
        Отменить генерацию последнего номер-кода.
        Запись с номер-кодом удаляется из таблицы нумератора.
        @return: True/False.
        """
        # Сначала создать таблицы (вдруг их нет)
        numerator_table = self.create_numerator_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            if self._num_code is not None:
                sql = numerator_table.delete().where(numerator_table.c.number_code == self._num_code)
                transaction.execute(sql)
            else:
                log.warning(u'Номер-код для отмены не определен')
                return False

            # Закрытие транзакции
            transaction.commit()

            # Все прошло успешно надо сбросить номер-код
            self._num_code = None
            return True
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка отмены генерации номер-кода нумератором')
        return False

    def del_not_actual(self, dt_actual=None):
        """
        Удаление старых(не актуальных) номеров
        для уменьшения размера таблицы нумератора.
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

        numerator_tab = self.get_numerator_table()
        if numerator_tab is not None:
            try:
                sql = numerator_tab.delete().where(sqlalchemy.and_(numerator_tab.c.dt_num < dt_actual))
                sql.execute()
            except:
                log.fatal(u'Ошибка удаления не актуальных данных нумератора')
            return True
        return False

    def do_gen(self, *args, **kwargs):
        """
        Сгенерировать новый номер-код.
        @return: Сгененрированный номер-код или None
            в случае ошибки.
        """
        self.connect()
        num_code = self.do_gen_num_code(*args, **kwargs)
        self.disconnect()
        return num_code

    # Другое наименование метода
    gen = do_gen

    def undo_gen(self):
        """
        Отменить генерацию нового номер-кода.
        @return: True/False.
        """
        self.connect()
        result = self.undo_gen_num_code()
        self.disconnect()
        return result


def test():
    """
    Тестовая функция.
    """
    numerator = icNumerator()
    result = numerator._gen_new_num_code('%Y%m%d - %N : %0', 123)
    print('TEST:', result)

if __name__ == '__main__':
    test()
