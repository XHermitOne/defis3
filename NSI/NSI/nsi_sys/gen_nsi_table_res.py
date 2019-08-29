#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс генератора ресурса таблицы хранения справочника по умолчанию.
"""

from ic.log import log
from ic.utils import util
from ic.utils import strfunc
from ic.engine import glob_functions

from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp

__version__ = (0, 1, 1, 2)


class icSpravTableResGenerator(object):
    """
    Генератор ресурса таблицы хранения справочника.
    """

    def getTableName(self):
        """
        Имя таблицы справочника.
        """
        log.error(u'Не определен метод определения имени таблицы хранения справочника')
        return None

    def getDBPsp(self):
        """
        Паспорт БД хранения справочника.
        """
        log.error(u'Не определен метод определения БД таблицы хранения справочника')
        return None

    def getDescription(self):
        """
        Описание компонента.
        """
        return u''

    def _createTabRes(self, table_name=None):
        """
        Создать ресурс таблицы хранения справочника.
        @param table_name: Имя таблицы.
        """
        if table_name is None:
            table_name = self.getTableName()

        if not table_name:
            log.warning(u'Не определено имя таблицы хранения справочника при генерации ресурса таблицы')
            return None

        tab_res = self._createTabSpc(table_name)

        fields_spc = self._createFieldSpc('type', field_description=u'Тип справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('cod', field_description=u'Код справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('name', field_description=u'Наименование')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('count', 'I', field_description=u'Количество ссылок на элемент справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('access', field_description=u'Права доступа')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('computer', field_description=u'Компьютер')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('username', field_description=u'Пользователь')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s1', 'T', field_description=u'Строка 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s2', 'T', field_description=u'Строка 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s3', 'T', field_description=u'Строка 3. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n1', 'I', field_description=u'Целое 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n2', 'I', field_description=u'Целое 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n3', 'I', field_description=u'Целое 3. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f1', 'F', field_description=u'Вещественное 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f2', 'F', field_description=u'Вещественное 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f3', 'F', field_description=u'Вещественное 3. Резерв.')
        tab_res['child'].append(fields_spc)

        return tab_res

    def _createTabSpc(self, table_name=None):
        """
        Создать спецификацию таблицы.
        @param table_name: Имя таблицы.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if table_name is None:
            table_name = self.getTableName()

        tab_spc['name'] = table_name
        tab_spc['description'] = strfunc.str2unicode(self.getDescription())
        tab_spc['table'] = table_name.lower()
        tab_spc['source'] = self.getDBPsp()
        tab_spc['children'] = list()  # Список имен подчиненных таблиц

        tab_spc['child'] = list()
        return tab_spc

    def _createFieldSpc(self, field_name, field_type='T', field_len=None,
                        field_default=None, field_description=u''):
        """
        Создать спецификацию поля.
        Функция необходима для вспомогательных и 
        служебных полей.
        @param field_name: Имя поля.
        @param field_type: Указание типа поля.
        @param field_len: Длина поля. В случае строковых полей.
        @param field_default: Значение по умолчанию для поля.
        @param field_description: Строковое описание поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = field_name
        field_spc['description'] = field_description
        field_spc['field'] = field_name.lower()
        field_spc['type_val'] = field_type
        field_spc['len'] = field_len
        field_spc['attr'] = 0
        field_spc['default'] = field_default

        return field_spc

    def _createTableResource(self, table_name=None):
        """
        Создание по описанию объекта ресурса таблицы, в
            которой хранятся данные объекта.
        @param table_name: Имя таблицы.
        """
        # Открыть проект
        prj_res_ctrl = glob_functions.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        if table_name is None:
            table_name = self.getTableName()

        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        is_res = prj_res_ctrl.isRes(table_name, 'tab')
        if table_name and not is_res:
            log.info(u'Создание ресурса таблицы <%s>' % table_name)
            table_res = self._createTabRes(table_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(table_name, 'tab', table_res)
            return table_res
        elif table_name and is_res:
            return prj_res_ctrl.loadRes(table_name, 'tab')
        else:
            log.warning(u'Не возможно определить таблицу хранения справочника <%s>' % table_name)
        return None
