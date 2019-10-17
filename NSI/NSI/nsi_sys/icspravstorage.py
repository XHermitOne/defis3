#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Хранилище справочников.
"""

# Подключение библиотек
import time
import copy
from ic.components import icwidget
from ic.utils import datetimefunc
from ic.utils import resource
from ic.log import log
from ic.utils import uuidfunc
from ic.db import icsqlalchemy
from ic.db import icdb
from ic.engine import glob_functions
from ic.utils import extfunc
from . import gen_nsi_table_res

# Версия
__version__ = (1, 1, 2, 3)

# Зарезервированные имена полей
RESERVER_FIELD_NAMES = ('type', 'count', 'cod', 'name', 'access', 'uuid')


class icSpravStorageInterface(object):
    """
    Класс абстрактного хранилища справочников. Реализует только интерфейс.
    """

    def __init__(self, parent_sprav=None, source_name=None, object_name=None):
        """
        Конструктор.
        @param parent_sprav: Объект справочника, к которому прикреплено
            хранилище справочников.
        @param source_name: Имя БД. Источник данных.
        @param object_name: Объект хранилища. Таблица.
        """
        self._sprav_parent = parent_sprav
        self._src_name = source_name
        self._obj_name = object_name

    def getSpravParent(self):
        """
        Объект справочника, к которому прикреплено хранилище справочников.
        """
        return self._sprav_parent

    def getSpravFieldNames(self, level_idx=0):
        """
        Список имен полей таблицы данных справочника.
        @param level_idx: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то индекс определяется как индекс самого верхнего уровня.
        @return: Список имен полей таблицы данных объекта-ссылки/справочника.
            Либо пустой список в случае ошибки.
        """
        return ['cod', 'name', 's1', 's2', 's3', 'n1', 'n2', 'n3', 'f1', 'f2', 'f3', 'access']

    def _getSpravFieldDict(self, field_values, level_idx=0):
        """
        Получить запись таблицы данных справочника в виде словаря.
        @param field_values: Список значений записи таблицы значений уровня.
        @param level_idx: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то индекс определяется как индекс самого верхнего уровня.
        @return: запись таблицы данных справочника в виде словаря.
        """
        log.warning(u'Не определен метод _getSpravFieldDict в <%s>' % self.__class__.__name__)
        return dict()

    def _str(self, value):
        return str(value)

    def _int(self, value):
        return int(float(value))

    def _float(self, value):
        return float(value)

    def typeSpravField(self):
        """
        Список типов полей таблицы данных справочника.
        """
        return [self.__class__._str, self.__class__._str, self.__class__._str,
                self.__class__._str, self.__class__._str, self.__class__._int,
                self.__class__._int, self.__class__._int, self.__class__._float,
                self.__class__._float, self.__class__._float, self.__class__._str]

    def setTypeLevelTable(self, table):
        """
        Преобразование таблицы данных уровня по типам.
        @return: Возвращает таблицу с преобразованными типами
        """
        field_types = self.typeSpravField()
        tab = []
        # Перебор по строкам
        for rec in table:
            # Перебор по полям
            rec = list(rec)
            for i_field in range(len(rec)):
                rec[i_field] = field_types[i_field](self, rec[i_field])
            tab.append(rec)
        return tab

    def getLevelBranch(self, struct_cod=None):
        """
        Получить ветку данных уровня,
        включая дочерние элементы по структурному коду.
        @param struct_cod: Структурный код ('COD1','COD2',None).
        @return: Словарно-списковую структуру следующего формата:
            [
                {
                'name':Имя узла,
                'child':[...], Список словарей дочерних узлов
                '__record__':Данные, прикреплямые к узлу  в виде списка.
                },
                ...
            ]
            или None  в случае ошибки.
        """
        if struct_cod is None:
            return self.getLevelTree()
        level_cod = ''.join([subcod for subcod in struct_cod if subcod is not None])
        if level_cod:
            return self.getLevelTree(level_cod)
        else:
            return self.getLevelTree()

    def getLevelTree(self, level_cod=None):
        """
        Дерево данных уровня, включая дочерние элементы.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то возвращаются данные самого верхнего уровня.
        @return: Словарно-списковую структуру следующего формата:
            [
                {
                'name':Имя узла,
                'child':[...], Список словарей дочерних узлов
                '__record__':Данные, прикреплямые к узлу  в виде списка.
                },
                ...
            ]
            или None  в случае ошибки.
        """
        return self._getLevelTree(level_cod)

    def _getLevelTree(self, level_cod=None):
        """
        Дерево данных уровня, включая дочерние элементы.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то возвращаются данные самого верхнего уровня.
        @return: Словарно-списковую структуру следующего формата:
            [
                {
                'name':Имя узла,
                'child':[...], Список словарей дочерних узлов
                '__record__':Данные, прикреплямые к узлу  в виде списка.
                },
                ...
            ]
            или None  в случае ошибки.
        """
        try:
            result = []
            # Получить таблицу уровня
            recs = self.getLevelTable(level_cod)
            if recs:
                for rec in recs:
                    item = {}
                    item['name'] = rec[0]
                    item['__record__'] = list(rec)
                    children = self._getLevelTree(rec[0])
                    item['child'] = children
                    result.append(item)
            return result
        except:
            log.fatal(u'Ошибка определения дерева данных уровня %s справочника %s.' % (level_cod,
                                                                                       self.getSpravParent().getName()))
            return None

    def limitLevelTree(self, tree_data, depth=-1):
        """
        Ограничение дерева справочника до определенного уровня.
        @param tree_data: Дерево данных. Формат:
            [
                {
                'name':Имя узла,
                'child':[...], Список словарей дочерних узлов
                '__record__':Данные, прикреплямые к узлу  в виде списка.
                },
                ...
            ]
        @param depth: Глубина ограничения, если -1,
            то ограничение делать не надо.
        """
        try:
            if depth < 0:
                return tree_data
            for i, item in enumerate(tree_data):
                if depth:
                    item['child'] = self.limitLevelTree(item['child'], depth - 1)
                else:
                    item['child'] = []
                tree_data[i] = item
            return tree_data
        except:
            log.fatal(u'Ошибка ограничения дерева данных справочника %s.' % self.getSpravParent().getName())
            return tree_data

    def setLevelTree(self, level_cod, table):
        """
        Сохранить таблицу данных уровня вместе с дочерними уровнями.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        log.warning(u'Не определен метод setLevelTree в <%s>' % self.__class__.__name__)
        return False

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
        log.warning(u'Не определен метод getLevelTable в <%s>' % self.__class__.__name__)
        return None

    def setLevelTable(self, level_cod, table):
        """
        Сохранить таблицу данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
            Имена полей таблицы данных уровня определятся с помощью функции
            getSpravFieldNames().
        @return: Возвращает результат выполнения операции True/False.
        """
        log.warning(u'Не определен метод setLevelTable в <%s>' % self.__class__.__name__)
        return False

    def getRecByCod(self, cod, dt=None):
        """
        Получить запись по коду.
        @param cod: Код.
        @param dt: Период актуальности.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        log.warning(u'Не определен метод getRecByCod в <%s>' % self.__class__.__name__)
        return None

    def updateRecByCod(self, cod, record_dict, dt=None):
        """
        Изменить запись по коду.
        @param cod: Код.
        @param record_dict: Словарь изменений.
        @param dt: Период актуальности.
        """
        log.warning(u'Не определен метод updateRecByCod в <%s>' % self.__class__.__name__)
        return None

    def delRecByCod(self, cod, dt=None):
        """
        Удалить запись по коду.
        @param cod: Код.
        @param dt: Период актуальности.
        """
        assert None, u'Не определен метод delRecByCod в <%s>' % self.__class__.__name__

    def addRecDictDataTab(self, record_dict):
        """
        Добавить запись в таблице данных.
        @param record_dict: Словарь данных записи.
        """
        log.warning(u'Не определен метод addRecDictDataTab в <%s>' % self.__class__.__name__)
        return None

    def clear(self):
        """
        Очистить справочник от данных.
        """
        assert None, u'Не определен метод clear в <%s>' % self.__class__.__name__

    def is_empty(self):
        """
        Проверка на пустой справочник.
        @return: True - справочник пустой, False - Есть данные.
        """
        log.warning(u'Не определен метод is_empty в <%s>' % self.__class__.__name__)
        return False

    def isCod(self, cod):
        """
        Есть такой код в справочнике?
        @param cod: Код.
        @return: True - Такой код присутствует в справочнике / False - нет.
        """
        return bool(self.getRecByCod(cod))

    def search(self, search_value, search_fieldname='name',
               order_by=None, is_desc=False):
        """
        Поиск по полю.
        @param search_value: Искомое значение.
        @param search_fieldname: Имя поля, по которому производим поиск.
        @param order_by: Порядок сортировки.
            Список полей порядка сортировки.
            Если сортировку надо производить по одному полю, то можно указать
            его имя в строковом виде.
        @param is_desc: Произвести обратную сортировку?
        @return: Список найденных кодов соответствующих искомому значению.
        """
        log.warning(u'Не определен метод search в <%s>' % self.__class__.__name__)
        return list()

    def getTableName(self):
        """
        Имя таблицы справочника.
        """
        sprav = self.getSpravParent()
        return sprav.getTableName() if sprav else None

    def getDBPsp(self):
        """
        Паспорт БД хранения справочника.
        """
        sprav = self.getSpravParent()
        return sprav.getDBPsp() if sprav else None

    def getDescription(self):
        """
        Описание компонента.
        """
        sprav = self.getSpravParent()
        return sprav.getDescription() if sprav else u''


class icSpravSQLStorage(icSpravStorageInterface,
                        gen_nsi_table_res.icSpravTableResGenerator):
    """
    Класс SQL хранилища справочника.
    """

    def __init__(self, parent_sprav, db_name, table_name, db_subsys=None, table_subsys=None):
        """
        Конструктор.
        @param parent_sprav: Объект справочника, к которому прикреплено
            хранилище справочников.
        @param db_name: Имя БД.
        @param table_name: Имя таблицы данных справочника.
        @param db_subsys: Имя подсистемы, откуда берется ресурс БД.
        @param table_subsys: Имя подсистемы, откуда берется ресурс таблицы.
        """
        icSpravStorageInterface.__init__(self, parent_sprav, db_name, table_name)

        # Если указана БД, тогда создать БД и подменить в таблицах хранения
        # в противном случае таблица сама знает в какой БД ей храниться
        db = None
        if db_name:
            pathRes = None
            if db_subsys:
                pathRes = resource.getSubsysPath(db_subsys)
            
            db_res = resource.icGetRes(db_name, 'src', pathRes=pathRes, nameRes=db_name)
            db = icdb.icSQLAlchemyDB(db_res)
        
        # Таблица данных
        # self._tab = icsqlalchemy.icSQLAlchemyTabClass(table_name, db_resource=db, sub_system_name=table_subsys)
        self._tab = None
        self._tab = self.getTable()
        # Таблица данных, изменненных во времени
        tab_time_name = self.getTabTimeName()
        
        self._tab_time = None
        if tab_time_name:
            self._tab_time = icsqlalchemy.icSQLAlchemyTabClass(tab_time_name, DB_=db, sub_system_name=table_subsys)

    def isTabTime(self):
        """
        Есть ли таблица временных значений.
        """
        return self.getSpravParent().isTabTime()
        
    def getTabTimeName(self):
        """
        Имя таблицы временных параметров.
        """
        if self._tab and self.isTabTime():
            tab_data_name = self._tab.getDBTableName()
            if tab_data_name:
                if 'data' in tab_data_name:
                    tab_time_name = tab_data_name.replace('data', 'time')
                else:
                    tab_time_name = tab_data_name+'_time'
                return tab_time_name
        return None        
        
    def getSpravTabClass(self):
        """
        Объект таблицы справочника.
        """
        if self._tab is None:
            tab_res = self._createTableResource()
            sprav = self.getSpravParent()
            self._tab = sprav.GetKernel().createObjBySpc(parent=None, res=tab_res) if sprav else None
        return self._tab

    # Объект таблицы справочника
    getTable = getSpravTabClass

    def getLevelTable(self, level_cod=None, dt=None):
        """
        Таблица данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
        @type dt: C{string}
        @param dt: Время актуальности данных.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Или None в случае ошибки.
        """
        cache = self._sprav_parent.getCache()
        is_auto_cache = self._sprav_parent.getAutoCache()
        if is_auto_cache:
            # Если включено автокеширование...
            if cache.hasObject(self._sprav_parent.getName(), (level_cod, dt)):
                # И в кеше эта таблица есть, то просто вернуть ее
                return cache.get(self._sprav_parent.getName(), (level_cod, dt))
        if dt:
            tab = self._getLevelTabDatetime(level_cod, dt)
        else:
            tab = self._getLevelTab(level_cod)
        # Прописать в кэше
        if is_auto_cache:
            # Если включено автокеширование...
            cache.add(self._sprav_parent.getName(), (level_cod, dt), tab)
        return tab

    def _getLevelTab(self, level_cod):
        """
        Таблица данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Или None в случае ошибки.
        """
        try:
            if not level_cod:
                level_cod = ''
                # Длина кода уровня
                level = self.getSpravParent().getLevelByCod(level_cod)
                level_len = level.getCodLen()
            else:
                # Длина кода уровня
                level = self.getSpravParent().getLevelByCod(level_cod).getNext()
                if level:
                    level_len = level.getCodLen()
                else:
                    return []

            # Имя таблицы данных
            tab_name = self._tab.getDBTableName()

            # Длина родительского кода уровня
            parent_len = len(level_cod)
            parent_code_str = level_cod

            # Генерация выборки данных, соответствующих текущему уровню
            field_names_str = ','.join(self.getSpravFieldNames())

            sql = '''SELECT %s FROM %s
                WHERE %s.type='%s' AND SUBSTR(%s.cod,1,%d) LIKE(\'%s\') AND
                LENGTH(SUBSTR(%s.cod,%d,LENGTH(%s.cod)-%d))=%d''' % (field_names_str,
                                                                     tab_name,
                                                                     tab_name,
                                                                     self.getSpravParent().getName(),
                                                                     tab_name,
                                                                     parent_len,
                                                                     parent_code_str,
                                                                     tab_name,
                                                                     parent_len+1,
                                                                     tab_name,
                                                                     parent_len,
                                                                     level_len)

            recs = self._tab.queryAll(sql)
            return recs
        except:
            log.fatal(u'Ошибка определения таблицы данных уровня %s справочника %s.' % (level_cod,
                                                                                        self.getSpravParent().getName()))
            return None

    def record_tuple2record_dict(self, record_tuple):
        """
        Преобразование записи в виде кортежа в словарь.
        @param record_tuple: Запись в виде кортежа.
        @return: Запись в виде словаря.
        """
        try:
            field_names = self.getSpravFieldNames()
            return dict([(field_name, record_tuple[i])for i, field_name in enumerate(field_names)])
        except:
            log.fatal(u'Ошибка преобразования кортежа записи %s к словарю' % str(record_tuple))
        return dict()

    def _getLevelTabDatetime(self, level_cod, dt):
        """
        Таблица данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
        @type dt: C{string}
        @param dt: Время актуальности данных.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Или None в случае ошибки.
        """
        try:
            if not self._tab_time:
                log.warning(u'Для справочника %s не определена таблица временных значений.' % self.getSpravParent().getName())
                return None
            
            if not level_cod:
                level_cod = ''
                # Длина кода уровня
                level = self.getSpravParent().getLevelByCod(level_cod)
                level_len = level.getCodLen()
            else:
                # Длина кода уровня
                level = self.getSpravParent().getLevelByCod(level_cod).getNext()
                if level:
                    level_len = level.getCodLen()
                else:
                    return []
            # Имя таблицы данных
            tab_name = self._tab_time.getDBTableName()
            # Длина родительского кода уровня
            parent_len = len(level_cod)
            parent_code_str = level_cod
            # Генерация выборки данных, соответствующих текущему уровню
            field_names_str = ','.join(self.getSpravFieldNames())

            sql = '''SELECT %s FROM %s
                WHERE %s.type='%s' AND SUBSTR(%s.cod,1,%d) LIKE(\'%s\') AND
                LENGTH(SUBSTR(%s.cod,%d,LENGTH(%s.cod)-%d))=%d AND
                time_start<='%s' AND (time_end>='%s' OR time_end='')''' % (field_names_str,
                                                                           tab_name,
                                                                           tab_name,
                                                                           self.getSpravParent().getName(),
                                                                           tab_name,
                                                                           parent_len,
                                                                           parent_code_str,
                                                                           tab_name,
                                                                           parent_len + 1,
                                                                           tab_name,
                                                                           parent_len,
                                                                           level_len,
                                                                           dt,
                                                                           dt)

            recs = self._tab_time.queryAll(sql)
            return recs
        except:
            log.fatal(u'Ошибка определения таблицы данных уровня с учетом временных значений %s справочника %s.' % (level_cod,
                                                                                                                    self.getSpravParent().getName()))
            return None

    def _setRecDataTab(self, record, record_data):
        """
        Установить/обновить запись в таблице данных.
        @param record: Объект записи таблицы данных.
        @param record_data: Кортеж данных записи.
        """
        try:
            sprav_type = self.getSpravParent().getName()
            field_data = self._getSpravFieldDict(record_data)
            return self._tab.update(id=record[0], type=sprav_type, count=0, **field_data)
        except:
            log.fatal(u'Ошибка обновления записи в таблице данных справочника [%s].' % self.getSpravParent().getName())
            return None

    def _setRecTimeTab(self, record, record_data, dt):
        """
        Установить/обновить запись в таблице временных значений.
        @param record: Объект записи таблицы данных.
        @param record_data: Кортеж данных записи.
        @param dt: Фиксируемое время.
        """
        try:
            if self._tab_time:
                return self._tab_time.update(id=record[0], time_end=str(dt))
        except:
            log.fatal(u'Ошибка обновления записи в таблице временныйх значений справочника [%s].' % self.getSpravParent().getName())
        return None

    def _addRecDataTab(self, table, record_data):
        """
        Добавить запись в таблице данных.
        @param table: Объект таблицы данных.
        @param record_data: Кортеж данных записи.
        """
        try:
            sprav_type = self.getSpravParent().getName()
            field_data = self._getSpravFieldDict(record_data)
            
            if ('uuid' not in field_data) or (not field_data['uuid']):
                # Если уникальный идентификатор записи не определен,
                # тогда сгенерировать его
                field_data['uuid'] = uuidfunc.get_uuid()
                
            return self._tab.add(type=sprav_type, count=0, **field_data)
        except:
            log.fatal(u'Ошибка добавления записи в таблицу данных справочника [%s].' % self.getSpravParent().getName())
            return None

    def _addRecTimeTab(self, table, record_data, record_id, dt):
        """
        Добавить запись в таблице временных значений.
        @param table: Объект таблицы временных значений.
        @param record_data: Кортеж данных записи.
        @param record_id: Идентификатор родительской записи таблицы данных.
        @param dt: Фиксируемое время.
        """
        try:
            sprav_type = self.getSpravParent().getName()
            field_data = self._getSpravFieldDict(record_data)
            return table.add(type=sprav_type, id_nsi_data=record_id,
                             time_start=str(dt), time_end='', **field_data)
        except:
            log.fatal(u'Ошибка добавления записи в таблицу временных значений справочника %s.' % self.getSpravParent().getName())
            return None

    def setLevelTable(self, level_cod, table, *arg, **kwarg):
        """
        Сохранить таблицу данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        ok = self._setLevelTabBuff(level_cod, table, *arg, **kwarg)
        if ok:
            # Если запись прошла удачно, то сбросить кэш
            self._sprav_parent.clearInCache()

    def _get_cod_lst(self, table, indx=0):
        """
        Возвращает список кодов таблицы.
        """
        return [r[indx] for r in table]

    def _cod2u(self, cod):
        """
        Конвертация кода в unicod.
        """
        if not isinstance(cod, str):
            return str(cod)
        return cod

    def _setLevelTabBuff(self, level_cod, table, *arg, **kwarg):
        """
        Сохранить таблицу данных уровня по буферу изменений.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня буфера - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            buff = kwarg.get('change_buff', None)
            today = datetimefunc.TodayFmt()
            # Перебор по записям таблицы данных
            sprav_type = self.getSpravParent().getName()
            # Старые записи
            t1 = time.clock()

            old_tab = self.getLevelTable(level_cod)
            old_cod_lst = self._get_cod_lst(old_tab)
            cod_lst = self._get_cod_lst(table)

            t2 = time.clock()

            # Удаляем записи
            del_cod_lst = list(set(old_cod_lst) - set(cod_lst))
            del_recs = [r for r in old_tab if r[0] in del_cod_lst]
            self.delLevelTable(del_recs)

            # Если задан буфер изменений
            if buff:
                # Список обновлений
                upd_rec = buff.update_rows_dct.values()+[el for key, el in buff.add_rows_dct.items() if key not in buff.update_rows_dct.keys()]
                upd_rec = [r for r in upd_rec if r[0] in cod_lst]
            else:
                upd_rec = table

            # Обновляем записи
            for rec in upd_rec:
                # !!! Строка приходит в unicode
                new_cod = self._cod2u(rec[0])
                sql_result = self._tab.select(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                                self._tab.c.cod == new_cod))
                recs = self._tab.listRecs(sql_result)
                if len(recs):
                    if not self._inTableIsRecord(old_tab, rec):
                        # Изменение записи
                        self._setRecDataTab(recs[0], rec)
                        # Запись данных в таблицу временных значений
                        if self._tab_time:
                            # Сначала прописать время окончания актуальности данных
                            time_sql_result = self._tab_time.select(icsqlalchemy.and_(self._tab_time.c.type == sprav_type,
                                                                                      self._tab_time.c.cod == new_cod,
                                                                                      self._tab_time.c.time_start <= today,
                                                                                      self._tab_time.c.time_end == ''))
                            time_recs = self._tab_time.listRecs(time_sql_result)
                            if len(time_recs):
                                self._setRecTimeTab(time_recs[0], rec, today)
                            # Добавить в таблицу временных значений
                            self._addRecTimeTab(self._tab_time, rec, new_cod[0], today)
                else:
                    # Добавление записи
                    new_rec = self._addRecDataTab(self._tab, rec)
                    # Запись данных в таблицу временных значений
                    if not self._inTableIsRecord(old_tab, rec):
                        # Добавить в таблицу временных значений
                        if self._tab_time:
                            self._addRecTimeTab(self._tab_time, rec,
                                                new_rec.last_inserted_ids()[-1], today)

            t3 = time.clock()
            print('\tget table: ', t2-t1)
            print('\tupdate: ', t3-t2)
            print('\tall time: ', t3-t1)
            return True
        except:
            log.fatal(u'Ошибка сохранения таблицы данных уровня %s справочника [%s].' % (level_cod,
                                                                                         self.getSpravParent().getName()))
            return False

    def _setLevelTab(self, level_cod, table, *arg, **kwarg):
        """
        Сохранить таблицу данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            today = datetimefunc.TodayFmt()
            # Перебор по записям таблицы данных
            sprav_type = self.getSpravParent().getName()
            # Старые записи
            t1 = time.clock()
            old_tab = self.getLevelTable(level_cod)
            t2 = time.clock()
            # Удаление старых записей
            del_recs = []
            for old_rec in old_tab:
                if not self._inTableIsRecord(table, old_rec, [0]):
                    del_recs.append(old_rec)
            if del_recs:
                self.delLevelTable(del_recs)
            # Затем добавить
            for rec in table:
                # !!! Строка приходит в unicode
                new_cod = self._cod2u(rec[0])
                sql_result = self._tab.select(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                                self._tab.c.cod == new_cod))
                recs = self._tab.listRecs(sql_result)
                if len(recs):
                    if not self._inTableIsRecord(old_tab, rec):
                        # Изменение записи
                        self._setRecDataTab(recs[0], rec)
                        # Запись данных в таблицу временных значений
                        if self._tab_time:
                            # Сначала прописать время окончания актуальности данных
                            time_sql_result = self._tab_time.select(icsqlalchemy.and_(self._tab_time.c.type == sprav_type,
                                                                                      self._tab_time.c.cod == new_cod,
                                                                                      self._tab_time.c.time_start <= today,
                                                                                      self._tab_time.c.time_end == ''))
                            time_recs = self._tab_time.listRecs(time_sql_result)
                            if len(time_recs):
                                self._setRecTimeTab(time_recs[0], rec, today)
                            # Добавить в таблицу временных значений
                            self._addRecTimeTab(self._tab_time, rec, new_cod[0], today)
                else:
                    # Добавление записи
                    new_rec = self._addRecDataTab(self._tab, rec)
                    # Запись данных в таблицу временных значений
                    if not self._inTableIsRecord(old_tab, rec):
                        # Добавить в таблицу временных значений
                        if self._tab_time:
                            self._addRecTimeTab(self._tab_time, rec,
                                                new_rec.last_inserted_ids()[-1], today)
            t3 = time.clock()
            print('\tget table: ', t2-t1)
            print('\tupdate: ', t3-t2)
            print('\tall time: ', t3-t1)
            return True
        except:
            log.fatal(u'Ошибка сохранения таблицы данных уровня %s справочника %s.'%(level_cod,
                                                                                     self.getSpravParent().getName()))
            return False

    def _compareValue(self, value1, value2):
        """
        Сравнение двух значений с учетом unicode.
        """
        # Внимание! Проверять нужно только строковые представления!
        if isinstance(value1, str) or isinstance(value2, str):
            # Если хотя бы одно значение в unicode
            # то сравнивать нужно unicode
            encoding = self._tab.db.getEncoding()
            val1 = str(value1) if not isinstance(value1, bytes) else value1.decode(encoding)
            val2 = str(value2) if not isinstance(value2, bytes) else value2.decode(encoding)
            return val1 == val2
        return str(value1) == str(value2)

    def _inTableIsRecord(self, table, record, fields=None):
        """
        Поверка, есть ли в таблице такая запись.
        @param table: Таблица-список кортежей.
        @param record: Запись-кортеж.
        @param fields: Список индексов проверяемых полей.
        """
        for rec in table:
            ok = True
            if fields is None:
                for i, value in enumerate(record):
                    try:
                        # Внимание! Проверять нужно только строковые представления!
                        if not self._compareValue(value, rec[i]):
                            ok = False
                            break
                    except IndexError:
                        break
            else:
                for i in fields:
                    try:
                        # Внимание! Проверять нужно только строковые представления!
                        if not self._compareValue(record[i], rec[i]):
                            ok = False
                            break
                    except IndexError:
                        break
            if ok:
                return True
        return False

    def delLevelTable(self, table, bIsCascade=True):
        """
        Удалить таблицу данных уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @param bIsCascade: Каскадное удаление?
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            # Перебор по записям таблицы данных
            sprav_type = self.getSpravParent().getName()
            for rec in table:
                # Удаление записи
                # !!! Строка приходит в unicode
                cod = self._cod2u(rec[0])

                if not bIsCascade:
                    self._tab.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                          self._tab.c.cod == cod))
                else:
                    self._tab.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                          self._tab.c.cod.startswith(cod)))
            return True
        except:
            log.fatal(u'Ошибка удаления таблицы данных уровня справочника %s.' % self.getSpravParent().getName())
            return False

    def getSpravFieldNames(self):
        """
        Список имен полей таблицы данных справочника.
        """
        if self._tab:
            field_names = [fld_name for fld_name in self._tab.getFieldNames() if fld_name not in RESERVER_FIELD_NAMES]
            # Поля cod и name всегда первые, а поле access всегда последнее
            return ['cod', 'name']+field_names+['access']
        else:
            return ['cod', 'name', 's1', 's2', 's3', 'n1', 'n2', 'n3', 'f1', 'f2', 'f3', 'access']

    def getCodeFieldName(self):
        """
        Имя поля кода справочника.
        @return: Имя поля кода справочника.
        """
        return 'cod'

    def _str(self, value):
        if isinstance(value, bytes):
            return value.decode(self._tab.db.getEncoding())
        elif not isinstance(value, str):
            return str(value)
        return value

    def _int(self, value):
        if not value:
            return 0
        return int(float(value))

    def _float(self, value):
        if not value:
            return 0.0
        return float(value)

    _TypeField2TypePy = {'T': _str,
                         'D': _str,
                         'I': _int,
                         'F': _float,
                         None: _str,
                         }

    def typeSpravField(self):
        """
        Список имен полей таблицы данных справочника.
        """
        if self._tab:
            field_names = self.getSpravFieldNames()
            field_types = [self._TypeField2TypePy.get(self._tab.getFieldType(field), icSpravSQLStorage._str) for field in field_names]
            return field_types
        else:
            return [icSpravStorageInterface.str, icSpravStorageInterface.str,
                    icSpravStorageInterface.str, icSpravStorageInterface.str,
                    icSpravStorageInterface.str, icSpravStorageInterface.int,
                    icSpravStorageInterface.int, icSpravStorageInterface.int,
                    icSpravStorageInterface.float, icSpravStorageInterface.float,
                    icSpravStorageInterface.float, icSpravStorageInterface.str]

    def _getSpravFieldDict(self, field_values, level_idx=0):
        """
        Получить запись таблицы данных справочника в виде словаря.
        @param field_values: Список значений записи таблицы значений уровня.
        @param level_idx: Индекс уровня объекта-ссылки/справочника.
            Если не определен, то индекс определяется как индекс самого верхнего уровня.
        @return: запись таблицы данных справочника в виде словаря.
        """
        fld_names = self.getSpravFieldNames()
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

            if fld_name == 'computer' and not value:
                fld_dict[fld_name] = extfunc.getComputerName()
            if fld_name == 'username' and not value:
                fld_dict[fld_name] = glob_functions.getCurUserName()
        return fld_dict

    def getRecByFieldValue(self, field_name, field_value, dt=None):
        """
        Получить словарь записи по уникальному значению поля.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param dt: Период актуальности.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        try:
            recs = None
            if dt is None:
                recs = self._getRecByFldVal(field_name, field_value)
            else:
                recs = self._getRecByFldValDatetime(field_name, field_value, dt)

            if recs is not None:
                if len(recs):
                    return recs[0]
        except:
            log.fatal(u'Ошибка определения словаря записи по значению <%s> поля <%s> записи' % (field_value,
                                                                                                field_name))
        return None

    def _getRecByFldVal(self, field_name, field_value):
        """
        Получить словарь записи по уникальному значению поля.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        sql = None
        try:
            # Имя таблицы данных
            tab_name = self._tab.getDBTableName()

            if isinstance(field_value, str):
                field_val_str = '\'' + field_value + '\''
            else:
                field_val_str = str(field_value)

            field_names = self.getSpravFieldNames()
            field_names_str = ','.join(field_names)
            sql = 'SELECT %s FROM %s WHERE %s.type=\'%s\' AND %s.%s=%s' % (field_names_str,
                                                                           tab_name,
                                                                           tab_name,
                                                                           self.getSpravParent().getName(),
                                                                           tab_name,
                                                                           field_name,
                                                                           field_val_str)
            
            recs = self._tab.queryAll(sql)
            # Сконвертировать список кортежей в список словарей
            if recs is not None:
                for i, rec in enumerate(recs):
                    recs[i] = dict([(fld[1], rec[fld[0]]) for fld in enumerate(field_names)])
            return recs
        except:
            log.fatal(u'Ошибка определения словаря записи по значению %s поля %s' % (field_value, field_name))
            log.error('SQL: <%s>' % sql)
            return None

    def _getRecByFldValDatetime(self, field_name, field_value, dt):
        """
        Получить словарь записи по уникальному значению поля.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param dt: Период актуальности.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        sql = None
        try:
            if not self._tab_time:
                log.warning(u'Для справочника [%s] не определена таблица временных значений.' % self.getSpravParent().getName())
                return None
            
            # Имя таблицы данных
            tab_name = self._tab_time.getDBTableName()

            field_val_str = str(field_value)
            if isinstance(field_value, str):
                field_val_str = '\''+field_val_str+'\''

            field_names = self.getSpravFieldNames()
            field_names_str = ','.join(field_names)
            sql = '''SELECT %s FROM %s
                WHERE %s.type='%s' AND %s.%s=%s AND
                time_start<='%s' AND (time_end>='%s' OR time_end='')''' % (field_names_str,
                                                                           tab_name,
                                                                           tab_name,
                                                                           self.getSpravParent().getName(),
                                                                           tab_name,
                                                                           field_name,
                                                                           field_val_str,
                                                                           dt,
                                                                           dt)

            recs = self._tab.queryAll(sql)
            # Сконвертировать список кортежей в список словарей
            for i, rec in enumerate(recs):
                recs[i] = dict([(fld[1], rec[fld[0]]) for fld in enumerate(field_names)])
            return recs
        except:
            log.fatal(u'Ошибка определения словаря записи по значению %s поля %s' % (field_value, field_name))
            log.error('SQL: <%s>' % sql)
        return None

    def getRecByCod(self, cod, dt=None):
        """
        Получить запись по коду.
        @param cod: Код.
        @param dt: Период актуальности.
        @return: Возвращает словарь записи или None в случае ошибки.
        """
        if cod:
            return self.getRecByFieldValue('cod', cod, dt)
        else:
            log.warning(u'Не определен код для получения словаря записи справочника <%s>' % self.getName())
        return None

    def delRecByCod(self, cod, dt=None, bIsCascade=True):
        """
        Удалить запись по коду.
        @param cod: Код.
        @param dt: Период актуальности.
        @param bIsCascade: Каскадное удаление.
        """
        if cod:
            code = self._cod2u(cod)
            try:
                sprav_type = self.getSpravParent().getName()
                # Удаление записи
                if not bIsCascade:
                    self._tab.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                          self._tab.c.cod == code))
                    if dt and self._tab_time:
                        self._tab_time.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                                   self._tab.c.cod == code))
                else:
                    self._tab.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                          self._tab.c.cod.startswith(code)))
                    if dt and self._tab_time:
                        self._tab_time.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                                   self._tab.c.cod.startswith(code)))

                return True
            except:
                log.fatal(u'Ошибка удаления записи по коду из справочника [%s]' % sprav_type)
                return False
        return None

    def updateRecByCod(self, cod, record_dict, dt=None):
        """
        Изменить запись по коду.
        @param cod: Код.
        @param record_dict: Словарь изменений.
        @param dt: Период актуальности.
        @return: Возвращает результат выполнения операции True/False.
        """
        try:
            if dt is None:
                if self._tab:
                    sprav_type = self.getSpravParent().getType()
                    sql_result = self._tab.select(icsqlalchemy.and_(self._tab.c.type == sprav_type,
                                                                    self._tab.c.cod == cod))
                    recs = self._tab.listRecs(sql_result)
                    if len(recs):
                        if 'id' in record_dict:
                            del record_dict['id']
                        if 'computer' in record_dict and not record_dict['computer']:
                            record_dict['computer'] = extfunc.getComputerName()
                        if 'username' in record_dict and not record_dict['username']:
                            record_dict['username'] = glob_functions.getCurUserName()

                        self._tab.update(id=recs[0][0], **record_dict)
                    else:
                        # Нет записи с таким кодом
                        return False
            else:
                # Изменить запись в таблице временных параметров
                if self._tab_time:
                    tab_time_name = self._tab_time.getDBTableName()
                    sql_result = self._tab_time.select('''WHERE %s.type='%s' AND
                        %s.cod='%s' AND
                        time_start<='%s' AND (time_end>='%s' OR time_end='')''' % (tab_time_name,
                                                                                   self.getSpravParent().getType(),
                                                                                   tab_time_name,
                                                                                   cod,
                                                                                   dt,
                                                                                   dt))

                    recs = self._tab.listRecs(sql_result)
                    if len(recs):
                        if 'id' in record_dict:
                            del record_dict['id']
                        if 'computer' in record_dict and not record_dict['computer']:
                            record_dict['computer'] = extfunc.getComputerName()
                        if 'username' in record_dict and not record_dict['username']:
                            record_dict['username'] = glob_functions.getCurUserName()
                        self._tab.update(recs[0][0], **record_dict)
                    else:
                        # Нет записи с таким кодом
                        return False
            return True
        except:
            log.fatal(u'Ошибка обновления записи по коду в <%s>' % self.getSpravParent().getType())
        return False

    def addRecDictDataTab(self, record_dict):
        """
        Добавить запись в таблице данных.
        @param record_dict: Словарь данных записи.
        """
        try:
            sprav_type = self.getSpravParent().getName()
            field_data = self._normRecDict(record_dict)
            return self._tab.add(type=sprav_type, count=0, **field_data)
        except:
            log.fatal(u'Ошибка добавления записи в таблицу данных справочника [%s].' % self.getSpravParent().getName())
        return None

    def _normRecDict(self, record_dict):
        """
        Нормализация словаря записи.
        @param record_dict: Словарь данных записи.
        """
        fld_names = self.getSpravFieldNames()
        fld_dict = {}
        for fld_name in fld_names:
            value = None
            try:
                value = record_dict[fld_name]
                fld_dict[fld_name] = value
            except KeyError:
                # Не все поля есть
                if self._tab:
                    if fld_name == 'uuid':
                        # Если uuid не определен, то сгенерировать его
                        value = uuidfunc.get_uuid()
                        fld_dict[fld_name] = value
                    else:
                        if self._tab.isFieldDefault(fld_name):
                            value = self._tab.getFieldDefault(fld_name)
                            fld_dict[fld_name] = value
            if fld_name == 'computer' and not value:
                fld_dict[fld_name] = extfunc.getComputerName()
            if fld_name == 'username' and not value:
                fld_dict[fld_name] - glob_functions.getCurUserName()

        return fld_dict

    def clear(self):
        """
        Очистить справочник.
        """
        sprav_type = self.getSpravParent().getName()
        self._tab.del_where(icsqlalchemy.and_(self._tab.c.type == sprav_type))
        if self._tab_time:
            self._tab_time.del_where(icsqlalchemy.and_(self._tab_time.c.type == sprav_type))

    def is_empty(self):
        """
        Проверка на пустой справочник.
        @return: True - справочник пустой, False - Есть данные.
        """
        sprav_type = self.getSpravParent().getName()
        rec_count = self._tab.count(icsqlalchemy.and_(self._tab.c.type == sprav_type))
        return not rec_count

    def getRecByUUID(self, UUID, dt=None):
        """
        Получить словарь записи по уникальному идентификатору.
        @param UUID: Уникальный идентификатор.
        @param dt: Период актуальности.
        @return: Возвращает словарь данных записи или None в случае ошибки.
        """
        if UUID:
            return self.getRecByFieldValue('uuid', UUID, dt)
        return None
        
    def getUUIDByCod(self, cod):
        """
        Получить уникальный идентификатор по коду.
        """
        rec = self.getRecByCod(cod)
        if rec:
            return rec.get('uuid')
        return None

    def search(self, search_value, search_fieldname='name',
               order_by=None, is_desc=False):
        """
        Поиск по полю.
        @param search_value: Искомое значение.
        @param search_fieldname: Имя поля, по которому производим поиск.
        @param order_by: Порядок сортировки. 
            Список полей порядка сортировки.
            Если сортировку надо производить по одному полю, то можно указать 
            его имя в строковом виде.
        @param is_desc: Произвести обратную сортировку?
        @return: Список найденных кодов соответствующих искомому значению.
        """
        result = list()
        if self._tab:
            try:
                field_type = self._tab.getFieldType(search_fieldname)
                field = getattr(self._tab.c, search_fieldname)
                sql = None
                if field_type in ('T', 'D'):
                    # Если поле текстовое, то ищем вхождение строки
                    search_like = '%%%s%%' % search_value
                    sql = self._tab.dataclass.select(field.ilike(search_like))
                elif field_type in ('I', 'F'):
                    # Если это числовое поле, то ищем точное значение
                    num_value = int(search_value) if field_type == 'I' else float(search_value)
                    sql = self._tab.dataclass.select(field == num_value)
                elif field_type == 'DateTime':
                    # Если это дата-время, то ищем точное совпадение, но необходимо
                    # сначала преобразовать строку в дату-время
                    dt_value = datetimefunc.strDateFmt2DateTime(search_value)
                    sql = self._tab.dataclass.select(field == dt_value)
                else:
                    log.warning(u'Поиск по полю типа <%s> не поддерживается системой' % field_type)

                if sql is not None and order_by:
                    if type(order_by) in (list, tuple):
                        if len(order_by) == 1:
                            # Одно поле сортировки
                            sql = sql.order_by(getattr(self._tab.c, order_by[0]) if not is_desc else icsqlalchemy.desc(getattr(self._tab.c, order_by[0])))
                        else:
                            # Несколько полей сортировки
                            sql = sql.order_by(*[getattr(self._tab.c, field_name) if not is_desc else getattr(self._tab.c, field_name).desc() for field_name in order_by])
                    elif isinstance(order_by, str):
                        # Одно поле сортировки
                        sql = sql.order_by(getattr(self._tab.c, order_by) if not is_desc else icsqlalchemy.desc(getattr(self._tab.c, order_by)))
                    else:
                        log.warning(u'Ошибка типа параметра сортировки ORDER BY в функции поиска по полю <%s>' % type(order_by))

                search_result = None
                if sql is not None:
                    # print(sql)
                    search_result = sql.execute()

                if search_result:
                    result = [rec.cod for rec in search_result]
            except:
                log.warning(u'''При возникновении ошибки типа:
----------------------------------------------------------------------------------
DatabaseError: (psycopg2.DatabaseError) server closed the connection unexpectedly
This probably means the server terminated abnormally
before or while processing the request.
----------------------------------------------------------------------------------
Проблема скорее всего в локали БД. ILIKE не может корректно преобразовать 
русские буквы в другой регистр. Связь с БД рушится.
Для правильной работы ILIKE БД должна быть создана с такими параметрами:
ENCODING = 'UTF8'               (Кодировка)
LC_COLLATE = 'ru_RU.UTF-8'      (Сопоставление)
LC_CTYPE = 'ru_RU.UTF-8'        (Тип символа)''')
                log.fatal(u'Ошибка поиска в справочнике <%s> по полю <%s>' % (self.getSpravParent().getName(),
                                                                                   search_fieldname))
        return result

    def find_code(self, **field_values):
        """
        Поиск кода по нескольким полям.
        @param field_values: Словарь значений полей.
            Например:
                {
                    'name': u'ОАО "Рога и копыта"',
                    'inn': '1234567890',
                    ...
                }
            Поиск производиться на точное сравнение по <И>.
        @return: Список найденных кодов соответствующих искомому значению.
        """
        find_list = [getattr(self._tab.c, fieldname) == value for fieldname, value in field_values.items()]
        where = icsqlalchemy.and_(*find_list)
        return self.find_code_where(where)

    def find_code_where(self, where):
        """
        Поиск кода по нескольким условиям выборке SQLAlchemy.
        @param where: Условия выборки SQLAlchemy.
        @return: Список найденных кодов соответствующих искомому значению.
        """
        result = list()
        if self._tab:
            try:
                sql = self._tab.dataclass.select(where)
                find_result = sql.execute()

                if find_result:
                    result = [rec.cod for rec in find_result]
            except:
                log.fatal(u'Ошибка поиска в справочнике <%s>' % self.getSpravParent().getName())
        else:
            log.warning(u'Не определена таблица справочника <%s>' % self.getSpravParent().getName())
        return result
