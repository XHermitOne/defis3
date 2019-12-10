#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль компонента БД.
"""

import os
import os.path
import copy

from ic.log import log

try:
    import sqlalchemy
except ImportError:
    log.error(u'Ошибка импорта SQLAlchemy')

from ic.interfaces import icsourceinterface

from ic.utils import lockfunc
from ic.kernel import icobject
from ic.utils import resource
from ic.dlg import dlgfunc
from ic.engine import glob_functions

# Типы БД
from .icSQLite import SQLITE_DB_TYPE
from .icPostgreSQL import POSTGRES_DB_TYPE
from .icMSSQL import MSSQL_DB_TYPE
from .icMySQL import MYSQL_DB_TYPE

# Спецификации (необходимы для компонентов НЕ УДАЛЯТЬ!!!)
from .icSQLite import SPC_IC_SQLITEDB
from .icPostgreSQL import SPC_IC_POSTGRESQL
from .icMSSQL import SPC_IC_MSSQL
from .icMySQL import SPC_IC_MYSQL

import ic

__version__ = (1, 1, 2, 3)

DB_TYPES = (SQLITE_DB_TYPE, POSTGRES_DB_TYPE, MSSQL_DB_TYPE, MYSQL_DB_TYPE)

# URL. Драйверы БД
DEFAULT_DB_URL_DRIVER = 'postgresql'
DB_TYPE_URL_DRIVER = {SQLITE_DB_TYPE: 'sqlite',
                      POSTGRES_DB_TYPE: 'postgresql+psycopg2',
                      MYSQL_DB_TYPE: 'mysql',
                      MSSQL_DB_TYPE: 'mssql+pyodbc',
                      }


def createDBUrl(res):
    """
    Функция создает URL БД по ее спецификации/ресурсному описанию.

    :param res: Ресурс БД.
    :return: Строка URL БД.
        Например:
            postgresql://username:password@host:port/dbname
    """
    db_type = res.get('type', POSTGRES_DB_TYPE)
    db_driver = DB_TYPE_URL_DRIVER.get(db_type, DEFAULT_DB_URL_DRIVER)
    if db_type in (POSTGRES_DB_TYPE, MSSQL_DB_TYPE, MYSQL_DB_TYPE):
        db_host = res.get('host', 'localhost')
        db_port = res.get('port', '5432')
        db_username = res.get('user', 'postgres')
        db_password = res.get('password', 'postgres')
        db_name = res.get('dbname', 'test')
        return '%s://%s:%s@%s:%s/%s' % (db_driver,
                                        db_username, db_password,
                                        db_host, db_port, db_name)
    elif db_type == SQLITE_DB_TYPE:
        db_path = res.get('path', '/')
        db_filename = res.get('filename', 'test.db')
        return '%s://%s%s' % (db_driver,
                              db_path, db_filename)
    return None


def checkDBConnect(db_url=None):
    """
    Проверка связи с БД.

    :param db_url: URL связи с БД.
    :return: True - есть связь.
    False - связь не установлена.
    """
    if db_url is None:
        # Не определена URL БД, тогда и проверять нечего
        log.warning(u'Не определено URL БД при проверке связи')
        return False

    engine = sqlalchemy.create_engine(db_url, echo=False)

    is_connect = False
    if engine:
        connection = None
        try:
            connection = engine.connect()
            result = connection.execute('SELECT 1').fetchall()
            if result:
                is_connect = True
            connection.close()
        except:
            if connection:
                connection.close()
            is_connect = False
    return is_connect


class icSQLAlchemyDB(icsourceinterface.icSourceInterface):
    """
    БД/коннекшн с БД.
    """
    connections_pool = {}
    # Словарь функций преобразования типов описания к типу БД
    _connectionTypesCreate = {SQLITE_DB_TYPE: 'sqlite',
                              POSTGRES_DB_TYPE: 'postgres',
                              MSSQL_DB_TYPE: 'mssql',
                              MYSQL_DB_TYPE: 'mysql',
                              }

    _connectionTypesConnectArgs = {SQLITE_DB_TYPE: {'detect_types': 1},
                                   POSTGRES_DB_TYPE: None,
                                   MSSQL_DB_TYPE: None,
                                   MYSQL_DB_TYPE: None,
                                   }

    def __init__(self, db_resource=None, bAutoScheme=False):
        """
        Конструктор.

        :param db_resource: Ресурсное описание БД.
        :param bAutoScheme: Автоматическое создание схемы.
        """
        icsourceinterface.icSourceInterface.__init__(self, db_resource)
        # URL
        self._db_url = createDBUrl(db_resource)
        # Связь с БД
        self._connection = None

        # Признак хранения строк в югикоде
        self.to_unicode = False

        self._db_type = None
        self._name = None
        self._metadata = None
        if db_resource:
            if isinstance(db_resource, dict):
                self._db_type = db_resource['type']
                self._name = db_resource['name']

            if not db_resource.get('dbname', None):
                # Читаем параметры соединения из ini файла
                if ic.load_ini_param('SYSDB', 'DB_ENGINE') == self._db_type:
                    db_resource = self.load_ini_par(db_resource)
                self._metadata = self._createDBMetadata(db_resource)
                icSQLAlchemyDB.connections_pool[self._name] = self._metadata
            elif icSQLAlchemyDB.connections_pool.get(self._name, None):
                self._metadata = icSQLAlchemyDB.connections_pool[self._name]
            else:
                self._metadata = self._createDBMetadata(db_resource)
                icSQLAlchemyDB.connections_pool[self._name] = self._metadata

        # Таблицы, зарегистрированные в БД
        self._tables = {}
        # Буфер сессии
        self._session = None

        if bAutoScheme:
            self.createScheme()
        if hasattr(self, 'countAttr'):
            self.countAttr('init_expr')

    def getDBUrl(self):
        """
        URL связи с БД.

        :return: Строку URL.
        """
        return self._db_url

    def checkConnect(self, db_url=None):
        """
        Проверка связи с БД.

        :param db_url: URL связи с БД.
        :return: True - есть связь.
        False - связь не установлена.
        """
        if db_url is None:
            db_url = self.getDBUrl()
        return checkDBConnect(db_url)

    def checkOnline(self):
        """
        Проверка текущей связи с БД

        :return: True - связь установлена / False - связь разорвана по какой либо причине.
        """
        if self._connection is None:
            # Не определена связь в принципе
            return False

        is_connect = False

        connection = None
        try:
            connection = self._connection.connect()
            result = connection.execute('SELECT 1').fetchall()
            if result:
                is_connect = True
            connection.close()
        except:
            if connection:
                connection.close()
            log.fatal(u'Ошибка определения онлайн состояния связи с БД')
            is_connect = False
        return is_connect

    def load_ini_par(self, res):
        """
        Загрузка параметров соединения из ini файла.
        """
        for key in self.component_spc.keys():
            val = ic.load_ini_param('SYSDB', key)
            if val:
                res[key] = val
        return res

    def getName(self):
        """
        Имя БД.
        """
        return self._name

    def getPsp(self):
        """
        Паспорт объекта БД.
        """
        return icobject.icObjectPassport((self._db_type, self._name, None, self._name + '.src', None))

    def getDBType(self):
        return self._db_type

    def _createDBMetadata(self, db_resource=None):
        """
        Создание метаданных работы с БД.
        """
        # В качестве указания БД может быть указано, только имя БД
        if isinstance(db_resource, str):
            db_resource = resource.icGetRes(db_resource, ext='src', bRefresh=False, nameRes=db_resource)
        try:
            metadata = None
            try:
                connection_url = self._getConnectionURL(db_resource)
                connection_args = self._getConnectionArgs(db_resource)
                # Параметры кодировки БД
                encoding = db_resource.get('encoding', 'UTF-8')
                if isinstance(encoding, str):
                    # ВНИМАНИЕ! В Unicode этот параметр быть не должен
                    # иначе ошибка в sqlalchemy появляется.
                    # Надо обязательно переводить в строку
                    encoding = str(encoding)
                self.to_unicode = db_resource.get('convert_unicode', False)

                log.info(u'Создание связи с БД <%s : %s : %s>' % (self._name, connection_url, connection_args))
                log.info('\t->to_unicode: <%s>' % self.to_unicode)
                log.info('\t->encode: <%s>' % encoding)

                db_engine = sqlalchemy.create_engine(connection_url,
                                                     connect_args=connection_args,
                                                     strategy='plain',
                                                     pool_size=20,
                                                     encoding=encoding,
                                                     convert_unicode=self.to_unicode)

                metadata = sqlalchemy.MetaData(db_engine)
                metadata.name = db_resource['name']
            except:
                log.fatal(u'Ошибка создания связи с БД <%s>.' % db_resource['name'])
                dlgfunc.openErrBox(u'ОШИБКА',
                                u'Ошибка создания связи с БД <%s>. Проверте параметры подключения!' % db_resource['name'])
                return None
            return metadata
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка создания связи c БД <%s>.' % db_resource['name'])
            dlgfunc.openErrBox(u'ОШИБКА', u'Ошибка создания связи c БД <%s>.' % db_resource['name'])
            return None

    def _changeDialect(self, buffer, new_dialect):
        """
        Смена диалекта в буфере.
        Так как диалек на каждый тип БД должен быть только один, надо
        у всех БД, при создании новой БД, менять диалект
        Смена происходит только у БД того же типа
        """
        for name, db in buffer.items():
            try:
                metadata = db.getMetaData()
                if metadata.engine._dialect.__class__.__name__ == new_dialect.__class__.__name__:
                    metadata.engine._dialect = new_dialect
            except:
                pass
        return buffer

    def _getConnectionURL(self, db_resource=None):
        """
        Создать по ресурсу БД URL связи с БД.
        """
        url = dict()
        url['drivername'] = self._connectionTypesCreate.setdefault(db_resource['type'], None)
        if url['drivername'] is None:
            log.warning(u'Тип драйвера БД не поддерживается.')
            return None
        # Словарь
        url['query'] = db_resource.get('query', None)

        if 'user' in db_resource:
            url['username'] = db_resource['user']
        if 'password' in db_resource:
            url['password'] = db_resource['password']
        if 'host' in db_resource:
            url['host'] = db_resource['host']
        if 'port' in db_resource:
            url['port'] = db_resource['port']
        if 'dbname' in db_resource:
            url['database'] = db_resource['dbname']
        if 'filename' in db_resource and 'path' in db_resource:
            full_path = ''
            if db_resource['filename'] and not db_resource['path']:
                full_path = os.path.abspath(db_resource['filename'])
            elif db_resource['filename'] and db_resource['path']:
                full_path = os.path.abspath(os.path.join(db_resource['path'], db_resource['filename']))
            else:
                log.warning(
                    u'Ошибка определения файла БД: path: <%s> filename: <%s>' % (db_resource['path'], db_resource['filename']))
            # Проверка существования папки БД
            dir_path = os.path.dirname(full_path)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                    log.info(u'Создана папка <%s>' % dir_path)
                except:
                    log.error(u'Ошибка создания папки <%s>' % dir_path)
            url['database'] = full_path

        url_obj = sqlalchemy.engine.url.URL(**url)
        return str(url_obj)

    def getConnectionDict(self, db_resource=None):
        """
        Создать по ресурсу БД словарь описания связи с БД.
        Эта функция необходима для получения словаря описания связи и
        последующем его сохранении в настроечных файлах.

        :param db_resource: Ресурс БД.
        :return: Словарь атрибутов связи с БД.
        """
        conn_dict = dict()
        conn_dict['drivername'] = self._connectionTypesCreate.setdefault(db_resource['type'], None)
        if conn_dict['drivername'] is None:
            log.warning(u'Тип драйвера БД не поддерживается.')
            return None

        if 'user' in db_resource:
            conn_dict['username'] = db_resource['user']
        if 'password' in db_resource:
            conn_dict['password'] = db_resource['password']
        if 'host' in db_resource:
            conn_dict['host'] = db_resource['host']
        if 'port' in db_resource:
            conn_dict['port'] = db_resource['port']
        if 'dbname' in db_resource:
            conn_dict['database'] = db_resource['dbname']
        if 'filename' in db_resource and 'path' in db_resource:
            full_path = ''
            if db_resource['filename'] and not db_resource['path']:
                full_path = os.path.abspath(db_resource['filename'])
            elif db_resource['filename'] and db_resource['path']:
                full_path = os.path.abspath(os.path.join(db_resource['path'], db_resource['filename']))
            else:
                log.warning(
                    u'Ошибка определения файла БД: path: <%s> filename: <%s>' % (db_resource['path'], db_resource['filename']))
            # Проверка существования папки БД
            dir_path = os.path.dirname(full_path)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                    log.info(u'Создана папка <%s>' % dir_path)
                except:
                    log.error(u'Ошибка создания папки <%s>' % dir_path)
            conn_dict['filename'] = full_path

        return conn_dict

    def _getConnectionArgs(self, db_resource=None):
        """
        Создать дополнительные аргументы для связи с БД.
        """
        args = self._connectionTypesConnectArgs.setdefault(db_resource['type'], None)
        if args:
            return args
        return {}

    def getMetaData(self):
        """
        Метаданные соединения.
        """
        return self._metadata

    def getConnection(self):
        """
        Создает соединение с базой.
        """
        try:
            return self._metadata.bind.connect()
        except:
            log.fatal(u'Ошибка определения связи с БД')
            dlgfunc.openErrBox(u'ОШИБКА',
                            u'Ошибка определения связи с БД [%s]. Проверте параметры соединения' % self._metadata)
            return None

    def createScheme(self, bReCreate=True):
        """
        Создать схему БД (все таблицы в БД).

        :param bReCreate: признак пересоздания схемы.
        """
        # Сначала отфильтровать таблицы которые не ссылаются на текущую БД
        if not self._tables or bReCreate:
            tab_resources = resource.getResourcesByType(ext='tab', pathRes=None)
            tab_resources = dict([(tab_res_name, tab_res) for tab_res_name, tab_res in tab_resources.items() \
                                  if tab_res])
            tab_resources = dict([(tab_res_name, tab_res) for tab_res_name, tab_res in tab_resources.items() \
                                  if tab_res[list(tab_res.keys())[0]]['source'] == self.getName() or \
                                  tab_res[list(tab_res.keys())[0]]['source'] == self.getPsp()])
            for tab_res_name, tab_res in tab_resources.items():
                tab_spc = tab_res[list(tab_res.keys())[0]]
                tab_psp = ((tab_spc['type'], tab_spc['name'], None, os.path.basename(tab_res_name), None),)
                obj = self.GetKernel().Create(tab_psp, parent=self)
        return self

    def getSession(self, autoflush=True, autocommit=True, bind=None, *args, **kwargs):
        """
        Создать объект сессии для транзакции.
        У метода есть другое название <getTransaction>.
        """
        autocommit = autocommit or kwargs.get('transactional', None)
        session = sqlalchemy.orm.sessionmaker(autoflush=autoflush,
                                              autocommit=autocommit,
                                              bind=bind or self._connection or self.getMetaData().bind)
        return session()

    # Другое наименование функции
    getTransaction = getSession

    def connect(self, db_url=None):
        """
        Установить связь с БД.

        :param db_url: URL связи с БД.
        :return: Объект связи с БД.
        """
        if db_url is None:
            db_url = self.getDBUrl()

        if self._connection:
            self.disconnect()

        self._connection = sqlalchemy.create_engine(db_url, echo=False)
        log.info(u'Установлена связь с БД <%s>' % db_url)
        return self._connection

    def disconnect(self):
        """
        Разорвать связь с БД.

        :return: True/False.
        """
        if self._connection:
            self._connection.dispose()
            self._connection = None
        return True

    def get_connection(self, auto_connect=True):
        """
        Объект связи с БД.

        :param auto_connect: Если не установлена связь,
            произвести автоматический коннект?
        """
        if self._connection is None and auto_connect:
            self.connect()
        return self._connection

    def session(self, autoflush=True, autocommit=True):
        """
        Сессия. Используется для обеспечения
        транзакционного механизма.

        :param autoflush: Авто сброс?
            Для транзакций установить в False.
        :param autocommit: Авто комитить?
            Для транзакций установить в False.
        :return: Объект сессии/Транзакции.
        """
        if not self._session:
            self._session = self.getSession(autoflush=autoflush,
                                            autocommit=autocommit)
        return self._session

    def getQuery(self, tab_name, sess=None):
        """
        Возвращает объект запроса.
        Пример:
        >>> r = scheme.getQuery('user')
        >>> obj_lst = r.filter(ridord_id).all()

        :param tab_name: Имя таблицы.
        :param sess: Сессия.
        """
        if not sess:
            dct = self.getTables()
            tab = dct.get(tab_name, None)
            tab_cls = tab.getMapperClass()
            sess = self.session()

            return sess.query(tab_cls)
        return sess.query()

    def iron_flush(self, mapper=None):
        """
        Иногда орм ругается, что flush уже сделан и пока не будет сделан query
        изменения в базу не попадают. Это связано со стратегией работы с session,
        когда autoflush=True.
        """
        try:
            self.session().flush()
        except:
            dct = self.getTables()
            if dct:
                self.session().query(mapper or list(dct.values())[0].getMapperClass()).get(1)

    def getTables(self):
        """
        Зарегистрированные в БД таблицы.
        """
        return self._tables

    def getTableByName(self, name):
        return self._tables.get(name, None)

    def _isSQLReturnResult(self, sql_query):
        """
        Проверка, должен ли результат запроса возвращать значения.

        :param sql_query: Строка запроса.
        """
        return bool(sql_query.lower().find('select') != -1)

    def executeSQL(self, sql_query, to_dict=False):
        """
        Выполнить строку запроса.

        :param sql_query: Строка запроса.
        :param to_dict: Преобразовать все записи в словари?
        :return: Возвражает словарь {'__fields__':((..),(..),..),'__data__':[(..),(..),..]}.
            Или None в случае ошибки.
        """
        result = None
        # Выполнить запрос
        try:
            # Доступ к конекшену DBAPI2
            connection = self._metadata.bind.connect().connection
            cursor = connection.cursor()
            cursor.execute(sql_query)
            if self._isSQLReturnResult(sql_query):
                fields = cursor.description
                # log.debug(u'SQL: %s RESULT FIELDS: %s' % (ic_str.toUnicode(sql_query), fields))
                data = cursor.fetchall()
                if data and to_dict:
                    new_data = [dict([(fields[i][0], val) for i, val in enumerate(rec)]) for rec in data]
                    data = new_data
                result = copy.deepcopy({'__fields__': fields, '__data__': data})
            cursor.close()
        except:
            err_txt = u'Ошибка выполнения запроса <%s>' % str(sql_query)
            log.fatal(err_txt)
            dlgfunc.openErrBox(u'ОШИБКА', err_txt)

            return None

        return result

    def _adaptFieldDescription(self, *field_description):
        """
        Преобразовать описания полей во внутренний вариан описаний.
        Метод абстрактный и переопределяется для каждой БД отдельно.

        :param field_description: Список описаний полей DBAPI2.
        :return: Список описаний полей во внутреннем формате:
            [
            ('Имя поля', 'Тип поля (T, I, F, DateTime, Boolean и т.п)', Длина поля),
            ...
            ]
        """
        log.warning(u'Не определен метод _adaptFieldDescription для БД <%s>' % self.__class__.__name__)
        return field_description

    def executeSQLOne(self, sql_query, to_dict=False):
        """
        Выполнить строку запроса и вернуть только одну запись.

        :param sql_query: Строка запроса.
        :param to_dict: Преобразовать запись в словарь?
        :return: Возвражает словарь {'__fields__':((..),(..),..),'__data__':[(..),(..),..]}.
            Или None в случае ошибки.
        """
        result = None
        # Выполнить запрос
        try:
            # Доступ к конекшену DBAPI2
            connection = self._metadata.bind.connect().connection
            cursor = connection.cursor()
            cursor.execute(sql_query)
            if self._isSQLReturnResult(sql_query):
                fields = self._adaptFieldDescription(cursor.description)
                # log.debug(u'Результирующие поля: %s' % str([str(field) for field in fields]))
                data = cursor.fetchone()
                if data and to_dict:
                    new_data = [dict([(fields[i][0], val) for i, val in enumerate(rec)]) for rec in data]
                    data = new_data
                result = copy.deepcopy({'__fields__': fields, '__data__': data})
            cursor.close()
        except:
            err_txt = u'DBAPI2. Ошибка выполнения запроса для получения одной записи <%s>' % str(sql_query)
            log.fatal(err_txt)
            dlgfunc.openErrBox(u'ОШИБКА', err_txt)
            return None

        return result

    def select(self, *args, **kwargs):
        """
        Выбрать список объектов из класса данных.
        См. описание функции select в SQLAlchemy.

        :param columns: Объекты колонок которые нужно выбрать.
        :param whereclause: Условие выбора.
        :param from_obj: Таблицы из которых производится выбор.
        :return: Возвражает объект SelectResults.
        """
        return sqlalchemy.select(*args, **kwargs).execute()

    def getEncoding(self):
        """
        Кодировка БД.
        """
        return self._metadata.bind.dialect.encoding

    # Поддержка блокировок
    def LockTable(self, name):
        """
        Блокирует таблицу.
        """
        return lockfunc.LockTable(name)

    def unLockTable(self, name):
        """
        Разблокирует таблицу.
        """
        return lockfunc.UnLockTable(name)

    def LockRec(self, name, id, lock_record=None):
        """
        Блокировка записи.
        """
        if lock_record is None:
            comp_name = lockfunc.ComputerName()
            user_name = glob_functions.getCurUserName()
            lock_record = str({'computer': comp_name, 'user': user_name})
        result = lockfunc.LockRecord(name, id, lock_record)
        log.debug(u'Запись заблокирована <%s : %s : %s : %s>' % (name, id, lock_record, result))
        if result != 0:
            return False
        return True

    def unLockRec(self, name, id):
        """
        Разблокирует запись.
        """
        if not self.IsLockRec(name, id):
            log.debug(u'Запись разблокирована <%s : %s>' % (name, id))
            return lockfunc.unLockRecord(name, id)
        return False

    def IsLockTable(self, name):
        """
        Возвращает признак блокировки таблицы.
        """
        return lockfunc.isLockTable(name)

    def IsLockRec(self, name, id):
        """
        Возвращает признак блокировки записи.
        """
        lock_msg = lockfunc.readMessage(name, id)

        if lock_msg:
            lock_rec = eval(lock_msg)
            # Если блокировка поставлена тем же пользователем,
            # тогда не считается что заблокировано
            log.debug(u'Проверка блокироваки записи <%s : %s> ' % (lock_rec, type(lock_rec)))
            if lock_rec and lock_rec['user'] == glob_functions.getCurUserName():
                return False
            return lockfunc.isLockRecord(name, id)
        return False

    def releaseConnection(self, conn):
        """
        Освобождает соединение.
        """
        pass

