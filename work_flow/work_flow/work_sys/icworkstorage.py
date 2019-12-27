#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Хранилище/БД всех объектов, документов и операций.
"""

# --- Подключение библиотек ---
import ic
import sqlalchemy
import sqlalchemy.sql
from ic.db import icsqlalchemy
from ic.log import log
from . import persistent

# Версия
__version__ = (0, 1, 1, 2)

# --- Функции ---
_WORK_SQL_STORAGE = dict()


def getWorkSQLStorageByPsp(db_psp):
    """
    Получить объект SQL хранилища документов по имени.
    """
    global _WORK_SQL_STORAGE
    
    if db_psp is None:
        assert None, 'getWorkSQLStorageByPsp Function: Data Base pasport not defined!'
        
    work_storage_name = db_psp[0][1]
    if work_storage_name not in _WORK_SQL_STORAGE:
        _WORK_SQL_STORAGE[work_storage_name] = icWorkSQLStorage(None, db_psp)
        log.info(u'Регистрация БД <%s> в списке хранилищ' % work_storage_name)
    return _WORK_SQL_STORAGE[work_storage_name]


class icWorkStorageInterface(object):
    """
    Интерфейс абстрактного хранилища/БД документов.
    """

    def __init__(self, parent, db_psp):
        """
        Конструктор.
        :param parent: Родительский объект.
        :param db_psp: Паспорт БД.
        """
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
        :param obj: Сохраняемый объект.
        """
        pass
        
    def loadObject(self, obj, obj_id):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        :param obj: Объект.
        :param obj_id: Идентификатор объекта.
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
        
    def setTable(self, table_name=None):
        """
        Установить таблицу, по ее имени.
        :param table_name: Имя таблицы.
        :return: Возвращает объект таблицы или None, если таблицу получить нельзя.
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
            

class icWorkSQLStorage(icWorkStorageInterface):
    """
    SQL хранилище/БД всяких бизнес объектов.
    """

    def __init__(self, parent, db_psp):
        """
        Конструктор.
        :param parent: Родительский объект.
        :param db_psp: Паспорт БД.
        """
        icWorkStorageInterface.__init__(self, parent, db_psp)
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
    def setCascadeDict(self, obj, record_id, data_dict, ident_fields=None):
        """
        Сохранение каскадного словаря значений в объект хранилища.
        :param obj: Объект/таблица, в который будет сохраняться запись.
        :param record_id: Идентификатор записи. 
            Если None, то запись будет добавлена.
        :param data_dict: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        :param ident_fields: Список имен полей идентифицирующих запись,
            если не указан идентификатор записи.
        :return: Результат выполнения True/False или None в случае ошибки.
        """
        if record_id is None:
            if ident_fields is None:
                return self.addCascadeDict(obj, data_dict)
            else:
                _id_ = self._identRecord(obj, data_dict, ident_fields)
                if _id_ == -1:
                    return self.addCascadeDict(obj, data_dict)
                elif isinstance(_id_, int) and _id_ >= 0:
                    return self._setCascadeDict(obj, _id_, data_dict)
                elif isinstance(_id_, list):
                    log.info(u'Ошибка идентификации записи. Много записей соответствуют запросу %s' % _id_)
                    return None
                else:
                    return None
        else:
            return self._setCascadeDict(obj, record_id, data_dict)

    def _identRecord(self, obj, data_dict, ident_fields):
        """
        Идентифицировать запись в объекте.
        :param obj: Объект/таблица, в который будет сохраняться запись.
        :param data_dict: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        :param ident_fields: Список имен полей идентифицирующих запись,
            если не указан идентификатор записи.
        :return: Идентификатор записи или -1 в случае если запись не найдена.
        """
        try:
            # Таблица данных
            tab = self._tabObj(obj)
            indent_rec = [getattr(tab.c, fld_name) == data_dict[fld_name] for fld_name in ident_fields]
            find_rec = tab.get_where(icsqlalchemy.and_(*indent_rec))
            if find_rec:
                if find_rec.rowcount == 1:
                    return find_rec[0].id
                elif find_rec.rowcount > 1:
                    return [rec.id for rec in find_rec]
        except:
            log.fatal(u'Ошибка идентификации записи в таблице %s.' % obj)
            return None
        return -1

    def _setCascadeDict(self, obj, record_id, data_dict):
        """
        Сохранение каскадного словаря значений в объект хранилища.
        :param obj: Объект/таблица, в который будет сохраняться запись.
        :param record_id: Идентификатор записи.
            Если None, то запись будет добавлена.
        :param data_dict: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        :return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            if isinstance(obj, str):
                tab = icsqlalchemy.icSQLAlchemyTabClass(obj)
            else:
                tab = obj
            # Добавление записи
            rec = dict([item for item in data_dict.items() if not isinstance(item[1], list)])
            tab.update(record_id, **rec)
            # Обработка дочерних таблиц
            children_tabs = dict([item for item in data_dict.items() if isinstance(item[1], list)])
            for child_tab_name in children_tabs.keys():
                for child_rec in children_tabs[child_tab_name]:
                    # Если есть возможнось,
                    # то прописать UUID родительской записи
                    child_rec['parent'] = rec.get('uuid', u'')
                    self._setCascadeDict(child_tab_name, record_id, child_rec)
            return True
        except:
            log.fatal(u'Ошибка обновления данных в каскад таблицы %s.' % obj)
        return None

    def _tabObj(self, obj):
        """
        Таблица объекта.
        :param obj: Объект/таблица, в который будет сохраняться запись.
        """
        # Таблица данных
        if isinstance(obj, str):
            # Таблица данных передается в виде имени
            tab = icsqlalchemy.icSQLAlchemyTabClass(obj)
        elif isinstance(obj, tuple):
            # Таблица данных передается в виде паспорта
            tab = self.getKernel().Create(obj)
        else:
            tab = obj
        return tab
        
    def addCascadeDict(self, obj, data_dict):
        """
        Добавление каскадного словаря значений в объект хранилища.
        :param obj: Объект/таблица, в который будет сохраняться запись.
        :param data_dict: Словарь значений.
            Словарь представлен в виде 
                {
                'имя реквизита':значение,
                ...
                'имя спецификации':[список словарей значений],
                ...
                }
        :return: Результат выполнения True/False или None в случае ошибки.
        """
        try:
            # Таблица данных
            tab = self._tabObj(obj)
            # Добавление записи
            rec = dict([(str(key),value) for key, value in data_dict.items() if not isinstance(value, list)])
            # Если вдруг ключи юникодовые то изменить их на строковые
            tab.add(**rec)
            # Обработка дочерних таблиц
            children_tabs = dict([item for item in data_dict.items() if isinstance(item[1], list)])
            for child_tab_name in children_tabs.keys():
                for rec in children_tabs[child_tab_name]:
                    self.addCascadeDict(child_tab_name, rec)
            return True
        except:
            log.fatal(u'Ошибка добавления данных в каскад таблицы %s.' % obj)
        return None

    def saveObject(self, obj):
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
        :param obj: Сохраняемый объект.
        """
        doc_table = self.container.getTable(obj.getTableName())

        # --- Начать транзакцию ---
        result = False
        doc_table.db.connect()
        transaction = doc_table.db.session(autoflush=False,
                                           autocommit=False)

        try:
            # Расширить словарь реквизитов значениями по умолчачнию
            requisite_dict = doc_table.getDefaultRecDict()
            requisite_dict.update(obj.getRequisiteData())
            try:
                log.info(u'WorkStorage Сохранение записи %s' % str(requisite_dict.keys()))
            except UnicodeDecodeError:
                log.warning(u'UnicodeDecodeError. WorkStorage Сохранение записи...')

            save_rec = dict([(str(fld_name), value) for fld_name, value in requisite_dict.items() if not isinstance(value, list)])
            if not doc_table.count(doc_table.c.uuid == obj.getUUID()):
                # Добавить
                try:
                    log.info(u'WorkStorage Добавление записи объекта <%s>' % obj.getUUID())
                except UnicodeDecodeError:
                    log.warning(u'UnicodeDecodeError. WorkStorage Добавление записи...')

                doc_table.add_rec_transact(rec=save_rec,
                                           transaction=transaction)
                id = doc_table.getLastInsertedId()
            else:
                # Отредактировать уже существующий
                rec = doc_table.select(doc_table.c.uuid == obj.getUUID()).first()
                id = rec.id if rec else 0
                doc_table.update_rec_transact(id, rec=save_rec,
                                              transaction=transaction)

            # Сохранить дочерние объекты
            children = [child for child in obj.getChildrenRequisites() if issubclass(child.__class__,
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
            log.fatal(u'Ошибка сохранения реквизитов объекта <%s>' % obj.__class__.__name__)

        doc_table.db.disconnect()
        return result
            
    def _saveObjectData(self, cur_obj, parent_table=None,
                        parent_id=None, transaction=None,
                        parent_uuid=''):
        """
        Сохранить данные объекта в хранилище.
        :param cur_obj: Текущий объект спецификации документа.
        :param parent_table: Объект родительской таблицы.
        :param parent_id: Идентификатор родительской записи.
        :param transaction: Объект транзакции (если надо).
        :param parent_uuid: UUID родительской записи.
        """
        table = self.container.getTable(cur_obj.getTableName())

        parent_id_fieldname = table.getLinkIdFieldName(parent_table)
        # Удалить записей спецификации
        where = sqlalchemy.and_(getattr(table.c, parent_id_fieldname) == parent_id)
        table.del_where_transact(where, transaction=transaction)

        children = [child for child in cur_obj.getChildrenRequisites() if issubclass(child.__class__,
                                                                                     persistent.icObjPersistent)]
        # Добавить записи спецификации
        obj_data = cur_obj.getData()
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

    def isObject(self, obj, UUID):
        """
        Проверка существования данных объекта в хранилище по идентификатору.
        :param obj: Объект.
        :param UUID: Уникальный идентификатор объекта.
        :return: True/False.
        """
        try:
            # Проинициализировать все дочерние объекты
            obj.init_children_data()

            tab = self.container.getTable(obj.getTableName())
            try:
                count = tab.count(tab.c.uuid == UUID)
            except:
                log.fatal(u'ОШИБКА наличия объекта в хранилище')
                return False
            return True if count > 0 else False
        except:
            log.fatal(u'ОШИБКА определения существования объекта <%s>' % UUID)
        return False

    def loadObject(self, obj, UUID):
        """
        Загрузить данные объекта из хранилища по идентификатору.
        :param obj: Объект.
        :param UUID: Уникальный идентификатор объекта.
        :return: True/False.
        """
        try:
            # Проинициализировать все дочерние объекты
            obj.init_children_data()
            
            tab = self.container.getTable(obj.getTableName())
            try:
                result = tab.select(tab.c.uuid == UUID)
            except:
                log.fatal(u'ОШИБКА чтения объекта их хранилища')
                return False

            if result.rowcount:
                # Запомнить идентификатор документа
                obj.uuid = UUID
                # Получить все данные документа в виде словаря
                cascade_data = tab.getCascadeDict(result.first().id)
                # log.info(u'GET Cascade Data %s' % cascade_data)
            else:
                log.info(u'Данные объекта <%s> не найдены' % UUID)
                return False
            # Установка внутренних данных в объекте
            # Только реквизиты
            obj_requisites = [requisite for requisite in obj.getAllRequisites() if issubclass(requisite.__class__,
                                                                                              persistent.icAttrPersistent)]
            
            # Перебор реквизитов
            for requisite in obj_requisites:
                value = cascade_data.get(requisite.getName(), None)
                requisite.setValue(value)
                
            # Только табличные реквизиты
            obj_tab = [obj_spc for obj_spc in obj.getAllRequisites() if issubclass(obj_spc.__class__,
                                                                                   persistent.icObjPersistent)]
            for obj_spc in obj_tab:
                tab_name = obj_spc.getTableName()
                if tab_name in cascade_data:
                    self._setObjectData(obj_spc, cascade_data[tab_name])
            return True
        except:
            log.fatal(u'ОШИБКА загрузки реквизитов объекта %s' % obj.getUUID())
        return False

    def _setObjectData(self, cur_obj, obj_data):
        """
        Установка данных объекта.
        :param cur_obj: Текущий объект.
        :param obj_data: Данные объекта.
        """
        # Только реквизиты
        requisites = [requisite for requisite in cur_obj.getChildrenRequisites() if issubclass(requisite.__class__,
                                                                                               persistent.icAttrPersistent)]
        # Табличные реквизиты
        tab_requisites = [requisite for requisite in cur_obj.getChildrenRequisites() if issubclass(requisite.__class__,
                                                                                                   persistent.icObjPersistent)]
        for rec_data in obj_data:
            row = dict()
            for requisite in requisites:
                value = rec_data.get(requisite.getName(), None)
                row[requisite.getName()] = value
            cur_obj.addRow(**row)

            for tab_requisite in tab_requisites:
                tab_name = tab_requisite.getTableName()
                if tab_name in rec_data:
                    self._setObjectData(tab_requisite, rec_data[tab_name])

    def _resultLen(self, query_result):
        """
        Количество записей результата запроса.
        :param query_result: Результат запроса.
        """
        if isinstance(query_result, list):
            return len(query_result)
        elif not query_result:
            return 0
        else:
            return query_result.rowcount
        return -1
    
    def getFieldNames(self, obj):
        """
        Список имен полей таблицы хранения объекта.
        :param obj: Объект.
        """
        obj_requisites = [requisite for requisite in obj.getAllRequisites() if issubclass(requisite.__class__,
                                                                                          persistent.icAttrPersistent)]
        fields = [obj_requisite.getFieldName() for obj_requisite in obj_requisites]
        # log.info(u'icworkstorage.getFieldNames::: %s' % fields)
        return fields
        
    def delAllData(self, obj, data_filter=None):
        """
        Удалить все данные объекта.
        :param obj: Объект.
        :param data_filter: Дополнительный фильтр. Словарь {'имя поля':значение}
        :return: Возвращает True/False или None  в случае ошибки.
        """
        try:
            obj_table = self.container.getTable(obj.getTableName())
            if data_filter:
                cur_filter = [getattr(obj_table.c, fld_name) == fld_value for fld_name, fld_value in data_filter.items()]
                # Фильтрация производится по "И"
                return obj_table.del_where(icsqlalchemy.and_(*cur_filter))
            else:
                return obj_table.dataclass.select().delete().execute()            
        except:
            log.fatal(u'ОШИБКА удаления объекта %s их хранилища' % obj.name)
        return None
        
    def getAllData(self, obj, data_filter=None):
        """
        Получить все данные объекта.
        :param obj: Объект.
        :param data_filter: Дополнительный фильтр.
        :return: Возвращает список или None  в случае ошибки.
        """
        try:
            # Проинициализировать все дочерние объекты
            obj.init_children_data()
            
            obj_table = self.container.getTable(obj.getTableName())
            try:
                if data_filter:
                    result = obj_table.queryAll(data_filter)
                else:
                    result = obj_table.select()

                if not self._resultLen(result):
                    log.info(u'Данные объекта %s не найдены' % obj.name)
                    # Только реквизиты
                    fields = self.getFieldNames(obj)
                    return {'fields': fields, 'data': []}
            except:
                log.fatal(u'ОШИБКА чтения объекта %s их хранилища' % obj.name)
            return None

            # Только реквизиты
            fields = self.getFieldNames(obj)

            # Перебор записей
            data = []
            for rec in result:
                # Перебор полей реквизитов
                if isinstance(rec, (tuple, list)):
                    rec_list = list(rec)
                else:
                    rec_list = list()
                    for field in fields:
                        rec_list.append(rec[field])
                    
                data.append(rec_list)
                
            return {'fields': fields, 'data': data}
        except:
            log.fatal(u'ОШИБКА. Получения всех данных объекта %s' % obj.name)
        return None

    def getAllUUID(self, obj, order_sort=None):
        """
        Получить все уникальные идентификаторы объектов UUID.
        :param obj: Объект документа.
        :param order_sort: Порядок сортировки.
            Список имен полей, в котором надо сортировать.
        :return: Список уникальных идентификаторов UUID
        """
        try:
            doc_table = self.container.getTable(obj.getTableName())
            # ВНИМАНИЕ! Пример SQL select'а с выбором опрределенных колонок
            sql = sqlalchemy.sql.select(columns=[doc_table.c.uuid],
                                        from_obj=[doc_table.dataclass])
            if order_sort:
                if isinstance(order_sort, list) or isinstance(order_sort, tuple):
                    for field_name in order_sort:
                        sql = sql.order_by(getattr(doc_table.c, field_name))
                elif isinstance(order_sort, str):
                    sql = sql.order_by(getattr(doc_table.c, order_sort))
                else:
                    log.warning(u'Не корректный тип <%s> параметра порядка сортировки в методе getAllUUID' % type(order_sort))

            records = sql.execute()
            return [record['uuid'] for record in records]
        except:
            log.fatal(u'Ошибка получения всех UUID')
        return list()

    def test(self):
        """
        Функция тестирования.
        """
        pass

        
if __name__ == '__main__':
    storage = icWorkSQLStorage(None, 'work_db_psgress')
    storage.test()
