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
        pass

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
        table_name = self._genTableName()
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
            table_name = self._genTableName()

        tab_res = self._createTabSpc(table_name)
        # Перебрать дочерние компоненты
        children_requisites = self.getChildrenRequisites()
        if children_requisites:
            for child_requisite in children_requisites:
                # Это реквизит
                fields_spc = child_requisite._createFieldSpc()
                if fields_spc is None:
                    log.warning(u'Не определена спецификация поля при создании таблицы хранимого объекта')
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
            table_name = self._genTableName()
        tab_spc['name'] = table_name
        tab_spc['description'] = strfunc.str2unicode(self.getDescription())
        tab_spc['table'] = table_name.lower()
        tab_spc['source'] = self.getDBPsp()

        tab_spc['children'] = []  # Список имен подчиненных таблиц

        # Поле кода-идентификатора объекта
        field_spc = self._createCodeFieldSpc()
        tab_spc['child'].append(field_spc)
        # Поле кода вкл/выкл объекта
        field_spc = self._createStatusFieldSpc()
        tab_spc['child'].append(field_spc)

        # Если у объекта есть родитель, то в таблице
        # должна отражатся информация о родителе
        level_idx = self.getLevelIdx()
        if level_idx:
            sprav = self.getSprav()
            level_names = [level.getName() for level in sprav.getLevels()]
            parent_level_name = level_names[level_idx - 1]
            link_spc = self._createLinkSpc(parent_level_name)
            tab_spc['child'].append(link_spc)

        # Перебрать все стандартные реквизиты и добавить их в виде полей в
        # ресурс таблицы
        for child_requisite in self.getChildrenRequisites():
            field_spc = child_requisite._createFieldSpc()
            tab_spc['child'].append(field_spc)

        return tab_spc

    def _createCodeFieldSpc(self, field_name='code'):
        """
        Создать спецификацию поля кода-идентификатора объекта-ссылки.
        @param field_name: Имя поля кода-идентификатора объекта-ссылки.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = field_name
        field_spc['description'] = u'Код'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'T'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = None

        return field_spc

    def _createStatusFieldSpc(self, field_name='status'):
        """
        Создать спецификацию поля вкл/выкл объекта-ссылки.
        @param field_name: Имя поля вкл/выкл объекта-ссылки.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = field_name
        field_spc['description'] = u'Вкл/Выкл объект'
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = 'Boolean'
        field_spc['len'] = None
        field_spc['attr'] = 0
        field_spc['default'] = True

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




