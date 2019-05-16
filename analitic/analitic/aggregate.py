#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Подсистема агригирования данных из основной таблицы по уровням нашего хранилища.
"""

# --- Подключение библиотек ---
from ic.storage import storesrc

from ic.utils import ic_file
from ic.log import log


# Версия
__version__ = (0, 1, 1, 1)

# --- Константы ---
# AGGREGATE_INI_DEFAULT='./analitic/aggregate.ini'


# --- Классы ---
class icAnaliticAggregate:
    """
    Подсистема агригирования данных из основной таблицы по уровням нашего хранилища.
    """
    def __init__(self, MetaTree_=None): #,AggregateINIFileName_=AGGREGATE_INI_DEFAULT):
        """
        Конструктор.
        """
        # Метадерево описания хранилища
        self._metatree = MetaTree_

        # ОБъектное хранилище агрегированных данных
        self._odb_storage = None
        if self._metatree:
            self._odb_storage = self._metatree.getStorage()

        # Текущий заполняемый файл. Нужен для внутренней работы
        self.__cur_file_storage = None
        self.__cur_file_data = None

        # Таблица-источник данных
        # self._source_tab=None

        # Конфигурация подсистемы агрегирования
        self._aggregate_ctrl = None     # ic_ini.Ini2Dict(ic_file.AbsolutePath(AggregateINIFileName_))
        if self._metatree:
            self._aggregate_ctrl = self.createAggregateCtrl(self._metatree)

    def createAggregateCtrl(self, MetaTree_):
        """
        Создать по метадереву структуру управления агрегированием.
        @param MetaTree_: Метадерево.
        """
        data_ctrl = MetaTree_.value.aggregate_ctrl
        return data_ctrl

    def initODBStroage(self, ODBStorage_):
        """
        Инициализация хранилища агрегированных данных.
        """
        self._odb_storage = storesrc.icObjStorageSrc(ODBStorage_)

    def initSourceTab(self, SourceTab_):
        """
        Инициализация таблицы-источника данных.
        """
        source_tab = ic_sqlobjtab.icSQLObjTabClass(SourceTab_)
        return source_tab

    def runDeliverSumm(self):
        """
        Запуск разноса сумм.
        """
        if not self._aggregate_ctrl:
            log.warning(u'Не определена конфигурация <%s>' % self._aggregate_ctrl)
            return False

        # Перебрать таблицы-источники
        source_tabs = dict(map(lambda src_tab_name: (src_tab_name, self.initSourceTab(src_tab_name)),
                           self._aggregate_ctrl.keys()))
        for source_tab_name, source_tab in source_tabs.items():
            # Получить запрос преобразования
            src_query = self._aggregate_ctrl[source_tab_name]['source_query']
            # Получиь путь разноса суммы
            summa_path = self._aggregate_ctrl[source_tab_name]['summa_path']
            # Получить список флагов разноса суммы по датам
            date_flags = self._aggregate_ctrl[source_tab_name]['date_flags']
            # Разносимые поля
            aggregate_fields = self._aggregate_ctrl[source_tab_name]['aggregate_fields']
            # Поле даты
            date_field = self._aggregate_ctrl[source_tab_name]['date_field']

            # Перебор записей в таблице-источнике
            recs = source_tab.execute(src_query)
            for rec in recs:
                # Определить разносимые суммы
                aggregate_values = dict(map(lambda field: (field, getattr(rec, field)),
                                        aggregate_fields))
                # Определить дату
                date_value = getattr(rec, date_field)
                # Получить путь для разноса сумм
                value_path = map(lambda field: getattr(rec, field), summa_path)
                # Разнести суммы
                self._deliverSumm(value_path, source_tab_name,
                                  aggregate_values, date_value, date_flags)

    def _deliverSumm(self, Path_, Name_, IterateSumm_, Date_, DateFlags_,
                     CurStorageNode_=None):
        """
        Разнести суммы в хранилище.
        @param Path_: Путь по которому необходимо разнести.
        @param Name_: Имя под которым нужно разнести.
        @param IterateSumm_: Добавочные значения.
        @param Date_: Дата.
        @param DateFlags_: Флаги разноса сумм по датам.
        @param CurStorageNode_: Текущий узел хранилища, в который происходит разнос.
        """
        if CurStorageNode_ is None:
            CurStorageNode_ = self._odb_storage

        if CurStorageNode_:
            if issubclass(CurStorageNode_.__class__, storesrc.icDirStorage):
                # Это каталог и буфферизацию производить не надо
                property = CurStorageNode_.getProperty()
                property = self.__do_deliverSumm(property, Name_, IterateSumm_)
                # Разнос сумм по датам
                if DateFlags_[0]:
                    if not property.has_key(Date_):
                        property[Date_] = {}
                    property[Date_] = self.__do_deliverSumm(property[Date_], Name_, IterateSumm_)

                CurStorageNode_.setProperty(property)

                # Рекурсивный разнос сумм
                if Path_:
                    self._deliverSumm(Path_[1:], Name_, IterateSumm_, Date_, DateFlags_[1:],
                                      CurStorageNode_[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True

            elif issubclass(CurStorageNode_.__class__, storesrc.icFileStorage):
                # Это файл и надо произвести буферизацию
                if self.__cur_file_storage is None:
                    self.__cur_file_storage = CurStorageNode_
                    self.__cur_file_data = self.__cur_file_storag.getData()
                elif self.__cur_file_storage != CurStorageNode_:
                    # Сначала сбросить данные в предыдущий файл
                    self.__cur_file_storage.save(self.__cur_file_data)
                    # Затем запомнить новый файл
                    self.__cur_file_storage = CurStorageNode_
                    self.__cur_file_data = self.__cur_file_storag.getData()

                self.__cur_file_data['property'] = self.__do_deliverSumm(self.__cur_file_data['property'],
                                                                         Name_, IterateSumm_)

                # Разнос сумм по датам
                if DateFlags_[0]:
                    if not self.__cur_file_data['property'].has_key(Date_):
                        self.__cur_file_data['property'][Date_] = {}
                    self.__cur_file_data['property'][Date_] = self.__do_deliverSumm(self.__cur_file_data['property'][Date_],
                                                                                    Name_, IterateSumm_)

                # Рекурсивный разнос сумм
                if Path_:
                    self._deliverSumm(Path_[1:], Name_, IterateSumm_, Date_, DateFlags_[1:],
                                      self.__cur_file_data[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True

            elif isinstance(CurStorageNode_, dict):
                # Это узел файла
                CurStorageNode_['property'] = self.__do_deliverSumm(CurStorageNode_['property'],
                                                                    Name_, IterateSumm_)

                # Разнос сумм по датам
                if DateFlags_[0]:
                    if not CurStorageNode_['property'].has_key(Date_):
                        CurStorageNode_['property'][Date_] = {}
                    CurStorageNode_['property'][Date_] = self.__do_deliverSumm(CurStorageNode_['property'][Date_],
                                                                               Name_, IterateSumm_)

                # Рекурсивный разнос сумм
                if Path_:
                    self._deliverSumm(Path_[1:], Name_, IterateSumm_, Date_, DateFlags_[1:],
                                      CurStorageNode_[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True
        return False

    def __do_deliverSumm(self, Property_, Name_, IterateSumm_):
        """
        Выполнить разнос суммы в свойстве узла.
        """
        if not Property_.has_key(Name_):
            Property_[Name_] = IterateSumm_
        else:
            Property_[Name_] = dict(map(lambda item: (item[0], item[1] + IterateSumm_[item[0]]),
                                        Property_[Name_].items()))
        return Property_

    def runZeroSumm(self):
        """
        Запуск обнуления сумм.
        """
        if not self._aggregate_ctrl:
            log.warning(u'Не определена конфигурация <%s>' % self._aggregate_ctrl)
            return False

        # Перебрать таблицы-источники
        source_tabs = dict(map(lambda src_tab_name: (src_tab_name, self.initSourceTab(src_tab_name)),
                               self._aggregate_ctrl.keys()))
        for source_tab_name, source_tab in source_tabs.items():
            # Получить запрос преобразования
            src_query = self._aggregate_ctrl[source_tab_name]['source_query']
            # Получиь путь разноса суммы
            summa_path = self._aggregate_ctrl[source_tab_name]['summa_path']
            # Получить список флагов разноса суммы по датам
            date_flags = self._aggregate_ctrl[source_tab_name]['date_flags']
            # Разносимые поля
            aggregate_fields = self._aggregate_ctrl[source_tab_name]['aggregate_fields']
            # Поле даты
            date_field = self._aggregate_ctrl[source_tab_name]['date_field']

            # Перебор записей в таблице-источнике
            recs = source_tab.execute(src_query)
            for rec in recs:
                # Определить разносимые суммы
                aggregate_values = dict(map(lambda field: (field, getattr(rec, field)),
                                            aggregate_fields))
                # Определить дату
                date_value = getattr(rec, date_field)
                # Получить путь для разноса сумм
                value_path = map(lambda field: getattr(rec, field), summa_path)
                # Разнести суммы
                self._zeroSumm(value_path, source_tab_name,
                               aggregate_values, date_value, date_flags)

    def __setSumm(self, Property_, Name_, Summ_):
        """
        Установка суммы в свойстве узла.
        """
        if not Property_.has_key(Name_):
            Property_[Name_] = Summ_
        return Property_

    def _initSumm(self, Path_, Name_, Summ_, Date_, DateFlags_,
                  CurStorageNode_=None):
        """
        Обнулить суммы в хранилище.
        @param Path_: Путь по которому необходимо разнести.
        @param Name_: Имя под которым нужно разнести.
        @param Summ_: Сумма.
        @param Date_: Дата.
        @param DateFlags_: Флаги разноса сумм по датам.
        @param CurStorageNode_: Текущий узел хранилища, в который происходит разнос.
        """
        if CurStorageNode_ is None:
            CurStorageNode_ = self._odb_storage

        if CurStorageNode_:
            if issubclass(CurStorageNode_.__class__, storesrc.icDirStorage):
                # Это каталог и буфферизацию производить не надо
                property = CurStorageNode_.getProperty()
                property = self.__setSumm(property, Name_, Summ_)
                #Разнос сумм по датам
                if DateFlags_[0]:
                    if not property.has_key(Date_):
                        property[Date_] = {}
                    property[Date_] = self.__setSumm(property[Date_], Name_, Summ_)

                CurStorageNode_.setProperty(property)

                # Рекурсивный разнос сумм
                if Path_:
                    self._initSumm(Path_[1:], Name_, Summ_, Date_, DateFlags_[1:],
                                   CurStorageNode_[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True

            elif issubclass(CurStorageNode_.__class__, storesrc.icFileStorage):
                #Это файл и надо произвести буферизацию
                if self.__cur_file_storage is None:
                    self.__cur_file_storage = CurStorageNode_
                    self.__cur_file_data = self.__cur_file_storag.getData()
                elif self.__cur_file_storage != CurStorageNode_:
                    # Сначала сбросить данные в предыдущий файл
                    self.__cur_file_storage.save(self.__cur_file_data)
                    # Затем запомнить новый файл
                    self.__cur_file_storage = CurStorageNode_
                    self.__cur_file_data = self.__cur_file_storag.getData()

                self.__cur_file_data['property'] = self.__setSumm(self.__cur_file_data['property'],
                                                                  Name_, Summ_)

                # Разнос сумм по датам
                if DateFlags_[0]:
                    if not self.__cur_file_data['property'].has_key(Date_):
                        self.__cur_file_data['property'][Date_] = {}
                    self.__cur_file_data['property'][Date_] = self.__setSumm(self.__cur_file_data['property'][Date_],
                                                                             Name_, Summ_)

                # Рекурсивный разнос сумм
                if Path_:
                    self._initSumm(Path_[1:], Name_, Summ_, Date_, DateFlags_[1:],
                                   self.__cur_file_data[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True

            elif isinstance(CurStorageNode_, dict):
                # Это узел файла
                CurStorageNode_['property'] = self.__setSumm(CurStorageNode_['property'],
                                                             Name_, Summ_)

                # Разнос сумм по датам
                if DateFlags_[0]:
                    if not CurStorageNode_['property'].has_key(Date_):
                        CurStorageNode_['property'][Date_] = {}
                    CurStorageNode_['property'][Date_] = self.__setSumm(CurStorageNode_['property'][Date_],
                                                                        Name_, Summ_)

                # Рекурсивный разнос сумм
                if Path_:
                    self._initSumm(Path_[1:], Name_, Summ_, Date_, DateFlags_[1:],
                                   CurStorageNode_[Path_[0]])
                else:
                    # Сбросить и выйти
                    if self.__cur_file_storage:
                        self.__cur_file_storage.save(self.__cur_file_data)
                    return True
        return False
