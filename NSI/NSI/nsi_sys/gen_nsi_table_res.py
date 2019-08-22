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

__version__ = (0, 1, 1, 1)


class icSpravTableResGenerator():
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

    def _createTabRes(self, sTableName=None):
        """
        Создать ресурс таблицы хранения справочника.
        @param sTableName: Имя таблицы.
        """
        if sTableName is None:
            sTableName = self.getTableName()

        if not sTableName:
            log.warning(u'Не определено имя таблицы хранения справочника при генерации ресурса таблицы')
            return None

        tab_res = self._createTabSpc(sTableName)

        fields_spc = self._createFieldSpc('type', sFieldDescription=u'Тип справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('cod', sFieldDescription=u'Код справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('name', sFieldDescription=u'Наименование')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('count', 'I', sFieldDescription=u'Количество ссылок на элемент справочника')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('access', sFieldDescription=u'Права доступа')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('computer', sFieldDescription=u'Компьютер')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('username', sFieldDescription=u'Пользователь')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s1', 'T', sFieldDescription=u'Строка 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s2', 'T', sFieldDescription=u'Строка 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('s3', 'T', sFieldDescription=u'Строка 3. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n1', 'I', sFieldDescription=u'Целое 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n2', 'I', sFieldDescription=u'Целое 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('n3', 'I', sFieldDescription=u'Целое 3. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f1', 'F', sFieldDescription=u'Вещественное 1. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f2', 'F', sFieldDescription=u'Вещественное 2. Резерв.')
        tab_res['child'].append(fields_spc)
        fields_spc = self._createFieldSpc('f3', 'F', sFieldDescription=u'Вещественное 3. Резерв.')
        tab_res['child'].append(fields_spc)

        return tab_res

    def _createTabSpc(self, sTableName=None):
        """
        Создать спецификацию таблицы.
        @param sTableName: Имя таблицы.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if sTableName is None:
            sTableName = self.getTableName()

        tab_spc['name'] = sTableName
        tab_spc['description'] = strfunc.str2unicode(self.getDescription())
        tab_spc['table'] = sTableName.lower()
        tab_spc['source'] = self.getDBPsp()
        tab_spc['children'] = list()  # Список имен подчиненных таблиц

        tab_spc['child'] = list()
        return tab_spc

    def _createFieldSpc(self, sFieldName, sFieldType='T', iFieldLen=None,
                        sFieldDefault=None, sFieldDescription=u''):
        """
        Создать спецификацию поля.
        Функция необходима для вспомогательных и 
        служебных полей.
        @param sFieldName: Имя поля.
        @param sFieldType: Указание типа поля.
        @param iFieldLen: Длина поля. В случае строковых полей.
        @param sFieldDefault: Значение по умолчанию для поля.
        @param sFieldDescription: Строковое описание поля.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)

        field_spc['name'] = sFieldName
        field_spc['description'] = sFieldDescription
        field_spc['field'] = sFieldName.lower()
        field_spc['type_val'] = sFieldType
        field_spc['len'] = iFieldLen
        field_spc['attr'] = 0
        field_spc['default'] = sFieldDefault

        return field_spc

    def _createTableResource(self, sTableName=None):
        """
        Создание по описанию объекта ресурса таблицы, в
            которой хранятся данные объекта.
        @param sTableName: Имя таблицы.
        """
        # Открыть проект
        prj_res_ctrl = glob_functions.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        if sTableName is None:
            sTableName = self.getTableName()

        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        is_res = prj_res_ctrl.isRes(sTableName, 'tab')
        if sTableName and not is_res:
            log.info(u'Создание ресурса таблицы <%s>' % sTableName)
            table_res = self._createTabRes(sTableName)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(sTableName, 'tab', table_res)
            return table_res
        elif sTableName and is_res:
            return prj_res_ctrl.loadRes(sTableName, 'tab')
        else:
            log.warning(u'Не возможно определить таблицу хранения справочника <%s>' % sTableName)
        return None
