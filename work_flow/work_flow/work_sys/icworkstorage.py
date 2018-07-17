#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Хранилище/БД всех объектов, документов и операций.
"""

# --- Подключение библиотек ---
import ic
import sqlalchemy
import sqlalchemy.sql
from ic.db import icsqlalchemy
from . import persistent

# Версия
__version__ = (0, 0, 2, 1)

# --- Функции ---
_WORK_SQL_STORAGE = dict()


def getWorkSQLStorageByPsp(DBPsp_):
    """
    Получить объект SQL хранилища документов по имени.
    """
    global _WORK_SQL_STORAGE
    
    if DBPsp_ is None:
        assert None, 'getWorkSQLStorageByPsp Function: Data Base pasport not defined!'
        
    work_storage_name = DBPsp_[0][1]
    if work_storage_name not in _WORK_SQL_STORAGE:
        _WORK_SQL_STORAGE[work_storage_name] = icWorkSQLStorage(None, DBPsp_)
        ic.io_prnt.outLog(u'Регистрация БД <%s> в списке хранилищ' % work_storage_name)
    return _WORK_SQL_STORAGE[work_storage_name]


class icWorkStorageInterface:
    """
    Интерфейс абстрактного хранилища/БД документов.
    """

    def __init__(self, Parent_, DBPsp_):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        @param DBPsp_: Паспорт БД.
        """
        self._parent = Parent_
        self._db_psp = DBPsp_

    def getParent(self):
        """
        Объект, к которому прикреплено хранилище.
        """
        return self._parent
    
    def saveObject(self, Obj_):
        """
        Сохранить объект в хранилище.
        @param Obj_: Сохраняемый объект.
        """
        pass
        
    def loadObject(self, Obj_, ID_):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        @param Obj_: Объект.
        @param ID_: Идентификатор объекта.
        """
        pass


class icWorkSQLStorageContainer(object):
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
        
    def setTable(self, TabName_=None):
        """
        Установить таблицу, по ее имени.
        @param TabName_: Имя таблицы.
        @return: Возвращает объект таблицы или None, если таблицу получить нельзя.
        """
        if TabName_:
            if not self.hasName(TabName_):
                # Создать таблицу
                self._all[TabName_] = icsqlalchemy.icSQLAlchemyTabClass(TabName_)
            return self._all[TabName_]
        return None
        
    def getTable(self, TabName_):
        """
        Получить таблицу по имени. Если ее нет, то создает ее.
        """
        self.setTable(TabName_)
        return self._all[TabName_]
            

class icWorkSQLStorage(object, icWorkStorageInterface):
    """
    SQL хранилище/БД всяких бизнес объектов.
    """

    def __init__(self, Parent_, DBPsp_):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        @param DBPsp_: Паспорт БД.
        """
        icWorkStorageInterface.__init__(self, Parent_, DBPsp_)
        # Контейнер
        self._container = icWorkSQLStorageContainer()

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

    # --- Методы каскадной записи/чтения данных ---
    def setCascadeDict(self, Obj_, ID_, Dict_, IdentFields_=None):
        """
        Сохранение каскадного словаря значений в объект хранилища.
        @param Obj_: Объект/таблица, в который будет сохраняться запись.
        @param ID_: Идентификатор записи. 
            Если None, то запись будет добавлена.
        @param Dict_: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        @param IdentFields_: Список имен полей идентифицирующих запись,
            если не указан идентификатор записи.
        @return: Результат выполнения True/False или None в случае ошибки.
        """
        if ID_ is None:
            if IdentFields_ is None:
                return self.addCascadeDict(Obj_, Dict_)
            else:
                _id_ = self._identRecord(Obj_, Dict_, IdentFields_)
                if _id_ == -1:
                    return self.addCascadeDict(Obj_, Dict_)
                elif isinstance(_id_, int) and _id_ >= 0:
                    return self._setCascadeDict(Obj_, _id_, Dict_)
                elif isinstance(_id_, list):
                    ic.io_prnt.outLog(u'Ошибка идентификации записи. Много записей соответствуют запросу %s' % _id_)
                    return None
                else:
                    return None
        else:
            return self._setCascadeDict(Obj_, ID_, Dict_)

    def _identRecord(self, Obj_, Dict_, IdentFields_):
        """
        Идентифицировать запись в объекте.
        @param Obj_: Объект/таблица, в который будет сохраняться запись.
        @param Dict_: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        @param IdentFields_: Список имен полей идентифицирующих запись,
            если не указан идентификатор записи.
        @return: Идентификатор записи или -1 в случае если запись не найдена.
        """
        try:
            # Таблица данных
            tab = self._tabObj(Obj_)
            indent_rec = [getattr(tab.c, fld_name) == Dict_[fld_name] for fld_name in IdentFields_]
            find_rec = tab.get_where(icsqlalchemy.and_(*indent_rec))
            if find_rec:
                if find_rec.rowcount == 1:
                    return find_rec[0].id
                elif find_rec.rowcount > 1:
                    return [rec.id for rec in find_rec]
        except:
            ic.io_prnt.outErr(u'Ошибка идентификации записи в таблице %s.' % Obj_)
            return None
        return -1

    def _setCascadeDict(self, Obj_, ID_, Dict_):
        """
        Сохранение каскадного словаря значений в объект хранилища.
        @param Obj_: Объект/таблица, в который будет сохраняться запись.
        @param ID_: Идентификатор записи. 
            Если None, то запись будет добавлена.
        @param Dict_: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        @return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            if isinstance(Obj_, str):
                tab = icsqlalchemy.icSQLAlchemyTabClass(Obj_)
            else:
                tab = Obj_
            # Добавление записи
            rec = dict([item for item in Dict_.items() if not isinstance(item[1], list)])
            tab.update(ID_, **rec)
            # Обработка дочерних таблиц
            children_tabs = dict([item for item in Dict_.items() if isinstance(item[1], list)])
            for child_tab_name in children_tabs.keys():
                for child_rec in children_tabs[child_tab_name]:
                    # Если есть возможнось,
                    # то прописать UUID родительской записи
                    child_rec['parent'] = rec.get('uuid', u'')
                    self._setCascadeDict(child_tab_name, ID_, child_rec)
            return True
        except:
            ic.io_prnt.outErr(u'Ошибка обновления данных в каскад таблицы %s.' % Obj_)
            return None

    def _tabObj(self, Obj_):
        """
        Таблица объекта.
        @param Obj_: Объект/таблица, в который будет сохраняться запись.
        """
        # Таблица данных
        if isinstance(Obj_, str):
            # Таблица данных передается в виде имени
            tab = icsqlalchemy.icSQLAlchemyTabClass(Obj_)
        elif isinstance(Obj_, tuple):
            # Таблица данных передается в виде паспорта
            tab = self.getKernel().Create(Obj_)
        else:
            tab = Obj_
        return tab
        
    def addCascadeDict(self, Obj_, Dict_):
        """
        Добавление каскадного словаря значений в объект хранилища.
        @param Obj_: Объект/таблица, в который будет сохраняться запись.
        @param Dict_: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        @return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            tab = self._tabObj(Obj_)
            # Добавление записи
            rec = dict([(str(key),value)for key, value in Dict_.items() if not isinstance(value, list)])
            # Если вдруг ключи юникодовые то изменить их на строковые
            tab.add(**rec)
            # Обработка дочерних таблиц
            children_tabs = dict([item for item in Dict_.items() if isinstance(item[1], list)])
            for child_tab_name in children_tabs.keys():
                for rec in children_tabs[child_tab_name]:
                    self.addCascadeDict(child_tab_name, rec)
            return True
        except:
            ic.io_prnt.outErr(u'Ошибка добавления данных в каскад таблицы %s.' % Obj_)
            return None

    def saveObject(self, Obj_):
        """
        Сохранить объект в хранилище.
        Все каскадное сохранение объекта должно производится
        в рамках одной транзакции.
        ВНИМАНИЕ! При возникновении ошибки
        <CompileError: Unconsumed column names: tab1, tab2>
        Необходимо проинициализировать табличные реквизиты tab1 и tab2
        пустыми списками перед записью:
            doc.setRequisiteValue('tab1', list())
            doc.setRequisiteValue('tab2', list())
        @param Obj_: Сохраняемый объект.
        """
        doc_table = self.container.getTable(Obj_.getTableName())

        # --- Начать транзакцию ---
        result = False
        doc_table.db.connect()
        transaction = doc_table.db.session(autoflush=False,
                                           autocommit=False)

        try:
            # Расширить словарь реквизитов значениями по умолчачнию
            requisite_dict = doc_table.getDefaultRecDict()
            requisite_dict.update(Obj_.getRequisiteData())
            try:
                ic.io_prnt.outLog(u'WorkStorage SAVE RECORD %s' % requisite_dict.keys())
            except UnicodeDecodeError:
                ic.io_prnt.outWarning(u'UnicodeDecodeError. WorkStorage SAVE RECORD')

            save_rec = dict([(str(fld_name), value) for fld_name, value in requisite_dict.items() if not isinstance(value, list)])
            if not doc_table.count(doc_table.c.uuid == Obj_.getUUID()):
                # Добавить
                try:
                    ic.io_prnt.outLog(u'WorkStorage ADD RECORD %s' % save_rec.keys())
                except UnicodeDecodeError:
                    ic.io_prnt.outWarning(u'UnicodeDecodeError. WorkStorage ADD RECORD')

                doc_table.add_rec_transact(rec=save_rec,
                                           transaction=transaction)
                id = doc_table.getLastInsertedId()
            else:
                # Отредактировать уже существующий
                rec = doc_table.select(doc_table.c.uuid == Obj_.getUUID()).first()
                id = rec.id if rec else 0
                doc_table.update_rec_transact(id, rec=save_rec,
                                              transaction=transaction)

            # Сохранить дочерние объекты
            children = [child for child in Obj_.getChildrenRequisites() if issubclass(child.__class__,
                                                                                     persistent.icObjPersistent)]
            for child in children:
                self._saveObjectData(child,
                                     parent_table=doc_table,
                                     parent_id=id,
                                     transaction=transaction,
                                     parent_uuid=save_rec.get('uuid', ''))

            # --- Закончить транзакцию ---
            transaction.commit()

            result = True
        except:
            # Вернуть транзакцию
            transaction.rollback()
            ic.io_prnt.outErr(u'ОШИБКА сохранения реквизитов объекта <%s>' % Obj_.__class__.__name__)

        doc_table.db.disconnect()
        return result
            
    def _saveObjectData(self, CurObj_, parent_table=None,
                        parent_id=None, transaction=None,
                        parent_uuid=''):
        """
        Сохранить данные объекта в хранилище.
        @param CurObj_: Текущий объект спецификации документа.
        @param parent_table: Объект родительской таблицы.
        @param parent_id: Идентификатор родительской записи.
        @param transaction: Объект транзакции (если надо).
        @param parent_uuid: UUID родительской записи.
        """
        table = self.container.getTable(CurObj_.getTableName())

        parent_id_fieldname = table.getLinkIdFieldName(parent_table)
        # Удалить записей спецификации
        where = sqlalchemy.and_(getattr(table.c, parent_id_fieldname) == parent_id)
        table.del_where_transact(where, transaction=transaction)

        children = [child for child in CurObj_.getChildrenRequisites() if issubclass(child.__class__,
                                                                                     persistent.icObjPersistent)]
        # Добавить записи спецификации
        obj_data = CurObj_.getData()
        if obj_data:
            for rec in obj_data:
                save_rec = table.getDefaultRecDict()
                rec_data = dict([(name, value) for name, value in rec.items() if not isinstance(value, list)])
                save_rec.update(rec_data)
                if parent_id:
                    save_rec[parent_id_fieldname] = parent_id
                    if parent_uuid:
                        save_rec['parent'] = parent_uuid
                table.add_rec_transact(rec=save_rec,
                                       transaction=transaction)
                id = table.getLastInsertedId()

                # Сохранить дочерние объекты
                for child in children:
                    self._saveObjectData(child,
                                         parent_table=table,
                                         parent_id=id,
                                         transaction=transaction,
                                         parent_uuid=save_rec.get('uuid', ''))
        
        return True

    def isObject(self, Obj_, UUID_):
        """
        Проверка существования данных объекта в хранилище по идентификатору.
        @param Obj_: Объект.
        @param UUID_: Уникальный идентификатор объекта.
        @return: True/False.
        """
        try:
            # Проинициализировать все дочерние объекты
            Obj_.init_children_data()

            tab = self.container.getTable(Obj_.getTableName())
            try:
                count = tab.count(tab.c.uuid == UUID_)
            except:
                ic.io_prnt.outErr(u'ОШИБКА наличия объекта в хранилище')
                return False
            return True if count > 0 else False
        except:
            ic.io_prnt.outErr(u'ОШИБКА определения существования объекта <%s>' % UUID_)
            return False

    def loadObject(self, Obj_, UUID_):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        @param Obj_: Объект.
        @param UUID_: Уникальный идентификатор объекта.
        @return: True/False.
        """
        try:
            # Проинициализировать все дочерние объекты
            Obj_.init_children_data()
            
            tab = self.container.getTable(Obj_.getTableName())
            try:
                result = tab.select(tab.c.uuid == UUID_)
            except:
                ic.io_prnt.outErr(u'ОШИБКА чтения объекта их хранилища')
                return False

            if result.rowcount:
                # Запомнить идентификатор документа
                Obj_.uuid = UUID_
                # Получить все данные документа в виде словаря
                cascade_data = tab.getCascadeDict(result.first().id)
                # ic.io_prnt.outLog(u'GET Cascade Data %s' % cascade_data)
            else:
                ic.io_prnt.outLog(u'Данные объекта <%s> не найдены' % UUID_)
                return False
            # Установка внутренних данных в объекте
            # Только реквизиты
            obj_requisites = [requisite for requisite in Obj_.getAllRequisites() if issubclass(requisite.__class__,
                                                                                               persistent.icAttrPersistent)]
            
            # Перебор реквизитов
            for requisite in obj_requisites:
                value = cascade_data.get(requisite.getName(), None)
                requisite.setValue(value)
                
            # Только табличные реквизиты
            obj_tab = [obj_spc for obj_spc in Obj_.getAllRequisites() if issubclass(obj_spc.__class__,
                                                                                    persistent.icObjPersistent)]
            for obj_spc in obj_tab:
                tab_name = obj_spc.getTableName()
                if tab_name in cascade_data:
                    self._setObjectData(obj_spc, cascade_data[tab_name])
            return True
        except:
            ic.io_prnt.outErr(u'ОШИБКА загрузки реквизитов объекта %s' % Obj_.getUUID())
            return False

    def _setObjectData(self, CurObj_, Data_):
        """
        Установка данных объекта.
        @param CurObj_: Текущий объект.
        @param Data_: Данные объекта.
        """
        # Только реквизиты
        requisites = [requisite for requisite in CurObj_.getChildrenRequisites() if issubclass(requisite.__class__,
                                                                                               persistent.icAttrPersistent)]
        # Табличные реквизиты
        tab_requisites = [requisite for requisite in CurObj_.getChildrenRequisites() if issubclass(requisite.__class__,
                                                                                                   persistent.icObjPersistent)]
        for rec_data in Data_:
            row = dict()
            for requisite in requisites:
                value = rec_data.get(requisite.getName(), None)
                row[requisite.getName()] = value
            CurObj_.addRow(**row)

            for tab_requisite in tab_requisites:
                tab_name = tab_requisite.getTableName()
                if tab_name in rec_data:
                    self._setObjectData(tab_requisite, rec_data[tab_name])

    def _resultLen(self, Result_):
        """
        Количество записей результата запроса.
        @param Result_: Результат запроса.
        """
        if isinstance(Result_, list):
            return len(Result_)
        elif not Result_:
            return 0
        else:
            return Result_.rowcount
        return -1
    
    def getFieldNames(self, Obj_):
        """
        Список имен полей таблицы хранения объекта.
        @param Obj_: Объект.
        """
        obj_requisites = [requisite for requisite in Obj_.getAllRequisites() if issubclass(requisite.__class__,
                                                                                           persistent.icAttrPersistent)]
        fields = [obj_requisite.getFieldName() for obj_requisite in obj_requisites]
        ic.io_prnt.outLog(u'icworkstorage.getFieldNames::: %s' % fields)
        return fields
        
    def delAllData(self, Obj_, Filter_=None):
        """
        Удалить все данные объекта.
        @param Obj_: Объект.
        @param Filter_: Дополнительный фильтр. Словарь {'имя поля':значение}
        @return: Возвращает True/False или None  в случае ошибки.
        """
        try:
            obj_table = self.container.getTable(Obj_.getTableName())
            if Filter_:
                filter = [getattr(obj_table.c, fld_name) == fld_value for fld_name, fld_value in Filter_.items()]
                # Фильтрация производится по "И"
                return obj_table.del_where(icsqlalchemy.and_(*filter))
            else:
                return obj_table.dataclass.select().delete().execute()            
        except:
            ic.io_prnt.outErr(u'ОШИБКА удаления объекта %s их хранилища' % Obj_.name)
            return None
        
    def getAllData(self, Obj_, Filter_=None):
        """
        Получить все данные объекта.
        @param Obj_: Объект.
        @param Filter_: Дополнительный фильтр.
        @return: Возвращает список или None  в случае ошибки.
        """
        try:
            # Проинициализировать все дочерние объекты
            Obj_.init_children_data()
            
            obj_table = self.container.getTable(Obj_.getTableName())
            try:
                if Filter_:
                    result = obj_table.queryAll(Filter_)
                else:
                    result = obj_table.select()

                if not self._resultLen(result):
                    ic.io_prnt.outLog(u'Данные объекта %s не найдены' % Obj_.name)
                    # Только реквизиты
                    fields = self.getFieldNames(Obj_)
                    return {'fields': fields, 'data': []}
            except:
                ic.io_prnt.outErr(u'ОШИБКА чтения объекта %s их хранилища' % Obj_.name)
                return None

            # Только реквизиты
            fields = self.getFieldNames(Obj_)

            # Перебор записей
            data = []
            for rec in result:
                # Перебор полей реквизитов
                if type(rec) in (tuple, list):
                    rec_list = list(rec)
                else:
                    rec_list = list()
                    for field in fields:
                        rec_list.append(rec[field])
                    
                data.append(rec_list)
                
            return {'fields': fields, 'data': data}
        except:
            ic.io_prnt.outErr(u'ОШИБКА. Получения всех данных объекта %s' % Obj_.name)
            return None

    def getAllUUID(self, Obj_, order_sort=None):
        """
        Получить все уникальные идентификаторы объектов UUID.
        @param Obj_: Объект документа.
        @param order_sort: Порядок сортировки.
            Список имен полей, в котором надо сортировать.
        @return: Список уникальных идентификаторов UUID
        """
        try:
            doc_table = self.container.getTable(Obj_.getTableName())
            # ВНИМАНИЕ! Пример SQL select'а с выбором опрределенных колонок
            sql = sqlalchemy.sql.select(columns=[doc_table.c.uuid],
                                        from_obj=[doc_table.dataclass])
            if order_sort:
                if isinstance(order_sort, list) or isinstance(order_sort, tuple):
                    for field_name in order_sort:
                        sql = sql.order_by(getattr(doc_table.c, field_name))
                elif isinstance(order_sort, str) or isinstance(order_sort, unicode):
                    sql = sql.order_by(getattr(doc_table.c, order_sort))
                else:
                    ic.io_prnt.outWarning(u'Не корректный тип <%s> параметра порядка сортировки в методе getAllUUID' % type(order_sort))

            records = sql.execute()
            return [record['uuid'] for record in records]
        except:
            ic.io_prnt.outErr(u'Ошибка получения всех UUID')
        return list()

    def test(self):
        """
        Функция тестирования.
        """
        pass

        
if __name__ == '__main__':
    storage = icWorkSQLStorage(None, 'work_db_psgress')
    storage.test()
