#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактные классы хранимых объектов.
По сути это генератор таблиц хранения объектов.
"""

import time

from ic.utils import modefunc

from ic.utils import lockfunc
from ic.utils import strfunc
from ic.utils import util
from ic.engine import glob_functions
from ic.utils import uuidfunc
from ic.log import log
from ic.dlg import dlgfunc

from ic.db import icsqlalchemy

from ic.storage import storesrc
from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp
from ic.components.user import ic_link_wrp

from STD.queries import filter_builder_env
from STD.queries import filter_convert
from STD.queries import filter_generate


# Version
__version__ = (0, 1, 1, 5)

# Префикс для кода справочника в словаре записи
NSI_CODE_PREFIX = '_'


class icObjPersistentProto(object):
    """
    Прототип компонентов, хранимых в БД.
        Реализует простейшие функции генерации имен таблиц и т.п.
    """

    def __init__(self, parent=None):
        """
        Конструктор.

        :param parent: Родительский объект.
        """
        self.uuid = None
        self.name = ''
        self.description = ''
        
        # Инициализация родительского класса
        self._parent = parent

        # Имя таблицы хранения
        self._table_name = ''
        self._table = None

        # Система блокировки
        lock_dir = None
        self._lockSystem = None
        self.read_only = True
        
        # Инициализировать систему блокировки
        self._initLockSystem()        

    def getName(self):
        """
        Имя объекта.
        """
        return self.name

    def getUUID(self):
        """
        Уникальный идентификатор.
        """
        if self.uuid is None:
            self.uuid = self.genUUID()
        return self.uuid

    def _validUUID(self, UUID):
        """
        Проверка корректного значения UUID.

        :return: True/False.
        """
        return uuidfunc.valid_uuid(UUID)

    def setUUID(self, UUID):
        """
        Уникальный идентификатор можно задать явным образом.
        """
        if self._validUUID(UUID):
            self.uuid = UUID
        else:
            log.warning(u'Не корректное устанавливаемое значение UUID <%s>. UUID остался прежним' % UUID)
        return self.uuid

    def genUUID(self):
        """
        Генерировать уникальный идентификатор.
        """
        self.uuid = uuidfunc.get_uuid()
        return self.uuid
    
    def getDBPsp(self):
        """
        Паспорт хранилища.
        """
        if self._parent:
            return self._parent.getDBPsp()
        return None
        
    def getDBName(self):
        """
        Имя хранилища.
        """
        db_psp = self.getDBPsp()
        if db_psp:
            return db_psp[0][1]

    def _genTableName(self):
        """
        Генерация имени таблицы хранения.
        """
        return str(self.name).lower()+'_tab'
        
    def getTableName(self):
        """
        Имя таблицы хранения.
        """
        if not self._table_name:
            self._table_name = self._genTableName()
        return self._table_name

    def getTable(self):
        """
        Таблица хранения.
        """
        return self._table
    
    def _createUuidFieldSpc(self, field_name='uuid'):
        """
        Создать спецификацию поля идентифицирующего документ.

        :param field_name: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_spc['name'] = field_name
        field_spc['description'] = u'Идентификатор UUID документа'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'T'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc
    
    def _createCodFieldSpc(self, field_name='cod'):
        """
        Создать спецификацию поля идентифицирующего объект по коду.

        :param field_name: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_spc['name'] = field_name
        field_spc['description'] = u'Код'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'T'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc

    def _createDateFieldSpc(self, field_name='x_date', description=''):
        """
        Создать спецификацию поля даты/времени.

        :param field_name: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_spc['name'] = field_name
        field_spc['description'] = strfunc.str2unicode(description)
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'D'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc
    
    def _createIntFieldSpc(self, field_name='x_int', description=''):
        """
        Создать спецификацию целочисленного поля.

        :param field_name: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_spc['name'] = field_name
        field_spc['description'] = strfunc.str2unicode(description)
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'I'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = -1
        
        return field_spc
    
    def _initLockSystem(self):
        """
        Функции поддержки блокировок.
        Инициализация системы блокировок.
        """
        # Система блокировки
        lock_dir = glob_functions.getVar('LOCK_DIR')
        self._lockSystem = lockfunc.icLockSystem(lock_dir)

    def lock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Заблокировать текущий. Блокировка ведется по UUID.

        :param UUID: UUID блокируемого объекта.
        """
        if UUID is None:
            UUID = self.getUUID()
        if self._lockSystem:
            return self._lockSystem.lockFileRes(UUID)
        return None
        
    def unLock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Разблокировать.

        :param UUID: UUID блокируемого объекта.
        """
        if UUID is None:
            UUID = self.getUUID()
        if self._lockSystem:
            return self._lockSystem.unLockFileRes(UUID)
        return None
        
    def isLock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Заблокирован?

        :param UUID: UUID блокируемого объекта.
        """
        if UUID is None:
            UUID = self.getUUID()
        if self._lockSystem:
            return self._lockSystem.isLockFileRes(UUID)
        return False
        
    def ownerLock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Владелец блокировки.

        :param UUID: UUID блокируемого объекта.
        """
        if UUID is None:
            UUID = self.getUUID()
        if self._lockSystem:
            lock_rec = self._lockSystem.getLockRec(UUID)
            return lock_rec['computer']
        return None
        
    def isMyLock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Моя блокировка?

        :param UUID: UUID блокируемого объекта.
        """
        return self.ownerLock(UUID) == lockfunc.getComputerName()

    def getFieldName(self):
        """
        Имя поля хранения значения атрибута.
        У объекта нет поля.
        Это метод-заглушка.
        """
        return None


