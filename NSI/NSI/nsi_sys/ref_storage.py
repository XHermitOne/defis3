#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Хранилище/БД всех объектов-ссылок/справочников.
"""

# --- Подключение библиотек ---
import datetime
import sqlalchemy

from ic.db import icsqlalchemy
from ic.log import log
from ic.utils import extfunc
from ic.engine import glob_functions

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
        self._parent = parent
        self._db_psp = db_psp

        icspravstorage.icSpravStorageInterface.__init__(self, parent_sprav=self._parent,
                                                        *args, **kwargs)

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
        log.warning(u'Не определен метод saveObject в <%s>' % self.__class__.__name__)

    def loadObject(self, obj, obj_id):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        @param obj: Объект.
        @param obj_id: Идентификатор объекта.
        """
        log.warning(u'Не определен метод loadObject в <%s>' % self.__class__.__name__)


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

    def clear(self):
        """
        Очистить справочник.
        """
        levels = self.getParent().getLevels()
        # В каскаде необходимо удалять данные сначала
        # из таблиц самого нижнего уровня,
        # поэтому перебор уровней производим в обратном проядке
        levels.reverse()
        for level in levels:
            level_table = level.getTable()
            level_table.clear()

    def _get_level_index_by_code(self, level_cod=None):
        """
        Определить индекс уровня по коду.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то считается что это самый верхний уровень.
        @return: Индекс уровня или None в случае ошибки или
            если код не принадлежит ни одному уровню.
        """
        if level_cod is None:
            return None
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
        try:
            levels = self.getParent().getLevels()
            if level_cod is None:
                level_idx = 0
                level_table = levels[level_idx].getTable()
                # Если запрашивается самый верхний уровень, то берем все значения
                recordset = level_table.select()
            else:
                # Определяем индекс уровня по коду
                level_idx = self._get_level_index_by_code(level_cod=level_cod)
                # log.debug(u'Код уровня <%s> -> Индекс уровня [%d]' % (str(level_cod), level_idx))

                if level_idx < len(levels) - 1:
                    level_table = levels[level_idx].getTable()
                    recordset = level_table.get_where(level_table.c.cod == level_cod)
                    parent_id = recordset.fetchone()['id']
                    if parent_id is None:
                        log.error(u'Не определен идентификатор родительской записи при получении таблицы уровня по коду <%s>' % level_cod)
                        return list()

                    parent_table_name = level_table.getName()
                    # Берем следующий уровень за тем, которому принадлежит код
                    #                          V
                    level = levels[level_idx + 1]
                    link_name = level._gen_parent_link_name(parent_table_name)
                    level_table = level.getTable()
                    recordset = level_table.get_where(getattr(level_table.c, link_name) == parent_id)
                    log.debug(u'Получение таблицы уровня <%s> по коду <%s : %d>' % (level_table.getName(), level_cod, parent_id))
                else:
                    recordset = list()
            return [tuple(record) for record in recordset]
        except:
            log.fatal(u'Ошибка определения таблицы данных уровня по коду <%s> объекта-ссылки/справочника <%s>' % (level_cod, self.getSpravParent().getName()))
        return None

    def getSpravFieldNames(self, level_idx=0):
        """
        Список имен полей таблицы данных объекта-ссылки/справочника.
        @param level_idx: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то считаем что это таблица самого верхнего уровня.
        @return: Список имен полей таблицы данных объекта-ссылки/справочника.
            Либо пустой список в случае ошибки.
        """
        if 0 <= level_idx < self.getParent().getLevelCount():
            level = self.getParent().getLevels()[level_idx]
            level_table = level.getTable()
            # ВНИМАНИЕ! В данном копоненте используются идентификаторы для связи таблиц
            # поэтому оставляем идентификаторы при преобразовании
            #                                       V
            return level_table.getFieldNames(bIsID=True)
        else:
            log.warning(u'Не корректный индекс [%d] уровня объекта-ссылки/справочника <%s>' % (level_idx, self.getParent().getName()))
        return list()

    def is_empty(self):
        """
        Проверка на пустой справочник.
        @return: True - справочник пустой, False - Есть данные.
        """
        sprav_table = self.getSpravParent().getTable()
        return sprav_table.is_empty()

    def _getSpravFieldDict(self, field_values, level_idx=0):
        """
        Получить запись таблицы данных справочника в виде словаря.
        @param field_values: Список значений записи таблицы значений уровня.
        @param level_idx: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то индекс определяется как индекс самого верхнего уровня.
        @return: запись таблицы данных справочника в виде словаря.
        """
        fld_names = self.getSpravFieldNames(level_idx=level_idx)
        fld_dict = dict()
        for i_fld, fld_name in enumerate(fld_names):
            value = None
            try:
                value = field_values[i_fld]
                fld_dict[fld_name] = value
            except IndexError:
                # Не все поля есть в гриде
                if self._tab:
                    if self._tab.isFieldDefault(fld_name):
                        value = self._tab.getFieldDefault(fld_name)
                        fld_dict[fld_name] = value

            if fld_name == 'dt_edit' and not value:
                fld_dict[fld_name] = datetime.datetime.now()
            if fld_name == 'computer' and not value:
                fld_dict[fld_name] = extfunc.getComputerName()
            if fld_name == 'username' and not value:
                fld_dict[fld_name] = glob_functions.getCurUserName()
        return fld_dict

    def getRecByCod(self, cod, dt=None):
        """
        Получить запись по коду.
        @param cod: Код.
        @param dt: Период актуальности.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        if cod:
            try:
                levels = self.getParent().getLevels()
                level_idx = self._get_level_index_by_code(level_cod=cod)
                level = levels[level_idx]
                level_table = level.getTable()
                recordset = level_table.get_where(level_table.c.cod == cod)
                record = recordset.fetchone()
                return dict(record)
            except:
                log.fatal(u'Ошибка определения записи по коду <%s>' % cod)
        return None


if __name__ == '__main__':
    storage = icRefSQLStorage(None, 'work_db_psgress')
    storage.test()
