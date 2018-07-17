#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс справочника.
"""

# Подключение библиотек
from ic.utils.coderror import *     # Коды ошибок
from ic.utils import coderror
from ic.utils import resource
from ic.utils import util
from ic.dlg import ic_dlg
from ic.utils import ic_cache

from ic.storage import storesrc

from ic.components import icwidget
from ic.components import icResourceParser

from ic.engine import ic_user
from ic.kernel import io_prnt
from . import icspravstorage
from NSI.nsi_dlg import icspraveditdlg
from NSI.nsi_dlg import icspravchoicetreedlg

# Версия
__version__ = (0, 0, 1, 4)

# Спецификация
SPC_IC_SPRAV = {'type': 'SpravDefault',
                'name': 'default',
                'description': '',      # Описание справочника
                'table': None,          # Имя таблицы храниения данных
                'db': None,             # Имя БД хранения данных
                'cache': True,          # Автоматически кэшировать?
                'is_tab_time': False,   # Есть ли у справочника таблица временных значений?
                'cache_frm': True,      # Автоматически кешировать формы?
                'choice_form': 'spravChoiceDlgStd',     # Форма для просмотра и выбора кода справочника
                'edit_form': 'spravEditDlgStd',         # Форма для редактирования справочника
                '__parent__': icwidget.SPC_IC_SIMPLE,
                }


class icSpravInterface:
    """
    Класс абстрактного справочника.
        Реализует только интерфейс.
    """

    def __init__(self, SpravManager_=None, Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя справочника в списке менеджера справочников.
            Оно же и является типом справочника в таблице справочников.
        """
        self._sprav_manager = SpravManager_

        if isinstance(Name_, unicode):
            Name_ = Name_.encode()

        self._name = Name_

        # указание хранилища справочников
        self._storage = None

        # Текущий выбранный код
        self._cur_code = None
        # Предыдущий выбранный код
        self._prev_code = None

    def setCurCode(self, Code_):
        """
        Выбрать код.
        """
        self._prev_code = self._cur_code
        self._cur_code = Code_

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

    def GetRecordDict(self, Record_):
        """
        Преобразовать запись SQLObject в словарь.
            {'field1':value1,'field2':value2,...}.
        """
        return dict(Record_)

    def GetRecordCount(self, rs):
        """
        Возвращает количество выбранных записей в объекте SelectResults после использования
        функции select(...). Функция написана для того, чтобы отвязаться от версии SQLObject -
        в версии 0.5 для определяния количества записей используется len(rs), в версии >= 0.6
        rs.count()

        @type rs: C{SQLObject.SelectResults}
        @param rs: Набор отобранных записей.
        """
        return rs.rowcount

    def getNsiStdClassName(self):
        """
        Возвращает имя класса, описывающего структуру стандартного справочников.
        """
        return None

    def getNsiStdTClassName(self, name=None):
        """
        Возвращает имя класса, описывающего структуру справочника изменяемых во
            времени параметров. Это имя генерируется по имени класса справочника.

        @type name: C{string}
        @param name: Имя класса данных, для хранения справочников.
        """
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
        @return: Объект таблицы справочника или None, если
            не возможно определеить таблицу.
        """
        storage = self.getStorage()
        if storage:
            try:
                return storage.getSpravTabClass()
            except:
                io_prnt.outWarning(u'Не определена таблица для справочника <%s>' % self.getName())
        return None

    def createStorage(self, ShowMsg_=True):
        """
        Создать хранилище справочников.
        @param ShowMsg_: Признак отображения предупреждения о неправильно определенном хранилище.
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
                                                                         DBSubSys_=db_subsys,
                                                                         TabSubSys_=self.getTabResSubSysName())
                    elif db_res['type'] == storesrc.OBJ_STORAGE_SRC_TYPE:
                        # Объектная БД
                        from . import icodb_spravstorage
                        self._storage = icodb_spravstorage.icSpravODBStorage(self, db_name, self.getTableName())
                    else:
                        io_prnt.outWarning(u'ОШИБКА! Не определенный тип БД %s СПРАВОЧНИКА %s' % (db_res['type'], self.getName()))
                except:
                    io_prnt.outErr(u'Ошибка создания хранилища справочников %s %s' % (db_name, self.getTableName()))
        else:
            # База данных не указана, поэтому считаем что по умолчанию
            # это SQL БД и таблица сама определяет в какой БД ей храниться
            # SQL-ная БД
            self._storage = icspravstorage.icSpravSQLStorage(self, None, self.getTableName())

        if ShowMsg_ and not self._storage:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Не определено хранилище справочника: %s БД: %s Таблица: %s' % (self.getName(),
                                                                                                           db_name,
                                                                                                           self.getTableName()))
        return self._storage

    def getDBName(self):
        """
        Имя БД.
        """
        return None

    def getDBResSubSysName(self):
        """
        Имя подсистемы ресурса БД.
        """
        return None
    
    def getTableName(self):
        """
        Имя объекта хранения/Таблицы.
        """
        return None

    def getTabResSubSysName(self):
        """
        Имя подсистемы ресурса таблицы.
        """
        return None

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return None

    def getTablePsp(self):
        """
        Паспорт объекта хранения/Таблицы.
        """
        return None

    def getDateTableName(self):
        """
        Имя объекта хранения/Таблицы временных значений.
        """
        return None

    def getAutoCache(self):
        """
        Признак автоматического кэширования.
        """
        return None

    def getAutoCacheFrm(self):
        """
        Признак автоматического кэширования форм.
        """
        return None

    def getChoiceFormName(self):
        """
        Форма для выбора данных справочника.
        """
        return None

    def getEditFormName(self):
        """
        Форма для редактирования данных справочника.
        """
        return None

    def getChoiceFormPsp(self):
        """
        Форма для выбора данных справочника.
        """
        return None

    def getEditFormPsp(self):
        """
        Форма для редактирования данных справочника.
        """
        return None

    def Clear(self, Ask_=False):
        """
        Очистить справочник от данных.
        @param Ask_: Спросить о подтверждении очистки справочника?
        """
        storage = self.getStorage()
        if storage:
            if Ask_:
                if ic_dlg.icAskBox(u'ВНИМАНИЕ!',
                                   u'Очистить справочник <%s> от всех данных?' % self.getName()):
                    return storage.clear()
            else:
                # Подтверждения не требуется - просто удалтиь
                return storage.clear()

    def isEmpty(self):
        """
        Проверка на пустой справочник.
        @return: True - справочник пустой, False - Есть данные.
        """
        storage = self.getStorage()
        if storage:
            return storage.is_empty()
        # Хранилище не определено
        # Считаем что справочник пустой
        return True

    def isTabTime(self):
        """
        Есть у справочника таблица временных параметров?.
        """
        return True

    def isCod(self, Cod_):
        """
        Есть такой код в справочнике?
        @param Cod_: Код.
        """
        return self.getStorage().isCod(Cod_)

    def delRec(self, Cod_, DateTime_=None):
        """
        Удалить запись по коду.
        @param Cod_: Код.
        @param DateTime_: Период актуальности.
        """
        return self.getStorage().delRecByCod(Cod_, DateTime_)

    def getRec(self, Cod_, DateTime_=None):
        """
        Получить запись по коду.
        @param Cod_: Код.
        @param DateTime_: Период актуальности.
        """
        return self.getStorage().getRecByCod(Cod_, DateTime_)

    def getDataTree(self):
        """
        Данные справочника в виде дерева.
        @return: Словарно-списковую структуру следующего формата:
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


class icSpravPrototype(icSpravInterface):
    """
    Класс справочника.
    """

    def __init__(self, SpravManager_=None, Name_=None):
        """
        Конструктор.
        @param SpravManager_: Объект менеджера справочника.
        @param Name_: Имя справочника в списке менеджера справочников.
        """
        icSpravInterface.__init__(self, SpravManager_, Name_)

        # Кэш
        self._cache = ic_cache.icCache()
        # Параметры вызова функции hlp - нужно для формы
        self._hlp_param = None

    def get_hlp_param(self):
        return self._hlp_param

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

    def Hlp(self, ParentCode=(None,), field=None, form=None, parentForm=None, DateTime_=None,
            default_selected_code=None, view_fields=None, search_fields=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного справочника.
        @type ParentCode: C{...}
        @param ParentCode: Код более верхнего уровня.
        @param field: Задает поле или группу полей, которые надо вернуть.
            Полу задается строкой. Поля задаются словарем.
        @param form: имя формы визуального интерфейса работы со справочником.
        @param parentForm: Родительская форма.
        @type DateTime_: C{string}
        @param DateTime_: Время актуальности кода.
        @param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        @param view_fields: Список имен полей для просмотра.
            Если не определено то отображаются <Код> и <Наименование>.
        @param search_fields: Список имен полей для поиска.
            Если не определено то поиск только по <Код> и <Наименование>.
        @return: Код ошибки, Результат выбора
        """
        result = IC_HLP_OK
        res_val = None

        try:
            if ParentCode is None:
                ParentCode = (None, )

            # Для обработки необходимо преобразовать в список
            parent_code = list(ParentCode)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике

            if self.getLevelCount() <= x_level:
                io_prnt.outWarning(u'Не корректный номер уровня %d' % x_level)
                return IC_HLP_FAILED_LEVEL, res_val

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                ic_dlg.icMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
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
                code = icspravchoicetreedlg.choice_sprav_dlg(parent=parentForm,
                                                             nsi_sprav=self,
                                                             fields=view_fields,
                                                             default_selected_code=default_selected_code,
                                                             search_fields=search_fields)
                if code:
                    return IC_HLP_OK, code, self.getFields(field, code)
                return IC_HLP_FAILED_IGNORE, code, None

            # if form is None:
            #     ic_dlg.icMsgBox(u'ОШИБКА', u'Не определена форма выбора кода!')
            #     return False

            # Вывести окно и возвратить выбранный код
            self._hlp_param = {'sprav_code': parent_code,
                               'sprav_field': field,
                               }
            evsp = util.InitEvalSpace({'OBJ': self})
            io_prnt.outLog('  .... begin:!!!!!')
            res_val = icResourceParser.ResultForm(form,
                                                  evalSpace=evsp,
                                                  parent=parentForm,
                                                  bBuff=self.getAutoCacheFrm(),
                                                  key=self.GetUUID()+'_'+self.ListCode2StrCode(parent_code))

            if res_val is None:
                # Нажали ESC
                result = IC_HLP_FAILED_IGNORE
            elif type(res_val) in (list, tuple):
                return res_val
            else:
                result = IC_HLP_OK
        except:
            io_prnt.outErr(u'СПРАВОЧНИК [%s] Ошибка в методе Hlp' % self._name)
            result = IC_HLP_FAILED_TYPE_SPRAV

        return result, res_val, self.getFields(field, res_val)

    # Другое название метода (я считаю что более правильное)
    Choice = Hlp

    def choice_record(self, parent=None, *args, **kwargs):
        """
        Вызов выбора записи из справочника.
        @param parent: Родительская форма.
        @return: Выбранную запись или None в случае ошибки.
        """
        try:
            field_names = tuple(self.getStorage().getSpravFieldNames())
            fields = dict([(field_name, field_name) for field_name in field_names])
            result = self.Hlp(field=fields, parentForm=parent,
                              *args, **kwargs)
            if result[0] in (0, coderror.IC_HLP_OK):
                record = result[2]
                # Преобразуем запись в словарь
                # record = dict([(field_name, field_values[i]) for i, field_name in enumerate(field_names)])
                return record
            else:
                io_prnt.outErr(u'Ошибка выбора справочника <%s>. Результат %s' % (self.getName(), result))
        except:
            io_prnt.outErr(u'Ошибка выбора записи справочника <%s>' % self.getName())
        return None

    def choice_code(self, parent=None, *args, **kwargs):
        """
        Вызов выбора кода из справочника.
        @param parent: Родительская форма.
        @return: Выбранный код.
        """
        record = self.choice_record(parent, *args, **kwargs)
        if record and isinstance(record, dict):
            return record.get('cod', None)
        return None

    def getFields(self, Fields_=None, Cod_=None):
        """
        Заполнение полей для возврата функцией Hlp().
        @param Fields_: Задает поле или группу полей, которые надо вернуть.
            Поля могут задаваться как имя одного поля в виде строки,
            так и как группы полей как словарь соответствий полей ключам
            или список имен полей.
        @param Cod_: Код записи таблицы данных.
        @return: Значение поля по коду или словарь заполненных
            полей.
        """
        res_val = None
        storage = self.getStorage()
        rec = storage.getRecByCod(Cod_)

        #   Формируем словарь значений, которые необходимо вернуть
        if rec:
            if isinstance(Fields_, dict):
                res_val = dict()
                for key in Fields_.keys():
                    fld_sprav = Fields_[key]
                    res_val[key] = rec[fld_sprav]
            elif type(Fields_) in (str, unicode):
                res_val = rec[Fields_]
            elif isinstance(Fields_, tuple) or isinstance(Fields_, list):
                res_val = dict([(field_name, rec[field_name]) for field_name in Fields_])

        return res_val

    def getLevelByCod(self, Cod_):
        """
        Определить уровень по коду.
        @param Cod_: Код в строковом представлении.
        """
        if Cod_ is None:
            return None
        levels = self.getLevels()
        for level in levels:
            Cod_ = Cod_[level.getCodLen():]
            if not Cod_.strip():
                return level
        return None

    def getLevelByIdx(self, Index_=-1):
        """
        Определить уровень по индексу.
        @param Index_: Индекс уровня.
        @return: Возвращает объект уровня или None в случае ошибки.
        """
        try:
            return self.getLevels()[Index_]
        except:
            io_prnt.outErr(u'СПРАВОЧНИК [%s] Ошибка определения уровня справочника по индексу' % self.name)
            return None

    def Edit(self, ParentCode_=(None,), ParentForm_=None):
        """
        Запуск окна редактирования справочника/перечисления.
        @param ParentCode: Код более верхнего уровня.
        @param ParentForm_: Родительская форма.
        @return: Возвращает результат выполнения опереции True/False.
        """
        try:
            if ParentCode_ is None:
                ParentCode_ = (None, )

            # Для обработки необходимо преобразовать в список
            parent_code = list(ParentCode_)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)
            parent_code_str = ''.join(parent_code[:x_level])

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике
            if self.getLevelCount() <= x_level:
                io_prnt.outWarning(u'Не корректный номер уровня <%d>' % x_level)
                return False

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                ic_dlg.icMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
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
                return icspraveditdlg.edit_sprav_dlg(parent=ParentForm_,
                                                     nsi_sprav=self)
            # if form is None:
            #     ic_dlg.icMsgBox(u'ОШИБКА', u'Не определена форма редактирования уровня!')
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
                                             filter={tab_name: sql}, evalSpace=evsp, parent=ParentForm_,
                                             bBuff=self.getAutoCacheFrm(),
                                             key=self.GetUUID()+'_'+self.ListCode2StrCode(parent_code))

            return ok
        except:
            io_prnt.outErr(u'СПРАВОЧНИК [%s] Ошибка редактирования' % self.name)
            return False

    def Ctrl(self, val, old=None, field='name', flds=None, bCount=True, cod='', DateTime_=None):
        """
        Функция контроля наличия в справочнике значения поля с указанным значением.
        @type cod: C{string}
        @param cod: Начальная подстрока структурного кода, ограничивающая множество возможных кодов.
        @type val: C{...}
        @param val: Проверяемое значение. Если тип картеж, то это означает, что проверяем структурное
            значение (например иерархический код справочника).
        @type old: C{...}
        @param old: Старое значение.
        @type field: C{string}
        @param filed: Поле, по которому проверяется значение.
        @type flds: C{dictionary}
        @param flds: Словарь соответствий между полями определенного класса данных и
            полями справочника. Если контроль значения пройдет успешно, то
            соответствующие значения из справочника будут перенесены в поля класса
            данных. Пример: {'summa':'f1', 'summa2':'f2'}
        @type DateTime_: C{string}
        @param DateTime_: Время актуальности кода.
        @type bCount: C{string}
        @param bCount: признак того, что необходимо вести количество ссылок.
        @rtype: C{int}
        @return: Код возврата функции контроля.
        """
        result = coderror.IC_CTRL_OK
        res_val = None

        try:
            storage = self.getStorage()
            level_tab = storage.getLevelTable(cod, DateTime_)
            # Список имен полей
            field_names = storage.getSpravFieldNames()
            # Словарь индексов
            field_indexes = dict([(item[1], item[0]) for item in enumerate(field_names)])
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
            io_prnt.outLog('CTRL: NOT_FOUND val=%s' % val)
        except:
            io_prnt.outErr(u'СПРАВОЧНИК [%s] Ошибка контроля' % self.name)
            result = coderror.IC_CTRL_FAILED_TYPE_SPRAV

        return result, res_val

    def Find(self, cod, field='name', DateTime_=None):
        """
        Поиск по коду.

        @type cod: C{...}
        @param cod: Код строки справочника.
        @type field: C{string | list }
        @param field: Имя поля или список полей.
        @type DateTime_: C{string}
        @param DateTime_: Время актуальности кода.
        @rtype: C{dictionary}
        @return: Значение либо словарь значений (если поле field задает список полей).
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
        ctrlCod, dict = self.Ctrl(cod, None, 'cod', fldDict,
                                  cod=level_cod, DateTime_=DateTime_)

        if ctrlCod != IC_CTRL_OK:
            ret = None
        elif isRetDict:
            ret = dict
        else:
            ret = dict[field]

        return ret

    def getParentLevelCod(self, Cod_):
        """
        Код родительского уровня.
        @param Cod_: Код.
        """
        return ''.join(filter(lambda subcod: bool(subcod),
                       self.StrCode2ListCode(Cod_))[:-1])

    def updateRec(self, Cod_, RecDict_, DateTime_=None, ClearCache_=False):
        """
        Обновить запись в справочнике по коду.
        @param Cod_: Код.
        @param RecDict_: Словарь изменений.
        @param DateTime_: Период актуальности.
        @param ClearCache_: Обновить кеш?
        @return: Возвращает результат выполнения операции.
        """
        level = self.getLevelByCod(Cod_)
        if level:
            # Контроль на уровне
            update_ctrl_result = level.getUpdateCtrl(locals())
            if update_ctrl_result is None:
                # Контроля производить не надо
                return self._updateRec(Cod_, RecDict_, DateTime_, ClearCache_)
            elif update_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._updateRec(Cod_, RecDict_, DateTime_, ClearCache_)
            elif update_ctrl_result in (coderror.IC_CTRL_FAILED,
                                        coderror.IC_CTRL_FAILED_IGNORE,
                                        coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                        coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                io_prnt.outWarning(u'Не прошел контроль обновление/изменение записи в справочник [%s]. Код ошибки: <%d>' %
                                   (self.getName(), update_ctrl_result))

        return False

    def _updateRec(self, Cod_, RecDict_, DateTime_=None, ClearCache_=False):
        """
        Обновить запись в справочнике по коду.
        @param Cod_: Код.
        @param RecDict_: Словарь изменений.
        @param DateTime_: Период актуальности.
        @param ClearCache_: Обновить кеш?
        @return: Возвращает результат выполнения операции.
        """
        storage = self.getStorage()
        if storage:
            result = storage.updateRecByCod(Cod_, RecDict_, DateTime_)
            # Если запись прошла удачно, то сбросить кэш
            if ClearCache_:
                self.clearInChache()
            return result

        return False

    def addRec(self, Cod_, RecDict_, DateTime_=None, ClearCache_=False):
        """
        Добавить запись в справочник по коду.
        @param Cod_: Код.
        @param RecDict_: Словарь изменений.
        @param DateTime_: Период актуальности.
        @param ClearCache_: Обновить кеш?
        @return: Возвращает результат выполнения операции.
        """
        level = self.getLevelByCod(Cod_)
        if level:
            # Контроль на уровне
            add_ctrl_result = level.getAddCtrl(locals())
            if add_ctrl_result is None:
                # Контроля производить не надо
                return self._addRec(Cod_, RecDict_, DateTime_, ClearCache_)
            elif add_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._addRec(Cod_, RecDict_, DateTime_, ClearCache_)
            elif add_ctrl_result in (coderror.IC_CTRL_FAILED,
                                     coderror.IC_CTRL_FAILED_IGNORE,
                                     coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                     coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                io_prnt.outWarning(u'Не прошел контроль добавления записи в справочник [%s]. Код ошибки: <%d>' %
                                   (self.getName(), add_ctrl_result))

        return False

    def _addRec(self, Cod_, RecDict_, DateTime_=None, ClearCache_=False):
        """
        Добавить запись в справочник по коду.
        @param Cod_: Код.
        @param RecDict_: Словарь изменений.
        @param DateTime_: Период актуальности.
        @param ClearCache_: Обновить кеш?
        @return: Возвращает результат выполнения операции.
        """
        storage = self.getStorage()
        if storage:
            if storage.isCod(Cod_):
                result = storage.updateRecByCod(Cod_, RecDict_, DateTime_)
            else:
                RecDict_['cod'] = Cod_
                result = storage.addRecDictDataTab(RecDict_)
            # Если запись прошла удачно, то сбросить кэш
            if ClearCache_:
                self.clearInCache()
            return result

        return False

    def delRec(self, Cod_, DateTime_=None):
        """
        Удалить запись по коду.
        @param Cod_: Код.
        @param DateTime_: Период актуальности.
        """
        level = self.getLevelByCod(Cod_)
        if level:
            # Контроль на уровне
            del_ctrl_result = level.getDelCtrl(locals())
            if del_ctrl_result is None:
                # Контроля производить не надо
                return self._delRec(Cod_, DateTime_)
            elif del_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._delRec(Cod_, DateTime_)
            elif del_ctrl_result in (coderror.IC_CTRL_FAILED,
                                     coderror.IC_CTRL_FAILED_IGNORE,
                                     coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                     coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                io_prnt.outWarning(u'Не прошел контроль удаления записи в справочник [%s]. Код ошибки: <%d>' %
                                   (self.getName(), del_ctrl_result))

        return False

    def _delRec(self, Cod_, DateTime_=None):
        """
        Удалить запись по коду.
        @param Cod_: Код.
        @param DateTime_: Период актуальности.
        """
        return self.getStorage().delRecByCod(Cod_, DateTime_)

    def getLevelRefSpravByCod(self, Cod_=None):
        """
        Получить объект справочника, связанного с уровнем.
        """
        if not Cod_:
            # Если это рут, то вернуть первый уровень
            level = self.getLevelByCod(Cod_)
        else:
            # Если это первый(второй,...) то вернуть следующий уровень
            level = self.getLevelByCod(Cod_).getNext()
        if level:
            ref_sprav_name = level.getRefSprav()
            if ref_sprav_name:
                sprav_manager = self.getSpravManager()
                return sprav_manager.getSpravByName(ref_sprav_name)
        return None

    def StrCode2ListCode(self, StrCode_):
        """
        Преобразовать строковый код в списковый код по уровням.
        @param StrCode_: Строковое представление кода.
        @param cod_encode: Однобайтовая кодировка кода.
        """
        if not StrCode_:
            return []

        levels = self.getLevels()
        list_cod = []
        for level in levels:
            subcod = StrCode_[:level.getCodLen()]
            list_cod.append(subcod)
            StrCode_ = StrCode_[level.getCodLen():]
        return list_cod

    def ListCode2StrCode(self, ListCode_):
        """
        Преобразовать списковый код по уровням в строковый код.
        @param ListCode_: Списковое/кортежное представление кода.
        """
        return ''.join([cod for cod in list(ListCode_) if cod is not None])

    def isSubCodes(self, Cod_):
        """
        Есть ли у указанного кода подкоды подуровней?
        @param Cod_: Код справочника.
        """
        storage = self.getStorage()
        if storage:
            recs = storage._getLevelTab(Cod_)
            return bool(recs)
        return False

    def _get_refspr_parent_cod(self, prnt_cod):
        """
        Определяет родительский код связанного справочника.
        @param prnt_cod: Родительский код текущего справочника.
        """
        ref_sprav = self.getLevelRefSpravByCod(prnt_cod)
        lev = self.getLevelByCod(prnt_cod).getNext()
        cod_lst = []
        if lev:
            cod_lst = self.StrCode2ListCode(prnt_cod)
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
        @param cod: Код.
        @param default_lst: Список словарей (для каждого уровня) значений полей.
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
                        io_prnt.outLog(u'ERROR. Not Found referer sprav <%s>' % ref)
                        raise
                    if ref_sprav:
                        try:
                            ref_prnt_cod = ''.join(self._get_refspr_parent_cod(prnt_cod))
                            ref_cod = ref_prnt_cod + cd
                            name = ref_sprav.Find(ref_cod)
                            df = {'name': name}
                        except:
                            io_prnt.outErr(u'Find <name> in ref sprav ERROR!')
                    else:
                        df = {'name': cd}

                self.addRec(prnt_cod+cd, df)
            prnt_cod += cd

    def getUUIDByCod(self, Cod_):
        """
        Получить уникальный идентификатор по коду.
        """
        storage = self.getStorage()
        if storage:
            return storage.getUUIDByCod(Cod_)
        io_prnt.outlog(u'У объекта справочника [%s] не определено хранилище.' % self.getName())
        return None