class icObjPersistent(icObjPersistentProto):
    """
    Базовый класс компонентов хранимых в БД.
        Реализует внутри себя механизм генерации спецификаций таблиц хранения.
    """

    def __init__(self, parent=None):
        """
        Конструктор.

        :param parent: Родительский объект.
        """
        icObjPersistentProto.__init__(self, parent)

        # Окружение конструктора фильтров для объектов
        self.filter_environment = None

        # Текущий фильтр бизнес-обектов
        # если None, то все объекты
        self._filter = None

        # Ограничение количества объектов. Если None, ограничения нет.
        self._limit = None

    def setFilter(self, cur_filter):
        """
        Установить фильтр.
        Для создания фильтров надо пользоваться
        функциями из STD.queries.filter_generate.
        Функции генерации фильтров для вызова
        из функций прикладного уровня.
        Использование:
            create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))

        :param cur_filter: Текущий устанавливаемый фильтр.
        """
        self._filter = cur_filter

    def getFilter(self):
        """
        Фильтр объектов.
        """
        return self._filter

    def setLimit(self, limit=None):
        """
        Ограничение количества объектов. Если None, ограничения нет.
        """
        self._limit = limit

    def getLimit(self):
        """
        Ограничение количества объектов. Если None, ограничения нет.
        """
        return self._limit

    def getTable(self):
        """
        Таблица хранения.
        """
        if self._table is None:
            tab_res = self._createTabRes()
            self._table = self.GetKernel().createObjBySpc(parent=None, res=tab_res)
        return self._table

    def save(self, UUID=None, data=None):
        """
        Сохранить внутренние данные в хранилище.

        :param UUID: Идентификатор.
        Если None, то сохранить текущий.
        :param data: Сохраняемые данные в виде каскадного словаря:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        Если данные не указаны, то берутся данные из дерева объектов.
        :return: Возвращает результат выполнения операции True/False.
        """
        session = None
        try:
            tab = self.getTable()
            # Начать транзакцию
            session = tab.db.getSession()
            session.begin()
            
            if UUID is None:
                UUID = self.getUUID()
            if data is None:
                data = self._getCascadeDataObj()
            result = self._saveCascadeData(tab, UUID, data)
            # Завершить транзакцию
            session.commit()
            return result
        except:
            if session:
                # Откатить транзакцию
                session.rollback()
                # if session.is_active:
                #    session.clear()
            log.fatal(u'Ошибка сохранения данных мета-объекта [%s]' % self.name)
        return None
            
    def _saveCascadeData(self, table, UUID, data):
        """
        Сохранить каскадные данные в хранилище.

        :param table: Таблица.
        :param UUID: Уникальный идентификатор.
        :param data: Словарь каскадных данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        :return: Возвращает True/False.
        """
        try:
            tab = self._tabObj(table)
            if tab:
                # Выбрать только реквизиты
                rec = dict([(str(fld_name), fld_value) for fld_name, fld_value in data.items() if not isinstance(fld_value, list)])
                save_rec = tab.get_where(tab.c.uuid == UUID).fetchone()
                tab.update_where(tab.c.uuid == UUID, **rec)

                result = True
                children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__, icObjPersistent)]
                # Обработка дочерних объектов
                for child_obj in children_obj:
                    child_tab_name = child_obj.getTableName()
                    child_name = child_obj.getName()
                    if child_tab_name in data:
                        # В данных указана дочерняя таблица по имени таблицы
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              data[child_tab_name], save_rec)
                    elif child_name in data:
                        # В данных указана дочерняя таблица по имени табличного реквизита
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              data[child_name], save_rec)
                    else:
                        log.warning(u'Не найдены данные для дочерней таблицы/реквизита <%s>/<%s>' % (child_tab_name, child_name))
                return result
        except:
            log.fatal(u'Ошибка сохранения каскада данных мета-объекта [%s]' % self.name)
        return False

    def _updateChildCascadeData(self, table, data, parent_record):
        """
        Сохранить каскадные данные в хранилище у дочерних объектов.

        :param table: Таблица.
        :param parent_record: Родительская запись.
        :param data: Список словарей каскадных данных:
        [{
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        },...]
        :return: Возвращает True/False.
        """
        tab = self._tabObj(table)
        if tab:
            recs = tab.get_where(tab.c.parent == parent_record['uuid']).fetchall()
            data_rec_count = len(data)
            for i, rec in enumerate(recs):
                if i < data_rec_count:
                    # Обновление записи
                    data_rec = dict([(str(key), value) for key, value in data[i].items()])
                    tab.update_where(tab.c.uuid == rec['uuid'], **data_rec)
                else:
                    # Удаление записи
                    tab.del_where(tab.c.uuid == rec['uuid'])
            if data_rec_count > len(recs):
                for i in range(len(recs), data_rec_count):
                    # Добавление записи
                    new_rec = dict([(str(key), value) for key, value in data[i].items()])
                    new_rec['parent'] = parent_record['uuid']
                    new_rec['uuid'] = self.genUUID()
                    link_names = [fld['name'].lower() for fld in tab.res['child'] if fld['type'] == 'Link']
                    for lnk_name in link_names:
                        new_rec[lnk_name] = parent_record['id']
                    tab.add(**new_rec)
                     
            result = True
            children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__, icObjPersistent)]
            # Обработка дочерних объектов
            for child_obj in children_obj:
                child_tab_name = child_obj.getTableName()
                for rec in data:
                    if child_tab_name in rec:
                        child_uuid = rec['uuid']
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              rec[child_tab_name], rec)
            return result
        return False

    def _load_data(self, UUID=None):
        """
        Загрузить внутренние данные из хранилища.

        :param UUID: Идентификатор.
        :return: Возвращает словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        .
        """
        try:
            if UUID is None:
                UUID = self.getUUID()
            return self._getCascadeDataTab(self.getTable(), UUID, True)
        except:
            log.error(u'Ошибка загрузки данных мета-объекта [%s]' % self.name)
            return None
        
    def load_data(self, UUID=None):
        """
        Загрузить внутренние данные из хранилища.

        :param UUID: Идентификатор.
        :return: Возвращает словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        .
        """
        return self._load_data(UUID=UUID)

    def load(self, UUID=None):
        """
        Загрузить внутренние данные из хранилища.

        :param UUID: Идентификатор.
        :return: True/False.
        """
        try:
            cascade_data = self._load_data(UUID)
            return self._setCascadeData(cascade_data)
        except:
            log.error(u'Ошибка загрузки данных мета-объекта [%s]' % self.name)
            return None
    
    def _getCascadeDataTab(self, table, UUID, bOneBreak=False):
        """
        Получить каскад данных из хранилища.

        :param table: Таблица.
        :param UUID: Иникальный идентификатор.
        :param bOneBreak: В данных дочерних объектов только одна запись?
        :return: Словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        """
        try:
            tab = self._tabObj(table)
            if tab:
                rec = tab.get_where(tab.c.uuid == UUID).fetchone()
                data = dict([(fld_name, rec[fld_name]) for fld_name in tab.getFieldNames()]) if rec else dict()
                
                # Обработать дочерние объекты
                children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__,
                                                                                              icObjPersistent)]
                for child_obj in children_obj:
                    tab_name = child_obj.getTableName()
                    data[tab_name] = child_obj._getChildCascadeDataTab(child_obj.getTable(), UUID)
                
                return data
        except:
            log.error(u'Ошибка определения каскада данных объекта [%s] из хранилища' % self.name)
        return None

    def _getChildCascadeDataTab(self, table, parent_uuid):
        """
        Получить каскад данных из хранилища.

        :param table: Таблица.
        :param parent_uuid: Уникальный идентификатор родительской записи.
        :return: Словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        """
        tab = self._tabObj(table)
        if tab:
            recs = tab.get_where(tab.c.parent == parent_uuid).fetchall()
            children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__,
                                                                                          icObjPersistent)]
            data = []
            for rec in recs:
                rec_dict = dict([(fld_name, rec[fld_name]) for fld_name in tab.getFieldNames()])
                
                # Обработать дочерние объекты
                for child_obj in children_obj:
                    tab_name = child_obj.getTableName()
                    rec_dict[tab_name] = child_obj._getChildCascadeDataTab(child_obj.getTable(), rec['uuid'])
                data.append(rec_dict)
                
            return data
        return None
        
    def _setCascadeData(self, data):
        """
        Каскадная установка значений реквизитов.

        :param data: Словарь данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        """
        try:
            # соответствие имен полей и реквизитов
            fld_requisites_dict = dict([(requisite.getFieldName(), requisite) for requisite in self.getChildrenRequisites()])
            
            # Выбрать только данные реквизитов
            requisites_data = dict([(fld_name, fld_value) for fld_name, fld_value in data.items()
                                    if not isinstance(fld_value, list)])
            # Раставить значения реквизитов
            for fld_name, fld_value in requisites_data.items():
                if fld_name in fld_requisites_dict:
                    fld_requisites_dict[fld_name].setValue(fld_value)
            
            result = True
            # Обработать дочерние объекты
            children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__,
                                                                                          icObjPersistent)]
            for child_obj in children_obj:
                if child_obj.name in data and data[child_obj.name]:
                    # ВНИМАНИЕ!!!
                    # Заполнение реквизитов дочерних объектов производится только по первой строке
                    result = result and child_obj._setCascadeData(data[child_obj.name][0])
            return result
        except:
            log.fatal(u'Ошибка каскадной установки значений реквизитов мета-объекта [%s]' % self.name)
        return False

    def _getCascadeDataObj(self, bInsertChildData_=True):
        """
        Сборка данных объекта в виде каскадного словаря:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }

        :param bInsertChildData_: Включать в каскад значения реквизитов
            дочерних объектов?
        """
        # Заполнить данными реквизитов
        data = {}
        # ВНИМАНИЕ! Здесь идет перебор по реквизитов объекта
        # т.к. значения берутся из реквизитов
        for child in self.getChildrenRequisites():
            if issubclass(child.__class__, icAttrPersistent):
                child_data = child.getValue()
                if isinstance(child_data, dict):
                    # Сразу определен словарь
                    data.update(child_data)
                else:
                    data[child.getFieldName()] = child_data
            elif issubclass(child.__class__, icObjPersistent):
                records = child._getData(data_filter={'parent': self.getUUID()})
                if bInsertChildData_:
                    # Взять из объектов
                    records = [child._getCascadeDataObj(bInsertChildData_)]
                else:
                    # Взять из таблиц
                    records = child._getData(data_filter={'parent': self.getUUID()})
                    
                if modefunc.isDebugMode():
                    log.info(u'CHILD: <%s> RECORDS: %s' % (child.name, records))
                    
                data[child.name] = records
                
        # Добавить идентификатор
        data['uuid'] = self.getUUID()

        return data

    def _getCascadeDefaultDataObj(self, bInsertChildData_=True):
        """
        Сборка данных по умолчанию объекта в виде каскадного словаря:
        {
        'имя поля реквизита':значение по умолчанию,
        ...
        'имя дочернего объекта':[список словарей значений по умолчанию],
        ...
        }

        :param bInsertChildData_: Включать в каскад значения реквизитов
            дочерних объектов?
        """
        # Заполнить данными реквизитов
        data = {}
        for child in self.getChildren():
            if issubclass(child.__class__, icAttrPersistent):
                child_data = child.getDefault()
                if isinstance(child_data, dict):
                    # Сразу определен словарь
                    data.update(child_data)
                else:
                    data[child.getFieldName()] = child_data
            elif issubclass(child.__class__, icObjPersistent):
                if bInsertChildData_:
                    # Взять из объектов
                    records = [child._getCascadeDefaultDataObj(bInsertChildData_)]
                else:
                    # Взять из таблиц
                    pass
                    
                if modefunc.isDebugMode():
                    log.info(u'CHILD: <%s> RECORDS: %s' % (child.name, records))
                    
                data[child.name] = records
                
        return data
    
    def getValue(self):
        """
        Каскад данных объекта.
        """
        try:
            return self._getCascadeDataObj()
        except:
            log.fatal(u'Ошибка определения данных мета-объекта [%s]' % self.name)
        return None

    def setValue(self, value):
        """
        Установить значения всех реквизитов.

        :param value: Словарь значений реквизитов.
        """
        try:
            for child in self.getChildrenRequisites():
                child.setValue(value[child.getFieldName()])
            return True
        except:
            log.fatal(u'Ошибка установки данных мета-объекта [%s]' % self.name)
        return None

    def _getData(self, table=None, data_filter=None):
        """
        Отфильтрованные данные.

        :param table: Объект таблицы.
        :param data_filter: Дополнительный фильтр.
        :return: Возвращает список отфильтрованных данных.
        """
        if table is None:
            table = self.getTable()
        try:
            tab = self._tabObj(table)
            if tab:
                return tab.queryAll(data_filter)
            else:
                if modefunc.isDebugMode():
                    log.error(u'Не определена таблица мета-объекта [%s]' % self.name)
        except:
            log.fatal(u'Ошибка получения отфильтрованных данных объекта [%s]' % self.name)
        return None

    def add(self, UUID=None, data=None, table=None):
        """
        Добавить в хранилище текущий объект.

        :param UUID: Идентификатор.
        Если None, то генерируется новый uuid.
        :param table: Главная таблица объекта. Если не указана, то генерируется.
        :return: Возвращает результат выполнения операции True/False.
        """
        if UUID is None:
            # Если uuid не указан явно, то сгенерировать новый
            UUID = self.genUUID()
        # Если сразу указаны данные для заполненения, то записать их
        data_dict = self.getChildrenDefault()
        if data is None:
            # Получить данные объекта в каскадном представлении
            data_dict_obj = self._getCascadeDataObj(True)
            data_dict.update(data_dict_obj)
        elif isinstance(data, dict):
            data_dict.update(data)
        else:
            log.warning(u'Не корректный тип данных <%s> объекта <%s>' % (data.__class__.__name__,
                                                                         self.getName()))
            return False

        session = None
        try:
            tab = table if table else self.getTable()
            if tab:
                # Начать транзакцию
                session = tab.db.getSession()
                session.begin()

                # if ic_mode.isDebugMode():
                #     log.info(u'Meta-object [%s] Add data: %s' % (self.name, data_dict))

                result = self._addCascadeData(tab, data_dict)
                
                # Закончить транзакцию
                session.commit()
                
                return result
        except:
            if session:
                # Откатить транзакцию
                session.rollback()
                # session.clear()
            log.fatal(u'Ошибка добавления в хранилище объекта [%s]' % self.name)
        return False

    def findChildByName(self, child_name):
        """
        Поиск дочернего реквизита по имени.

        :param child_name: Имя дочернего реквизита
        :return: Объект реквизита или None если реквизит не найден.
        """
        find_children = [child for child in self.getChildrenRequisites()
                         if issubclass(child.__class__, icObjPersistent) and child.getName() == child_name]
        if find_children:
            return find_children[0]
        return None

    getRequisite = findChildByName

    def _tabObj(self, table):
        """
        Таблица объекта.

        :param table: Объект/таблица, в который будет сохраняться запись.
        """
        # Таблица данных
        if isinstance(table, str):
            # Таблица данных передается в виде имени
            if table == self.getTableName():
                # Таблица задается именем таблицы
                tab = self.getTable()
            elif self.findChildByName(table):
                # Таблица задается именем табличного реквизита
                child = self.findChildByName(table)
                tab = icsqlalchemy.icSQLAlchemyTabClass(child.getTableName())
            else:
                # Просто определить таблицу по имени
                tab = icsqlalchemy.icSQLAlchemyTabClass(table)
        elif isinstance(table, tuple):
            # Таблица данных передается в виде паспорта
            tab = self.getKernel().Create(table)
        else:
            # Таблица передается как есть
            tab = table
        return tab
        
    def _addCascadeData(self, table, data_dict, parent_record=None):
        """
        Добавление каскадного словаря значений в объект хранилища.

        :param table: Объект/таблица, в который будет сохраняться запись.
        :param data_dict: Словарь значений.
            Словарь представлен в виде 
                {
                'имя поля реквизита':значение,
                ...
                'имя дочернего объекта':[список словарей значений],
                ...
                }
        :param PrentRecord_: Объект родительской записи для организации каскада.
        :return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            tab = self._tabObj(table)
            # Добавление записи
            rec = dict([(str(key), value) for key, value in data_dict.items() if not isinstance(value, list)])
            
            # Если при добавлении не указан UUID, то сгенерировать его
            if ('uuid' not in rec) or (not rec['uuid']):
                rec['uuid'] = self.genUUID()
            
            # Если у объекта есть родительский объект, то указать его uuid
            if self._parent:
                rec['parent'] = self._parent.getUUID()
                
            # Если есть родительская таблица, то проинициализировать
            # ссылки на ее в текущей записи
            if parent_record:
                link_names = [fld['name'].lower() for fld in tab.res['child'] if fld['type'] == 'Link']
                for lnk_name in link_names:
                    inserted_rec = parent_record.last_inserted_params()
                    # ВНИМАНИЕ! В sqlalchemy идентификатор последней добавленной записи
                    #                                    v
                    rec[lnk_name] = parent_record.inserted_primary_key[0] if parent_record.inserted_primary_key else 0
                    rec['parent'] = inserted_rec.get('uuid', None)
                
            # Если вдруг ключи юникодовые то изменить их на строковые
            rec_obj = tab.add(**rec)
            # Обработка дочерних таблиц
            children_obj = dict([(name, data) for name, data in data_dict.items() if isinstance(data, list)])
            for tab_name in children_obj.keys():
                # Обработка дочерних таблиц
                for rec in children_obj[tab_name]:
                    self._addCascadeData(tab_name, rec, rec_obj)
            return True
        except:
            log.fatal(u'Ошибка добавления данных в каскад таблицы <%s>.' % table)
        return None

    def delete(self, UUID=None):
        """
        Удалить из хранилища текущий объект.

        :param UUID: Идентификатор.
        Если None, то берется uuid объекта.
        :return: Возвращает результат выполнения операции True/False.
        """
        if UUID is None:
            # Если uuid не указан явно, то взять текущий объекта
            UUID = self.getUUID()

        transaction = None
        try:
            tab = self.getTable()
            if tab:
                # Начать транзакцию
                transaction = tab.db.getSession()
                transaction.begin()

                # Получить данные объекта в каскадном представлении
                if modefunc.isDebugMode():
                    log.info(u'Meta-object [%s] Delete data: <%s>' % (self.name, UUID))
                recs = tab.get_where(tab.c.uuid == UUID)

                # Получить идентификатор записи
                rec_id = 0
                if recs:
                    recs_first = recs.first()
                    rec_id = recs_first.id if recs_first else 0

                if rec_id:
                    result = self._delCascadeData(tab, rec_id, transaction)
                else:
                    log.warning(u'Не найдена запись объекта с UUID <%s>' % UUID)
                    result = False
                
                # Завершить транзакцию
                transaction.commit()
                
                return result
        except:
            if transaction:
                # Откатить транзакцию
                transaction.rollback()
                # session.clear()
            log.fatal(u'Ошибка удаления из хранилища объекта [%s]' % self.name)
        return False

    def clear(self, bAsk=False):
        """
        Удалить из хранилища все объекты.

        :param bAsk: Спросить об удалении всех объектов?
        :return: Возвращает результат выполнения операции True/False.
        """
        is_clear = dlgfunc.openAskBox(u'ВНИМАНИЕ!', u'Удалить все объекты <%s>?' % self.name) if bAsk else True
        if not is_clear:
            # Не разрешео удалять действиями пользвателя
            return False

        transaction = None
        try:
            tab = self.getTable()
            if tab:
                # Начать транзакцию
                transaction = tab.db.getSession()
                transaction.begin()

                # Получить идентификаторы объектов для каскадного удаления
                records = transaction.query(tab.dataclass.columns.id).all()
                obj_ids = [rec[0] for rec in records]
                if modefunc.isDebugMode():
                    log.info(u'Meta-object [%s] Clear all data %s' % (self.name, obj_ids))

                result = True
                for obj_id in obj_ids:
                    result = result and self._delCascadeData(tab, obj_id,
                                                             transaction=transaction)

                # Завершить транзакцию
                transaction.commit()

                return result
        except:
            if transaction:
                # Откатить транзакцию
                transaction.rollback()
                # session.clear()
            log.fatal(u'Ошибка очистки объектов [%s] из хранилища' % self.name)
        return False

    def _getUuidsByParent(self, table, parent_uuid):
        """
        Получение уникальных идентификаторов по идентификатору родителя.
        """
        tab = self._tabObj(table)
        return [rec.uuid for rec in tab.select(tab.c.parent == parent_uuid)]

    def _delCascadeData(self, table, rec_id, transaction=None):
        """
        Удалить каскад данных из хранилища по уникальонму идентификатору.

        :param table: Объект таблицы.
        :param rec_id: Идентификатор удаляемой записи.
        :param transaction: Объект транзакции.
        :return: True/False.
        """
        result = True
        # Таблица данных
        tab = self._tabObj(table)
        if not tab:
            # Таблица не определена по какойто причине
            log.warning(u'Удаление данных. Не определена таблица <%s>' % table)
            return False
        try:
            # ВНИМАНИЕ! Сначала нужно удалять записи
            # из дочерних таблиц иначе будет нарушение
            # целостности данных

            # Обработать дочерние объекты
            children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__,
                                                                                          icObjPersistent)]
            for child_obj in children_obj:
                child_tab = child_obj.getTable()
                where = icsqlalchemy.and_(getattr(child_tab.c, child_tab.getLinkIdFieldName(tab)) == rec_id)
                child_recs = child_tab.get_where(where)
                if child_recs:
                    for child_rec in child_recs.fetchall():
                        result = result and child_obj._delCascadeData(child_tab, child_rec['id'], transaction)
                else:
                    log.info(u'Не найдено дочерних записей в таблице <%s>' % child_tab.getDBTableName())

            # Удалить запись из родительской таблицы в конце
            tab.del_where_transact(tab.c.id == rec_id,
                                   transaction=transaction)
            return result
        except:
            log.fatal(u'Ошибка каскадного удаления данных из таблицы <%s>.' % table)
        return False

    def getChildrenRequisites(self):
        """
        Все реквизиты объекта в виде списка.
            Метод должен переопределяться в классе-компоненте.
        """
        return list()

    def getChildren(self):
        """
        Все внутренние объекты: реквизиты объекта и вложенные объекты в виде списка.
        """
        return list()
        
    def getDefaultRequisites(self):
        """
        Все реквизиты объекта по умолчанию в виде списка.
        """
        return list()

    def getChildrenDefault(self):
        """
        Получить словарь значений реквизитов по умолчанию.

        :return: Словарь {'имя реквизита': значение реквизита по умолчанию, ...}
        """
        defaults = dict()
        for child in self.getChildrenRequisites():
            default = child.getDefault()
            if default is None:
                # Значение по умолчанию не указано
                continue
            elif isinstance(default, dict):
                # Если значение по умолчанию задается словарем
                # значит надо выставить значения по умолчанию
                # нескольких реквизитов
                defaults.update(default)
            else:
                defaults[child.getName()] = default
        return defaults

    # Функции создания ресурса таблиц хранения объекта
    def _createTableResource(self, parent_tabname=None):
        """
        Создание по описанию объекта ресурса таблицы, в 
            которой хранятся данные объекта.

        :param parent_tabname: Имя родительской таблицы.
        """
        # Открыть проект
        prj_res_ctrl = glob_functions.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()
    
        # Проверка на добавление нового ресурса
        table_name = self.getTableName()
        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if table_name and not prj_res_ctrl.isRes(table_name, 'tab'):
            table_res = self._createTabRes(table_name)
            # Создать связь с родительской таблицей
            if parent_tabname:
                link_spc = self._createLinkSpc(parent_tabname)
                table_res['child'].append(link_spc)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(table_name, 'tab', table_res)
            
    def _createLinkSpc(self, table_name):
        """
        Создать спецификацию связи c таблицей.
        """
        # Инициализировать спецификацию связи
        link_spc = util.icSpcDefStruct(util.DeepCopy(ic_link_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        link_spc['name'] = 'id_' + table_name.lower()
        link_spc['description'] = strfunc.str2unicode('Связь с таблицей ' + table_name)
        link_spc['table'] = (('Table', table_name, None, None, None),)
        link_spc['del_lnk'] = True
        return link_spc
        
    def _createTabRes(self, table_name=None):
        """
        Создать ресурс таблицы хранения спецификации/объекта.
        """
        if table_name is None:
            table_name = self.getTableName()

        tab_res = self._createTabSpc(table_name)
        # Перебрать дочерние компоненты
        children_requisites = self.getChildrenRequisites()
        if children_requisites:
            for child_requisite in children_requisites:
                if issubclass(child_requisite.__class__, icAttrPersistent):
                    # Это реквизит
                    fields_spc = child_requisite._createFieldSpc()
                    if fields_spc is None:
                        log.warning(u'Не определена спецификация поля при создании таблицы хранимого объекта')
                    tab_res['child'].append(fields_spc)
                elif issubclass(child_requisite.__class__, icObjPersistent):
                    # Это спецификация табличной части
                    child_requisite._createTableResource(table_name)
                    # Прописать имя дочерней ьаблицы в списке подчиненных таблиц
                    tab_res['children'].append(child_requisite.getTableName())
                else:
                    log.warning(u'Неизвестный тип дочернего компонента <%s> объекта' % child_requisite)
                    
        return tab_res
       
    def _createTabSpc(self, table_name=None):
        """
        Создать спецификацию таблицы.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if table_name is None:
            table_name = self.getTableName()
        tab_spc['name'] = table_name
        tab_spc['description'] = strfunc.str2unicode(self.description)
        tab_spc['table'] = table_name.lower()
        tab_spc['source'] = self.getDBPsp()
        
        tab_spc['children'] = []    # Список имен подчиненных таблиц

        # Поле идентификатора объекта
        field_spc = self._createUuidFieldSpc()
        tab_spc['child'].append(field_spc)
        
        # Если у объекта есть родитель, то в таблице
        # должна отражатся информация о родителе
        if self._parent:
            field_spc = self._createFieldSpc('parent')
            tab_spc['child'].append(field_spc)
        
        # Перебрать все стандартные реквизиты и добавить их в виде полей в
        # ресурс таблицы
        for std_requisite in self.getDefaultRequisites():
            field_spc = std_requisite._createFieldSpc()
            tab_spc['child'].append(field_spc)
            
        return tab_spc

    def _createFieldSpc(self, field_name, field_type='T', field_len=None, field_default=None):
        """
        Создать спецификацию поля.
        Функция необходима для вспомогательных и 
        служебных полей.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = field_name
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = field_type
        field_spc['len'] = field_len
        field_spc['attr'] = 0
        field_spc['default'] = field_default
        
        return field_spc

    def getFilterEnv(self):
        """
        Окружение конструктора фильтров объектов.
        """
        if self.filter_environment is None:
            self.filter_environment = self._genFilterEnv()
        return self.filter_environment
    
    def _genFilterEnv(self):
        """
        Генерация окружения конструктора фильтров объекта.
        """        
        env = {'requisites': [],  # Список возможных для выбора реквизитов
               'logic': filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS,  # Стандартные логические операции
               'funcs': filter_builder_env.DEFAULT_ENV_FUNCS,  # Стандартные функции
               }
        
        for requisite in self.getChildrenRequisites():
            if requisite.isSearch():
                req_env = dict()
                req_env['name'] = requisite.name
                req_env['description'] = requisite.description
                req_env['field'] = requisite.getField()
                req_env['type'] = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(requisite.getTypeValue())
                req_env['funcs'] = requisite.getFilterFuncs()
                if requisite.type == 'NSIRequisite':
                    # Для привязки контрола редактирования фильтрами
                    # необходимо их перепривязывать к справочнику
                    req_env['nsi_psp'] = requisite.getICAttr('nsi_psp')
                
                env['requisites'].append(req_env)
        return env
    
    def getFilterSQL(self, data_filter=None, fields=None, limit=None):
        """
        Фильтр в SQL представлении.

        :param data_filter: Фильтр.
        :param fields: Поля выбора. Если None, то будут выбираться только
        идентифицирующие объект поля.
        :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        if fields is None:
            fields = tuple([requisite.getFieldName() for requisite in self.getChildrenRequisites() if requisite.isIDAttr()])
        if not fields:
            fields = ('*',)
        else:
            # Необхдимо, что бы в результате запроса всегда
            # присутствовал UUID  объекта
            fld_lst = list(fields)
            fld_lst.append('uuid')
            fields = tuple(fld_lst)
            
        sql = filter_convert.convertFilter2PgSQL(data_filter, self.getTableName(), fields,
                                                 limit=limit)
        return sql

    def getFilterSQLAlchemy(self, sql_filter=None, fields=None, limit=None):
        """
        Фильтр в SQLAlchemy представлении.

        :param sql_filter: Фильтр.
        :param fields: Поля выбора. Если None, то будут выбираться только 
        идентифицирующие объект поля.
        :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        if fields is None:
            field_list = [requisite.getFieldName() for requisite in self.getChildrenRequisites()
                          if requisite.isIDAttr()]
            # ВНИМАНИЕ! Обязательно должен присутствовать UUID
            # иначе идентифицировать объект никак не получится
            field_list += ['uuid'] if 'uuid' not in field_list else list()
            fields = tuple(field_list)
        elif fields == '*':
            fields = ('*',)
        else:
            # Необхдимо, что бы в результате запроса всегда
            # присутствовал UUID  объекта
            fld_lst = list(fields)
            fld_lst.append('uuid')
            fields = tuple(fld_lst)

        query = filter_convert.convertFilter2SQLAlchemy(sql_filter, self.getTable(), fields,
                                                        limit=limit)
        return query

    def _resultFilter2Dataset(self, filter_result):
        """
        Подготовка результата фильтрации в виде датасета для 
        грида объектов в виде списка словарей.

        :param filter_result: Список записей - результат фильтрации.
        :return: Список словарей записей - результат фильтрации.
        """
        # Из-за оптимизации функции код стал менее читабельным
        # Словарь соответствий имя поля: справочник реквизита
        nsi_requisite_spravs = dict(
            [(requisite.getFieldName(), requisite.getSprav()) for requisite in self.getChildrenRequisites() if
             requisite.isIDAttr() and requisite.type == 'NSIRequisite'])
        # Замена кодов идентифицирующих реквизитов на значение <КОД Наименование>
        recordset = [dict(
            [(NSI_CODE_PREFIX + fld_name, value) if value and fld_name in nsi_requisite_spravs else (fld_name, value)
             for fld_name, value in record.items()]) for record in filter_result]

        for record in recordset:
            for fld_name, sprav in nsi_requisite_spravs.items():
                # Получить запись справочника по коду
                nsi_record = sprav.getCachedRec(record.get(NSI_CODE_PREFIX + fld_name, u''))
                # log.debug(u'NSI record: %s' % str(nsi_record))
                # Взять только наименование
                record[fld_name] = nsi_record.get('name', u'') if nsi_record is not None else u''
        return recordset

    def _prepareDatasetRecord(self, requisite_data=None):
        """
        ВНИМАНИЕ! Для реквизитов справочников поля должны преабразовываться
        в виде field_name = name и _field_name = cod.
        Эта функция это и делает. Используется в менеджере навигации
        документов для корректного отображения на экране а также в
        контролах работы с документами.

        :param requisite_data: Словарь данных реквизитов.
        :return: Подготовленный словарь данных.
        """
        if requisite_data is None:
            requisite_data = self.getRequisiteData()
        # Словарь соответствий имя поля: справочник реквизита
        nsi_requisite_spravs = dict(
            [(requisite.getFieldName(), requisite.getSprav()) for requisite in self.getChildrenRequisites() if
             requisite.isIDAttr() and requisite.type == 'NSIRequisite'])
        for fld_name, sprav in nsi_requisite_spravs.items():
            # Получить запись справочника по коду
            nsi_code = requisite_data.get(fld_name, u'')
            nsi_record = sprav.getCachedRec(nsi_code)
            # log.debug(u'NSI record: %s' % str(nsi_record))
            requisite_data[NSI_CODE_PREFIX + fld_name] = nsi_code
            requisite_data[fld_name] = nsi_record.get('name', u'') if nsi_record is not None else u''
        return requisite_data

    def getRequisiteData(self):
        """
        ВНИМАНИЕ! Этот метод переопределяется в дочерних классах.

        Получить все реквизиты документа/спецификации в виде словаря.

        :return: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
        """
        log.warning(u'Не определен метод получения реквизитов документа/спецификации в виде словаря.')
        return dict()

    def filterRequisiteData(self, filter_requisite_data=None):
        """
        Отфильтровать объекты согласно данным фильтра.

        :param filter_requisite_data: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        :return: Возвращает список-dataset объектов, соответствующих заданному фильтру.
        """
        if filter_requisite_data is None:
            # Если None, то берется текущий фильтр бизнес объектов.
            filter_requisite_data = self.getFilter()

        if filter_requisite_data is None:
            # Если фильтр не определен, то показываем все объекты
            filter_requisite_data = {}
        # Сначала убрать значения реквизитов с не указанными значениями
        filter_requisite_data = dict([(name, value) for name, value in filter_requisite_data.items() if value])
        return filter_requisite_data

    def getDataDict(self, filter_requisite_data=None, limit=None):
        """
        Набор записей.Каждая запись в виде словаря.
        Этот метод также имеет название getDataset и getRecordset.

        :param filter_requisite_data: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        :return: Список словарей записей.
        """
        if not filter_requisite_data:
            filter_requisite_data = None

        log.info(u'Бизнес-объект <%s>. Получение набора записей' % self.getName())
        data_filter = self.filterRequisiteData(filter_requisite_data)
        if limit is None:
            limit = self._limit
        # log.info(u'\tФильтр: <%s>. Ограничение кол. записей: [%s]' % (data_filter, limit))
        query = self.getFilterSQLAlchemy(data_filter, limit=limit)
        # log.info(u'\tЗапрос <%s>' % query)
        result = self.getTable().getConnection().execute(query)
        log.info(u'\tКол. записей результата: [%s]' % result.rowcount)
        start_time = time.time()
        recordset = self._resultFilter2Dataset(result.fetchall())
        # log.info(u'\tПреобразование списка записей. Время выполнения: %s' % str(time.time()-start_time))
        return recordset

    # Другие наименования метода
    getDataset = getDataDict
    getRecordset = getDataDict

    def countDataDict(self, filter_requisite_data=None):
        """
        Количество записей набора записей.
        Этот метод также имеет название countDataset и countRecordset.

        :param filter_requisite_data: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        :return: Возвращает количество записей набора записей, удовлетворяющих фильтру.
        """
        if not filter_requisite_data:
            filter_requisite_data = None

        log.info(u'BUSINES OBJECT get count data')
        data_filter = self.filterRequisiteData(filter_requisite_data)
        log.info(u'\tFilter: <%s>' % data_filter)
        query = self.getFilterSQLAlchemy(data_filter)
        # ВНИМАНИЕ! Подзапрос должен иметь алиас.
        # Иначе возникает ошибка SQL <ERROR:  subquery in FROM must have an alias>
        #               v
        query = query.alias().count()
        log.info(u'\tQuery: <%s>' % query)
        # Небходимо просто получить число. Поэтому берем значение явно
        #                                                          v
        result = self.getTable().getConnection().execute(query).fetchone()
        int_result = result[0]
        log.info(u'\tResult: [%s]' % int_result)
        return int_result

    # Другие наименования метода
    countDataset = countDataDict
    countRecordset = countDataDict

    def findRequisiteData(self, **find_requisite_data):
        """
        Найти UUIDы объектов согласно данным фильтра.

        :param find_requisite_data: Словарь значений реквизитов фильтров.
            Если не указан, то берется текущий фильтр бизнес объектов.
            Сравнение происходит по <И>.
        :return: Возвращает uuidы объектов, соответствующих заданному фильтру.
            Если ничего не найдено, то возвращается пустой список.
        """
        if not find_requisite_data:
            filter_requisite_data = None
        else:
            # Если фильтр по значениям реквизитам указан, то
            # сделать фильтр
            compare_list = [filter_generate.create_filter_compare_requisite(name, '==', value) for name, value in find_requisite_data.items()]
            filter_requisite_data = filter_generate.create_filter_group_AND(*compare_list)

        find_dataset = self.getDataDict(filter_requisite_data)

        if find_dataset:
            find_dataset = [record.get('uuid', None) for record in find_dataset]
        return find_dataset


class icAttrPersistent(object):
    """
    Базовый класс атрибута компонента хранимого в БД.
        Реализует внутри себя механизм генерации спецификации хранения.
    """

    def __init__(self, parent=None):
        """
        Конструктор.

        :param parent: Родительский объект.
        """
        self.name = ''

    def getName(self):
        """
        Имя объекта.
        """
        return self.name

    def getField(self):
        """
        Имя поля хранения значения атрибута.
        """
        return None

    def getDefault(self):
        """
        Значение атрибута по умолчанию.
        """
        return None

    def _genFieldName(self):
        """
        Генерация имени поля.
        """
        try:
            field_name = str(self.name).lower()
        except UnicodeEncodeError:
            log.error(u'Не латинские буквы в имени атрибута <%s> запрещены' % self.name)
            field_name = 'no_name_field'
        return field_name
        
    def getFieldName(self):
        """
        Имя поля хранения значения атрибута.
        """
        field = self.getField()
        if field:
            return field
        else:
            return self._genFieldName()
        
    def _createFieldSpc(self):
        """
        Создать спецификацию поля ресурса.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = self.getFieldName()
        field_spc['name'] = field_name
        field_spc['description'] = strfunc.str2unicode(self.description)
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = self.type_val
        field_spc['len'] = self.len
        field_spc['attr'] = 0
        field_spc['default'] = self.getDefault()
        
        return field_spc
       
    def _createFieldsSpc(self):
        """
        Создать спецификацию поля ресурса регистра.
        """
        return [self._createFieldSpc()]
        
    def getDefault(self):
        """
        Значение по умолчанию.
        """
        return None
    
    def getFilterFuncs(self):
        """
        Список функций фильтрации.
        """
        req_type = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(self.getTypeValue())
        return filter_builder_env.DEFAULT_FUNCS.get(req_type)


