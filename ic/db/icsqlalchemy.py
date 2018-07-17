#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль компонента таблицы и БД.
"""

# Подключение библиотек
import copy
import new

from ic.log import log

try:
        import sqlalchemy
        import sqlalchemy.orm

        from sqlalchemy import *
        from sqlalchemy.sql.functions import *

        sqlalchemy_field_type_Integer = sqlalchemy.Integer
        sqlalchemy_field_type_Float = sqlalchemy.Float
        sqlalchemy_field_type_String = sqlalchemy.String
        sqlalchemy_field_type_Text = sqlalchemy.Text
        sqlalchemy_field_type_Binary = sqlalchemy.Binary
        sqlalchemy_field_type_DateTime = sqlalchemy.DateTime
        sqlalchemy_field_type_PickleType = sqlalchemy.PickleType
        sqlalchemy_field_type_BigInteger = sqlalchemy.BigInteger
        sqlalchemy_field_type_Boolean = sqlalchemy.Boolean
except:
        log.error('SQLAlchemy import error')
        sqlalchemy_field_type_Integer = None
        sqlalchemy_field_type_Float = None
        sqlalchemy_field_type_String = None
        sqlalchemy_field_type_Text = None
        sqlalchemy_field_type_Binary = None
        sqlalchemy_field_type_DateTime = None
        sqlalchemy_field_type_PickleType = None
        sqlalchemy_field_type_BigInteger = None
        sqlalchemy_field_type_Boolean = None

from ic.interfaces import icdataclassinterface
from ic.interfaces import icsourceinterface
from ic.utils import resource
from ic.utils import ic_file
from ic.utils import ic_mode
from ic.utils import util
from ic.utils import ic_str

import ic
from ic.utils import lock
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.engine import ic_user
from ic.kernel import icobject

from ic.components import icwidget

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

__version__ = (0, 1, 6, 1)

DB_TYPES = [SQLITE_DB_TYPE, POSTGRES_DB_TYPE, MSSQL_DB_TYPE, MYSQL_DB_TYPE]

# Типы таблиц
TABLE_TYPE = 'Table'

# Типы полей
FIELD_TYPE = 'Field'
LINK_TYPE = 'Link'

MULTIPLE_JOIN_TAG = 0
RELATED_JOIN_TAG = 1

# Спецификация таблицы
SPC_IC_TABLE = {'type': TABLE_TYPE,
                'name': 'default',

                'description': '',
                'scheme': None,
                'table': None,
                'import': None,
                'filter': None,
                'child': [],    # Имена дочерних таблиц, Если организуется каскад, то обязательно!
                'source': None,
                'idx': None,

                '__parent__': icwidget.SPC_IC_SIMPLE,
                }

# Типы данных полей
TEXT_FIELD_TYPE = 'T'
DATE_FIELD_TYPE = 'D'
INT_FIELD_TYPE = 'I'
FLOAT_FIELD_TYPE = 'F'
DATETIME_FIELD_TYPE = 'DateTime'
BINARY_FIELD_TYPE = 'Binary'
PICKLE_FIELD_TYPE = 'PickleType'
BIGINT_FIELD_TYPE = 'BigInteger'
BOOLEAN_FIELD_TYPE = 'Boolean'
FIELD_VALUES_ALL_TYPES = (TEXT_FIELD_TYPE,
                          DATE_FIELD_TYPE, 
                          INT_FIELD_TYPE, 
                          FLOAT_FIELD_TYPE, 
                          DATETIME_FIELD_TYPE, 
                          BINARY_FIELD_TYPE, 
                          PICKLE_FIELD_TYPE,
                          BIGINT_FIELD_TYPE,
                          BOOLEAN_FIELD_TYPE)

# Спецификация поля
SPC_IC_FIELD = {'type': FIELD_TYPE,
                'name': 'default_field',

                'description': '',
                'default': None,
                'server_default': None,     # Значение по умолчанию, выполняемое на стороне сервера
                'label': '',
                'type_val': TEXT_FIELD_TYPE,
                'unique': False,    # Уникальность значения поля в таблице
                'nullable': True,   # Поле может иметь значение NULL?
                'len': -1,
                'store': None,
                'dict': {},
                'field': None,
                'attr': 0,
                'idx': None,

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'server_default': u'Значение по умолчанию, выполняемое на стороне сервера',
                                 'label': u'Надпись в формах',
                                 'unique': u'Уникальность значения поля в таблице',
                                 'nullable': u'Поле может иметь значение NULL?',
                                 },
                }

# Спецификация связи
SPC_IC_LNK = {'type': LINK_TYPE,
              'name': 'default_lnk',

              'description': '',
              'lnk_type': 'phisical',   # Жесткая/логическая связь
              'table': None,
              'del_cascade': False,
              'field': None,

              '__parent__': icwidget.SPC_IC_SIMPLE,
              '__attr_hlp__': {'lnk_type': u'Жесткая/логическая связь',
                               },
              }

# Кодировка  БД по умолчанию
DEFAULT_DB_ENCODING = 'utf-8'

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
    @param res: Ресурс БД.
    @return: Строка URL БД.
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
    @param db_url: URL связи с БД.
    @return: True - есть связь.
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

    def __init__(self, DB_=None, AutoScheme_=False):
        """
        Конструктор.
        @param DB_: Ресурсное описание БД.
        @param AutoScheme_: Автоматическое создание схемы.
        """
        icsourceinterface.icSourceInterface.__init__(self, DB_)
        # URL
        self._db_url = createDBUrl(DB_)
        # Связь с БД
        self._connection = None

        # Признак хранения строк в югикоде
        self.to_unicode = False

        self._db_type = None
        self._name = None
        self._metadata = None
        if DB_:
            if isinstance(DB_, dict):
                self._db_type = DB_['type']
                self._name = DB_['name']

            if not DB_.get('dbname', None):
                # Читаем параметры соединения из ini файла
                if ic.load_ini_param('SYSDB', 'DB_ENGINE') == self._db_type:
                    DB_ = self.load_ini_par(DB_)
                self._metadata = self._createDBMetadata(DB_)
                icSQLAlchemyDB.connections_pool[self._name] = self._metadata
            elif icSQLAlchemyDB.connections_pool.get(self._name, None):
                self._metadata = icSQLAlchemyDB.connections_pool[self._name]
            else:
                self._metadata = self._createDBMetadata(DB_)
                icSQLAlchemyDB.connections_pool[self._name] = self._metadata

        # Таблицы, зарегистрированные в БД
        self._tables = {}
        # Буфер сессии
        self._session = None

        if AutoScheme_:
            self.createScheme()
        if hasattr(self, 'countAttr'):
            self.countAttr('init_expr')

    def getDBUrl(self):
        """
        URL связи с БД.
        @return: Строку URL.
        """
        return self._db_url

    def checkConnect(self, db_url=None):
        """
        Проверка связи с БД.
        @param db_url: URL связи с БД.
        @return: True - есть связь.
        False - связь не установлена.
        """
        if db_url is None:
            db_url = self.getDBUrl()
        return checkDBConnect(db_url)

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
        return icobject.icObjectPassport((self._db_type, self._name, None, self._name+'.src', None))

    def getDBType(self):
        return self._db_type

    def _createDBMetadata(self, DBRes_=None):
        """
        Создание метаданных работы с БД.
        """
        # В качестве указания БД может быть указано, только имя БД
        if type(DBRes_) in (str, unicode):
            DBRes_ = resource.icGetRes(DBRes_, ext='src', bRefresh=False, nameRes=DBRes_)
        try:
            metadata = None
            try:
                connection_url = self._getConnectionURL(DBRes_)
                connection_args = self._getConnectionArgs(DBRes_)
                # Параметры кодировки БД
                encoding = DBRes_.get('encoding', 'UTF-8')
                if isinstance(encoding, unicode):
                    # ВНИМАНИЕ! В Unicode этот параметр быть не должен
                    # иначе ошибка в sqlalchemy появляется.
                    # Надо обязательно переводить в строку
                    encoding = str(encoding)
                self.to_unicode = DBRes_.get('convert_unicode', False)

                log.info('Create DB connection <%s : %s : %s>' % (self._name, connection_url, connection_args))
                log.info('\t->to_unicode: <%s>' % self.to_unicode)
                log.info('\t->encode: <%s>' % encoding)

                db_engine = sqlalchemy.create_engine(connection_url,
                                                     connect_args=connection_args,
                                                     strategy='plain',
                                                     pool_size=20,
                                                     encoding=encoding,
                                                     convert_unicode=self.to_unicode)

                metadata = sqlalchemy.MetaData(db_engine)
                metadata.name = DBRes_['name']
            except:
                log.fatal(u'Ошибка создания связи с БД <%s>.' % DBRes_['name'])
                ic_dlg.icErrBox(u'ОШИБКА', u'Ошибка создания связи с БД <%s>. Проверте параметры подключения!' % DBRes_['name'])
                return None
            return metadata
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка создания связи c БД <%s>.' % DBRes_['name'])
            ic_dlg.icErrBox(u'ОШИБКА', u'Ошибка создания связи c БД <%s>.' % DBRes_['name'])
            return None

    def _changeDialect(self, Buff_, NewDialect_):
        """
        Смена диалекта в буфере.
        Так как диалек на каждый тип БД должен быть только один, надо
        у всех БД, при создании новой БД, менять диалект
        Смена происходит только у БД того же типа
        """
        for name, db in Buff_.items():
            try:
                metadata = db.getMetaData()
                if metadata.engine._dialect.__class__.__name__ == NewDialect_.__class__.__name__:
                    metadata.engine._dialect = NewDialect_
            except:
                pass
        return Buff_

    def _getConnectionURL(self, DBRes_=None):
        """
        Создать по ресурсу БД URL связи с БД.
        """
        url = dict()
        url['drivername'] = self._connectionTypesCreate.setdefault(DBRes_['type'], None)
        if url['drivername'] is None:
            log.warning(u'Тип драйвера БД не поддерживается.')
            return None
        # Словарь
        url['query'] = DBRes_.get('query', None)

        if 'user' in DBRes_:
            url['username'] = DBRes_['user']
        if 'password' in DBRes_:
            url['password'] = DBRes_['password']
        if 'host' in DBRes_:
            url['host'] = DBRes_['host']
        if 'port' in DBRes_:
            url['port'] = DBRes_['port']
        if 'dbname' in DBRes_:
            url['database'] = DBRes_['dbname']
        if 'filename' in DBRes_ and 'path' in DBRes_:
            full_path = ''
            if DBRes_['filename'] and not DBRes_['path']:
                full_path = ic_file.AbsolutePath(DBRes_['filename'])
            elif DBRes_['filename'] and DBRes_['path']:
                full_path = ic_file.AbsolutePath(DBRes_['path']+DBRes_['filename'])
            else:
                log.warning(u'Ошибка определения файла БД: path: <%s> filename: <%s>' % (DBRes_['path'], DBRes_['filename']))
            # Проверка существования папки БД
            dir_path = ic_file.DirName(full_path)
            if not ic_file.Exists(dir_path):
                log.info(u'CREATE NEW DIR <%s>' % dir_path)
                ic_file.MakeDirs(dir_path)
            url['database'] = full_path

        url_obj = sqlalchemy.engine.url.URL(**url)
        return str(url_obj)

    def _getConnectionArgs(self, DBRes_=None):
        """
        Создать дополнительные аргументы для связи с БД.
        """
        args = self._connectionTypesConnectArgs.setdefault(DBRes_['type'], None)
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
            log.fatal(u'Connection error [SQLAlchemy:bind.connect()]')
            ic_dlg.icErrBox(u'ОШИБКА', u'Connection error [%s]. Verify db connection parameters!' % self._metadata)
            return None

    def createScheme(self, reCreate=True):
        """
        Создать схему БД (все таблицы в БД).
        @param reCreate: признак пересоздания схемы.
        """
        # Сначала отфильтровать таблицы которые не ссылаются на текущую БД
        if not self._tables or reCreate:
            tab_resources = resource.getResourcesByType(ext='tab', pathRes=None)
            tab_resources = dict([(tab_res_name, tab_res) for tab_res_name, tab_res in tab_resources.items() \
                                  if tab_res])
            tab_resources = dict([(tab_res_name, tab_res) for tab_res_name, tab_res in tab_resources.items() \
                                  if tab_res[tab_res.keys()[0]]['source'] == self.getName() or \
                                  tab_res[tab_res.keys()[0]]['source'] == self.getPsp()])
            for tab_res_name, tab_res in tab_resources.items():
                tab_spc = tab_res[tab_res.keys()[0]]
                tab_psp = ((tab_spc['type'], tab_spc['name'], None, ic_file.BaseName(tab_res_name), None),)
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
        @param db_url: URL связи с БД.
        @return: Объект связи с БД.
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

    def session(self, autoflush=True, autocommit=True):
        """
        Сессия. Используется для обеспечения
        транзакционного механизма.
        @param autoflush: Авто сброс?
            Для транзакций установить в False.
        @param autocommit: Авто комитить?
            Для транзакций установить в False.
        @return: Объект сессии/Транзакции.
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
        >>> obj_lst = r.filter('id < 100').all()
        @param tab_name: Имя таблицы.
        @param sess: Сессия.
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
                self.session().query(mapper or dct.values()[0].getMapperClass()).get(1)

    def getTables(self):
        """
        Зарегистрированные в БД таблицы.
        """
        return self._tables
    
    def getTableByName(self, name):
        return self._tables.get(name, None)

    def _isSQLReturnResult(self, SQLQuery_):
        """
        Проверка, должен ли результат запроса возвращать значения.
        @param SQLQuery_: Строка запроса.
        """
        return bool(SQLQuery_.lower().find('select') != -1)

    def executeSQL(self, SQLQuery_, to_dict=False):
        """
        Выполнить строку запроса.
        @param SQLQuery_: Строка запроса.
        @param to_dict: Преобразовать все записи в словари?
        @return: Возвражает словарь {'__fields__':((..),(..),..),'__data__':[(..),(..),..]}.
        Или None в случае ошибки.
        """
        result = None
        # Выполнить запрос
        try:
            # Доступ к конекшену DBAPI2
            connection = self._metadata.bind.connect().connection
            cursor = connection.cursor()
            cursor.execute(SQLQuery_)
            if self._isSQLReturnResult(SQLQuery_):
                fields = cursor.description
                # log.debug(u'SQL: %s RESULT FIELDS: %s' % (ic_str.toUnicode(SQLQuery_), fields))
                data = cursor.fetchall()
                if data and to_dict:
                    new_data = [dict([(fields[i][0], val) for i, val in enumerate(rec)]) for rec in data]
                    data = new_data
                result = copy.deepcopy({'__fields__': fields, '__data__': data})
            cursor.close()
        except:
            err_txt = u'Ошибка выполнения запроса <%s>' % ic_str.toUnicode(SQLQuery_)
            log.fatal(err_txt)
            ic_dlg.icErrBox(u'ОШИБКА', err_txt)

            return None

        return result

    def select(self, *args, **kwargs):
        """
        Выбрать список объектов из класса данных.
        См. описание функции select в SQLAlchemy.
        @param columns: Объекты колонок которые нужно выбрать.
        @param whereclause: Условие выбора.
        @param from_obj: Таблицы из которых производится выбор.
        @return: Возвражает объект SelectResults.
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
        return lock.LockTable(name)

    def unLockTable(self, name):
        """
        Разблокирует таблицу.
        """
        return lock.UnLockTable(name)

    def LockRec(self, name, id, LockRec_=None):
        """
        Блокировка записи.
        """
        if LockRec_ is None:
            comp_name = lock.ComputerName()
            user_name = ic_user.getCurUserName()
            LockRec_ = str({'computer': comp_name, 'user': user_name})
        result = lock.LockRecord(name, id, LockRec_)
        log.debug(u'LOCK_RECORD <%s : %s : %s : %s>' % (name, id, LockRec_, result))
        if result != 0:
            return False
        return True

    def unLockRec(self, name, id):
        """
        Разблокирует запись.
        """
        if not self.IsLockRec(name, id):
            log.debug(u'UNLOCK_RECORD <%s : %s>' % (name, id))
            return lock.unLockRecord(name, id)
        return False

    def IsLockTable(self, name):
        """
        Возвращает признак блокировки таблицы.
        """
        return lock.isLockTable(name)

    def IsLockRec(self, name, id):
        """
        Возвращает признак блокировки записи.
        """
        lock_msg = lock.readMessage(name, id)

        if lock_msg:
            lock_rec = eval(lock_msg)
            # Если блокировка поставлена тем же пользователем,
            # тогда не считается что заблокировано
            log.debug(u'IS LOCK <%s : %s> ' % (lock_rec, type(lock_rec)))
            if lock_rec and lock_rec['user'] == ic_user.getCurUserName():
                return False
            return lock.isLockRecord(name, id)
        return False

    def releaseConnection(self, conn):
        """
        Освобождает соединение.
        """
        pass


class icSQLAlchemyDataClass(icdataclassinterface.icDataClassInterface, object):
    """
    Таблица.
    """
    _regDB = {}     # Зарегистрированные БД

    def __init__(self, Tab_, TabResName_=None, ReCreate_=False, Refresh_=False, DB_=None):
        """
        Конструктор.
        @param Tab_: Ресурсное описание класса данных/таблицы.
        @param TabResName_: Указание ресурса описаний классов данных.
        @param ReCreate_: Флаг пересоздания класса таблицы.
            По умолчанию не пересоздавать.
        @param Refresh_: Признак обовления ресурсного описания.
        """
        icdataclassinterface.icDataClassInterface.__init__(self, Tab_)

        # Родительские таблицы
        self._parent_tables = {}

        # Дочерние таблицы
        self._children_tables = {}

        # БД
        self.db = DB_
        if self.db is None:
            if Tab_['source'] and isinstance(Tab_['source'], tuple):
                self.db = self._createDB(Tab_['source'][0][1], Tab_['source'])
            else:
                # Вдруг определен родитель и тогда можно взять БД у него
                if hasattr(self, 'parent') and self.parent and issubclass(self.parent.__class__, icSQLAlchemyDataClass):
                    self.db = self.parent.db
                else:
                    log.warning(u'Не назначена  БД у таблицы <%s>' % self.getResource()['name'])
        else:
            # Зарегистрировать БД
            self._registerDB(self.db.getName(), self.db)

        self.dataclass = self._createDataClass(Tab_)
        if self.dataclass is not None:
            if not ic_mode.isRuntimeMode():
                # Если в режиме редактирования, то сразу провести
                # синхронизацию с БД.
                sync_ok = self.syncDB()
                if sync_ok:
                    ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Различие структур таблицы <%s> в описании и БД. В БД создана копия таблицы <%s>. Старая таблица удалена.' % (self.dataclass.name, self.dataclass.name))

        # Маппер
        self._mapper_class = None

        # Последние добавленные идентификаторы
        self._last_inserted_ids = list()

    def _get_to_unicode(self):
        """
        Признак перекодирования в Юникод.
        """
        if self.db:
            return self.db.to_unicode
        return False

    def _registerDB(self, DBName_, DB_):
        """
        Зарегистрировать БД.
        """
        if DB_ and DB_.getMetaData():
            self._regDB = DB_._changeDialect(self._regDB, DB_.getMetaData().bind.dialect)
        self._regDB[DBName_] = DB_

    def _createDB(self, DBName_, DBPsp_):
        """
        Создание БД.
        """
        if DBName_ in self._regDB:
            db=self._regDB[DBName_]
            return db

        db = None
        try:
            # Создание БД через ядро
            db = self.GetKernel().Create(DBPsp_)
        except AttributeError:
            # Если не получилось, то по старому
            db_res = resource.icGetRes(DBName_, 'src', nameRes=DBName_)
            db = icSQLAlchemyDB(db_res, False)

        # Зарегистрировать БД
        self._registerDB(DBName_, db)
        return db

    def _createDataClass(self, TabRes_, AutoCreate_=True, ReCreate_=False):
        """
        Создание объекта таблицы.
        @param TabRes_: Ресурс таблицы.
        @param AutoCreate_: Автоматически создать в БД?
        @param ReCreate_: Признак пересоздания таблицы.
        """
        tab_name = TabRes_['name']
        log.info(u'Создание объекта таблицы <%s>' % tab_name)

        # Зарегистрировать таблицу в БД
        if self.db:
            self.db._tables[tab_name] = self

        if TabRes_['table']:
            tab_name = self.getAliasTableName()

        tab = None
        if self.db:
            metadata = self.db.getMetaData()
            try:
                if tab_name in metadata.tables and not ReCreate_:
                    log.debug(u'GET FROM BUFFER. TABLE <%s>' % tab_name)
                    # Проверить таблицу на изменение структуры
                    # Если структура изменена, тогда сигнализировать ошибку
                    fields_with_id_count = len(TabRes_['child'])+1
                    if len(metadata.tables[tab_name].columns) != fields_with_id_count:
                        log.warning(u'Ошибка создания таблицы <%s>!' % tab_name)
                        ic_dlg.icWarningBox(u'ВНИМАНИЕ',
                                            u'В системе существует таблица <%s> с другой структурой!' % tab_name)
                        assert None, u'Table <%s> change structure!!!' % tab_name
                        return None
                    return metadata.tables[tab_name]

                if AutoCreate_:
                    tab = sqlalchemy.Table(tab_name, metadata)
                    if not tab.exists():
                        # Таблицы нет и нужно ее создать
                        if tab_name in metadata.tables:
                            metadata.remove(metadata.tables[tab_name])
                        tab = self._create(TabRes_)
                        try:
                            tab.create()
                        except:
                            log.fatal()
                    else:
                        # Перегрузить таблицу с описанием колонок
                        metadata.remove(metadata.tables[tab_name])
                        tab = self._create(TabRes_)
                else:
                    # Таблицы нет и нужно ее создать
                    tab = self._create(TabRes_)

                log.info(u'CREATE TABLE <%s>' % tab_name)
            except:
                log.fatal(u'Ошибка создания объекта таблицы %s' % tab_name)
                ic_dlg.icErrBox(u'ОШИБКА', u'Create DataClass [%s] Error. Verify db connection parameters!' % tab_name)

        return tab

    def _create(self, TabRes_):
        """
        Создать таблицу в БД.
        @param TabRes_: Ресурс таблицы.
        """
        tab_name = TabRes_['name']
        if TabRes_['table']:
            tab_name = self.getAliasTableName()
        log.info(u'Создание таблицы <%s> в БД' % tab_name)

        table = None
        columns = [sqlalchemy.Column(self.getIdName(), sqlalchemy.Integer, primary_key=True)]
        # Создание колонок
        for fld in TabRes_['child']:
            if fld['type'] == 'Field':
                field = self._createField(fld)
            elif fld['type'] == 'Link':
                field = self._createLink(fld)
            else:
                log.warning(u'Тип поля не определен <%s>' % fld['type'])
            columns.append(field)
        # Создание таблицы
        try:
            args = tuple([tab_name, self.db.getMetaData()]+columns)
            table = sqlalchemy.Table(*args)
            log.info(u'Таблица <%s> создана в БД' % table)
        except:
            log.fatal(u'Ошибка создания sqlalchemy таблицы <%s>' % tab_name)
        return table

    _FieldTypes2SQLAlchemyTypes = {INT_FIELD_TYPE: sqlalchemy_field_type_Integer,
                                   TEXT_FIELD_TYPE: sqlalchemy_field_type_Text,
                                   FLOAT_FIELD_TYPE: sqlalchemy_field_type_Float,
                                   DATE_FIELD_TYPE: sqlalchemy_field_type_Text,
                                   DATETIME_FIELD_TYPE: sqlalchemy_field_type_DateTime,
                                   BINARY_FIELD_TYPE: sqlalchemy_field_type_Binary,
                                   PICKLE_FIELD_TYPE: sqlalchemy_field_type_PickleType,
                                   BIGINT_FIELD_TYPE: sqlalchemy_field_type_BigInteger,
                                   BOOLEAN_FIELD_TYPE: sqlalchemy_field_type_Boolean,
                                   }

    def _createField(self, FieldRes_):
        """
        Создать объект поля таблицы.
        @param FieldRes_: Ресурс поля.
        """
        name = FieldRes_['field']
        if name is None:
            name = FieldRes_['name'].lower()
        log.info(u'Создание поля <%s>' % name)
        # Проверка на корректность создания поля
        if 'activate' in FieldRes_:
            if FieldRes_['activate'] in (0, False, 'false', 'FALSE', '0'):
                FieldRes_['activate'] = 0
            else:
                FieldRes_['activate'] = 1
            if not FieldRes_['activate']:
                return None

        typ = self._FieldTypes2SQLAlchemyTypes.setdefault(FieldRes_['type_val'], sqlalchemy_field_type_Text)
        len = FieldRes_['len']
        if typ == sqlalchemy_field_type_Text:
            if len is not None and len > 0:
                typ = sqlalchemy_field_type_String(len)
            else:
                typ = sqlalchemy_field_type_Text
        elif typ == sqlalchemy_field_type_PickleType:
            typ = sqlalchemy_field_type_PickleType(0)

        # Уникальность
        unique = FieldRes_.get('unique', False)
        # В поле может быть значение NULL?
        nullable = FieldRes_.get('nullable', True)
        # Значение по умолчанию
        default = FieldRes_.get('default', None)

        # Значение по умолчанию, выполняемое на стороне сервера
        server_default = None
        if not default and FieldRes_.get('server_default', None):
            server_default = sqlalchemy.text(FieldRes_['server_default'])

        # Подготовка аргументов конструктора колонки
        kwargs = {'unique': unique,
                  'nullable': nullable,
                  }
        if server_default:
            kwargs['server_default'] = server_default

        return sqlalchemy.Column(name, typ, **kwargs)

    def _createLink(self, LinkRes_):
        """
        Создать связь с таблицей.
        @param LinkRes_: Ресурс связи.
        """
        name = None
        if 'field' in LinkRes_:
            name = LinkRes_['field']
        if name is None:
            name = LinkRes_['name'].lower()
        log.info(u'Создание связи с таблицей <%s>' % name)

        # Проверка на корректность создания поля
        if 'activate' in LinkRes_:
            if LinkRes_['activate'] in (0, False, 'false', 'FALSE', '0'):
                LinkRes_['activate'] = 0
            else:
                LinkRes_['activate'] = 1

            if not LinkRes_['activate']:
                return None

        link_tab_psp = LinkRes_['table']
        if link_tab_psp:
            link_tab = link_tab_psp[0][1]
            # Прописать таблицу в родительской
            if self.db:
                if link_tab not in self.db._tables:
                    # Создать родительскую таблицу, если она не создана
                    try:
                        parent_table = self.GetKernel().Create(link_tab_psp)
                    except:
                        parent_table = icSQLAlchemyTabClass(link_tab)
                    self._parent_tables[parent_table.getDBTableName()] = parent_table

                if link_tab in self.db._tables:
                    self.db._tables[link_tab]._children_tables[self.getResource()['name']] = self

            # Поддержка жестких и логических связей
            if 'lnk_type' in LinkRes_ and LinkRes_['lnk_type'] == 'logical':
                return sqlalchemy.Column(name, sqlalchemy_field_type_Integer)
            else:
                return sqlalchemy.Column(name, sqlalchemy_field_type_Integer,
                                         sqlalchemy.ForeignKey('%s.id' % link_tab))
        return None

    def getAliasTableName(self):
        """
        Альтернативное имя таблицы.
        """
        tab_res = self.getResource()

        tab_alias = tab_res.get('table', '')
        tab_name = tab_res.get('name', None)
        if tab_alias.startswith('@'):
            tab_name = util.ic_eval(tab_res['table'])
        elif tab_alias:
            tab_name = tab_alias
        return tab_name

    def getDataClassC(self):
        if self.dataclass is not None:
            return self.dataclass.c
        return None

    # Перенаправление вызова свойства self.c на self.dataclass.c
    c = property(getDataClassC)

    def getFieldNames(self, IsID_=False):
        """
        Список имен полей таблицы.
        @param IsID_: С идентификационным полем?
        """
        if self.dataclass is not None:
            if IsID_:
                result = [column.name.encode() for column in self.dataclass.columns]
            else:
                result = [column.name.encode() for column in self.dataclass.columns if column.name != u'id']
        else:
            res = self.getResource()
            if IsID_:
                result = ['id']+[field['field'] for field in res['child']]
            else:
                result = [field['field'] for field in res['child']]
        return result

    def getFieldIdx(self, FieldName_):
        """
        Индекс поля таблицы.
        @param FieldName_: Имя поля таблицы.
        """
        fld_names = self.getFieldNames(True)
        try:
            return fld_names.index(FieldName_)
        except ValueError:
            # Нет такого поля в этой таблице
            log.error(u'Поле <%s> не определено в таблице <%s>' % (FieldName_, self.getDBTableName()))
            return -1
        
    def getFieldType(self, FieldName_):
        """
        Тип поля по его имени.
        @param FieldName_: Имя поля таблицы.
        """
        if self.dataclass is not None:
            try:
                field = [field for field in self.getResource()['child'] if field['name'] == FieldName_][0]
            except IndexError:
                return None
            return field['type_val']
        return None

    def getFieldLength(self, FieldName_):
        """
        Длина поля по его имени.
        @param FieldName_: Имя поля таблицы.
        """
        if self.dataclass is not None:
            try:
                field = [field for field in self.getResource()['child'] if field['name'] == FieldName_][0]
            except IndexError:
                return None
            return field['len']
        return None

    def getConnection(self):
        """
        Возвращает объект соединения с базой данных.
        """
        return self.db.getConnection()

    def getDB(self):
        """
        БД.
        """
        return self.db

    def getClassName(self):
        """
        Возвращает имя класса данных.
        """
        if self.dataclass is not None:
            return self.dataclass.name
        return None

    def getDBTableName(self):
        """
        Возвращает имя таблицы в базе данных, соответствующих данному классу
        данных.
        """
        if self.dataclass is not None:
            tab_name = self.dataclass.name
            if isinstance(tab_name, unicode):
                tab_name = tab_name.encode()
            return tab_name
        return None

    def setDBTableName(self, db_tab_name):
        """
        Установить имя таблицы в базе данных, соответствующих данному классу
        данных.
        @param db_tab_name: Новое имя таблицы в БД.
        """
        if self.dataclass is not None:
            self.dataclass.name = db_tab_name
        else:
            log.warning(u'Не определен класс данных SQLAlchemy при установке имени таблицы в БД')

    def getDBColumnNameDict(self):
        """
        Возвращает словарь соответствий между именами атрибутов в классе данных
        и именами полей в базе.
        """
        if self.dataclass is not None:
            dbColumnDict = dict()

            for column in self.dataclass.columns:
                dbName = column.name
                dbColumnDict[dbName] = column.name

            return dbColumnDict
        return dict()

    def getIdName(self):
        """
        Возвращает имя поля с уникальным идентификатором (обычно 'id')
        """
        return 'id'

    def delete(self, id):
        """
        Удаления объекта класса данных.

        @type id: C{int}
        @param id: Идентификатор объекта.
        """
        if self.dataclass is not None:
            try:
                row = self.dataclass.delete(self.dataclass.c.id == id).execute()
                return coderror.IC_DEL_OK
            except:
                log.fatal(u'Ошибка удаления записи.')
        return coderror.IC_DEL_FAILED

    def del_where(self, *args, **kwargs):
        """
        Удалить все записи по условию выбора.
        ВНИМАНИЕ! Пример использования:
        tab.del_where(icsqlalchemy.and_(tab.c.uuid == obj_uuid))
        или
        tab.del_where(icsqlalchemy.and_(tab.c.type == sprav_type,
                                        tab.c.cod == cod))
        """
        try:
            return self.dataclass.delete(*args, **kwargs).execute()
        except:
            log.fatal(u'Ошибка удаления записей из таблицы по условию')

    def del_where_transact(self, where, transaction=None):
        """
        Удалить записи из таблицы.
        Переписанные низкоуровневые операции с поддержкой транзакций.
        @param where: Условие выбора записей (SQLAlchemy).
            Например:
                icsqlalchemy.and_(tab.c.uuid == obj_uuid)
            или
                icsqlalchemy.and_(tab.c.type == sprav_type,
                                  tab.c.cod == cod)
        @param transaction: Объект транзакции.
        @return: True/False.
        """
        if self.dataclass is None:
            log.warning(u'Не определен dataclass у объекта таблицы <%s>' % self.getClassName())
            return False

        sql = self.dataclass.delete().where(where)

        if transaction:
            transaction.execute(sql)
            return True
        else:
            log.warning(u'Не определен объект транзакии в функции добавления записи')
        return False

    def _str(self, Value_):
        if Value_ is None:
            return Value_

        if self._get_to_unicode():
            if not isinstance(Value_, unicode):
                return unicode(str(Value_), DEFAULT_DB_ENCODING)
            else:
                return Value_
        else:
            if isinstance(Value_, unicode):
                return Value_.encode(DEFAULT_DB_ENCODING)
        try:
            return str(Value_)
        except TypeError:
            return Value_

    def _int(self, Value_):
        if not Value_:
            return 0
        try:
            return int(float(Value_))
        except TypeError:
            return Value_

    def _float(self, Value_):
        if not Value_:
            return 0.0
        try:
            return float(Value_)
        except TypeError:
            return Value_

    def _datetime(self, Value_):
        if not Value_:
            return None
        return Value_

    def _bin(self, Value_):
        if not Value_:
            return None
        return Value_

    def _pickle(self, Value_):
        if not Value_:
            return None
        return Value_

    _fieldTypeConvert = {TEXT_FIELD_TYPE: _str,
                         FLOAT_FIELD_TYPE: _float,
                         INT_FIELD_TYPE: _int,
                         DATE_FIELD_TYPE: _str,
                         DATETIME_FIELD_TYPE: _datetime,
                         BINARY_FIELD_TYPE: _bin,
                         PICKLE_FIELD_TYPE: _pickle,
                         BIGINT_FIELD_TYPE: _int,
                         BOOLEAN_FIELD_TYPE: _int,
                         }

    def _prepareRecData(self, RecData_):
        """
        Приведение данных записи к типу.
        @param RecData_: Словарь или список записи.
        """
        try:
            if isinstance(RecData_, dict):
                # Строка задана словарем
                fields = [fld for fld in self.getResource()['child'] if fld['type'] == 'Field']
                for field in fields:
                    if field['name'] in RecData_:
                        try:
                            # Пробуем привести типы
                            RecData_[field['name']] = self._fieldTypeConvert[field['type_val']](self, RecData_[field['name']])
                        except:
                            # Не получилось ну и ладно
                            log.error(u'''Ошибка приведения типа.
                            Поле <%s> Тип <%s> Значение <%s> Тип значения <%s>''' % (field['name'],
                                                                                     field['type_val'],
                                                                                     RecData_[field['name']],
                                                                                     type(RecData_[field['name']])))
            elif isinstance(RecData_, tuple):
                # Строка задана кортежем
                rec_data = list(RecData_)
                len_rec_data = len(rec_data)
                for i, field in enumerate(self.getResource()['child']):
                    if i < len_rec_data:
                        try:
                            # Пробуем привести типы
                            rec_data[i] = self._fieldTypeConvert[field['type_val']](self, rec_data[i])
                        except:
                            # Не получилось ну и ладно
                            log.error(u'''Ошибка приведения типа.
                            Поле <%s> Тип <%s> Значение <%s> Тип значения <%s>''' % (field['name'],
                                                                                     field['type_val'],
                                                                                     rec_data[i],
                                                                                     type(rec_data[i])))
                            pass
                    else:
                        break
                RecData_ = tuple(rec_data)
            elif isinstance(RecData_, list):
                # Строка задана списком
                rec_data = RecData_
                len_rec_data = len(rec_data)
                for i, field in enumerate(self.getResource()['child']):
                    if i < len_rec_data:
                        try:
                            # Пробуем привести типы
                            rec_data[i] = self._fieldTypeConvert[field['type_val']](self, rec_data[i])
                        except:
                            # Не получилось ну и ладно
                            log.error(u'''Ошибка приведения типа.
                            Поле <%s> Тип <%s> Значение <%s> Тип значения <%s>''' % (field['name'],
                                                                                     field['type_val'],
                                                                                     rec_data[i],
                                                                                     type(rec_data[i])))
                            pass
                    else:
                        break
                RecData_ = rec_data
        except:
            log.fatal(u'Ошибка приведения типов записи')

        return RecData_

    def _record_norm(self, RecData_):
        """
        Правильно представить запись для использования ее в функции добавления/обновления.
        """
        for item in RecData_.items():
            if isinstance(item[0], unicode):
                new_item = item[0].encode()
                del RecData_[item[0]]
                RecData_[new_item] = item[1]
        return RecData_

    def add(self, *args, **kwargs):
        """
        Добавить объект.
        @return: Возвращает объект управления добавленной записью.
        Получить идентификатор добавленной записи, как
        InsertObject.last_inserted_ids()[-1].
        """
        if self.dataclass is not None:
            fields = None
            try:
                # Подготовить данные
                args = self._prepareRecData(args)
                row = None
                if args:
                    row = self.dataclass.insert(values=args).execute()
                elif kwargs:
                    # Добавить значения по умолчанию не используемых полей
                    fields = self.getDefaultRecDict()
                    fields.update(kwargs)
                    fields = self._prepareRecData(fields)

                    row = self.dataclass.insert().execute(**fields)
                # Запомнить последние добавленные идентификаторы
                self._last_inserted_ids = row.inserted_primary_key
                return row
            except:
                log.fatal(u'Ошибка добавления записи. Fields: <%s>' % fields)
        return None

    def add_rec_transact(self, rec=None, transaction=None):
        """
        Добавить запись в таблицу.
        Переписанные низкоуровневые операции с поддержкой транзакций.
        @param rec: Запись таблицы.
        @param transaction: Объект транзакции.
        @return: True/False.
        """
        if self.dataclass is None:
            log.warning(u'Не определен dataclass у объекта таблицы <%s>' % self.getClassName())
            return False
        if rec is None:
            log.warning(u'Не определена запись для добавления в талицу <%s>' % self.getClassName())
            return False

        # Подготовить данные
        # Добавить значения по умолчанию не используемых полей
        fields = self.getDefaultRecDict()
        fields.update(rec)
        fields = self._prepareRecData(fields)

        sql = self.dataclass.insert().values(**fields)
        if transaction:
            result = transaction.execute(sql)
            # Запомнить последние добавленные идентификаторы
            self._last_inserted_ids = result.inserted_primary_key
            return
        else:
            log.warning(u'Не определен объект транзакии в функции добавления записи')
        return False

    def getLastInsertedIds(self):
        """
        Последние добавленные идентификаторы.
        """
        return self._last_inserted_ids

    def getLastInsertedId(self):
        """
        Последний добавленный идентификатор.
        """
        return self._last_inserted_ids[-1]

    def update(self, id, *args, **kwargs):
        """
        Изменить объект.
        @param id: Идентификатор записи.
        """
        if self.dataclass is not None:
            try:
                # Подготовить данные
                _args = self._prepareRecData(args)
                _kwargs = self._prepareRecData(kwargs)
                if _args:
                    row = self.dataclass.update(self.dataclass.c.id == id).execute(*_args)
                if _kwargs:
                    row = self.dataclass.update(self.dataclass.c.id == id).execute(**_kwargs)
                return row
            except:
                log.fatal(u'Ошибка изменения записи.')

        return None

    def update_rec_transact(self, rec_id, rec=None, transaction=None):
        """
        Изменить запись в таблице.
        Переписанные низкоуровневые операции с поддержкой транзакций.
        @param rec_id: Идентификатор записи.
        @param rec: Запись таблицы в виде словаря.
        @param transaction: Объект транзакции.
        @return: True/False.
        """
        if self.dataclass is None:
            log.warning(u'Не определен dataclass у объекта таблицы <%s>' % self.getClassName())
            return False
        if rec is None:
            log.warning(u'Не определена запись для изменения в талицу <%s>' % self.getClassName())
            return False
        # Подготовить данные
        fields = self._prepareRecData(rec)
        sql = self.dataclass.update(self.dataclass.c.id == rec_id).values(**fields)
        if transaction:
            transaction.execute(sql)
            return True
        else:
            log.warning(u'Не определен объект транзакии в функции изменения записи')
        return False

    def update_where(self, where, *args, **kwargs):
        """
        Изменить объект.
        @param where: Условие выборки.
        """
        if self.dataclass is not None:
            try:
                # Подготовить данные
                _args = self._prepareRecData(args)
                _kwargs = self._prepareRecData(kwargs)

                row = None
                if _args:
                    row = self.dataclass.update(where).execute(*_args)
                if _kwargs:
                    row = self.dataclass.update(where).values(**_kwargs).execute()
                return row
            except:
                log.fatal(u'Ошибка изменения записи.')
        return None

    def get(self, id):
        """
        Получить объект.
        """
        if self.dataclass is not None:
            try:
                return self.dataclass.select(self.dataclass.c.id == id).execute()
            except:
                log.fatal(u'Ошибка получения записи.')
        return None

    def get_where(self, *args, **kwargs):
        """
        Получить запись по условию.
        ВНИМАНИЕ! Пример использования:
        tab.get_where(icsqlalchemy.and_(tab.c.uuid == obj_uuid))
        или
        tab.get_where(icsqlalchemy.and_(tab.c.type == sprav_type,
                                        tab.c.cod == cod))
        """
        if self.dataclass is not None:
            return self.dataclass.select(*args, **kwargs).execute()
        return None

    def get_where_transact(self, where=None, transaction=None):
        """
        Получить записи по условию.
        Переписанные низкоуровневые операции с поддержкой транзакций.
        ВНИМАНИЕ! Пример использования:
        tab.get_where_transact(where=icsqlalchemy.and_(tab.c.uuid == obj_uuid),
                               transaction=transaction)
        или
        tab.get_where_transact(where=icsqlalchemy.and_(tab.c.type == sprav_type,
                                        tab.c.cod == cod), transaction=transaction)
        """
        if self.dataclass is not None:
            sql = self.dataclass.select(where)
            if transaction:
                result = transaction.execute(sql)
                return result
            else:
                log.warning(u'Не определена транзакция для операции с транзакции')
        return None

    def is_id(self, id):
        """
        Проверить есть ли такой идентификатор в таблице.
        """
        if self.dataclass is not None:
            return self.dataclass.get(id) is not None
        return None

    def count(self, *args, **kwargs):
        """
        Количество записей, соответствующих запросу sqlalchemy.
        @return: Количество записей.
        """
        if self.dataclass is not None:
            # log.debug(u'\tSQL COUNT: %d' % self.dataclass.select(*args, **kwargs).execute().rowcount)
            return self.dataclass.select(*args, **kwargs).execute().rowcount
        return -1

    def select(self, *args, **kwargs):
        """
        Выбрать список объектов из класса данных.
        ВНИМАНИЕ! Пример использования:
        tab.select(icsqlalchemy.and_(tab.c.uuid == obj_uuid))
        или
        tab.select(icsqlalchemy.and_(tab.c.type == sprav_type,
                                     tab.c.cod == cod))

        @return: Возвражает объект SelectResults.
        """
        if self.dataclass is not None:
            return self.dataclass.select(*args, **kwargs).execute()
        return None

    def _decodeUnicode(self, Struct_):
        """
        Обратное преобразование из юникода в строку.
        """
        if isinstance(Struct_, list):
            # Список
            for i, value in enumerate(Struct_):
                value = self._decodeUnicode(value)
                Struct_[i] = value

        elif isinstance(Struct_, tuple):
            # Кортеж
            Struct_ = tuple(self._decodeUnicode(list(Struct_)))

        elif isinstance(Struct_, dict):
            # Словарь
            for key, value in Struct_.items():
                key_new = self._decodeUnicode(key)
                value_new = self._decodeUnicode(value)
                del Struct_[key]
                Struct_[key_new] = value_new

        elif isinstance(Struct_, unicode):
            # Строка юникод
            return Struct_.encode(DEFAULT_DB_ENCODING)

        else:
            # Оставить без изменений все другие типы
            return Struct_
        return Struct_

    def _encodeUnicode(self, Struct_):
        """
        Преобразование из строки в юникод.
        """
        if isinstance(Struct_, list):
            # Список
            for i, value in enumerate(Struct_):
                value = self._encodeUnicode(value)
                Struct_[i] = value

        elif isinstance(Struct_, tuple):
            # Кортеж
            Struct_ = tuple(self._encodeUnicode(list(Struct_)))

        elif isinstance(Struct_, dict):
            # Словарь
            for key, value in Struct_.items():
                key_new = self._encodeUnicode(key)
                value_new = self._encodeUnicode(value)
                del Struct_[key]
                Struct_[key_new] = value_new

        elif isinstance(Struct_, str):
            # Строка юникод
            return unicode(Struct_, DEFAULT_DB_ENCODING)
        else:
            # Оставить без изменений все другие типы
            return Struct_
        return Struct_

    def listRecs(self, SQLResult_):
        """
        Приведение результата запроса к списку кортежей.
        """
        try:
            recs = [tuple(rec) for rec in list(SQLResult_)]
            if self._get_to_unicode():
                recs = self._decodeUnicode(recs)
            return recs
        except:
            log.fatal(u'Ошибка приведения результата запроса <%s> к списку кортежей' % str(SQLResult_))
            return None

    def listRecsUnicode(self, SQLResult_):
        """
        Приведение результата запроса к списку кортежей где строки в виде Unicode.
        """
        try:
            recs = [tuple(rec) for rec in list(SQLResult_)]
            return self._encodeUnicode(recs)
        except:
            log.fatal(u'Ошибка приведения результата запроса <%s> к списку кортежей c Unicode-строками' % str(SQLResult_))
            return None

    def _encodeTextSQL(self, SQL_):
        """
        Приведение к юникоду строки запроса.
        """
        try:
            if self._get_to_unicode():
                SQL_ = self._encodeUnicode(SQL_)
            return SQL_
        except:
            log.fatal(u'Ошибка приведения текста запроса <%s> к юникоду' % SQL_)
            return SQL_

    def _str2SQL(self, Value_):
        """
        Преобразавание значени по типу поля в текст значения в SQL запросе.
        """
        return '\''+self._str(Value_)+'\''

    _fieldType2SQLTxt = {TEXT_FIELD_TYPE: _str2SQL,
                         FLOAT_FIELD_TYPE: _float,
                         INT_FIELD_TYPE: _int,
                         DATE_FIELD_TYPE: _str2SQL,
                         BIGINT_FIELD_TYPE: _int,
                         BOOLEAN_FIELD_TYPE: _int,
                         }

    def _structFilter2SQLTxt(self, Filter_=None, SQLWhereJoin_='AND'):
        """
        Перевод структурного фильтра в SQL представление.
        """
        if Filter_ is None:
            # Если фильтр не указывается то имеется ввиду что
            # нужно выбрать все записи
            return 'SELECT * FROM %s' % self.getDBTableName()
        elif isinstance(Filter_, dict):
            sql_txt = 'SELECT * FROM %s ' % self.getDBTableName()
            sql_where_join = ' '+SQLWhereJoin_+' '
            where_txt = sql_where_join.join(['%s=%s' % (fld_name, self._fieldType2SQLTxt[self.getFieldType(fld_name)](self, fld_value)) for fld_name, fld_value in Filter_.items()])
            sql_txt += 'WHERE '+where_txt
            log.debug(u'CONVERT STRUCT FILTER <%s> TO SQL: \'%s\'' % (Filter_, sql_txt))
            return sql_txt
        else:
            log.warning(u'Ошибка преобразования фильтра %s' % Filter_)
        return None

    def queryAll(self, *args, **kwargs):
        """
        Выполнить запрос класса данных.
        @return: Возвращает список кортежей.
        """
        if self.db:
            try:
                if len(args) == 1 and type(args[0]) in (str, unicode):
                    # Если запрос задается строкой,
                    # то сразу перекодировать его юникод
                    args = (self._encodeTextSQL(args[0]),)
                elif len(args) == 1 and isinstance(args[0], dict):
                    # Задан структурный фильтр
                    # Сначала нужно перевести его в строковое представление
                    sql_txt = self._structFilter2SQLTxt(args[0])
                    # Затем перекодировать в юникод
                    sql_txt = self._encodeTextSQL(sql_txt)
                    args = (sql_txt,)
                conn = self.getConnection()
                if args or kwargs:
                    sql_result = conn.execute(*args, **kwargs)
                else:
                    # Если параметры выборки не указаны, то вернуть всю таблицу
                    sql_result = conn.execute(self.dataclass.select())
                return self.listRecsUnicode(sql_result.fetchall())
            except:
                log.fatal(u'Ошибка выполнения запроса: <%s>, <%s>' % (args, kwargs))
        else:
            log.warning(u'Не определена БД  в таблице <%s>' % self.getResource()['name'])
        return None

    def queryRecs(self, SQLQuery_):
        """
        Выполнить запрос класса данных.
        @param SQLQuery_: Строка запроса.
        @return: Возвражает список объектов icSQLRecord.
        """
        if self.db:
            # Выполнить запрос
            return self.db.executeSQL(SQLQuery_)
        return None

    def executeSQL(self, SQLQuery_):
        """
        Выполнить строку запроса.
        @param SQLQuery_: Строка запроса.
        @return: Возвражает список объектов icSQLRecord.
        """
        return self.queryRecs(SQLQuery_)

    def convQueryToSQL(self, SQLText_):
        """
        Конвертация запроса в терминах класса в SQL запрос.
        @param SQLText_: Текст SQL запроса.
        """
        tab_class_name = self.getClassName()
        tab_real_name = self.getDBTableName()
        sql_txt = SQLText_.replace(tab_class_name, tab_real_name)
        return sql_txt

    def _get_drop_sql_txt(self, Cascade_):
        """
        Текст запроса удаления таблицы из БД.
        @param Cascade_: Признак удаления дочерних таблиц.
        @return: Возвращает строку запроса на удаление таблицы из БД.
        """
        drop_sql = ''
        if Cascade_:
            children = self.getChildrenDataclass()
            if children:
                for child in children:
                    drop_sql += child._get_drop_sql_txt()
        drop_sql += 'DROP TABLE %s;' % self.getDBTableName()
        return drop_sql

    def drop(self, Cascade_=False):
        """
        Удалить таблицу из БД.
        @param Cascade_: Признак удаления дочерних таблиц.
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            if self.dataclass is not None:
                if Cascade_:
                    for child_tab in self._children_tables.values():
                        child_tab.drop(Cascade_)
                self.dataclass.drop()

            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка удаления таблицы <%s> из БД.' % self.dataclass.name)
            return False

    def syncDB(self):
        """
        Функция синхронизации ресурса таблицы с представлением в БД.
        @return: Возвращает True/False.
        """
        try:
            result = False
            if self.dataclass is not None:
                res_fld_names = [child['name'] for child in self.getResource()['child']]
                tab_fld_names = self.getFieldNames()
                if res_fld_names != tab_fld_names:
                    # Необходимо синхронизировать
                    rec_count = self.count()
                    if rec_count > 0:
                        # Если записи есть, то сделать копию таблицы
                        log.info(u'Table <%s> create backup' % self.getDBTableName())
                        result = self.makeBackup()
                    elif rec_count == 0:
                        result = True
                    if result:
                        log.info(u'Table <%s> drop' % self.getDBTableName())
                        self.drop()
                        # Заново создать таблицу
                        self.dataclass = self._createDataClass(self.getResource(), ReCreate_=True)
            return result
        except:
            log.fatal(u'Ошибка синхронизации таблицы <%s> в БД.' % self.dataclass.name)
            return False

    def makeBackup(self, BAKTableName_=None):
        """
        Сделать бекап таблицы в БД.
        @param BAKTableName_: Имя таблицы бекапа. Если None, тогда имя генерируется.
        @return: Возвращает True/False.
        """
        if BAKTableName_ is None:
            from ic.utils import ic_time
            time_name = str(ic_time.genUnicalTimeName())
            BAKTableName_ = self.dataclass.name+'_'+time_name
        return self.copy_to(BAKTableName_)

    def copy_to(self, NewTableName_):
        """
        Копирвание содержимого таблицы в новую таблицу.
        @param NewTableName_: Новое имя таблицы.
        @return: Возвращает True/False.
        """
        try:
            if self.dataclass is not None:
                # Сначала создать таблицу такойже структуры
                fields = [column.copy() for column in self.dataclass.columns] + \
                         [constraint.copy() for constraint in self.dataclass.constraints]
                new_table = sqlalchemy.Table(NewTableName_, self.dataclass.metadata, *tuple(fields))
                new_table.create()

                # Затем перенести данные
                result = self.dataclass.select().execute()
                recs = tuple([dict(rec) for rec in result])
                result = new_table.insert().execute(*recs)
                # Запомнить последние добавленные идентификаторы
                self._last_inserted_ids = result.inserted_primary_key
                return True
        except:
            log.fatal(u'Ошибка копирования таблицы %s в таблицу %s' % (self.dataclass.name, NewTableName_))
        return False

    # Функции блокировок
    def Lock(self):
        """
        Блокирует таблицу.
        """
        if self.db:
            return self.db.LockTable(self.getClassName())
        return None

    def unLock(self):
        """
        Разблокирует таблицу.
        """
        if self.db:
            return self.db.unLockTable(self.getClassName())
        return None

    def LockObject(self, id, str=None):
        """
        Блокировка изменения объекта.
        """
        if self.db:
            return self.db.LockRec(self.getClassName(), id, str)
        return False

    def unLockObject(self, id):
        """
        Разблокирует объект.
        """
        if self.db:
            return self.db.unLockRec(self.getClassName(), id)
        return None

    def IsLock(self):
        """
        Возвращает признак блокировки класса данных.
        """
        if self.db:
            return self.db.IsLockTable(self.getClassName())
        return None

    def IsLockObject(self, id):
        """
        Возвращает признак блокировки объекта класса данных.
        """
        if self.db:
            return self.db.IsLockRec(self.getClassName(), id)
        return None

    def releaseConnection(self, conn):
        """
        Освобождает соединение.
        """
        if self.dataclass is not None:
            self.db.releaseConnection(conn)

    def clear(self):
        """
        Очистить таблицу.
        """
        if self.dataclass is not None:
            return self.dataclass.delete().execute()
        return None

    def getFieldDefault(self, FieldName_):
        """
        Значение по умолчанию поля.
        """
        if self.dataclass is not None:
            for field in self.getResource()['child']:
                if field['name'] == FieldName_:
                    value = None
                    if field['type'] == 'Field':
                        value = field['default']
                    elif field['type'] == 'Link':
                        value = 0
                    if value in ('None', 'NULL'):
                        value = None
                    return value
        return None

    def isFieldDefault(self, FieldName_):
        """
        Есть значение по умолчанию поля?
        """
        result = False
        if self.dataclass is not None:
            for field in self.getResource()['child']:
                if field['name'] == FieldName_:
                    if field['type'] == 'Field':
                        if field['default']:
                            result = True
                        else:
                            if 'server_default' in field and field['server_default']:
                                result = False
                            else:
                                result = True
                    elif field['type'] == 'Link':
                        result = True
                    return result
        return result

    def getDefaultRecDict(self):
        """
        Возвращает словарь записи со значениями полей по умолчанию.
        """
        rec = {}
        field_names = self.getFieldNames()
        if self.dataclass is not None:
            for field in self.getResource()['child']:
                if 'activate' not in field or int(field['activate']):
                    # Имя поля(не должно быть unicode)
                    fld_name = field['name']
                    if isinstance(fld_name, unicode):
                        fld_name = fld_name.encode()

                    if field['type'] == 'Field':
                        try:
                            # Если определено значение по умолчанию, тогда взять его
                            if field['default']:
                                rec[fld_name] = field['default']
                            else:
                                # Если значение по умолчанию не определено,
                                # но определено значение по умолчанию на сервере
                                # то значение по умолчанию добавлять не надо
                                if 'server_default' in field:
                                    if not field['server_default']:
                                        rec[fld_name] = field['default']
                                else:
                                    rec[fld_name] = field['default']
                        except:
                            pass
                    elif field['type'] == 'Link':
                        rec[fld_name] = 0
        return rec

    def getCascadeDict(self, Id_):
        """
        Получить данные каскада в виде словаря по идентификатору.
        @param Id_: Идентификатор головной записи.
        """
        try:
            return self._getCascadeDict(Id_)
        except:
            log.fatal(u'Ошибка определения данных каскада в виде словаря таблицы <%s>.' % self.getClassName())
            return None

    def _createTabByName(self, tab_name):
        """
        Создать таблицу по имени.
        @param tab_name: Имя таблицы.
        @return: Объект таблицы или None, если ошибка.
        """
        tab = None
        # Пробуем получить объект по таблицы по сгенерированному паспорту
        try:
            tab_psp = (('Table', tab_name, None, tab_name + '.tab', ic_user.getPrjName()),)
            tab = ic_user.getKernel().Create(tab_psp)
        except:
            log.fatal(u'Ошибка создания таблицы по имени <%s>' % tab_name)
        return tab

    def getChildTable(self, tab_name):
        """
        Получить объект дочерней таблицы по имени.
        @param tab_name: Имя дочерней таблицы.
        @return: Объект таблицы или None,
            если дочерняя таблица не найдена.
        """
        tab = self._children_tables.get(tab_name, None)
        if tab is None:
            log.warning(u'Дочерняя таблица <%s> не найдена среди %s' % (tab_name,
                                                                        self._children_tables.keys()))
            # Дочерняя таблица не зарегистрирована
            # Создаем по имени
            tab = self._createTabByName(tab_name)
        return tab

    def getParentTable(self, tab_name):
        """
        Получить объект родительской таблицы по имени.
        @param tab_name: Имя родительской таблицы.
        @return: Объект таблицы или None,
            если родительская таблица не найдена.
        """
        tab = self._parent_tables.get(tab_name, None)
        if tab is None:
            log.warning(u'Родительская таблица <%s> не найдена среди %s' % (tab_name,
                                                                            self._parent_tables.keys()))
            # Родительская таблица не зарегистрирована.
            # Создаем по имени
            tab = self._createTabByName(tab_name)
        return tab

    def getLinkIdFieldName(self, parent_table):
        """
        Имя поля идентификатора родительской таблицы в дочерней таблице.
        @param parent_table: Родительская таблица.
            Может задаваться как именем, так и объектом.
        @return: Строка идентификатора родительской таблицы.
            Например:
                'id_table1_tab'
        """
        if isinstance(parent_table, str) or isinstance(parent_table, unicode):
            # Родительская таблица задается именем
            tab = self.getParentTable(parent_table)
            if tab:
                return 'id_'+tab.getDBTableName()
        elif issubclass(parent_table.__class__, icSQLAlchemyDataClass):
            # Родительская таблица задается объектом
            return 'id_' + parent_table.getDBTableName()
        else:
            log.warning(u'Не поддерживаемый тип <%s> аргумента в функции getLinkIdFieldName' % parent_table.__class__.__name__)
        return None

    def _getCascadeDict(self, Id_=0):
        """
        Получить данные каскада в виде словаря по идентификатору.
        @param Id_: Идентификатор записи.
        """
        cascade_dict = dict()
        root_rec = self.get(Id_)
        if root_rec.rowcount:
            record = root_rec.first()
            res = self.getResource()
            # Заполнить словарь значениями полей
            for field in res['child']:
                if field['type'] == 'Field':
                    cascade_dict[field['name']] = getattr(record, field['name'])
            # Заполнить словарь данными из дочерних таблиц
            children_tabname = res['children'] if res['children'] else list()
            for child_tabname in children_tabname:
                cascade_dict[child_tabname] = list()
                child_tab = self.getChildTable(child_tabname)
                if child_tab:
                    # Определить список дочерних идентификаторов
                    where = sqlalchemy.and_(getattr(child_tab.c, child_tab.getLinkIdFieldName(self)) == Id_)
                    recs = child_tab.get_where(where)
                    if recs and recs.rowcount:
                        child_records = recs.fetchall()
                        for child_rec in child_records:
                            child_cascade_dict = child_tab._getCascadeDict(child_rec.id)
                            cascade_dict[child_tabname].append(child_cascade_dict)
        return cascade_dict

    # Поддержка sqlalchemy мапперов
    def _getMapperCascadeStr(self, CascadeParam_):
        """
        Параметры связи в каскаде.
        """
        if 'del_cascade' in CascadeParam_ and CascadeParam_['del_cascade']:
            return 'all, delete-orphan'
        return None

    def _genMapperClass(self, Children_=None, CascadeParams_=None, AutoMapper_=False):
        """
        Генерация класса-ассоциации (маппера) текущей таблицы.
        """
        self._mapper_class = None
        try:
            if self.dataclass is not None:
                # Создание класса
                mapperclass_name = self.dataclass.name
                if isinstance(mapperclass_name, unicode):
                    mapperclass_name = mapperclass_name.encode()
                self._mapper_class = new.classobj(mapperclass_name, (object,), {})

                field_names = [fld['name'] for fld in self.getResource()['child'] if fld['type'] == FIELD_TYPE]
                _init_ = self._gen_mapper_init_(field_names)
                # Установить конструктор
                self._mapper_class.__init__ = new.instancemethod(_init_, None, self._mapper_class)
                if AutoMapper_:
                    _properties_ = None
                    if Children_:
                        _properties_ = dict([(child.dataclass.name,
                                            sqlalchemy.orm.relation(child._mapper_class,
                                             cascade=self._getMapperCascadeStr(CascadeParams_[child.dataclass.name]))) for child in Children_])
                    # Создание маппера
                    sqlalchemy.orm.mapper(self._mapper_class, self.dataclass, _properties_)
                # Обработка связей
                links = [lnk for lnk in self.getResource()['child'] if lnk['type'] == LINK_TYPE]
                cascade_params = {}
                for link in links:
                    tab_name = link['table'][0][1]
                    if tab_name in self.db._tables:
                        tab = self.db._tables[tab_name]
                    else:
                        # Создать родительскую таблицу
                        try:
                            tab = self.GetKernel().Create(link['table'])
                        except:
                            tab = icSQLAlchemyTabClass(tab_name)
                    # Прописать дочерние таблицы
                    if self.dataclass.name not in tab._children_tables:
                        tab._children_tables[self.dataclass.name] = self
                    # Прописать родительские таблицы
                    self._parent_tables[tab.getDBTableName()] = tab
                    # Заполнение параметров связи в каскаде
                    cascade_params = dict([(child.dataclass.name, child._getCascadeParams(tab)) for child in tab._children_tables.values()])

                    # Продолжить мапинг
                    tab._genMapperClass(tab._children_tables.values(), cascade_params, AutoMapper_)
        except:
            log.fatal(u'Ошибка генерации маппера таблицы.')

        return self._mapper_class

    def _getCascadeParams(self, ParentTable_):
        """
        Параметры каскада.
        """
        link_cascade = [field for field in self.getResource()['child'] \
                        if field['type'] == LINK_TYPE and field['table'] and \
                        field['table'][0][1] == ParentTable_.getResource()['name']]

        if link_cascade:
            result = {'del_cascade': False}
            if 'del_cascade' in link_cascade[0]:
                result['del_cascade'] = link_cascade[0]['del_cascade']
            return result
        return {}

    def _getFieldDefaultStr(self, FieldName_):
        """
        Значение поля по умолчанию в строковом представлении.
        """
        if self.isFieldDefault(FieldName_):
            field_default = self.getFieldDefault(FieldName_)
            if isinstance(field_default, str):
                return '\''+str(field_default)+'\''
            elif isinstance(field_default, unicode):
                return 'u\''+str(field_default)+'\''
            return str(field_default)
        return None

    def _gen_mapper_init_(self, FieldNames_):
        """
        Функция генерации копструктора маппера таблицы.
        """
        init_func_txt = ''
        try:
            fields = ['%s=%s' % (fld_name, self._getFieldDefaultStr(fld_name)) for fld_name in FieldNames_]
            init_func_txt = 'def __init__(self,%s):\n' % (','.join(fields))
            if FieldNames_:
                for field_name in FieldNames_:
                    init_func_txt += '\tself.%s=%s\n' % (field_name, field_name)
            else:
                init_func_txt += '\tpass\n'

            exec init_func_txt      # in name_space
            return __init__
        except:
            log.fatal(u'Ошибка генерации конструктора маппера табицы.')

    def getMapperClass(self, AutoMapper_=True):
        """
        Класс-ассоциация (маппера) текущей таблицы.
        """
        if self._mapper_class:
            return self._mapper_class
        return self._genMapperClass(AutoMapper_=AutoMapper_)

    def setMapperClass(self, MapperClass_):
        """
        Класс-ассоциация (маппера) текущей таблицы.
        """
        self._mapper_class = MapperClass_

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
            fields = tuple([(field_name,
                             self.getFieldType(field_name),
                             self.getFieldLength(field_name)) for field_name in self.getFieldNames()])
            data = self.queryAll()
            return copy.deepcopy({'__fields__': fields, '__data__': data})
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
            log.fatal(u'Ошибка нормализации результата запроса к таблице')
        return None


class icSQLAlchemyTabClass(icSQLAlchemyDataClass):
    """
    Таблица.
    """
    def __init__(self, TabName_, ReCreate_=False, Refresh_=False, SubSys_=None, **kwargs):
        """
        Конструктор.
        @param TabName_: Ресурсное описание класса данных/таблицы.
        @param ReCreate_: Флаг пересоздания класса таблицы.
            По умолчанию не пересоздавать.
        @param Refresh_: Признак обовления ресурсного описания.
        @param SubSys_: Имя подсистемы, из которой берется ресурс таблицы.
        """
        pathRes = None
        if SubSys_:
            pathRes = resource.getSubsysPath(SubSys_)
            
        icSQLAlchemyDataClass.__init__(self,
                                       resource.icGetRes(TabName_, 'tab', pathRes=pathRes, nameRes=TabName_),
                                       TabName_, ReCreate_, Refresh_, **kwargs)
