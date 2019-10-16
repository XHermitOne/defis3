#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактные классы хранимых объектов.
По сути это генератор таблиц хранения объектов.

Поддержка каскадов таблиц хранения объекта-ссылки/справочника.
"""

from ic.log import log
from ic.utils import util
from ic.utils import strfunc
from ic.utils import lockfunc
from ic.engine import glob_functions

# Для спецификаций таблиц, полей, связей
from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp
from ic.components.user import ic_link_wrp


# Версия
__version__ = (0, 1, 1, 1)


class icRefTablePersistent(object):
    """
    Базовый класс компонентов хранимых в БД.
    Реализует внутри себя механизм генерации спецификаций таблиц хранения.
    Поддержка каскадов таблиц хранения объекта-ссылки/справочника.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        # Закешированное имя таблицы
        self.table_name = None
        # Объект таблицы хранения
        self._table = None

        # Система блокировки
        self._lockSystem = None
        self.read_only = True

        # Инициализировать систему блокировки
        self._initLockSystem()

    # Методы поддержни блокировок
    def _initLockSystem(self):
        """
        Функции поддержки блокировок.
        Инициализация системы блокировок.
        """
        # Система блокировки
        lock_dir = glob_functions.getVar('LOCK_DIR')
        self._lockSystem = lockfunc.icLockSystem(lock_dir)

    def lock(self, code=None):
        """
        Функции поддержки блокировок.
        Заблокировать текущий. Блокировка ведется по UUID.
        @param code: Код блокируемого объекта.
        """
        if code:
            if self._lockSystem:
                lock_name = self.getSprav().getName() + self.getName() + code
                return self._lockSystem.lockFileRes(lock_name)
        return None

    def unLock(self, code=None):
        """
        Функции поддержки блокировок.
        Разблокировать.
        @param code: Код блокируемого объекта.
        """
        if code:
            if self._lockSystem:
                lock_name = self.getSprav().getName() + self.getName() + code
                return self._lockSystem.unLockFileRes(lock_name)
        return None

    def isLock(self, code=None):
        """
        Функции поддержки блокировок.
        Заблокирован?
        @param code: Код блокируемого объекта.
        """
        if code:
            if self._lockSystem:
                lock_name = self.getSprav().getName() + self.getName() + code
                return self._lockSystem.isLockFileRes(lock_name)
        return False

    def ownerLock(self, code=None):
        """
        Функции поддержки блокировок.
        Владелец блокировки.
        @param code: Код блокируемого объекта.
        """
        if code:
            if self._lockSystem:
                lock_name = self.getSprav().getName() + self.getName() + code
                lock_rec = self._lockSystem.getLockRec(lock_name)
                return lock_rec['computer']
        return None

    def isMyLock(self, code=None):
        """
        Функции поддержки блокировок.
        Моя блокировка?
        @param code: Код блокируемого объекта.
        @return: True/False.
        """
        if code:
            lock_name = self.getSprav().getName() + self.getName() + code
            return self.ownerLock(lock_name) == lockfunc.ComputerName()
        return False

    # Методы генерации ресурса таблицы
    def genTableRes(self, table_name=None):
        """
        Генерация ресурса таблицы уровня.
        @param table_name: Имя таблицы уровня.
        @return: True - ресурс успешно создан / False - ошибка.
        """
        # Открыть проект
        prj_res_ctrl = glob_functions.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        if table_name is None:
            table_name = self.getTableName()
        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if table_name and not prj_res_ctrl.isRes(table_name, 'tab'):
            table_res = self._createTableRes(table_name)
            # Сохранить ресурс
            return prj_res_ctrl.saveRes(table_name, 'tab', table_res)
        return False

    def getChildrenRequisites(self):
        """
        Все реквизиты объекта в виде списка.
            Метод должен переопределяться в классе-компоненте.
        """
        log.warning(u'Не определен метод полручения списка реквизитов уровня объекта-ссылки')
        return list()

    def getDescription(self):
        """
        Получить описание компонента.
        """
        return u''

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        log.warning(u'Не определен метод получения паспорта БД в <%s>' % self.__class__.__name__)
        return u''

    def getLevelIdx(self):
        """
        Индекс текущего уровня в списке уровней объекта-ссылки/справочника.
        """
        name = self.getName()
        sprav = self.getSprav()
        level_names = [level.getName() for level in sprav.getLevels()]
        level_idx = level_names.index(name)
        return level_idx

    def getTableName(self):
        """
        Получить имя таблицы уровня.
        """
        if self.table_name is None:
            self.table_name = self._genTableName()
        return self.table_name

    def _genTableName(self):
        """
        Генерация имени таблицы уровня.
        @return: Имя таблицы уровня.
        """
        sprav = self.getSprav()
        level_names = [level.getName() for level in sprav.getLevels()]
        level_idx = self.getLevelIdx()
        table_name = '_'.join(level_names[:level_idx + 1])
        return table_name + '_tab'

    def _createTableRes(self, table_name=None):
        """
        Генерация спецификации таблицы уровня.
        @param table_name: Имя таблицы уровня.
        @return: True - ресурс успешно создан / False - ошибка.
        """
        if table_name is None:
            table_name = self.getTableName()

        tab_res = self._createTabSpc(table_name)
        # Перебрать дочерние компоненты
        children_requisites = self.getChildrenRequisites()
        if children_requisites:
            for child_requisite in children_requisites:
                # Это реквизит
                fields_spc = child_requisite._createFieldSpc()
                if fields_spc is None:
                    log.warning(u'Не определена спецификация поля при создании таблицы хранимого объекта')
                else:
                    tab_res['child'].append(fields_spc)

        return tab_res

    def _createTabSpc(self, table_name=None):
        """
        Создать спецификацию таблицы.
        @param table_name: Имя таблицы уровня.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if table_name is None:
            table_name = self.getTableName()
        tab_spc['name'] = table_name
        tab_spc['description'] = strfunc.str2unicode(self.getDescription())
        tab_spc['table'] = table_name.lower()
        tab_spc['source'] = self.getDBPsp()

        tab_spc['children'] = []  # Список имен подчиненных таблиц

        # Если у объекта есть родитель, то в таблице
        # должна отражатся информация о родителе
        level_idx = self.getLevelIdx()
        if level_idx:
            levels = self.getSprav().getLevels()
            parent_level = levels[level_idx - 1]
            link_spc = self._createLinkSpc(parent_level.getTableName())
            tab_spc['child'].append(link_spc)

        return tab_spc

    def _createFieldSpc(self, **field_attrs):
        """
        Создать спецификацию поля кода-идентификатора объекта-ссылки.
        @param field_attrs: Атрибуты поля.
        @param field_name: Имя поля кода-идентификатора объекта-ссылки.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_name = field_attrs.get('name', 'default')
        field_spc['name'] = field_name
        field_spc['description'] = field_attrs.get('description', '')
        field_spc['field'] = field_attrs.get('field', field_name.lower())
        field_spc['type_val'] = field_attrs.get('type_val', 'T')
        field_spc['len'] = field_attrs.get('len', None)
        field_spc['attr'] = field_attrs.get('attr', 0)
        field_spc['default'] = field_attrs.get('default', None)

        return field_spc

    def _createLinkSpc(self, table_name):
        """
        Создать спецификацию связи c таблицей.
        @param table_name: Имя таблицы с которой устанавливается связь.
        """
        # Инициализировать спецификацию связи
        link_spc = util.icSpcDefStruct(util.DeepCopy(ic_link_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        link_spc['name'] = 'id_' + table_name.lower()
        link_spc['description'] = strfunc.str2unicode('Связь с таблицей ' + table_name)
        link_spc['table'] = (('Table', table_name, None, None, None),)
        link_spc['del_lnk'] = True
        return link_spc

    def getTable(self):
        """
        Таблица хранения.
        """
        if self._table is None:
            tab_res = self._createTableRes()
            self._table = self.GetKernel().createObjBySpc(parent=None, res=tab_res)
        return self._table


class icRefFieldPersistent(object):
    """
    Базовый класс атрибута компонента хранимого в БД.
        Реализует внутри себя механизм генерации спецификации хранения.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        pass

    def _createFieldSpc(self):
        """
        Создать спецификацию поля ресурса.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        # Установить свойства связи с таблицей
        field_name = self.getFieldName()
        field_spc['name'] = field_name
        field_spc['description'] = strfunc.str2unicode(self.getDescription())
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = self.getTypeValue()
        field_spc['len'] = self.getFieldLen()
        field_spc['attr'] = 0
        field_spc['default'] = self.getDefault()

        return field_spc

    def getFieldName(self):
        """
        Имя поля хранения значения реквизита.
        """
        log.warning(u'Не определен метод полчения имени поля хранения реквизита в <%s>' % self.__class__.__name__)
        return u'default'

    def getDefault(self):
        """
        Значение по умолчанию.
        """
        log.warning(u'Не определен метод полчения значения по умолчанию поля хранения реквизита в <%s>' % self.__class__.__name__)
        return None

    def getDescription(self):
        """
        Описание реквизита.
        """
        return u''

    def getFieldLen(self):
        """
        Длина значения поля.
        """
        log.warning(u'Не определен метод полчения длины значения поля хранения реквизита в <%s>' % self.__class__.__name__)
        return None

    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        log.warning(u'Не определен метод полчения типа значения поля хранения реквизита в <%s>' % self.__class__.__name__)
        return 'T'




