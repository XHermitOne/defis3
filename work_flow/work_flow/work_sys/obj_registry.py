#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль реализации регистра объектов.
Реестр/Регистр объектов сделан для
    организации движения изменения состояния объектов системы.
    Все по аналогии с регистром накопления.
"""

import uuid
import datetime
import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

# from services.ic_std.log import log
from ic.log import log

__version__ = (0, 0, 1, 8)

# Имя таблицы движения по умолчанию
DEFAULT_OPERATIONS_TABLE = 'operations'
# Имя таблицы объектов по умолчанию
DEFAULT_OBJ_TABLE = 'object_tab'

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

# Имена полей таблицы движения
UUID_OBJ_OPERATION_FIELD = 'uuid'   # Поле UUID объекта
OBJ_OPERATION_FIELD = 'n_obj'       # Поле номера объекта
PREV_OPERATION_FIELD = 'prev'       # Поле кода предыдущего состояния объекта
POST_OPERATION_FIELD = 'post'       # Поле кода последующего состояния объекта
DT_OPERATION_FIELD = 'dt_oper'      # Поле даты-времени выполнения операции

# Имена полей таблицы объектов
UUID_OBJ_FIELD = 'uuid'             # Поле UUID объекта
N_OBJ_FIELD = 'n_obj'               # Поле номера объекта
DTCREATE_OBJ_FIELD = 'dt_create'    # Поле даты-времени создания
STATE_OBJ_FIELD = 'state'           # Поле текущего состояния объекта
DTSTATE_OBJ_FIELD = 'dt_state'      # Поле даты-времени последней смены состояния

# Значение по умолчанию при создании объекта
DEFAULT_CREATE_STATE = 'CREATED'


class icObjRegistry(object):
    """
    Класс реестра/регистра объектов.
    Общий вид работы регистра:

    Событие 1-----+
    Событие 2---+ |
    Событие 3-+ | |
              | | |
    +---------| | |-------------------------+
    |         V V V   Регистр объектов      |
    | +===============+                     |
    | | Учет движений |                     |
    | +===============+                     |
    |       |                               |
    |       V                               |
    | +=============================+       |
    | | Учет состояния объектов     |       |
    | +=============================+       |
    +---------------------------------------+

    Объект идентифицируется полем UUID и номером объекта.
    UUID - идентификатор уровня БД.
    Номер объекта - идентифиактор прикладной системы.
    В объекте присутствуе символьное поле состояния.
    Изменение состояния регистрируется в таблице движения:
    prev - предыдущее состояние объекта.
    post - последующее состояние объекта.
    Значения состояний задаются кодом прикладной системы.
    """

    def __init__(self, db_url=None,
                 operation_table_name=DEFAULT_OPERATIONS_TABLE,
                 obj_table_name=DEFAULT_OBJ_TABLE):
        """
        Конструктор.
        @param db_url: Параметры подключения к БД.
        @param operation_table_name: Имя таблицы движений.
        @param obj_table_name: Имя таблицы объектов.
        """
        self._db_url = DEFAULT_DB_URL if db_url is None else db_url
        self._connection = None

        self._operation_table_name = operation_table_name
        self._operation_table = None
        self._obj_table_name = obj_table_name
        self._obj_table = None

        # Реквизиты объекта
        self._obj_requisites = list()

    def get_operation_table(self):
        """
        Таблица sqlalchemy операций движения.
        """
        if self._operation_table is None:
            self.create_operation_table()
        return self._operation_table

    def get_obj_table(self):
        """
        Таблица sqlalchemy объектов.
        """
        if self._obj_table is None:
            self.create_obj_table()
        return self._obj_table

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

    def create_operation_table(self, operation_table_name=None):
        """
        Создание таблицы движений.
        ВНИМАНИЕ!
        Для таблицы движения надо завести поля:
            1. поле даты-времени операции.
            2. поле UUID - идентификатор объекта UUID
            3. номер объекта
            Двойная идентификация производиться для того чтобы
            можно было идентифицировать объект на разных уровнях:
                на системном - UUID
                на прикладном - номер объекта
            4. поле предыдущего состояния объекта
            5. поле последующего сосотояния объекта
        @param operation_table_name: Имя таблицы движений.
        @return: Объект таблицы движений или None в случае ошибки.
        """
        if operation_table_name is None:
            operation_table_name = self._operation_table_name

        dt_requisite = dict(requisite_name=DT_OPERATION_FIELD,
                            requisite_type=DT_REQUISITE_TYPE)
        uuidobj_requisite = dict(requisite_name=UUID_OBJ_OPERATION_FIELD,
                                 requisite_type=TEXT_REQUISITE_TYPE)
        nobj_requisite = dict(requisite_name=OBJ_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        prev_requisite = dict(requisite_name=PREV_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        post_requisite = dict(requisite_name=POST_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        requisites = [dt_requisite,
                      uuidobj_requisite,
                      nobj_requisite,
                      prev_requisite,
                      post_requisite] + self._obj_requisites
        self._operation_table = self.gen_table(operation_table_name, requisites)
        self._operation_table.create(checkfirst=True)
        return self._operation_table

    def create_obj_table(self, obj_table_name=None):
        """
        Создание таблицы объектов.
        @param obj_table_name: Имя таблицы объектов.
        @return: Объект таблицы объектов или None в случае ошибки.
        """
        if obj_table_name is None:
            obj_table_name = self._obj_table_name

        uuidobj_requisite = dict(requisite_name=UUID_OBJ_FIELD,
                                 requisite_type=TEXT_REQUISITE_TYPE)
        nobj_requisite = dict(requisite_name=N_OBJ_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        dtcreate_requisite = dict(requisite_name=DTCREATE_OBJ_FIELD,
                                  requisite_type=DT_REQUISITE_TYPE)
        state_requisite = dict(requisite_name=STATE_OBJ_FIELD,
                               requisite_type=TEXT_REQUISITE_TYPE)
        dtstate_requisite = dict(requisite_name=DTSTATE_OBJ_FIELD,
                                 requisite_type=DT_REQUISITE_TYPE)

        requisites = [uuidobj_requisite,
                      nobj_requisite,
                      dtcreate_requisite,
                      state_requisite,
                      dtstate_requisite] + self._obj_requisites
        self._obj_table = self.gen_table(obj_table_name, requisites)
        self._obj_table.create(checkfirst=True)
        return self._obj_table

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

    def get_obj_requisite_names(self):
        """
        Имена реквизитов объекта.
        @return: Список имен реквизитов.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._obj_requisites]
        return names

    def append_obj_requisite(self, requisite_name, requisite_type):
        """
        Добавление реквизита объекта.
        @param requisite_name: Имя реквизита.
        @param requisite_type: Тип реквизита.
            Тип реквизита реквизита
            м.б. целый ('int'), вещественный ('float'),
            дата-время('datetime') или текстовый ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._obj_requisites.append(requisite)

    def _get_operation_requisite_values(self, **requisite_values):
        """
        Отфильтровать только небходимые значения реквизитов
        для таблицы операций движения.
        @param requisite_values: Значения реквизитов.
        @return: Список реквизитов используемых в регистре.
        """
        used_requisite_names = [UUID_OBJ_OPERATION_FIELD,
                                OBJ_OPERATION_FIELD,
                                DT_OPERATION_FIELD,
                                PREV_OPERATION_FIELD,
                                POST_OPERATION_FIELD] + self.get_obj_requisite_names()
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def do_state(self, **requisite_values):
        """
        Установить новое состояние объекта.
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        obj_table = self.create_obj_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        sql = None
        # Текущее системное время. Будет использоваться далее
        dt_now = datetime.datetime.now()
        try:
            result = True
            # Определить способ идентификации объекта
            uuid_obj = requisite_values.get(UUID_OBJ_FIELD, None)
            n_obj = requisite_values.get(N_OBJ_FIELD, None)
            obj_id_requisites = [(name, value) for name, value in [(UUID_OBJ_FIELD, uuid_obj),
                                                                   (N_OBJ_FIELD, n_obj)] if value]

            # Поиск объекта по заданным идентификаторам
            where = [getattr(obj_table.c, name) == value for name, value in obj_id_requisites]
            find = obj_table.select(sqlalchemy.and_(*where)).execute()
            if not find.rowcount:
                # Если объект с таким идентификатором не найден,
                # то создать его
                obj_requisite_names = self.get_obj_requisite_names()
                obj_requisites = dict([(name, requisite_values.get(name, None)) for name in obj_requisite_names])
                obj_requisites[DTCREATE_OBJ_FIELD] = requisite_values.get(DTCREATE_OBJ_FIELD, dt_now)
                obj_requisites[N_OBJ_FIELD] = n_obj
                # У объекта обязательно д.б. UUID
                uuid_obj = uuid_obj if uuid_obj else str(uuid.uuid4())
                obj_requisites[UUID_OBJ_FIELD] = uuid_obj
                # Определить текущее состояния объекта
                obj_state = None
                new_state = requisite_values[STATE_OBJ_FIELD] if STATE_OBJ_FIELD in requisite_values else DEFAULT_CREATE_STATE
                # Записать новое состояние
                obj_requisites[STATE_OBJ_FIELD] = new_state
                obj_requisites[DTSTATE_OBJ_FIELD] = dt_now
                sql = obj_table.insert().values(**obj_requisites)
                transaction.execute(sql)
            else:
                find_obj = find.first()
                # Определить текущее состояния объекта
                obj_state = find_obj[STATE_OBJ_FIELD]
                # Новое состояние объекта
                new_state = requisite_values.get(STATE_OBJ_FIELD, obj_state)
                uuid_obj = find_obj[UUID_OBJ_FIELD]
                n_obj = find_obj[N_OBJ_FIELD]

                # Записать новое состояние объекта и реквизиты
                obj_requisite_names = self.get_obj_requisite_names()
                obj_requisites = dict([(name, requisite_values.get(name, None)) for name in obj_requisite_names])
                obj_requisites[STATE_OBJ_FIELD] = new_state
                obj_requisites[DTSTATE_OBJ_FIELD] = dt_now
                sql = obj_table.update().where(sqlalchemy.and_(*where)).values(**obj_requisites)
                transaction.execute(sql)

            # Записать операцию движения
            if obj_state != new_state:
                # Только если у нас действительно меняется состояние
                # иначе движения не происходит
                operation_requisite_values = self._get_operation_requisite_values(**requisite_values)
                operation_requisite_values[DT_OPERATION_FIELD] = dt_now
                operation_requisite_values[UUID_OBJ_OPERATION_FIELD] = uuid_obj
                operation_requisite_values[OBJ_OPERATION_FIELD] = n_obj
                operation_requisite_values[PREV_OPERATION_FIELD] = obj_state
                operation_requisite_values[POST_OPERATION_FIELD] = new_state

                sql = operation_table.insert().values(**operation_requisite_values)
                transaction.execute(sql)
            else:
                # Изменение значений реквизитов без операции движения
                operation_requisite_values = self._get_operation_requisite_values(**requisite_values)
                operation_requisite_values[DT_OPERATION_FIELD] = dt_now
                operation_requisite_values[UUID_OBJ_OPERATION_FIELD] = uuid_obj
                operation_requisite_values[OBJ_OPERATION_FIELD] = n_obj

                where = [getattr(operation_table.c, UUID_OBJ_OPERATION_FIELD) == uuid_obj,
                         getattr(operation_table.c, OBJ_OPERATION_FIELD) == n_obj,
                         getattr(operation_table.c, POST_OPERATION_FIELD) == new_state]
                sql = operation_table.update().where(sqlalchemy.and_(*where)).values(**operation_requisite_values)
                transaction.execute(sql)

            if result:
                # Закрытие транзакции
                transaction.commit()
            return result
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка выполнения операции движения <%s>' % requisite_values)
        return False

    def undo_state(self, **requisite_values):
        """
        Восстановить предыдущее состояние объекта.
        @param requisite_values: Значения реквизитов.
        @return: True - операция прошла успешно.
            False - Операция не закончена по причине какой-то ошибки.
            Транзакция откатила выполнение операции.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        obj_table = self.create_obj_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = True
            # Определить способ идентификации объекта
            uuid_obj = requisite_values.get(UUID_OBJ_FIELD, None)
            n_obj = requisite_values.get(N_OBJ_FIELD, None)
            obj_id_requisites = [(name, value) for name, value in [(UUID_OBJ_FIELD, uuid_obj),
                                                                   (N_OBJ_FIELD, n_obj)] if value]
            # Найти последнюю регистрацию изменения состояния объекта
            oper_where = [getattr(operation_table.c, name) == value for name, value in obj_id_requisites]
            obj_where = [getattr(obj_table.c, name) == value for name, value in obj_id_requisites]
            find = operation_table.select(sqlalchemy.and_(*oper_where)).order_by(desc(DT_OPERATION_FIELD)).execute()
            if find.rowcount:
                # Записи есть в таблице движений
                if find.rowcount == 1:
                    # Если это последняя запись в таблице движений,
                    # то документ удалить
                    sql = operation_table.delete().where(sqlalchemy.and_(*oper_where))
                    transaction.execute(sql)
                    sql = obj_table.delete().where(sqlalchemy.and_(*obj_where))
                    transaction.execute(sql)
                else:
                    find_state = find.fetchone()
                    prev_state = find.fetchone()
                    # Это не последняя запись
                    # надо сделать откат на предыдущее состояние
                    obj_requisites = dict()
                    obj_requisites[STATE_OBJ_FIELD] = find_state[PREV_OPERATION_FIELD]
                    obj_requisites[DTSTATE_OBJ_FIELD] = prev_state[DT_OPERATION_FIELD]
                    # Восстановить значения реквизитов объекта,
                    # соответствующих предыдущему состоянию
                    obj_requisite_names = self.get_obj_requisite_names()
                    for requisite_name in obj_requisite_names:
                        obj_requisites[requisite_name] = prev_state[requisite_name]
                    requisite_values.update(obj_requisites)

                    sql = obj_table.update().where(sqlalchemy.and_(*obj_where)).values(**requisite_values)
                    transaction.execute(sql)

                    # ВНИМАНИЕ! Здесь удаляется запись последнего состояния.
                    # Проверка производится на полное совпадение записи.
                    sql = operation_table.delete().where(sqlalchemy.and_(*oper_where))
                    transaction.execute(sql)
            else:
                # ВНИМАНИЕ! Если записей в журнале движений нет
                # то не возможно определить предыдущее состояние объекта
                # а значит нелзя и сделать отмену
                result = False

            if result:
                # Закрытие транзакции
                transaction.commit()
            return result
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка выполнения отмены операции движения <%s>' % requisite_values)
        return False

    def clear_all(self):
        """
        ВНИМАНИЕ! Функция удаляет все данные из регистра!!!
            Пользоваться только с очень большой осторожностью.
        @return: True/False.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()
        obj_table = self.create_obj_table()

        # Начало транзакции
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            sql = operation_table.delete()
            transaction.execute(sql)

            sql = obj_table.delete()
            transaction.execute(sql)

            # Закрытие транзакции
            transaction.commit()
            return True
        except:
            # Откат транзакции
            transaction.rollback()
            log.fatal(u'Ошибка очистки регистра объектов')
        return False

    def get_operation_state_record(self, uuid_obj=None, n_obj=None, state=None):
        """
        Получить запись операции движения по переводу объекта
            в состояние state.
        @param uuid_obj: UUID объекта. Если не указан, то
            документ определяется по n_obj.
        @param n_obj: Номер-идентификатор объекта.
            Если не указан, то документ определяется по UUID.
        @param state: Состояние объекта.
        @return: Словарь записи операции движения
            соответствующего (проверка по POST_OPERATION_FILED)
            состоянию state.
            Если такое состояние такого объекта не найдено,
            то возвращается None.
        """
        # Сначала создать таблицы (вдруг их нет)
        operation_table = self.create_operation_table()

        # Определить способ идентификации операции движения
        obj_id_requisites = [(name, value) for name, value in [(UUID_OBJ_FIELD, uuid_obj),
                                                               (N_OBJ_FIELD, n_obj),
                                                               (POST_OPERATION_FIELD, state)] if value]

        # Поиск операции по заданным идентификаторам
        where = [getattr(operation_table.c, name) == value for name, value in obj_id_requisites]
        find = operation_table.select(sqlalchemy.and_(*where)).order_by(desc(DT_OPERATION_FIELD)).execute()
        if find.rowcount == 1:
            record = find.first()
            return dict(record)
        elif find.rowcount > 1:
            log.warning(u'Избыточные данные об операции состояния <%s> объекта [%s : %s]' % (state, uuid_obj, n_obj))
            record = find.first()
            return dict(record)
        elif find.rowcount < 1:
            log.warning(u'Нет данные об операции состояния <%s> объекта [%s : %s]' % (state, uuid_obj, n_obj))

        return None

    def del_not_actual_operation(self, dt_actual=None):
        """
        Удаление старых(не актуальных) операций
        для уменьшения размера таблицы операций движения.
        Бывают задачи, в которых старые движения не нужны.
        @param dt_actual: Дата, с которой данные считаются
            актуальными. Если None, то берется сегодняшняя дата.
        @return: True/False.
        """
        if dt_actual is None:
            dt_actual = datetime.date.today()
        operation_tab = self.get_operation_table()
        if operation_tab is not None:
            try:
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
    registry = icObjRegistry(db_url, 'test_oper_obj', 'test_object')
    registry.connect()

    registry.append_obj_requisite('test_tab', 'text')
    registry.append_obj_requisite('test_num', 'int')

    registry.clear_all()

    registry.do_state(n_obj='1234',
                      test_tab='zz',
                      test_num=21)

    registry.do_state(n_obj='1234',
                      test_tab='z2',
                      test_num=3,
                      state='STATE2')

    registry.do_state(n_obj='1234',
                      test_tab='z0',
                      test_num=-3,
                      state='STATE2')

    registry.do_state(n_obj='1234',
                      test_tab='z3',
                      test_num=4,
                      state='STATE3')

    registry.do_state(n_obj='1234',
                      test_tab='z4',
                      test_num=5,
                      state='STATE4')

    registry.undo_state(n_obj='1234')

    log.debug(u'Operation record <STATE2> - %s' % registry.get_operation_state_record(n_obj='1234', state='STATE2'))

    registry.disconnect()

if __name__ == '__main__':
    test()
