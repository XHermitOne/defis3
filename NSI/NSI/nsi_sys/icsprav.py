#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс справочника.
"""

# Подключение библиотек
from ic.utils.coderror import *     # Коды ошибок
from ic.utils import coderror
from ic.utils import resource
from ic.utils import util
from ic.dlg import dlgfunc
from ic.utils import system_cache
from ic.log import log
from ic.engine import glob_functions

from ic.storage import storesrc

from ic.components import icwidget
from ic.components import icResourceParser

from . import icspravstorage
from NSI.nsi_dlg import icspraveditdlg
from NSI.nsi_dlg import icspravchoicetreedlg

# Версия
__version__ = (0, 1, 4, 1)

# Спецификация
SPC_IC_SPRAV = {'type': 'SpravDefault',
                'name': 'default',
                'description': '',      # Описание справочника
                'table': None,          # Паспорт таблицы храниения данных
                'db': None,             # Паспорт БД хранения данных
                'cache': True,          # Автоматически кэшировать?
                'is_tab_time': False,   # Есть ли у справочника таблица временных значений?
                'cache_frm': True,      # Автоматически кешировать формы?
                'choice_form': 'spravChoiceDlgStd',     # Форма для просмотра и выбора кода справочника
                'edit_form': 'spravEditDlgStd',         # Форма для редактирования справочника
                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'table': u'Паспорт таблицы храниения данных',
                                 'db': u'Паспорт БД хранения данных',
                                 'cache': u'Автоматически кэшировать?',
                                 'is_tab_time': u'Есть ли у справочника таблица временных значений?',
                                 'cache_frm': u'Автоматически кешировать формы?',
                                 'choice_form': u'Форма для просмотра и выбора кода справочника',
                                 'edit_form': u'Форма для редактирования справочника',
                                 },
                }


class icSpravInterface(object):
    """
    Класс абстрактного справочника.
        Реализует только интерфейс.
    """

    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.

        :param sprav_manager: Объект менеджера справочника.
        :param name: Имя справочника в списке менеджера справочников.
            Оно же и является типом справочника в таблице справочников.
        """
        self._sprav_manager = sprav_manager

        # if isinstance(name, unicode):
        #    name = name.encode()

        self._name = name

        # указание хранилища справочников
        self._storage = None

        # Текущий выбранный код
        self._cur_code = None
        # Предыдущий выбранный код
        self._prev_code = None

        # Кэш
        self._cache = system_cache.icCache()

    def getCache(self):
        """
        Кэш.
        """
        return self._cache

    def clearInCache(self):
        """
        Убрать справочник из кеша.
        """
        if self.getAutoCache():
            self.getCache().clear(self.getName())

    def getCachedRec(self, code):
        """
        Получить закешированную запись по коду.

        :param code: Код справочника.
        :return: Словарь записи.
        """
        if self._cache.hasObject(self.getName(), id=code):
            record = self._cache.get(classObj=self.getName(), id=code)
        else:
            storage = self.getStorage()
            record = storage.getRecByCod(code)
            self._cache.add(classObj=self.getName(), id=code, obj=record)
        return record

    def setCurCode(self, code):
        """
        Выбрать код.
        """
        self._prev_code = self._cur_code
        self._cur_code = code

    def getCurCode(self):
        """
        Текущий выбранный код.
        """
        return self._cur_code

    def getPrevCode(self):
        """
        Предыдущий выбранный код.
        """
        return self._prev_code

    def getSpravManager(self):
        """
        Менеджер справочника.
        """
        return self._sprav_manager

    def getName(self):
        """
        Имя/тип справочника.
        """
        return self._name

    def getType(self):
        """
        Имя/тип справочника.
        """
        return self._name

    def getRecordDict(self, record):
        """
        Преобразовать запись SQLObject в словарь.
            {'field1':value1,'field2':value2,...}.
        """
        return dict(record)

    def getRecordCount(self, rs):
        """
        Возвращает количество выбранных записей в объекте SelectResults после использования
        функции select(...). Функция написана для того, чтобы отвязаться от версии SQLObject -
        в версии 0.5 для определяния количества записей используется len(rs), в версии >= 0.6
        rs.count()

        :type rs: C{SQLObject.SelectResults}
        :param rs: Набор отобранных записей.
        """
        return rs.rowcount

    def getNsiStdClassName(self):
        """
        Возвращает имя класса, описывающего структуру стандартного справочников.
        """
        log.warning(u'Не определен метод getNsiStdClassName в <%s>' % self.__class__.__name__)
        return None

    def getNsiStdTClassName(self, name=None):
        """
        Возвращает имя класса, описывающего структуру справочника изменяемых во
            времени параметров. Это имя генерируется по имени класса справочника.

        :type name: C{string}
        :param name: Имя класса данных, для хранения справочников.
        """
        log.warning(u'Не определен метод getNsiStdTClassName в <%s>' % self.__class__.__name__)
        return None

    def getStorage(self):
        """
        Хранилище справочников.
        """
        if self._storage is None:
            self.createStorage()
        return self._storage

    def getTable(self):
        """
        Таблица справочника.

        :return: Объект таблицы справочника или None, если
            не возможно определеить таблицу.
        """
        storage = self.getStorage()
        if storage:
            try:
                return storage.getSpravTabClass()
            except:
                log.fatal(u'Не определена таблица для справочника <%s>' % self.getName())
        return None

    def createStorage(self, ShowMsg_=True):
        """
        Создать хранилище справочников.

        :param ShowMsg_: Признак отображения предупреждения о неправильно определенном хранилище.
        """
        db_name = self.getDBName()
        self._storage = None

        if db_name:
            path_res = None
            db_subsys = self.getDBResSubSysName()
            if db_subsys:
                path_res = resource.getSubsysPath(db_subsys)
                
            db_res = resource.icGetRes(db_name, ext='src',
                                       pathRes=path_res, nameRes=db_name)
            if db_res:
                try:
                    if db_res['type'] != storesrc.OBJ_STORAGE_SRC_TYPE:
                        # SQL-ная БД
                        self._storage = icspravstorage.icSpravSQLStorage(self,
                                                                         db_name, self.getTableName(),
                                                                         db_subsys=db_subsys,
                                                                         table_subsys=self.getTabResSubSysName())
                    elif db_res['type'] == storesrc.OBJ_STORAGE_SRC_TYPE:
                        # Объектная БД
                        from . import icodb_spravstorage
                        self._storage = icodb_spravstorage.icSpravODBStorage(self, db_name, self.getTableName())
                    else:
                        log.warning(u'Не определенный тип БД %s СПРАВОЧНИКА %s' % (db_res['type'],
                                                                                   self.getName()))
                except:
                    log.fatal(u'Ошибка создания хранилища справочников <%s>. Таблица <%s>' % (db_name,
                                                                                              self.getTableName()))
        else:
            # База данных не указана, поэтому считаем что по умолчанию
            # это SQL БД и таблица сама определяет в какой БД ей храниться
            # SQL-ная БД
            try:
                self._storage = icspravstorage.icSpravSQLStorage(parent_sprav=self, db_name=None,
                                                                 table_name=self.getTableName())
            except:
                log.fatal(u'Ошибка создания SQL хранилища справочника <%s>' % self.getName())

        if ShowMsg_ and not self._storage:
            dlgfunc.openMsgBox(u'ВНИМАНИЕ!', u'Не определено хранилище справочника: %s БД: %s Таблица: %s' % (self.getName(),
                                                                                                              db_name,
                                                                                                              self.getTableName()))
        return self._storage

    def getDBName(self):
        """
        Имя БД.
        """
        log.warning(u'Не определен метод getDBName в <%s>' % self.__class__.__name__)
        return None

    def getDBResSubSysName(self):
        """
        Имя подсистемы ресурса БД.
        """
        log.warning(u'Не определен метод getDBResSubSysName в <%s>' % self.__class__.__name__)
        return None
    
    def getTableName(self):
        """
        Имя объекта хранения/Таблицы.
        """
        log.warning(u'Не определен метод getTableName в <%s>' % self.__class__.__name__)
        return None

    def getTabResSubSysName(self):
        """
        Имя подсистемы ресурса таблицы.
        """
        log.warning(u'Не определен метод getTabResSubSysName в <%s>' % self.__class__.__name__)
        return None

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        log.warning(u'Не определен метод getDBPsp в <%s>' % self.__class__.__name__)
        return None

    def getTablePsp(self):
        """
        Паспорт объекта хранения/Таблицы.
        """
        log.warning(u'Не определен метод getTablePsp в <%s>' % self.__class__.__name__)
        return None

    def getDateTableName(self):
        """
        Имя объекта хранения/Таблицы временных значений.
        """
        log.warning(u'Не определен метод getDateTableName в <%s>' % self.__class__.__name__)
        return None

    def getAutoCache(self):
        """
        Признак автоматического кэширования.
        """
        log.warning(u'Не определен метод getAutoCache в <%s>' % self.__class__.__name__)
        return None

    def getAutoCacheFrm(self):
        """
        Признак автоматического кэширования форм.
        """
        log.warning(u'Не определен метод getAutoCacheFrm в <%s>' % self.__class__.__name__)
        return None

    def getChoiceFormName(self):
        """
        Форма для выбора данных справочника.
        """
        log.warning(u'Не определен метод getChoiceFormName в <%s>' % self.__class__.__name__)
        return None

    def getEditFormName(self):
        """
        Форма для редактирования данных справочника.
        """
        log.warning(u'Не определен метод getEditFormName в <%s>' % self.__class__.__name__)
        return None

    def getChoiceFormPsp(self):
        """
        Форма для выбора данных справочника.
        """
        log.warning(u'Не определен метод getChoiceFormPsp в <%s>' % self.__class__.__name__)
        return None

    def getEditFormPsp(self):
        """
        Форма для редактирования данных справочника.
        """
        log.warning(u'Не определен метод getEditFormPsp в <%s>' % self.__class__.__name__)
        return None

    def Clear(self, bAsk=False):
        """
        Очистить справочник от данных.

        :param bAsk: Спросить о подтверждении очистки справочника?
        """
        storage = self.getStorage()
        if storage:
            if bAsk:
                if dlgfunc.openAskBox(u'ВНИМАНИЕ!',
                                      u'Очистить справочник <%s> от всех данных?' % self.getName()):
                    return storage.clear()
            else:
                # Подтверждения не требуется - просто удалтиь
                return storage.clear()

    def isEmpty(self):
        """
        Проверка на пустой справочник.

        :return: True - справочник пустой, False - Есть данные.
        """
        storage = self.getStorage()
        if storage:
            return storage.is_empty()
        # Хранилище не определено
        log.warning(u'Не определено хранилище у справочника <%s>' % self.getName())
        # Считаем что справочник пустой
        return True

    def isTabTime(self):
        """
        Есть у справочника таблица временных параметров?.
        """
        log.warning(u'Не определен метод isTabTime в <%s>' % self.__class__.__name__)
        return True

    def isCod(self, cod):
        """
        Есть такой код в справочнике?

        :param cod: Код.
        """
        return self.getStorage().isCod(cod)

    def isActive(self, cod):
        """
        Проверка активности кода в справочнике?
        Если справочник не поддерживает признак активности,
        то считается что он всегда включен.

        :param cod: Код.
        :return: True - код активен / False - код выключен.
        """
        record = self.getStorage().getRecByCod(cod)
        if not record:
            # Если нет записи, то выключено
            return False
        # Проверяем значение поля активации
        # Если справочник не поддерживает признак активации, то считаем
        # что код всегда включен-------+
        #                    V         V
        return record.get('activate', True)

    def isSubCodes(self, cod):
        """
        Есть ли у указанного кода подкоды подуровней?

        :param cod: Код справочника.
        """
        storage = self.getStorage()
        if storage:
            recs = storage.getLevelTable(cod)
            return bool(recs)
        return False

    def addRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Добавить запись в справочник по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции True/False.
        """
        log.warning(u'Не определен метод addRec в <%s>' % self.getName())
        return False

    def delRec(self, cod, dt=None):
        """
        Удалить запись по коду.

        :param cod: Код.
        :param dt: Период актуальности.
        """
        return self.getStorage().delRecByCod(cod, dt)

    def getRec(self, cod, dt=None):
        """
        Получить запись по коду.

        :param cod: Код.
        :param dt: Период актуальности.
        """
        return self.getStorage().getRecByCod(cod, dt)

    def getDataTree(self):
        """
        Данные справочника в виде дерева.

        :return: Словарно-списковую структуру следующего формата:
            [
                {
                'name':Имя узла,
                'child':[...], Список словарей дочерних узлов
                '__record__': Данные, прикреплямые к узлу  в виде списка.
                },
                ...
            ]
            или None  в случае ошибки.
        """
        return self.getStorage().getLevelTree()

    def getFields(self, fields=None, cod=None):
        """
        Заполнение полей для возврата функцией Hlp/Choice.

        :param fields: Задает поле или группу полей, которые надо вернуть.
            Поля могут задаваться как имя одного поля в виде строки,
            так и как группы полей как словарь соответствий полей ключам
            или список имен полей.
        :param cod: Код записи таблицы данных.
        :return: Значение поля по коду или словарь заполненных
            полей.
        """
        res_val = None
        storage = self.getStorage()
        rec = storage.getRecByCod(cod)

        # Формируем словарь значений, которые необходимо вернуть
        if rec:
            if isinstance(fields, dict):
                res_val = dict()
                for key in fields.keys():
                    fld_sprav = fields[key]
                    res_val[key] = rec[fld_sprav]
            elif isinstance(fields, str):
                res_val = rec[fields]
            elif isinstance(fields, tuple) or isinstance(fields, list):
                res_val = dict([(field_name, rec[field_name]) for field_name in fields])

        return res_val

    def getLevelByIdx(self, index=-1):
        """
        Определить уровень по индексу.

        :param index: Индекс уровня.
        :return: Возвращает объект уровня или None в случае ошибки.
        """
        try:
            return self.getLevels()[index]
        except:
            log.fatal(u'СПРАВОЧНИК [%s] Ошибка определения уровня справочника по индексу' % self.name)
        return None

    def getLevelByCod(self, cod):
        """
        Определить уровень по коду.

        :param cod: Код в строковом представлении.
        :return: Объект уровня, соответствующего коду или None в случае ошибки.
        """
        if cod is None:
            log.warning(u'Не определен код для определения объекта уровня')
            return None
        levels = self.getLevels()
        for level in levels:
            cod = cod[level.getCodLen():]
            if not cod.strip():
                return level
        return None

    def Hlp(self, parent_code=(None,), field=None, form=None, parent=None, dt=None,
            default_selected_code=None, view_fields=None, search_fields=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного справочника.

        :type parent_code: C{...}
        :param parent_code: Код более верхнего уровня.
        :param field: Задает поле или группу полей, которые надо вернуть.
            Полу задается строкой. Поля задаются словарем.
        :param form: имя формы визуального интерфейса работы со справочником.
        :param parent: Родительская форма.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        :param view_fields: Список имен полей для просмотра.
            Если не определено то отображаются <Код> и <Наименование>.
        :param search_fields: Список имен полей для поиска.
            Если не определено то поиск только по <Код> и <Наименование>.
        :return: Код ошибки, Результат выбора
        """
        log.warning(u'Не определен метод Hlp в <%s>' % self.__class__.__name__)
        return None, None

    # Другое название метода
    Choice = Hlp

    def Edit(self, parent_code=(None,), parent=None):
        """
        Запуск окна редактирования справочника/перечисления.

        :param parent_code: Код более верхнего уровня.
        :param parent: Родительская форма.
            Если не определена, то берется главная форма.
        :return: Возвращает результат выполнения опереции True/False.
        """
        log.warning(u'Не определен метод Edit в <%s>' % self.__class__.__name__)
        return False

    def Ctrl(self, val, old=None, field='name', flds=None, bCount=True, cod='', dt=None):
        """
        Функция контроля наличия в справочнике значения поля
        с указанным значением.

        :type cod: C{string}
        :param cod: Начальная подстрока структурного кода, ограничивающая множество возможных кодов.
        :type val: C{...}
        :param val: Проверяемое значение. Если тип картеж, то это означает, что проверяем структурное
            значение (например иерархический код справочника).
        :type old: C{...}
        :param old: Старое значение.
        :type field: C{string}
        :param filed: Поле, по которому проверяется значение.
        :type flds: C{dictionary}
        :param flds: Словарь соответствий между полями определенного класса данных и
            полями справочника. Если контроль значения пройдет успешно, то
            соответствующие значения из справочника будут перенесены в поля класса
            данных. Пример: {'summa':'f1', 'summa2':'f2'}
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :type bCount: C{string}
        :param bCount: признак того, что необходимо вести количество ссылок.
        :rtype: C{int}
        :return: Код возврата функции контроля.
        """
        log.warning(u'Не определен метод Ctrl в <%s>' % self.__class__.__name__)
        return None

    def Find(self, cod, field='name', dt=None):
        """
        Поиск по коду.

        :type cod: C{...}
        :param cod: Код строки справочника.
        :type field: C{string | list }
        :param field: Имя поля или список полей.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :rtype: C{dictionary}
        :return: Значение либо словарь значений (если поле field задает список полей).
            None, если строка с заданным кодом не найдена.
        """
        log.warning(u'Не определен метод Find в <%s>' % self.__class__.__name__)
        return None

    def getParentLevelCod(self, cod):
        """
        Код родительского уровня.

        :param cod: Код.
        :return: Код родительского уровня.
        """
        return ''.join([subcode for subcode in self.StrCode2ListCode(cod) if bool(subcode)][:-1])

    def StrCode2ListCode(self, str_code):
        """
        Преобразовать строковый код в списковый код по уровням.

        :param str_code: Строковое представление кода.
        :param cod_encode: Однобайтовая кодировка кода.
        """
        if not str_code:
            return []

        levels = self.getLevels()
        list_cod = []
        for level in levels:
            subcod = str_code[:level.getCodLen()]
            list_cod.append(subcod)
            str_code = str_code[level.getCodLen():]
        return list_cod

    def ListCode2StrCode(self, list_code):
        """
        Преобразовать списковый код по уровням в строковый код.

        :param list_code: Списковое/кортежное представление кода.
        """
        return ''.join([cod for cod in list(list_code) if cod is not None])

    def getLevels(self):
        """
        Список уровней справочника.
        """
        log.warning(u'Не определен метод getLevels в <%s>' % self.__class__.__name__)
        return list()

    def findCodes(self, **field_values):
        """
        Поиск кода по нескольким полям.

        :param field_values: Словарь значений полей.
            Например:
                {
                    'name': u'ОАО "Рога и копыта"',
                    'inn': '1234567890',
                    ...
                }
            Поиск производиться на точное сравнение по <И>.
        :return: Список найденных кодов соответствующих искомому значению.
            Или None в случае ошибки.
        """
        storage = self.getStorage()
        if storage is not None:
            return storage.find_code(**field_values)
        else:
            log.warning(u'Не определено хранилище в справочнике <%s>' % self.getName())
        return None

    def choice_record(self, parent=None, *args, **kwargs):
        """
        Вызов выбора записи из справочника.

        :param parent: Родительская форма.
        :return: Выбранную запись или None в случае ошибки.
        """
        try:
            field_names = tuple(self.getStorage().getSpravFieldNames())
            fields = dict([(field_name, field_name) for field_name in field_names])
            result = self.Hlp(field=fields, parent=parent,
                              *args, **kwargs)
            if result[0] in (0, coderror.IC_HLP_OK):
                record = result[2]
                # Преобразуем запись в словарь
                # record = dict([(field_name, field_values[idx]) for idx, field_name in enumerate(field_names)])
                return record
            else:
                log.error(u'Ошибка выбора справочника <%s>. Результат %s' % (self.getName(), result))
        except:
            log.fatal(u'Ошибка выбора записи справочника <%s>' % self.getName())
        return None

    def choice_code(self, parent=None, *args, **kwargs):
        """
        Вызов выбора кода из справочника.

        :param parent: Родительская форма.
        :return: Выбранный код.
        """
        record = self.choice_record(parent, *args, **kwargs)
        if record and isinstance(record, dict):
            return record.get('cod', None)
        return None


