#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль компонента таблицы и БД.
"""

# Подключение библиотек
import copy
import types

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
from ic.utils import resource
from ic.utils import ic_mode
from ic.utils import util

from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.engine import ic_user

from ic.components import icwidget

from . import icdb

__version__ = (1, 1, 3, 1)

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
                'children': [],    # Имена дочерних таблиц, Если организуется каскад, то обязательно!
                'source': None,
                'idx': None,

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'scheme': u'',
                                 'table': u'Альтернативное наименование таблицы в БД',
                                 'import': u'',
                                 'filter': u'',
                                 'source': u'Паспорт БД',
                                 'idx': u'',
                                 'children': u'Имена дочерних таблиц, Если организуется каскад, то обязательно!',
                                 },
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
                                 'type_val': u'Тип хранимого значения',
                                 'len': u'Длина хранимого значения',
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
                    ic_dlg.icWarningBox(u'ВНИМАНИЕ',
                                        u'Различие структур таблицы <%s> в описании и БД. В БД создана копия таблицы <%s>. Старая таблица удалена.' % (self.dataclass.name, self.dataclass.name))

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
        if issubclass(DB_.__class__, icdb.icSQLAlchemyDB):
            if DB_.getMetaData():
                self._regDB = DB_._changeDialect(self._regDB, DB_.getMetaData().bind.dialect)
            self._regDB[DBName_] = DB_
        else:
            log.error(u'Ошибка типа БД <%s> при регистрации' % DBName_)

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
            db = icdb.icSQLAlchemyDB(db_res, False)

        # Зарегистрировать БД
        self._registerDB(DBName_, db)
        return db

    def _createDataClass(self, TabRes_, AutoCreate_=True, ReCreate_=False):
        """
        Создание объекта таблицы.
        @param TabRes_: Ресурс таблицы.
        @param AutoCreate_: Автоматически создать в БД?
        @param ReCreate_: Признак пересоздания таблицы.
        @return: Созданный объект sqlalchemy.Table.
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
                    log.debug(u'Получение таблицы <%s> из буфера' % tab_name)
                    # Проверить таблицу на изменение структуры
                    # Если структура изменена, тогда сигнализировать ошибку
                    fields_with_id_count = len([fld for fld in TabRes_['child'] if fld.get('activate', True)])+1
                    if len(metadata.tables[tab_name].columns) != fields_with_id_count:
                        log.warning(u'Ошибка создания таблицы <%s>!' % tab_name)
                        ic_dlg.icWarningBox(u'ВНИМАНИЕ',
                                            u'В системе существует таблица <%s> с другой структурой!' % tab_name)
                        assert None, u'Изменена структура таблицы <%s>' % tab_name
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

                log.info(u'Создана таблица <%s>' % tab_name)
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
        # log.info(u'Создание поля <%s>' % name)
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
                result = [column.name for column in self.dataclass.columns]
            else:
                result = [column.name for column in self.dataclass.columns if column.name != u'id']
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
            if not isinstance(Value_, str):
                return str(Value_)
            else:
                return Value_
        else:
            if isinstance(Value_, bytes):
                return Value_.decode(DEFAULT_DB_ENCODING)
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

    def _bool(self, Value_):
        try:
            return bool(Value_)
        except TypeError:
            return Value_

    _fieldTypeConvert = {TEXT_FIELD_TYPE: _str,
                         FLOAT_FIELD_TYPE: _float,
                         INT_FIELD_TYPE: _int,
                         DATE_FIELD_TYPE: _str,
                         DATETIME_FIELD_TYPE: _datetime,
                         BINARY_FIELD_TYPE: _bin,
                         PICKLE_FIELD_TYPE: _pickle,
                         BIGINT_FIELD_TYPE: _int,
                         BOOLEAN_FIELD_TYPE: _bool,
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
            if isinstance(item[0], str):
                new_item = item[0]
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

    def is_links(self, link_field, link_value):
        """
        Проверка наличия связей для проверки целостности данных таблицы.
        Поиск наличия связи проверяется по count(*)
        SQL аналог:
            SELECT COUNT(*) FROM TABLE_NAME WHERE <link_field> = <link_value>
        @param link_field: Имя поля связи.
        @param link_value: Значение связи.
        @return: True - есть ссылки/связи / False - нет / None в случае ошибки.
        """
        if self.dataclass is not None:
            link_count = self.dataclass.select(getattr(self.c, link_field) == link_value).count()
            return link_count > 0
        return None

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

        elif isinstance(Struct_, bytes):
            # Строка юникод
            return Struct_.decode(DEFAULT_DB_ENCODING)

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
            return Struct_
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
            log.debug(u'Конвертация структурного фильтра <%s> в SQL: \'%s\'' % (Filter_, sql_txt))
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
                if len(args) == 1 and isinstance(args[0], str):
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
                        log.info(u'Создание резервной копии таблицы <%s>' % self.getDBTableName())
                        result = self.makeBackup()
                    elif rec_count == 0:
                        result = True
                    if result:
                        log.info(u'Удаление таблицы <%s>' % self.getDBTableName())
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

    def clear(self, transaction=None):
        """
        Очистить таблицу.
        @param transaction: Объект транзакции.
            Если определена транзакция то очищаем через транзакционный механизм.
        """
        if transaction is None:
            if self.dataclass is not None:
                return self.dataclass.delete().execute()
        else:
            return self.clear_transact(transaction=transaction)
        return None

    def clear_transact(self, transaction=None):
        """
        Очистить таблицу. Транзакционный механизм.
        @param transaction: Объект транзакции.
        """
        if transaction is not None and self.dataclass is not None:
            sql = self.dataclass.delete()
            transaction.execute(sql)
            return True
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
        if isinstance(parent_table, str):
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
                    try:
                        where = sqlalchemy.and_(getattr(child_tab.c, child_tab.getLinkIdFieldName(self)) == Id_)
                    except AttributeError:
                        log.error(u'Ошибка обработки дочерней таблицы <%s>' % child_tabname)
                        raise
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
                if isinstance(mapperclass_name, str):
                    mapperclass_name = mapperclass_name
                self._mapper_class = type(mapperclass_name, (object,), {})

                field_names = [fld['name'] for fld in self.getResource()['child'] if fld['type'] == FIELD_TYPE]
                _init_ = self._gen_mapper_init_(field_names)
                # Установить конструктор
                self._mapper_class.__init__ = types.MethodType(_init_, self._mapper_class)
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

            exec(init_func_txt)      # in name_space
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
