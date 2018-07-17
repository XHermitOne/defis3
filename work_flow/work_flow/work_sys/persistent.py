#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Абстрактные классы хранимых объектов.
По сути это генератор таблиц хранения объектов.
"""

# Imports
from ic.utils import ic_mode

from ic.utils import lock
from ic.utils import ic_str
from ic.utils import util
from ic.engine import ic_user
from ic.utils import ic_uuid
from ic import io_prnt
from ic.dlg import ic_dlg

from ic.db import icsqlalchemy

from ic.storage import storesrc
from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp
from ic.components.user import ic_link_wrp

from STD.queries import filter_builder_env
from STD.queries import filter_convert
from STD.queries import filter_generate


# Version
__version__ = (0, 0, 5, 4)


class icObjPersistentPrototype:
    """
    Прототип компонентов, хранимых в БД.
        Реализует простейшие функции генерации имен таблиц и т.п.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        self.uuid = None
        self.name = ''
        self.description = ''
        
        # Инициализация родительского класса
        self._parent = Parent_

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
        @return: True/False.
        """
        return ic_uuid.valid_uuid(UUID)

    def setUUID(self, UUID):
        """
        Уникальный идентификатор можно задать явным образом.
        """
        if self._validUUID(UUID):
            self.uuid = UUID
        else:
            io_prnt.outWarning(u'Не корректное устанавливаемое значение UUID <%s>. UUID остался прежним' % UUID)
        return self.uuid

    def genUUID(self):
        """
        Генерировать уникальный идентификатор.
        """
        self.uuid = ic_uuid.get_uuid()
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
    
    def _createUuidFieldSpc(self, FieldName_='uuid'):
        """
        Создать спецификацию поля идентифицирующего документ.
        @param FieldName_: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = FieldName_
        field_spc['name'] = field_name
        field_spc['description'] = u'Идентификатор UUID документа'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'T'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc
    
    def _createCodFieldSpc(self, FieldName_='cod'):
        """
        Создать спецификацию поля идентифицирующего объект по коду.
        @param FieldName_: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = FieldName_
        field_spc['name'] = field_name
        field_spc['description'] = u'Код'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'T'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc

    def _createDateFieldSpc(self, FieldName_='x_date', Description_=''):
        """
        Создать спецификацию поля даты/времени.
        @param FieldName_: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = FieldName_
        field_spc['name'] = field_name
        field_spc['description'] = ic_str.str2unicode(Description_)
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'D'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None
        
        return field_spc
    
    def _createIntFieldSpc(self, FieldName_='x_int', Description_=''):
        """
        Создать спецификацию целочисленного поля.
        @param FieldName_: Имя идентифицирующего поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = FieldName_
        field_spc['name'] = field_name
        field_spc['description'] = ic_str.str2unicode(Description_)
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
        lock_dir = ic_user.icGet('LOCK_DIR')
        self._lockSystem = lock.icLockSystem(lock_dir)

    def lock(self, UUID=None):
        """
        Функции поддержки блокировок.
        Заблокировать текущий. Блокировка ведется по UUID.
        @param UUID: UUID блокируемого объекта.
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
        @param UUID: UUID блокируемого объекта.
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
        @param UUID: UUID блокируемого объекта.
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
        @param UUID: UUID блокируемого объекта.
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
        @param UUID: UUID блокируемого объекта.
        """
        return self.ownerLock(UUID) == lock.ComputerName()

    def getFieldName(self):
        """
        Имя поля хранения значения атрибута.
        У объекта нет поля.
        Это метод-заглушка.
        """
        return None


class icObjPersistent(icObjPersistentPrototype):
    """
    Базовый класс компонентов хранимых в БД.
        Реализует внутри себя механизм генерации спецификаций таблиц хранения.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icObjPersistentPrototype.__init__(self, Parent_)

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
        @param cur_filter: Текущий устанавливаемый фильтр.
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

    def save(self, UUID_=None, Data_=None):
        """
        Сохранить внутренние данные в хранилище.
        @param UUID_: Идентификатор. 
        Если None, то сохранить текущий.
        @param Data_: Сохраняемые данные в виде каскадного словаря:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        Если данные не указаны, то берутся данные из дерева объектов.
        @return: Возвращает результат выполнения операции True/False.
        """
        session = None
        try:
            tab = self.getTable()
            # Начать транзакцию
            session = tab.db.getSession()
            session.begin()
            
            if UUID_ is None:
                UUID_ = self.getUUID()
            if Data_ is None:
                Data_ = self._getCascadeDataObj()
            result = self._saveCascadeData(tab, UUID_, Data_)
            # Завершить транзакцию
            session.commit()
            return result
        except:
            if session:
                # Откатить транзакцию
                session.rollback()
                # if session.is_active:
                #    session.clear()
            io_prnt.outErr(u'Ошибка сохранения данных мета-объекта [%s]' % self.name)
            return None
            
    def _saveCascadeData(self, Tab_, UUID_, Data_):
        """
        Сохранить каскадные данные в хранилище.
        @param Tab_: Таблица.
        @param UUID_: Уникальный идентификатор.
        @param Data_: Словарь каскадных данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        @return: Возвращает True/False.
        """
        try:
            tab = self._tabObj(Tab_)
            if tab:
                # Выбрать только реквизиты
                rec = dict([(str(fld_name), fld_value) for fld_name, fld_value in Data_.items() if not isinstance(fld_value, list)])
                save_rec = tab.get_where(tab.c.uuid == UUID_).fetchone()
                tab.update_where(tab.c.uuid == UUID_, **rec)

                result = True
                children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__, icObjPersistent)]
                # Обработка дочерних объектов
                for child_obj in children_obj:
                    child_tab_name = child_obj.getTableName()
                    child_name = child_obj.getName()
                    if child_tab_name in Data_:
                        # В данных указана дочерняя таблица по имени таблицы
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              Data_[child_tab_name], save_rec)
                    elif child_name in Data_:
                        # В данных указана дочерняя таблица по имени табличного реквизита
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              Data_[child_name], save_rec)
                    else:
                        io_prnt.outWarning(u'Не найдены данные для дочерней таблицы/реквизита <%s>/<%s>' % (child_tab_name, child_name))
                return result
        except:
            io_prnt.outErr(u'Ошибка сохранения каскада данных мета-объекта [%s]' % self.name)
        return False

    def _updateChildCascadeData(self, Tab_, Data_, ParentRecord_):
        """
        Сохранить каскадные данные в хранилище у дочерних объектов.
        @param Tab_: Таблица.
        @param ParentRecord_: Родительская запись.
        @param Data_: Список словарей каскадных данных:
        [{
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        },...]
        @return: Возвращает True/False.
        """
        tab = self._tabObj(Tab_)
        if tab:
            recs = tab.get_where(tab.c.parent == ParentRecord_['uuid']).fetchall()
            data_rec_count = len(Data_)
            for i, rec in enumerate(recs):
                if i < data_rec_count:
                    # Обновление записи
                    data_rec = dict([(str(key), value) for key, value in Data_[i].items()])
                    tab.update_where(tab.c.uuid == rec['uuid'], **data_rec)
                else:
                    # Удаление записи
                    tab.del_where(tab.c.uuid == rec['uuid'])
            if data_rec_count > len(recs):
                for i in range(len(recs), data_rec_count):
                    # Добавление записи
                    new_rec = dict([(str(key), value) for key, value in Data_[i].items()])
                    new_rec['parent'] = ParentRecord_['uuid']
                    new_rec['uuid'] = self.genUUID()
                    link_names = [fld['name'].lower() for fld in tab.res['child'] if fld['type'] == 'Link']
                    for lnk_name in link_names:
                        new_rec[lnk_name] = ParentRecord_['id']
                    tab.add(**new_rec)
                     
            result = True
            children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__, icObjPersistent)]
            # Обработка дочерних объектов
            for child_obj in children_obj:
                child_tab_name = child_obj.getTableName()
                for rec in Data_:
                    if child_tab_name in rec:
                        child_uuid = rec['uuid']
                        result = result and child_obj._updateChildCascadeData(child_obj.getTable(),
                                                                              rec[child_tab_name], rec)
            return result
        return False
        
    def _saveCascadeData_old_2010_05_19(self, Tab_, UUID_, Data_):
        """
        Сохранить каскадные данные в хранилище.
        @param Tab_: Таблица.
        @param UUID_: Уникальный идентификатор.
        @param Data_: Словарь каскадных данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        @return: Возвращает True/False.
        """
        try:
            # Проще сначала все удалить а затем добавить,
            # чем проверять что нужно добавить а что удалить
            self._delCascadeData(Tab_, UUID_)
            # Чтобы корневой элемент создавался с темже uuidом
            Data_['uuid'] = UUID_
            result = self._addCascadeData(Tab_, Data_)
            return result
        except:
            io_prnt.outErr(u'Ошибка сохранения каскада данных мета-объекта [%s]' % self.name)
        return False
        
    def _load_data(self, UUID_=None):
        """
        Загрузить внутренние данные из хранилища.
        @param UUID_: Идентификатор.
        @return: Возвращает словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        .
        """
        try:
            if UUID_ is None:
                UUID_ = self.getUUID()
            return self._getCascadeDataTab(self.getTable(), UUID_, True)
        except:
            io_prnt.outErr(u'Ошибка загрузки данных мета-объекта [%s]' % self.name)
            return None
        
    def load_data(self, UUID_=None):
        """
        Загрузить внутренние данные из хранилища.
        @param UUID_: Идентификатор.
        @return: Возвращает словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        .
        """
        return self._load_data(UUID_=UUID_)

    def load(self, UUID_=None):
        """
        Загрузить внутренние данные из хранилища.
        @param UUID_: Идентификатор.
        @return: True/False.
        """
        try:
            cascade_data = self._load_data(UUID_)
            return self._setCascadeData(cascade_data)
        except:
            io_prnt.outErr(u'Ошибка загрузки данных мета-объекта [%s]' % self.name)
            return None
    
    def _getCascadeDataTab(self, Tab_, UUID_, OneBreak_=False):
        """
        Получить каскад данных из хранилища.
        @param Tab_: Таблица.
        @param UUID_: Иникальный идентификатор.
        @param OneBreak_: В данных дочерних объектов только одна запись?
        @return: Словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        """
        try:
            tab = self._tabObj(Tab_)
            if tab:
                rec = tab.get_where(tab.c.uuid == UUID_).fetchone()
                data = dict([(fld_name, rec[fld_name]) for fld_name in tab.getFieldNames()]) if rec else dict()
                
                # Обработать дочерние объекты
                children_obj = [child for child in self.getChildrenRequisites() if issubclass(child.__class__,
                                                                                              icObjPersistent)]
                for child_obj in children_obj:
                    tab_name = child_obj.getTableName()
                    data[tab_name] = child_obj._getChildCascadeDataTab(child_obj.getTable(), UUID_)
                
                return data
        except:
            io_prnt.outErr(u'Ошибка определения каскада данных объекта [%s] из хранилища' % self.name)
        return None

    def _getChildCascadeDataTab(self, Tab_, ParentUUID_):
        """
        Получить каскад данных из хранилища.
        @param Tab_: Таблица.
        @param ParentUUID_: Уникальный идентификатор родительской записи.
        @return: Словарь каскада данных:
        {
        'имя поля реквизита':значение,
        ...
        'имя дочернего объекта':[список словарей значений],
        ...
        }
        """
        tab = self._tabObj(Tab_)
        if tab:
            recs = tab.get_where(tab.c.parent == ParentUUID_).fetchall()
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
        
    def _setCascadeData(self, Data_):
        """
        Каскадная установка значений реквизитов.
        @param Data_: Словарь данных:
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
            requisites_data = dict([(fld_name, fld_value) for fld_name, fld_value in Data_.items()
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
                if child_obj.name in Data_ and Data_[child_obj.name]:
                    # ВНИМАНИЕ!!!
                    # Заполнение реквизитов дочерних объектов производится только по первой строке
                    result = result and child_obj._setCascadeData(Data_[child_obj.name][0])
            return result
        except:
            io_prnt.outErr(u'Ошибка каскадной установки значений реквизитов мета-объекта [%s]' % self.name)
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
        @param bInsertChildData_: Включать в каскад значения реквизитов
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
                records = child._getData(Filter_={'parent': self.getUUID()})
                if bInsertChildData_:
                    # Взять из объектов
                    records = [child._getCascadeDataObj(bInsertChildData_)]
                else:
                    # Взять из таблиц
                    records = child._getData(Filter_={'parent': self.getUUID()})
                    
                if ic_mode.isDebugMode():
                    io_prnt.outLog(u'CHILD: <%s> RECORDS: %s' % (child.name, records))
                    
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
        @param bInsertChildData_: Включать в каскад значения реквизитов
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
                    
                if ic_mode.isDebugMode():
                    io_prnt.outLog(u'CHILD: <%s> RECORDS: %s' % (child.name, records))
                    
                data[child.name] = records
                
        return data
    
    def getValue(self):
        """
        Каскад данных объекта.
        """
        try:
            return self._getCascadeDataObj()
        except:
            io_prnt.outErr(u'Ошибка определения данных мета-объекта [%s]' % self.name)
        return None

    def setValue(self, Value_):
        """
        Установить значения всех реквизитов.
        @param Value_: Словарь значений реквизитов.
        """
        try:
            for child in self.getChildrenRequisites():
                child.setValue(Value_[child.getFieldName()])
            return True
        except:
            io_prnt.outErr(u'Ошибка установки данных мета-объекта [%s]' % self.name)
            return None

    def _getData(self, Tab_=None, Filter_=None):
        """
        Отфильтрованные данные.
        @param Tab_: Объект таблицы.
        @param Filter_: Дополнительный фильтр.
        @return: Возвращает список отфильтрованных данных.
        """
        if Tab_ is None:
            Tab_ = self.getTable()
        try:
            tab = self._tabObj(Tab_)
            if tab:
                return tab.queryAll(Filter_)
            else:
                if ic_mode.isDebugMode():
                    io_prnt.outErr(u'Не определена таблица мета-объекта [%s]' % self.name)
        except:
            io_prnt.outErr(u'Ошибка получения отфильтрованных данных объекта [%s]' % self.name)
        return None

    def add(self, UUID_=None, Data_=None, table=None):
        """
        Добавить в хранилище текущий объект.
        @param UUID_: Идентификатор.
        Если None, то генерируется новый uuid.
        @param table: Главная таблица объекта. Если не указана, то генерируется.
        @return: Возвращает результат выполнения операции True/False.
        """
        if UUID_ is None:
            # Если uuid не указан явно, то сгенерировать новый
            UUID_ = self.genUUID()
        # Если сразу указаны данные для заполненения, то записать их
        data_dict = self.getChildrenDefault()
        if Data_ is None:
            # Получить данные объекта в каскадном представлении
            data_dict_obj = self._getCascadeDataObj(True)
            data_dict.update(data_dict_obj)
        elif isinstance(Data_, dict):
            data_dict.update(Data_)
        else:
            io_prnt.outWarning(u'Не корректный тип данных <%s> объекта <%s>' % (Data_.__class__.__name__,
                                                                                self.getName()))
            return False

        session = None
        try:
            tab = table if table else self.getTable()
            if tab:
                # Начать транзакцию
                session = tab.db.getSession()
                session.begin()

                if ic_mode.isDebugMode():
                    io_prnt.outLog(u'Meta-object [%s] Add data: %s' % (self.name, data_dict))

                result = self._addCascadeData(tab, data_dict)
                
                # Закончить транзакцию
                session.commit()
                
                return result
        except:
            if session:
                # Откатить транзакцию
                session.rollback()
                # session.clear()
            io_prnt.outErr(u'Ошибка добавления в хранилище объекта [%s]' % self.name)
        return False

    def findChildByName(self, child_name):
        """
        Поиск дочернего реквизита по имени.
        @param child_name: Имя дочернего реквизита
        @return: Объект реквизита или None если реквизит не найден.
        """
        find_children = [child for child in self.getChildrenRequisites()
                         if issubclass(child.__class__, icObjPersistent) and child.getName() == child_name]
        if find_children:
            return find_children[0]
        return None

    getRequisite = findChildByName

    def _tabObj(self, Tab_):
        """
        Таблица объекта.
        @param Tab_: Объект/таблица, в который будет сохраняться запись.
        """
        # Таблица данных
        if isinstance(Tab_, str) or isinstance(Tab_, unicode):
            # Таблица данных передается в виде имени
            if Tab_ == self.getTableName():
                # Таблица задается именем таблицы
                tab = self.getTable()
            elif self.findChildByName(Tab_):
                # Таблица задается именем табличного реквизита
                child = self.findChildByName(Tab_)
                tab = icsqlalchemy.icSQLAlchemyTabClass(child.getTableName())
            else:
                # Просто определить таблицу по имени
                tab = icsqlalchemy.icSQLAlchemyTabClass(Tab_)
        elif isinstance(Tab_, tuple):
            # Таблица данных передается в виде паспорта
            tab = self.getKernel().Create(Tab_)
        else:
            # Таблица передается как есть
            tab = Tab_
        return tab
        
    def _addCascadeData(self, Tab_, Dict_, ParentRecord_=None):
        """
        Добавление каскадного словаря значений в объект хранилища.
        @param Tab_: Объект/таблица, в который будет сохраняться запись.
        @param Dict_: Словарь значений.
            Словарь представлен в виде 
                {
                'имя поля реквизита':значение,
                ...
                'имя дочернего объекта':[список словарей значений],
                ...
                }
        @param PrentRecord_: Объект родительской записи для организации каскада.
        @return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            tab = self._tabObj(Tab_)
            # Добавление записи
            rec = dict([(str(key), value)for key, value in Dict_.items() if not isinstance(value, list)])
            
            # Если при добавлении не указан UUID, то сгенерировать его
            if ('uuid' not in rec) or (not rec['uuid']):
                rec['uuid'] = self.genUUID()
            
            # Если у объекта есть родительский объект, то указать его uuid
            if self._parent:
                rec['parent'] = self._parent.getUUID()
                
            # Если есть родительская таблица, то проинициализировать
            # ссылки на ее в текущей записи
            if ParentRecord_:
                link_names = [fld['name'].lower() for fld in tab.res['child'] if fld['type'] == 'Link']
                for lnk_name in link_names:
                    inserted_rec = ParentRecord_.last_inserted_params()
                    # ВНИМАНИЕ! В sqlalchemy идентификатор последней добавленной записи
                    #                                    v
                    rec[lnk_name] = ParentRecord_.inserted_primary_key[0] if ParentRecord_.inserted_primary_key else 0
                    rec['parent'] = inserted_rec.get('uuid', None)
                
            # Если вдруг ключи юникодовые то изменить их на строковые
            rec_obj = tab.add(**rec)
            # Обработка дочерних таблиц
            children_obj = dict([(name, data) for name, data in Dict_.items() if isinstance(data, list)])
            for tab_name in children_obj.keys():
                # Обработка дочерних таблиц
                for rec in children_obj[tab_name]:
                    self._addCascadeData(tab_name, rec, rec_obj)
            return True
        except:
            io_prnt.outErr(u'Ошибка добавления данных в каскад таблицы <%s>.' % Tab_)
            return None

    def delete(self, UUID_=None):
        """
        Удалить из хранилища текущий объект.
        @param UUID_: Идентификатор.
        Если None, то берется uuid объекта.
        @return: Возвращает результат выполнения операции True/False.
        """
        if UUID_ is None:
            # Если uuid не указан явно, то взять текущий объекта
            UUID_ = self.getUUID()

        transaction = None
        try:
            tab = self.getTable()
            if tab:
                # Начать транзакцию
                transaction = tab.db.getSession()
                transaction.begin()

                # Получить данные объекта в каскадном представлении
                if ic_mode.isDebugMode():
                    io_prnt.outLog(u'Meta-object [%s] Delete data: <%s>' % (self.name, UUID_))
                recs = tab.get_where(tab.c.uuid == UUID_)

                # Получить идентификатор записи
                rec_id = 0
                if recs:
                    recs_first = recs.first()
                    rec_id = recs_first.id if recs_first else 0

                if rec_id:
                    result = self._delCascadeData(tab, rec_id, transaction)
                else:
                    io_prnt.outWarning(u'Не найдена запись объекта с UUID <%s>' % UUID_)
                    result = False
                
                # Завершить транзакцию
                transaction.commit()
                
                return result
        except:
            if transaction:
                # Откатить транзакцию
                transaction.rollback()
                # session.clear()
            io_prnt.outErr(u'Ошибка удаления из хранилища объекта [%s]' % self.name)
        return False

    def clear(self, ask=False):
        """
        Удалить из хранилища все объекты.
        @param ask: Спросить об удалении всех объектов?
        @return: Возвращает результат выполнения операции True/False.
        """
        is_clear = ic_dlg.icAskBox(u'ВНИМАНИЕ!', u'Удалить все объекты <%s>?' % self.name) if ask else True
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
                if ic_mode.isDebugMode():
                    io_prnt.outLog(u'Meta-object [%s] Clear all data %s' % (self.name, obj_ids))

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
            io_prnt.outErr(u'Ошибка очистки объектов [%s] из хранилища' % self.name)
        return False

    def _getUuidsByParent(self, Tab_, ParentUUID_):
        """
        Получение уникальных идентификаторов по идентификатору родителя.
        """
        tab = self._tabObj(Tab_)
        return [rec.uuid for rec in tab.select(tab.c.parent == ParentUUID_)]

    def _delCascadeData(self, Tab_, rec_id, transaction=None):
        """
        Удалить каскад данных из хранилища по уникальонму идентификатору.
        @param Tab_: Объект таблицы.
        @param rec_id: Идентификатор удаляемой записи.
        @param transaction: Объект транзакции.
        @return: True/False.
        """
        result = True
        # Таблица данных
        tab = self._tabObj(Tab_)
        if not tab:
            # Таблица не определена по какойто причине
            io_prnt.outWarning(u'Удаление данных. Не определена таблица <%s>' % Tab_)
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
                    io_prnt.outLog(u'Не найдено дочерних записей в таблице <%s>' % child_tab.getDBTableName())

            # Удалить запись из родительской таблицы в конце
            tab.del_where_transact(tab.c.id == rec_id,
                                   transaction=transaction)
            return result
        except:
            io_prnt.outErr(u'Ошибка каскадного удаления данных из таблицы <%s>.' % Tab_)
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
        @return: Словарь {'имя реквизита': значение реквизита по умолчанию, ...}
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
    def _createTableResource(self, ParentTableName_=None):
        """
        Создание по описанию объекта ресурса таблицы, в 
            которой хранятся данные объекта.
        @param ParentTableName_: Имя родительской таблицы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()
    
        # Проверка на добавление нового ресурса
        table_name = self.getTableName()
        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if table_name and not prj_res_ctrl.isRes(table_name, 'tab'):
            table_res = self._createTabRes(table_name)
            # Создать связь с родительской таблицей
            if ParentTableName_:
                link_spc = self._createLinkSpc(ParentTableName_)
                table_res['child'].append(link_spc)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(table_name, 'tab', table_res)
            
    def _createLinkSpc(self, TableName_):
        """
        Создать спецификацию связи c таблицей.
        """
        # Инициализировать спецификацию связи
        link_spc = util.icSpcDefStruct(util.DeepCopy(ic_link_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        link_spc['name'] = 'id_'+TableName_.lower()
        link_spc['description'] = ic_str.str2unicode('Связь с таблицей '+TableName_)
        link_spc['table'] = (('Table', TableName_, None, None, None),)
        link_spc['del_lnk'] = True
        return link_spc
        
    def _createTabRes(self, TableName_=None):
        """
        Создать ресурс таблицы хранения спецификации/объекта.
        """
        if TableName_ is None:
            TableName_ = self.getTableName()

        tab_res = self._createTabSpc(TableName_)
        # Перебрать дочерние компоненты
        children_requisites = self.getChildrenRequisites()
        if children_requisites:
            for child_requisite in children_requisites:
                if issubclass(child_requisite.__class__, icAttrPersistent):
                    # Это реквизит
                    fields_spc = child_requisite._createFieldsSpc()
                    if fields_spc is None:
                        io_prnt.outWarning(u'Не определена спецификация поля при создании таблицы хранимого объекта')
                    tab_res['child'] += fields_spc
                elif issubclass(child_requisite.__class__, icObjPersistent):
                    # Это спецификация табличной части
                    child_requisite._createTableResource(TableName_)
                    # Прописать имя дочерней ьаблицы в списке подчиненных таблиц
                    tab_res['children'].append(child_requisite.getTableName())
                else:
                    io_prnt.outWarning(u'Неизвестный тип дочернего компонента <%s> объекта' % child_requisite)
                    
        return tab_res
       
    def _createTabSpc(self, TableName_=None):
        """
        Создать спецификацию таблицы.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if TableName_ is None:
            TableName_ = self.getTableName()
        tab_spc['name'] = TableName_
        tab_spc['description'] = ic_str.str2unicode(self.description)
        tab_spc['table'] = TableName_.lower()
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

    def _createFieldSpc(self, FieldName_, FieldType_='T', FieldLen_=None, FieldDefault_=None):
        """
        Создать спецификацию поля.
        Функция необходима для вспомогательных и 
        служебных полей.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = FieldName_
        field_spc['field'] = FieldName_.lower()
        field_spc['type_val'] = FieldType_
        field_spc['len'] = FieldLen_
        field_spc['attr'] = 0
        field_spc['default'] = FieldDefault_
        
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
    
    def getFilterSQL(self, Filter_=None, Fields_=None, limit=None):
        """
        Фильтр в SQL представлении.
        @param Filter_: Фильтр.
        @param Fields_: Поля выбора. Если None, то будут выбираться только 
        идентифицирующие объект поля.
        @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        if Fields_ is None:
            Fields_ = tuple([requisite.getFieldName() for requisite in self.getChildrenRequisites() if requisite.isIDAttr()])
        if not Fields_:
            Fields_ = ('*',)
        else:
            # Необхдимо, что бы в результате запроса всегда
            # присутствовал UUID  объекта
            fld_lst = list(Fields_)
            fld_lst.append('uuid')
            Fields_ = tuple(fld_lst)
            
        sql = filter_convert.convertFilter2PgSQL(Filter_, self.getTableName(), Fields_,
                                                 limit=limit)
        return sql

    def getFilterSQLAlchemy(self, Filter_=None, Fields_=None, limit=None):
        """
        Фильтр в SQLAlchemy представлении.
        @param Filter_: Фильтр.
        @param Fields_: Поля выбора. Если None, то будут выбираться только 
        идентифицирующие объект поля.
        @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        if Fields_ is None:
            field_list = [requisite.getFieldName() for requisite in self.getChildrenRequisites()
                          if requisite.isIDAttr()]
            # ВНИМАНИЕ! Обязательно должен присутствовать UUID
            # иначе идентифицировать объект никак не получится
            field_list += ['uuid'] if 'uuid' not in field_list else list()
            Fields_ = tuple(field_list)
        elif Fields_ == '*':
            Fields_ = ('*',)
        else:
            # Необхдимо, что бы в результате запроса всегда
            # присутствовал UUID  объекта
            fld_lst = list(Fields_)
            fld_lst.append('uuid')
            Fields_ = tuple(fld_lst)

        query = filter_convert.convertFilter2SQLAlchemy(Filter_, self.getTable(), Fields_,
                                                        limit=limit)
        return query

    def _resultFilter2Dataset(self, FilterResult_):
        """
        Подготовка результата фильтрации в виде датасета для 
        грида объектов в виде списка словарей.
        """
        # Замена кодов идентифицирующих реквизитов на значение <КОД Наименование>
        result = []
        id_nsi_requisites = [requisite for requisite in self.getChildrenRequisites() if requisite.isIDAttr() and requisite.type == 'NSIRequisite']
        for record in FilterResult_:
            rec = dict(record)
            for nsi_requisite in id_nsi_requisites:
                fld_name = nsi_requisite.getFieldName()
                # Если код определен, тогда найти наименование в справочнике
                if rec[fld_name]:
                    # Но сохранить и код c новым именем
                    rec['_'+fld_name] = rec[fld_name]
                    rec[fld_name] = nsi_requisite.getSprav().Find(rec[fld_name])
            result.append(rec)
                
        return result

    def filterRequisiteData(self, FilterRequisiteData_=None):
        """
        Отфильтровать объекты согласно данным фильтра.
        @param FilterRequisiteData_: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        @return: Возвращает список-dataset объектов, соответствующих заданному фильтру.
        """
        if FilterRequisiteData_ is None:
            # Если None, то берется текущий фильтр бизнес объектов.
            FilterRequisiteData_ = self.getFilter()

        if FilterRequisiteData_ is None:
            # Если фильтр не определен, то показываем все объекты
            FilterRequisiteData_ = {}
        # Сначала убрать значения реквизитов с не указанными значениями
        filter_requisite_data = dict([(name, value) for name, value in FilterRequisiteData_.items() if value])
        return filter_requisite_data

    def getDataDict(self, filter_requisite_data=None, limit=None):
        """
        Набор записей.Каждая запись в виде словаря.
        Этот метод также имеет название getDataset и getRecordset.
        @param filter_requisite_data: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        if not filter_requisite_data:
            filter_requisite_data = None

        io_prnt.outLog(u'BUSINES OBJECT get data')
        data_filter = self.filterRequisiteData(filter_requisite_data)
        io_prnt.outLog(u'\tFilter: <%s>' % data_filter)
        query = self.getFilterSQLAlchemy(data_filter,
                                         limit=limit if limit else self._limit)
        # io_prnt.outLog(u'\tQuery: <%s>' % query)
        result = self.getTable().getConnection().execute(query)
        io_prnt.outLog(u'\tResult: [%s]' % result.rowcount)
        return self._resultFilter2Dataset(result.fetchall())

    # Другие наименования метода
    getDataset = getDataDict
    getRecordset = getDataDict

    def countDataDict(self, filter_requisite_data=None):
        """
        Количество записей набора записей.
        Этот метод также имеет название countDataset и countRecordset.
        @param filter_requisite_data: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        @return: Возвращает количество записей набора записей, удовлетворяющих фильтру.
        """
        if not filter_requisite_data:
            filter_requisite_data = None

        io_prnt.outLog(u'BUSINES OBJECT get count data')
        data_filter = self.filterRequisiteData(filter_requisite_data)
        io_prnt.outLog(u'\tFilter: <%s>' % data_filter)
        query = self.getFilterSQLAlchemy(data_filter)
        # ВНИМАНИЕ! Подзапрос должен иметь алиас.
        # Иначе возникает ошибка SQL <ERROR:  subquery in FROM must have an alias>
        #               v
        query = query.alias().count()
        io_prnt.outLog(u'\tQuery: <%s>' % query)
        # Небходимо просто получить число. Поэтому берем значение явно
        #                                                          v
        result = self.getTable().getConnection().execute(query).fetchone()
        int_result = result[0]
        io_prnt.outLog(u'\tResult: [%s]' % int_result)
        return int_result

    # Другие наименования метода
    countDataset = countDataDict
    countRecordset = countDataDict

    def findRequisiteData(self, **find_requisite_data):
        """
        Найти UUIDы объектов согласно данным фильтра.
        @param find_requisite_data: Словарь значений реквизитов фильтров.
            Если не указан, то берется текущий фильтр бизнес объектов.
            Сравнение происходит по <И>.
        @return: Возвращает uuidы объектов, соответствующих заданному фильтру.
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


class icAttrPersistent:
    """
    Базовый класс атрибута компонента хранимого в БД.
        Реализует внутри себя механизм генерации спецификации хранения.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
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
            io_prnt.outErr(u'Не латинские буквы в имени атрибута <%s> запрещены' % self.name)
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
        field_spc['description'] = ic_str.str2unicode(self.description)
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
        @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        data_filter = self.filterRequisiteData()
        query = self.getFilterSQLAlchemy(data_filter, Fields_='*', limit=limit)
        result = query.execute()
        io_prnt.outLog(u'ACCUMULATE REGISTRY get data\n\tResult: [%s]' % result.rowcount)
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
        @param obj_type_code:  Код типа дочернего объекта.
        @param default: Словарь реквизитов, заполняемых по умолчанию нового дочернего объекта.
            Если не указывается, то этот словарь берется из справочника типов объектов.
        @return: True - дочерний объект успешно создан и зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def addChildObject(self, child_obj):
        """
        Регистрация существующего объекта как дочернего.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как дочернего.
        @param child_obj: Объект - наследник icNodePersistent
        @return: True - дочерний объект успешно зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def addChildObjectUUID(self, child_obj_uuid):
        """
        Регистрация существующего объекта как дочернего по его UUID.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как дочернего.
        @param child_obj_uuid: UUID объекта добавляемого, как дочерний.
            Объект с таким UUID должен уже присутствовать в таблице объектов.
        @return: True - дочерний объект успешно зарегистрирован как дочерний
            False - указанный тип объекта не может быть использован для текущего объекта
            как дочерний или по какой-либо другой ошибке.
        """
        pass

    def delChildObject(self, child_obj, auto_delete=False):
        """
        Удаление зарегистрированного существующего объекта из списка дочерних.
        @param child_obj: Объект - наследник icNodePersistent
        @param auto_delete: Проверить автоматическое удаление дочернего объекта, если
            он больше не связан с другим родительским объектом.
            Удаление дочерних объектов происходит каскадно.
        @return: True - дочерний объект успешно удален как дочерний.
            False - какая-либо ошибка удаления.
        """
        pass

    def delChildObjectUUID(self, child_obj_uuid, auto_delete=False):
        """
        Удаление зарегистрированного существующего объекта из списка дочерних по его UUID.
        @param child_obj_uuid: UUID удаляемого дочернего объекта.
        @param auto_delete: Проверить автоматическое удаление дочернего объекта, если
            он больше не связан с другим родительским объектом.
            Удаление дочерних объектов происходит каскадно.
        @return: True - дочерний объект успешно удален как дочерний.
            False - какая-либо ошибка удаления.
        """
        pass

    def getChildObjectUUID(self, child_obj_uuid):
        """
        Получить дочерний объект текущего по его UUID.
        При получении объекта производиться проверка на существование зарегистрированного дочернего объекта.
        @param child_obj_uuid: UUID запрашиваемого дочернего объекта.
        @return: Объект наследник icNodePersistent с заполненными данными дочернего объекта
            или None, если запрашиваемый объект не является дочерним текущего.
        """
        pass

    def newLinkObject(self, obj_type_code, default=None):
        """
        Создание нового объекта-ссылки по его типу.
        После создания объект автоматически прописывается в списке ссылок.
        При создании объекта производиться контроль на возможность использования
        типа объекта как ссылочного.
        @param obj_type_code:  Код типа объекта.
        @param default: Словарь реквизитов, заполняемых по умолчанию нового объекта.
            Если не указывается, то этот словарь берется из справочника типов объектов.
        @return: True - объект успешно создан и зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def addLinkObject(self, link_obj):
        """
        Регистрация существующего объекта как ссылочного.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как ссылочного.
        @param link_obj: Объект - наследник icNodePersistent
        @return: True - объект успешно зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def addLinkObjectUUID(self, link_obj_uuid):
        """
        Регистрация существующего объекта как ссылочного по его UUID.
        При добавлении объекта производиться контроль на возможность использования
        типа объекта как ссылочного.
        @param link_obj_uuid: UUID объекта добавляемого, как ссылочный
            Объект с таким UUID должен уже присутствовать в таблице объектов.
        @return: True - объект успешно зарегистрирован как ссылочный
            False - указанный тип объекта не может быть использован для текущего объекта
            как ссылочный или по какой-либо другой ошибке.
        """
        pass

    def delLinkObject(self, link_obj):
        """
        Удаление зарегистрированного существующего объекта из списка ссылочных.
        @param link_obj: Объект - наследник icNodePersistent
            ВНИМАНИЕ! У ссылочного объект может удалятся только ссылка на него.
            Сам объект не удаляется.
        @return: True - ссылка на объект успешно удалена.
            False - какая-либо ошибка удаления.
        """
        pass

    def delLinkObjectUUID(self, link_obj_uuid):
        """
        Удаление зарегистрированного существующего объекта из списка ссылок по его UUID.
        @param link_obj_uuid: UUID удаляемого объекта-ссылки.
            ВНИМАНИЕ! У ссылочного объект может удалятся только ссылка на него.
            Сам объект не удаляется.
        @return: True - ссылка на объект успешно удалена.
            False - какая-либо ошибка удаления.
        """
        pass

    def getLinkObjectUUID(self, link_obj_uuid):
        """
        Получить ссфлочный объект текущего по его UUID.
        При получении объекта производиться проверка на существование зарегистрированного объекта-ссылки.
        @param link_obj_uuid: UUID запрашиваемого объекта-ссылки.
        @return: Объект наследник icNodePersistent с заполненными данными объекта-ссылки
            или None, если запрашиваемый объект не является ссылкой текущего.
        """
        pass