class icSpravProto(icSpravInterface):
    """
    Класс справочника.
    """

    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.

        :param sprav_manager: Объект менеджера справочника.
        :param name: Имя справочника в списке менеджера справочников.
        """
        icSpravInterface.__init__(self, sprav_manager, name)

        # Параметры вызова функции hlp - нужно для формы
        self._hlp_param = None

    def get_hlp_param(self):
        return self._hlp_param

    def Hlp(self, parent_code=(None,), field=None, form=None, parent=None, dt=None,
            default_selected_code=None, view_fields=None, search_fields=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного справочника.

        :type parent_code: C{...}
        :param parent_code: Код более верхнего уровня.
        :param field: Задает поле или группу полей, которые надо вернуть.
            Полу задается строкой. Поля задаются словарем.
        :param form: имя формы визуального интерфейса работы со справочником.
        :param parent: Родительская форма.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        :param view_fields: Список имен полей для просмотра.
            Если не определено то отображаются <Код> и <Наименование>.
        :param search_fields: Список имен полей для поиска.
            Если не определено то поиск только по <Код> и <Наименование>.
        :return: Код ошибки, Результат выбора
        """
        result = IC_HLP_OK
        res_val = None

        try:
            if parent_code is None:
                parent_code = (None,)

            # Для обработки необходимо преобразовать в список
            parent_code = list(parent_code)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике

            if self.getLevelCount() <= x_level:
                log.warning(u'Не корректный номер уровня %d' % x_level)
                return IC_HLP_FAILED_LEVEL, res_val

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
                return IC_HLP_FAILED_LEVEL, res_val

            result = IC_HLP_FAILED

            # Определить форму выбора кода
            if form is None:
                form = self.getLevels()[x_level].getHelpFormName()

                # Если форма не определена в уровне, то
                # значит взять форму из описания справочник
                if form is None:
                    form = self.getChoiceFormName()

            if not form:
                # Форма выбора не определена
                # обработка штатной функцией
                code = icspravchoicetreedlg.choice_sprav_dlg(parent=parent,
                                                             nsi_sprav=self,
                                                             fields=view_fields,
                                                             default_selected_code=default_selected_code,
                                                             search_fields=search_fields)
                if code:
                    return IC_HLP_OK, code, self.getFields(field, code)
                return IC_HLP_FAILED_IGNORE, code, None

            # if form is None:
            #     ic_dlg.openMsgBox(u'ОШИБКА', u'Не определена форма выбора кода!')
            #     return False

            # Вывести окно и возвратить выбранный код
            self._hlp_param = {'sprav_code': parent_code,
                               'sprav_field': field,
                               }
            evsp = util.InitEvalSpace({'OBJ': self})
            # log.info('  .... begin:!!!!!')
            res_val = icResourceParser.ResultForm(form,
                                                  evalSpace=evsp,
                                                  parent=parent,
                                                  bBuff=self.getAutoCacheFrm(),
                                                  key=self.GetUUID()+'_'+self.ListCode2StrCode(parent_code))

            if res_val is None:
                # Нажали ESC
                result = IC_HLP_FAILED_IGNORE
            elif isinstance(res_val, (list, tuple)):
                return res_val
            else:
                result = IC_HLP_OK
        except:
            log.fatal(u'СПРАВОЧНИК [%s] Ошибка в методе Hlp' % self._name)
            result = IC_HLP_FAILED_TYPE_SPRAV

        return result, res_val, self.getFields(field, res_val)

    def Edit(self, parent_code=(None,), parent=None):
        """
        Запуск окна редактирования справочника/перечисления.

        :param parent_code: Код более верхнего уровня.
        :param parent: Родительская форма.
            Если не определена, то берется главная форма.
        :return: Возвращает результат выполнения опереции True/False.
        """
        if parent is None:
            parent = glob_functions.getMainWin()

        try:
            if parent_code is None:
                parent_code = (None,)

            # Для обработки необходимо преобразовать в список
            parent_code = list(parent_code)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)
            parent_code_str = ''.join(parent_code[:x_level])

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике
            if self.getLevelCount() <= x_level:
                log.warning(u'Не корректный номер уровня <%d>' % x_level)
                return False

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
                return False

            parent_len = len(parent_code_str)

            # Имя таблицы данных
            tab_name = self.getTableName()
            # Имя формы редактрования справочника/перечисления
            form = self.getLevels()[x_level].getEditFormName()
            # Если форма не определена в уровне, то
            # значит взять форму из описания справочник
            if form is None:
                form = self.getEditFormName()

            if not form:
                # Форма не определена
                return icspraveditdlg.edit_sprav_dlg(parent=parent,
                                                     nsi_sprav=self)
            # if form is None:
            #     ic_dlg.openMsgBox(u'ОШИБКА', u'Не определена форма редактирования уровня!')
            #     return False

            sql = '''SELECT id FROM %s
                WHERE SUBSTR(%s.cod,1,%d) LIKE(\'%s\') AND
                LENGTH(SUBSTR(%s.cod,%d,LENGTH(%s.cod)-%d))=%d''' % (tab_name,
                                                                     tab_name,
                                                                     parent_len,
                                                                     parent_code_str,
                                                                     tab_name,
                                                                     parent_len+1,
                                                                     tab_name,
                                                                     parent_len,
                                                                     level_len)

            # Инициализация пространства имен формы редактирования справочника
            evsp = util.InitEvalSpace({'OBJ': self})
            ok = icResourceParser.ResultForm(form,
                                             filter={tab_name: sql}, evalSpace=evsp, parent=parent,
                                             bBuff=self.getAutoCacheFrm(),
                                             key=self.GetUUID()+'_'+self.ListCode2StrCode(parent_code))

            return ok
        except:
            log.fatal(u'СПРАВОЧНИК [%s] Ошибка редактирования' % self.name)
            return False

    def Ctrl(self, val, old=None, field='name', flds=None, bCount=True, cod='', dt=None):
        """
        Функция контроля наличия в справочнике значения поля
        с указанным значением.

        :type cod: C{string}
        :param cod: Начальная подстрока структурного кода, ограничивающая множество возможных кодов.
        :type val: C{...}
        :param val: Проверяемое значение. Если тип картеж, то это означает, что проверяем структурное
            значение (например иерархический код справочника).
        :type old: C{...}
        :param old: Старое значение.
        :type field: C{string}
        :param filed: Поле, по которому проверяется значение.
        :type flds: C{dictionary}
        :param flds: Словарь соответствий между полями определенного класса данных и
            полями справочника. Если контроль значения пройдет успешно, то
            соответствующие значения из справочника будут перенесены в поля класса
            данных. Пример: {'summa':'f1', 'summa2':'f2'}
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :type bCount: C{string}
        :param bCount: признак того, что необходимо вести количество ссылок.
        :rtype: C{int}
        :return: Код возврата функции контроля.
        """
        result = coderror.IC_CTRL_OK
        res_val = None

        try:
            storage = self.getStorage()
            level_tab = storage.getLevelTable(cod, dt)
            # Список имен полей
            field_names = storage.getSpravFieldNames()
            # Словарь индексов
            field_indexes = dict([(field_name, i) for i, field_name in enumerate(field_names)])
            field_idx = field_indexes[field]

            # Перебор строк
            for rec in level_tab:
                if rec[field_idx] == val:
                    # Перебор полей
                    if flds and isinstance(flds, dict):
                        res_val = dict([(item[0], rec[field_indexes[item[1]]]) for item in flds.items()])
                    else:
                        res_val = None
                    # Нашли запись и заполнили выходной словарь
                    return result, res_val
            # Не найдено
            result = coderror.IC_CTRL_FAILED
            log.warning(u'Не найден код <%s> в справочнике <%s>' % (val, self.getName()))
        except:
            log.fatal(u'СПРАВОЧНИК [%s] Ошибка контроля' % self.name)
            result = coderror.IC_CTRL_FAILED_TYPE_SPRAV

        return result, res_val

    def Find(self, cod, field='name', dt=None):
        """
        Поиск по коду.

        :type cod: C{...}
        :param cod: Код строки справочника.
        :type field: C{string | list }
        :param field: Имя поля или список полей.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :rtype: C{dictionary}
        :return: Значение либо словарь значений (если поле field задает список полей).
            None, если строка с заданным кодом не найдена.
        """
        if isinstance(field, str):
            flds = [field]
            isRetDict = False
        else:
            flds = [x for x in field]
            isRetDict = True

        fldDict = {}

        #   Формируем словарь соотношений для функции контроля
        for x in flds:
            fldDict[x] = x

        #   Используем функцию для контроля. Она возвращает словарь значений.
        level_cod = self.getParentLevelCod(cod)
        ctrlCod, dict = self.Ctrl(cod, None, 'cod', fldDict, cod=level_cod, dt=dt)

        if ctrlCod != IC_CTRL_OK:
            ret = None
        elif isRetDict:
            ret = dict
        else:
            ret = dict[field]

        return ret

    def updateRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Обновить запись в справочнике по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции.
        """
        level = self.getLevelByCod(cod)
        if level:
            # Контроль на уровне
            update_ctrl_result = level.getUpdateCtrl(locals())
            if update_ctrl_result is None:
                # Контроля производить не надо
                return self._updateRec(cod, record_dict, dt, bClearCache)
            elif update_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._updateRec(cod, record_dict, dt, bClearCache)
            elif update_ctrl_result in (coderror.IC_CTRL_FAILED,
                                        coderror.IC_CTRL_FAILED_IGNORE,
                                        coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                        coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                log.warning(u'Не прошел контроль обновление/изменение записи в справочник [%s]. Код ошибки: <%d>' %
                                   (self.getName(), update_ctrl_result))

        return False

    def _updateRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Обновить запись в справочнике по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции.
        """
        storage = self.getStorage()
        if storage:
            result = storage.updateRecByCod(cod, record_dict, dt)
            # Если запись прошла удачно, то сбросить кэш
            if bClearCache:
                self.clearInChache()
            return result

        return False

    def addRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Добавить запись в справочник по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции True/False.
        """
        level = self.getLevelByCod(cod)
        if level:
            # Контроль на уровне
            add_ctrl_result = level.getAddCtrl(locals())
            if add_ctrl_result is None:
                # Контроля производить не надо
                return self._addRec(cod, record_dict, dt, bClearCache)
            elif add_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._addRec(cod, record_dict, dt, bClearCache)
            elif add_ctrl_result in (coderror.IC_CTRL_FAILED,
                                     coderror.IC_CTRL_FAILED_IGNORE,
                                     coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                     coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                log.warning(u'Не прошел контроль добавления записи в справочник [%s]. Код ошибки: <%d>' %
                            (self.getName(), add_ctrl_result))

        return False

    def _addRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Добавить запись в справочник по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции True/False.
        """
        storage = self.getStorage()
        if storage:
            if storage.isCod(cod):
                result = storage.updateRecByCod(cod, record_dict, dt)
            else:
                record_dict['cod'] = cod
                result = storage.addRecDictDataTab(record_dict)
            # Если запись прошла удачно, то сбросить кэш
            if bClearCache:
                self.clearInCache()
            return result

        return False

    def delRec(self, cod, dt=None):
        """
        Удалить запись по коду.

        :param cod: Код.
        :param dt: Период актуальности.
        """
        level = self.getLevelByCod(cod)
        if level:
            # Контроль на уровне
            del_ctrl_result = level.getDelCtrl(locals())
            if del_ctrl_result is None:
                # Контроля производить не надо
                return self._delRec(cod, dt)
            elif del_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._delRec(cod, dt)
            elif del_ctrl_result in (coderror.IC_CTRL_FAILED,
                                     coderror.IC_CTRL_FAILED_IGNORE,
                                     coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                     coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                log.warning(u'Не прошел контроль удаления записи в справочник [%s]. Код ошибки: <%d>' %
                                   (self.getName(), del_ctrl_result))

        return False

    def _delRec(self, cod, dt=None):
        """
        Удалить запись по коду.

        :param cod: Код.
        :param dt: Период актуальности.
        """
        return self.getStorage().delRecByCod(cod, dt)

    def getLevelRefSpravByCod(self, cod=None):
        """
        Получить объект справочника, связанного с уровнем.
        """
        if not cod:
            # Если это рут, то вернуть первый уровень
            level = self.getLevelByCod(cod)
        else:
            # Если это первый(второй,...) то вернуть следующий уровень
            level = self.getLevelByCod(cod).getNext()
        if level:
            ref_sprav_name = level.getRefSprav()
            if ref_sprav_name:
                sprav_manager = self.getSpravManager()
                return sprav_manager.getSpravByName(ref_sprav_name)
        return None

    def _get_refspr_parent_cod(self, parent_cod):
        """
        Определяет родительский код связанного справочника.

        :param parent_cod: Родительский код текущего справочника.
        """
        ref_sprav = self.getLevelRefSpravByCod(parent_cod)
        lev = self.getLevelByCod(parent_cod).getNext()
        cod_lst = []
        if lev:
            cod_lst = self.StrCode2ListCode(parent_cod)
            # определяем часть кода, которая относится к связанному справочнику
            rl = lev.getRefLevel()+1
            ix = lev.getIndex()+1
            beg = ix - rl
            old = cod_lst
            cod_lst = [el for el in cod_lst[beg:ix] if el]
        return cod_lst

    def gen_precod(self, cod, default_lst=None):
        """
        Генерирут строки родительских кодов.

        :param cod: Код.
        :param default_lst: Список словарей (для каждого уровня) значений полей.
        """
        lst = self.StrCode2ListCode(cod)
        default_lst = default_lst or []
        prnt_cod = ''
        for indx, cd in enumerate(lst[:-1]):
            if not self.isCod(prnt_cod+cd):
                if indx < len(default_lst):
                    df = default_lst[indx]
                else:
                    df = {'name': cd}
                    lev = self.getLevels()[indx]
                    ref = lev.getRefSprav()
                    mngr = self.getSpravManager()
                    ref_sprav = mngr.getSpravByName(ref)
                    if ref and not ref_sprav:
                        log.warning(u'Не найдена ссылка на справочник <%s>' % ref)
                        # raise
                    if ref_sprav:
                        try:
                            ref_prnt_cod = ''.join(self._get_refspr_parent_cod(prnt_cod))
                            ref_cod = ref_prnt_cod + cd
                            name = ref_sprav.Find(ref_cod)
                            df = {'name': name}
                        except:
                            log.fatal(u'Ошибка поиска <name> в ссылочном справочнике')
                    else:
                        df = {'name': cd}

                self.addRec(prnt_cod+cd, df)
            prnt_cod += cd

    def getUUIDByCod(self, cod):
        """
        Получить уникальный идентификатор по коду.
        """
        storage = self.getStorage()
        if storage:
            return storage.getUUIDByCod(cod)
        log.warning(u'У объекта справочника [%s] не определено хранилище.' % self.getName())
        return None
