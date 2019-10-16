#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Хранилище/БД всех объектов-ссылок/справочников.
"""

# --- Подключение библиотек ---
import ic
import sqlalchemy
import sqlalchemy.sql

from ic.db import icsqlalchemy
from ic.log import log

from . import ref_persistent
from . import icspravstorage

# Версия
__version__ = (0, 1, 1, 1)

# --- Функции ---
_REF_SQL_STORAGE = dict()


def getRefSQLStorageByPsp(db_psp, ref_object=None):
    """
    Получить объект SQL хранилища объектов-ссылок/справочников по имени.
    @param db_psp: Паспорт БД.
    @param ref_object: Объект-ссылка/справочник.
    @return: Объект SQL хранилища объектов-ссылок/справочников.
    """
    global _REF_SQL_STORAGE

    if db_psp is None:
        assert None, u'В функции getRefSQLStorageByPsp не определен паспорт БД'

    storage_name = db_psp[0][1]
    if storage_name not in _REF_SQL_STORAGE:
        _REF_SQL_STORAGE[storage_name] = icRefSQLStorage(parent=ref_object, db_psp=db_psp)
        log.info(u'Регистрация БД <%s> в списке хранилищ' % storage_name)
    return _REF_SQL_STORAGE[storage_name]


class icRefStorageInterface(icspravstorage.icSpravStorageInterface):
    """
    Интерфейс абстрактного хранилища/БД объектов-ссылок/справочников.
    """

    def __init__(self, parent, db_psp, *args, **kwargs):
        """
        Конструктор.
        @param parent: Родительский объект.
        @param db_psp: Паспорт БД.
        """
        icspravstorage.icSpravStorageInterface.__init__(self, *args, **kwargs)

        self._parent = parent
        self._db_psp = db_psp

    def getParent(self):
        """
        Объект, к которому прикреплено хранилище.
        """
        return self._parent

    def saveObject(self, obj):
        """
        Сохранить объект в хранилище.
        @param obj: Сохраняемый объект.
        """
        pass

    def loadObject(self, obj, obj_id):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        @param obj: Объект.
        @param obj_id: Идентификатор объекта.
        """
        pass


class icRefSQLStorageContainer(object):
    """
    Контейнер таблиц SQL хранилища.
    Контейнер необходим для организации доступа к
    таблицам ч/з точку из компонента SQL хранилища.
    """

    def __init__(self):
        """
        Конструктор.
        """
        self.__dict__['_all'] = dict()

    def getAll(self):
        """
        Все внутренние объекты.
        """
        return self._all

    all = property(getAll)

    def hasName(self, name):
        """
        Зарегистрирован документ с таким именем?
        """
        return name in self._all

    def setTable(self, table_name=None):
        """
        Установить таблицу, по ее имени.
        @param table_name: Имя таблицы.
        @return: Возвращает объект таблицы или None, если таблицу получить нельзя.
        """
        if table_name:
            if not self.hasName(table_name):
                # Создать таблицу
                self._all[table_name] = icsqlalchemy.icSQLAlchemyTabClass(table_name)
            return self._all[table_name]
        return None

    def getTable(self, table_name):
        """
        Получить таблицу по имени. Если ее нет, то создает ее.
        """
        self.setTable(table_name)
        return self._all[table_name]


class icRefSQLStorage(icRefStorageInterface):
    """
    SQL хранилище/БД объектов-ссылок/справочников.
    """

    def __init__(self, parent, db_psp):
        """
        Конструктор.
        @param parent: Родительский объект.
        @param db_psp: Паспорт БД.
        """
        icRefStorageInterface.__init__(self, parent, db_psp)
        # Контейнер
        self._container = icRefSQLStorageContainer()

    # --- Методы поддержки доступа к таблицам черезточку ---
    def getContainer(self):
        """
        Контейнер таблиц.
        """
        return self._container

    container = property(getContainer)

    def __nonzero__(self):
        """
        Провера на не 0.
        """
        return not isinstance(self, None)

    def __getattr__(self, name):
        """
        Доступ к объектам через точку.
        """
        container = self.__dict__['_container']
        if container.hasName(name):
            # Если объект таблицы не создан, то создать его
            return container.setTable(name)
        else:
            # По умолчанию
            try:
                return self.__dict__[name]
            except KeyError:
                return None

    def _get_level_index_by_code(self, level_cod=None):
        """
        Определить индекс уровня по коду.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то считается что это самый верхний уровень.
        @return: Индекс уровня или None в случае ошибки.
        """
        if level_cod is None:
            return 0
        level_cod_length = len(level_cod)
        levels = self.getParent().getLevels()
        level_cod_len_list = [level.getCodLen() for level in levels]
        cod_len = 0
        for i, level_cod_len in enumerate(level_cod_len_list):
            cod_len += level_cod_len
            if level_cod_length == cod_len:
                return i
            elif level_cod_length < cod_len:
                log.warning(u'Не корректный код <%s> объекта-ссылки/справочника <%s>. Длины кодов %s' % (level_cod, self.self.getParent().getName(), str(level_cod_len_list)))
        return None

    def getLevelTable(self, level_cod=None, dt=None):
        """
        Таблица данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то возвращаются данные самого верхнего уровня.
        @type dt: C{string}
        @param dt: Время актуальности данных.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Имена полей таблицы данных уровня определятся с помощью функции
            getSpravFieldNames().
            Или None в случае ошибки.
        """
        # Определяем индекс уровня по коду
        level_idx = self._get_level_index_by_code(level_cod=level_cod)
        if level_idx is not None:
            level = self.getParent().getLevels()[level_idx]
            level_table = level.getTable()
            recordset = level_table.get_where(level_table.c.code == level_cod)
            return [tuple(record) for record in recordset]
        return None

    def getSpravFieldNames(self, index=0):
        """
        Список имен полей таблицы данных объекта-ссылки/справочника.
        @param index: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то считаем что это таблица самого верхнего уровня.
        @return: Список имен полей таблицы данных объекта-ссылки/справочника.
            Либо пустой список в случае ошибки.
        """
        if 0 <= index < self.getParent().getLevelCount():
            level = self.getParent().getLevels()[index]
            level_table = level.getTable()
            return level_table.getFieldNames()
        else:
            log.warning(u'Не корректный индекс [%d] уровня объекта-ссылки/справочника <%s>' % (index, self.getParent().getName()))
        return list()


if __name__ == '__main__':
    storage = icRefSQLStorage(None, 'work_db_psgress')
    storage.test()