class icAccRegPersistent(icObjPersistent):
    """
    Класс персистента регистра накопления.
        В самом регистре присутствует вся информация о схеме
        объекта. Этот класс необходим для организации
        интерфейсных функций работы с объектом из
        скриптов прикладного уровня.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icObjPersistent.__init__(self, *args, **kwargs)

    def getTable(self):
        """
        Таблица хранения операций.
        """
        return self.get_operation_table()

    def getDataDict(self, limit=None):
        """
        Данные операций.
            Набор записей. Каждая запись в виде словаря.
            ВНИМАНИЕ! Функция переписана для адаптации
            списка операций движения регистра накопления
            для просмотра в контролах.

        :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        data_filter = self.filterRequisiteData()
        query = self.getFilterSQLAlchemy(data_filter, fields='*', limit=limit)
        result = query.execute()
        log.info(u'ACCUMULATE REGISTRY get data\n\tResult: [%s]' % result.rowcount)
        return self._resultFilter2Dataset(result.fetchall())


class icNodePersistent(icObjPersistent):
    """
    ВНИМАНИЕ! Пока не реализовано!!!

    Класс поддержки хранения данных объектов связанных объектов/документов.
        Связи осуществляются при помощи UUIDов объектов.
        Связь документов организована двух видов:
        1. Взаимодействие в виде древовидной структуры
            Для реализации связей используются поля parent_uuid и children_uuid.
            parent_uuid - список UUIDов родительских объектов текущего объекта
            children_uuid - список UUIDов дочерних объектов текущего объекта
        2. Взаимодействие в виде ссылок (Для организации графов)
            Для реализации связей используется поле link_uuid.
            link_uuid - список UUIDов объектов на которые ссылается текущий объект

        Также присутствует поле obj_type - код справочника типов объектов
        Справочник типов объектов - справочник, определяющий правила связей объектов по типам.
        В нем должны быть определены поля:
            can_contain - список типов объектов, которые могут включаться в объект в качестве дочерних
            can_not_contain - список типов объектов, которые НЕ могут включаться в объект в качестве дочерних
            can_link - список типов объектов, на которые может ссылаться объект
            can_not_link - список типов объектов, на которые НЕ может ссылаться объект
            default - словарь значений реквизитов, заполняемых по умолчанию при создании нового объекта указанного типа
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icObjPersistent.__init__(self, *args, **kwargs)

    def newChildObject(self, obj_type_code, default=None):
        """
        Создание нового дочернего объекта по его типу.
        После создания объект автоматически прописывается как дочерний.
        При создании объекта производиться контроль на возможность использования
        типа объекта как дочернего.

        :param obj_type_code:  Код типа дочернего объекта.
        :param default: Словарь реквизитов, заполняемых по умолчанию нового дочернего объекта.
            Если не указывается, то этот словарь берется из справочника типов объектов.
        :return: True - дочерний объект успешно создан и зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def addChildObject(self, child_obj):
        """
        Регистрация существующего объекта как дочернего.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как дочернего.

        :param child_obj: Объект - наследник icNodePersistent
        :return: True - дочерний объект успешно зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def addChildObjectUUID(self, child_obj_uuid):
        """
        Регистрация существующего объекта как дочернего по его UUID.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как дочернего.

        :param child_obj_uuid: UUID объекта добавляемого, как дочерний.
            Объект с таким UUID должен уже присутствовать в таблице объектов.
        :return: True - дочерний объект успешно зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def delChildObject(self, child_obj, auto_delete=False):
        """
        Удаление зарегистрированного существующего объекта из списка дочерних.

        :param child_obj: Объект - наследник icNodePersistent
        :param auto_delete: Проверить автоматическое удаление дочернего объекта, если
            он больше не связан с другим родительским объектом.
            Удаление дочерних объектов происходит каскадно.
        :return: True - дочерний объект успешно удален как дочерний.
            False - какая-либо ошибка удаления.
        """
        pass

    def delChildObjectUUID(self, child_obj_uuid, auto_delete=False):
        """
        Удаление зарегистрированного существующего объекта из списка
        дочерних по его UUID.

        :param child_obj_uuid: UUID удаляемого дочернего объекта.
        :param auto_delete: Проверить автоматическое удаление дочернего объекта, если
            он больше не связан с другим родительским объектом.
            Удаление дочерних объектов происходит каскадно.
        :return: True - дочерний объект успешно удален как дочерний.
            False - какая-либо ошибка удаления.
        """
        pass

    def getChildObjectUUID(self, child_obj_uuid):
        """
        Получить дочерний объект текущего по его UUID.
        При получении объекта производиться проверка на
        существование зарегистрированного дочернего объекта.

        :param child_obj_uuid: UUID запрашиваемого дочернего объекта.
        :return: Объект наследник icNodePersistent с заполненными данными дочернего объекта
            или None, если запрашиваемый объект не является дочерним текущего.
        """
        pass

    def newLinkObject(self, obj_type_code, default=None):
        """
        Создание нового объекта-ссылки по его типу.
        После создания объект автоматически прописывается в списке ссылок.
        При создании объекта производиться контроль на возможность использования
        типа объекта как ссылочного.

        :param obj_type_code:  Код типа объекта.
        :param default: Словарь реквизитов, заполняемых по умолчанию нового объекта.
            Если не указывается, то этот словарь берется из справочника типов объектов.
        :return: True - объект успешно создан и зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def addLinkObject(self, link_obj):
        """
        Регистрация существующего объекта как ссылочного.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как ссылочного.

        :param link_obj: Объект - наследник icNodePersistent
        :return: True - объект успешно зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def addLinkObjectUUID(self, link_obj_uuid):
        """
        Регистрация существующего объекта как ссылочного по его UUID.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как ссылочного.

        :param link_obj_uuid: UUID объекта добавляемого, как ссылочный
            Объект с таким UUID должен уже присутствовать в таблице объектов.
        :return: True - объект успешно зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def delLinkObject(self, link_obj):
        """
        Удаление зарегистрированного существующего объекта из списка ссылочных.

        :param link_obj: Объект - наследник icNodePersistent
            ВНИМАНИЕ! У ссылочного объект может удалятся только ссылка на него.
            Сам объект не удаляется.
        :return: True - ссылка на объект успешно удалена.
            False - какая-либо ошибка удаления.
        """
        pass

    def delLinkObjectUUID(self, link_obj_uuid):
        """
        Удаление зарегистрированного существующего объекта из списка
        ссылок по его UUID.

        :param link_obj_uuid: UUID удаляемого объекта-ссылки.
            ВНИМАНИЕ! У ссылочного объект может удалятся только ссылка на него.
            Сам объект не удаляется.
        :return: True - ссылка на объект успешно удалена.
            False - какая-либо ошибка удаления.
        """
        pass

    def getLinkObjectUUID(self, link_obj_uuid):
        """
        Получить ссфлочный объект текущего по его UUID.
        При получении объекта производиться проверка на
        существование зарегистрированного объекта-ссылки.

        :param link_obj_uuid: UUID запрашиваемого объекта-ссылки.
        :return: Объект наследник icNodePersistent с заполненными данными объекта-ссылки
            или None, если запрашиваемый объект не является ссылкой текущего.
        """
        pass


