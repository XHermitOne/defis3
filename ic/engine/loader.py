#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер загрузки ресурса.
"""

import os.path
import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import interfaces as orm_ifs

from ic.kernel import io_prnt
from ic.utils import ic_res
from ic.utils import lock as lockmod
from . import ic_user


__version__ = (0, 0, 1, 1)


class Resources(object):
    def __init__(self, path, res, user=None, lock=False, ttl=None):
        self.path = path
        self.res = res
        self.lock = lock
        self.user = user
        self.ttl = ttl
        self.computer = lockmod.ComputerName()

    def _get_res(self):
        return self._res

    def _set_res(self, res):
        self._res = res

    res = property(_get_res, _set_res)


def mapclass(sysdb, tab_name=None):
    """
    Мапируем класс.
    """
    tab_name = tab_name or 'resource_tab'
    resources_tab = sa.Table(tab_name, sysdb.getMetaData(),
        sa.Column('res_id', sa.Integer, sa.Sequence('%s_id_seq' % tab_name), primary_key=True),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('computer', sa.String(), nullable=True),
        sa.Column('user', sa.String(), nullable=True),
        sa.Column('last_modified', sa.DateTime, onupdate=sa.func.current_timestamp()),
        sa.Column('res', sa.PickleType(0), nullable=False),
        sa.Column('lock', sa.Boolean(), default=False),
        sa.Column('ttl', sa.Integer, nullable=True),
    )
    orm.clear_mappers()
    orm.mapper(Resources, resources_tab, extension=ResEventExtension(),
               properties={'_res': orm.deferred(resources_tab.c.res)})
    io_prnt.outLog('MAP Resource Loader class.')
    return resources_tab, Resources


class ResEventExtension(orm_ifs.MapperExtension):
    pass


def todbpath(func):
    def wrap(self, path, *arg, **kwarg):
        path = path.replace('\\','/').replace('//','/')
        lst = path.split('/')
        if len(lst) > 1:
            path = '/'.join(lst[-2:])
        return func(self, path, *arg, **kwarg)
    return wrap


LOCKREC = 'LOCKREC'


class icLoader(object):
    """
    Управление загрузкой ресурса. Ресурсы могут хранится только в PostgreSQL.
    """
    def __init__(self, *arg, **kwarg):
        import ic
        self.ic = ic
        self.dbstore = None
        self.sysdb = None
        ic.resource_loader = self
        self.typdb = typdb = ic.load_ini_param('SYSDB', 'DB_ENGINE')
        if typdb == 'PostgreSQLDB':
            self.init_ini_auth()
        else:
            self.init_db_auth()
            
        if self.dbstore:
            self.dbstore = [el.strip() for el in self.dbstore.split(',')]

    def init_ini_auth(self):
        """
        Определяет источник данных где будут хранится системные ресурсы через .ini файл.
        """
        from ic.components.user import ic_postgres_wrp
        ic = self.ic
        try:
            tab_name = ic.load_ini_param('SYSDB', 'sys_table_name')
            self.sysdb = ic_postgres_wrp.icPostgreSQL(None)
            self.systab, self.syscls = mapclass(self.sysdb, tab_name)
            io_prnt.outLog('(+) INIT SYSDB:%s, %s, %s' % (self.sysdb, self.systab, self.syscls))
            if not self.systab.exists():
                self.systab.create()
                io_prnt.outLog('(+) CREATE SYSTEM TABLE: %s' % self.systab)
            self.dbstore = ic.load_ini_param('RESOURCE', 'dbstore').strip()
        except:
            io_prnt.outErr('')
            io_prnt.outLog('(!) SYSDB ERROR. POSSIBLE INVALID CONNECTION PARAMETERS IN <PRJNAME>.INI FILE.')
        
    def init_db_auth(self):
        """
        Определяет источник данных где будут хранится системные ресурсы через параметры проекта.
        """
        db_auth = ic_user.icGet('db_auth')
        if db_auth in ('0', '', None, 'None', 'false', 'False', 'FALSE'):
            db_auth = False
        else:
            db_auth = True

        sys_table_name = ic_user.icGet('sys_table_name') or 'sys_table'
        db_engine = ic_user.icGet('db_engine')
        convert_unicode = ic_user.icGet('convert_unicode') or 'UTF-8'
        dbname = ic_user.icGet('dbname')
        host = ic_user.icGet('host') or '127.0.0.1'
        user = ic_user.icGet('user')
        password = ic_user.icGet('password')
        port = ic_user.icGet('port')
        dbstore = ic_user.icGet('dbstore') or '.acc'

        if not db_auth or not db_engine or not dbname or not user or not password or not port:
            return
        
        res = dict(convert_unicode=convert_unicode,
                   dbname=dbname,
                   encoding='UTF-8',
                   host=host,
                   port=port,
                   user=user,
                   password=password)
        try:
            if db_engine == 'PostgreSQLDB':
                from ic.components.user import ic_postgres_wrp
                self.sysdb = ic_postgres_wrp.icPostgreSQL(None, -1, res)
            
            if self.sysdb:
                self.systab, self.syscls = mapclass(self.sysdb, sys_table_name)
                io_prnt.outLog('(+) DB INIT SYSDB:%s, %s, %s' % (self.sysdb, self.systab, self.syscls))
                if not self.systab.exists():
                    self.systab.create()
                    io_prnt.outLog('(+) CREATE SYSTEM TABLE: %s' % self.systab)
                self.dbstore = dbstore
        except:
            io_prnt.outErr('')
            io_prnt.outLog('(!) SYSDB ERROR. POSSIBLE INVALID CONNECTION PARAMETERS IN <PRJNAME>.PRO FILE.')
        
    def is_db_store(self, path=None):
        """
        Принак хранения ресурса в базе.
        @param path: Идентификатор ресурса (путь в файловой системе).
        """
        return self.dbstore and [el for el in self.dbstore if el in path or []]

    @todbpath
    def load_db_res(self, path):
        """
        Загрузка из базы.
        @param path: Идентификатор ресурса (путь в файловой системе).
        """
        if self.sysdb:
            session = self.sysdb.session()
            lst = session.query(self.syscls).filter_by(path=path).all()
            if lst:
                obj = lst[0]
                io_prnt.outLog('Load resource from DB')
                return obj.res

    @todbpath
    def lock_db(self, path, flag=True, ttl=None):
        """
        Блокирование ресурса.
        @param path: Идентификатор.
        @param flag: Признак блокировки/разблокировки.
        @param bDel: Признак удаления записи.
        """
        if self.sysdb:
            session = self.sysdb.session()
            lst = session.query(self.syscls).filter_by(path=path).all()
            if not lst and flag:
                self.save_db_res(path, 'LOCKREC', block=True, ttl=ttl)
                io_prnt.outLog('.lock resource %s' % path)
            elif lst:
                obj = lst[0]
                obj.lock = flag
                obj.ttl = ttl
                obj.user = self.get_user()
                obj.computer = lockmod.ComputerName()
                session.add(obj)
                session.flush()
                if flag:
                    io_prnt.outLog('.lock resource %s' % path)
                else:
                    io_prnt.outLog('.unlock resource %s' % path)
                return True
        return False

    @todbpath
    def unlock_db(self, path, bDel=False):
        """
        Разблокирование ресурса.
        @param path: Идентификатор.
        @param bDel: Признак удаления записи.
        """
        if self.sysdb:
            if bDel:
                session = self.sysdb.session()
                lst = session.query(self.syscls).filter_by(path=path).all()
                if lst:
                    session.delete(lst[0])
                    session.flush()
                    io_prnt.outLog('.unlock and delete resource %s' % path)
            else:
                return self.lock_db(path, False)

    def lock_file(self, path,  ttl=None):
        """
        Блокирование ресурса.
        @param path: Идентификатор.
        """
        p, tail = os.path.split(path)
        nm, ext = tail.split('.')
        ic_res.lockRes(None, nm, ext)

    def unlock_file(self, path):
        """
        Разблокирование ресурса.
        @param path: Идентификатор.
        """
        p, tail = os.path.split(path)
        nm, ext = tail.split('.')
        ic_res.unlockRes(None, nm, ext)

    def lock_res(self, path, ttl=None, bAdd=True):
        """
        Блокирование ресурса.
        @param path: Идентификатор.
        """
        if self.is_db_store(path):
            return self.lock_db(path, ttl=ttl)
        else:
            return self.lock_file(path, ttl=ttl)

    def unlock_res(self, path):
        """
        Блокирование ресурса.
        @param path: Идентификатор.
        """
        if self.is_db_store(path):
            return self.unlock_db(path)
        else:
            return self.unlock_file(path)

    @todbpath
    def is_lock_db(self, path):
        """
        Признак блокировки объекта.
        @param path: Идентификатор.
        """
        if self.sysdb:
            session = self.sysdb.session()
            lst = session.query(self.syscls).filter_by(path=path).all()
            if lst:
                obj = lst[0]
                user = getattr(self.ic, 'getCurUserName', None)
                if user:
                    user = user()
                if obj.computer == lockmod.ComputerName() and (obj.user is None or obj.user == user):
                    return False
                # Если время жизни блокировки прошло, снимаем блокировку
                elif obj.ttl:
                    dt = datetime.datetime.now() - obj.last_modified
                    if obj.ttl <= dt.seconds:
                        obj.lock = False
                        session.add(obj)
                        session.flush()
                return obj.lock
        return False

    def is_lock_file(self, path):
        """
        Признак блокировки объекта.
        @param path: Идентификатор.
        """
        p, tail = os.path.split(path)
        nm, ext = tail.split('.')
        ic_res.isLockRes(None, nm, ext)

    def is_lock_res(self, path):
        """
        Признак блокирования ресурса.
        @param path: Идентификатор.
        """
        if self.dbstore and [el for el in self.dbstore if el in path]:
            return self.is_lock_db(path)
        else:
            return self.is_lock_file(path)

    def load_file_res(self, path, bRefresh=True):
        """
        Загрузка из файла.
        @param path: Идентификатор.
        """
        res = ic_res.ReadAndEvalFile(path, bRefresh=bRefresh)
        return res

    def load_res(self, path, bRefresh=True):
        """
        Загружает ресурс.
        @param path: Идентификатор.
        """
        res = None
        if self.is_db_store(path):
            res = self.load_db_res(path)
        if not res or not (type(res) in (dict, list, tuple)):
            return self.load_file_res(path, bRefresh)
        return res

    @todbpath
    def get_db_rec(self, path):
        session = self.sysdb.session()
        lst = session.query(self.syscls).filter_by(path=path).all()
        if lst:
            obj = lst[0]
            dct = {'computer': obj.computer, 'user':obj.user}
            return dct

    def get_lock_rec(self, path):
        if self.is_db_store(path):
            return self.get_db_rec(path)
        else:
            p, tail = os.path.split(path)
            nm, ext = tail.split('.')
            return ic_res.getLockResRecord(None, nm, ext)

    def get_user(self):
        if hasattr(self.ic, 'getCurUserName'):
            return self.ic.getCurUserName()

    @todbpath
    def save_db_res(self, path, res, block=False, ttl=None):
        """
        Сохранение в базу.
        """
        session = self.sysdb.session()
        lst = session.query(self.syscls).filter_by(path=path).all()
        user = self.get_user()
        if lst:
            obj = lst[0]
            obj.res = res
        else:
            obj = self.syscls(path, res, user)
        obj.computer = lockmod.ComputerName()
        obj.user = user
        obj.lock = block
        obj.ttl = ttl
        obj.last_modified = datetime.datetime.now()
        session.add(obj)
        session.flush()
        io_prnt.outLog('Save resource to DB')
        return obj

    def save_file_res(self, path, res):
        """
        Сохранение в файл.
        """
        text = str(res)
        file = open(path, 'wb')
        file.write(text)
        file.close()

    def save_res(self, path, res):
        """
        Сохраняет ресурс.
        """
        if self.is_db_store(path):
            return self.save_db_res(path, res)
        else:
            return self.save_file_res(path, res)
