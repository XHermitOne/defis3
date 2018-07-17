#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента перечисления конфигурации 1с.
"""

import os
import os.path
import copy

from . import iccfresource
from . import iccfobject

from ic.log import log
from ic.utils import util1c
from ic.utils import util
from ic.utils import ic_str
import ic


__version__ = (0, 0, 1, 1)

DEFAULT_ENUM_RES = 'nsi_enum_1c'


class icCFEnumValue(iccfobject.icCFObject):
    """
    Класс элемента значения перечисления.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self, uid=iccfobject.ANY_UID, *args, **kwargs)

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'ui-button.png')
        self.description = u''

    def init(self, res=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if res is None:
            return

        self.name = unicode(res[0][1][2], 'utf-8')

        if self.uid == iccfobject.ANY_UID:
            self.uid = res[0][1][1][2] if res[0][1][1][2] else iccfobject.NONE_UID

        try:
            self.description = unicode(res[0][1][3][2], 'utf-8')
        except:
            self.description = u''


class icCFEnum(iccfobject.icCFObject):
    """
    Класс элемента перечисления конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.description = ''
        
        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'sort-alphabet.png')

        # Значения перечисления
        self.values = list()

    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_obj_filename = os.path.join(os.path.abspath(self.cf_dir), 'metadata', self.uid)
        if not os.path.exists(cf_obj_filename):
            cf_obj_filename = os.path.join(os.path.abspath(self.cf_dir), self.uid)
        if not os.path.exists(cf_obj_filename):
            log.warning(u'Не найден файл <%s>' % cf_obj_filename)
            return

        cf_doc_res = iccfresource.icCFResource(cf_obj_filename)
        cf_doc_res.loadData()

        if cf_doc_res.data is None:
            log.warning(u'Ошибка загрузки данных перечисления <%s>' % self.uid)
            return

        # util1c.print_idx_paths(cf_doc_res.data)
        # import sys
        # sys.exit(1)

        self.name = unicode(cf_doc_res.data[1][5][1][2], 'utf-8')
        self.description = u''
        if len(cf_doc_res.data[1][5][1][3]) > 1:
            self.description = unicode(cf_doc_res.data[1][5][1][3][2], 'utf-8')

        for res in cf_doc_res.data[6][2:]:
            value = icCFEnumValue(self)
            value.init(res)
            self.values.append(value)

        self.children = [iccfobject.icCFFolder(parent=self,
                                               name=u'Значения', children=self.values,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'ui-buttons.png')),
                         ]

    def gen_resource(self):
        """
        Генерация ресурса, соответстствующего объеку 1С.
        @return: True/False.
        """
        # Открыть проект
        prj_res_ctrl = ic.getKernel().getProjectResController()
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения перечислений 1С не взможна.')
            return False
        else:
            log.debug(u'Контроллер управления ресурсом проекта <%s>' % prj_res_ctrl)
        prj_res_ctrl.openPrj()

        # Создать необходимые ресурсные файлы
        self._gen_enum_tab(prj_res_ctrl)
        self._gen_enum_spravmanager(prj_res_ctrl)
        self._gen_enum_sprav(prj_res_ctrl)

        # Добавить в таблицу значения перечислений
        self._add_values(prj_res_ctrl)

        return True

    def _add_values(self, prj_res_ctrl=None):
        """
        Добавить в таблицу значения перечислений.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        """
        tab_name = self._get_enum_tabname(prj_res_ctrl)
        if prj_res_ctrl.isRes(tab_name, 'tab'):
            tab = ic.getKernel().CreateObj(tab_name, tab_name, 'tab')
            if tab:
                name_lat = ic_str.rus2lat(self.name)
                len_code = self._get_enum_spravlevel_len()
                code_fmt = '%%0%dd' % len_code
                # Сначала удалить все данные представления
                tab.del_where(tab.c.type == name_lat)
                # Затем добавить значения
                values = self.children[0].children
                for i, value in enumerate(values):
                    code = code_fmt % (i + 1)
                    tab.add(type=name_lat, cod=code, name=value.description,
                            s1=value.name, uid1c=value.uid)
            else:
                log.warning(u'Ошибка создания объекта таблицы хранения перечислений 1С <%s>' % tab_name)
        else:
            log.warning(u'Не найден ресурс таблицы хранения перечислений 1С <%s>' % tab_name)

    def _get_enum_tabname(self, prj_res_ctrl=None):
        """
        Имя таблицы хранения перечислений 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        """
        return DEFAULT_ENUM_RES

    def _gen_enum_field_res(self, field_name, field_type='T', field_len=0,
                            field_default=None, field_description=u''):
        """
        Генерация ресурса поля.
        @return: Сгенерированный ресурс поля.
        """
        from ic.components.user import ic_field_wrp

        field_res = util.icSpcDefStruct(copy.deepcopy(ic_field_wrp.ic_class_spc), None)

        field_res['name'] = field_name
        field_res['description'] = field_description
        field_res['label'] = field_description
        field_res['field'] = field_name.lower()
        field_res['type_val'] = field_type
        field_res['len'] = field_len
        field_res['attr'] = 0
        field_res['default'] = field_default

        return field_res

    def _gen_enum_tab_res(self, prj_res_ctrl=None, table_name=None):
        """
        Создать ресурс таблицы хранения перечислений 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        """
        from ic.components.user import ic_tab_wrp

        if table_name is None:
            table_name = self._get_enum_tabname(prj_res_ctrl)

        tab_res = util.icSpcDefStruct(copy.deepcopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        tab_res['name'] = table_name
        tab_res['description'] = ic_str.str2unicode(self.description)
        tab_res['table'] = table_name.lower()
        tab_res['source'] = self._get_db_psp(prj_res_ctrl)

        tab_res['child'].append(self._gen_enum_field_res(field_name='type', field_description=u'Тип справочника'))
        tab_res['child'].append(self._gen_enum_field_res(field_name='cod', field_description=u'Код справочника'))
        tab_res['child'].append(self._gen_enum_field_res(field_name='name', field_description=u'Наименование'))
        tab_res['child'].append(self._gen_enum_field_res(field_name='count', field_type='I', field_description=u'Cчетчик'))
        tab_res['child'].append(self._gen_enum_field_res(field_name='access', field_description=u'Доступ'))
        tab_res['child'].append(self._gen_enum_field_res(field_name='s1', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_enum_field_res(field_name='s2', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_enum_field_res(field_name='s3', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_enum_field_res(field_name='n1', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_enum_field_res(field_name='n2', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_enum_field_res(field_name='n3', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_enum_field_res(field_name='f1', field_type='F', field_default=0.0))
        tab_res['child'].append(self._gen_enum_field_res(field_name='f2', field_type='F', field_default=0.0))
        tab_res['child'].append(self._gen_enum_field_res(field_name='f3', field_type='F', field_default=0.0))
        # Добавить поле UID объекта из 1С. Его необходимо заполнять при заполнении данными
        # Через это поле будет контролироваться целосность данных при импорте данных из 1С
        tab_res['child'].append(self._gen_enum_field_res(field_name='uid1c', field_type='T',
                                                         field_description=u'UID объекта из 1С'))

        return tab_res

    def _gen_enum_tab(self, prj_res_ctrl=None):
        """
        Генерация ресурса таблицы хранения перечислений 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения перечислений 1С не взможна.')
            return False

        # Проверка на добавление нового ресурса
        table_name = self._get_enum_tabname()
        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if table_name and not prj_res_ctrl.isRes(table_name, 'tab'):
            table_res = self._gen_enum_tab_res(prj_res_ctrl, table_name=table_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(table_name, 'tab', table_res)
            return True

        return False

    def _gen_enum_spravmanager_res(self, prj_res_ctrl=None, res_name=None):
        """
        Генерация ресурса справочников перечислений 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: Ресурс справочников перечислений 1С.
        """
        from NSI.usercomponents import spravmanager

        if res_name is None:
            res_name = DEFAULT_ENUM_RES

        res = util.icSpcDefStruct(copy.deepcopy(spravmanager.ic_class_spc), None)
        res['name'] = res_name
        res['description'] = u'Менеджер справочников перечислений 1С'
        return res

    def _gen_enum_spravmanager(self, prj_res_ctrl=None):
        """
        Генерация ресурса справочников перечислений 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения перечислений 1С не взможна.')
            return False

        # Проверка на добавление нового ресурса
        res_name = DEFAULT_ENUM_RES
        if res_name and not prj_res_ctrl.isRes(res_name, 'mtd'):
            res = self._gen_enum_spravmanager_res(prj_res_ctrl, res_name=res_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(res_name, 'mtd', res)
            return True
        return False

    def _get_enum_spravlevel_len(self):
        """
        Длина кода уровня справочника перечислений.
        """
        return len(str(len(self.children))) + 2 if len(self.children) < 10 else 1

    def _gen_enum_sprav_res(self, prj_res_ctrl=None, name=None, description=u'',
                            uuid=iccfobject.NONE_UID):
        """
        Генерация ресурса справочника перечисления 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @param name: Наименование объекта ресурса.
        @param description: Описание объекта ресурса.
        @param uuid: Уникальный идентификатор объекта ресурса.
        @return: Ресурс справочника перечисления 1С.
        """
        from NSI.usercomponents import sprav
        from NSI.usercomponents import spravlevel

        # Преобразовать русское наименование из 1С в латинское
        name_lat = ic_str.rus2lat(name)
        tab_name = self._get_enum_tabname(prj_res_ctrl)
        res = util.icSpcDefStruct(copy.deepcopy(sprav.ic_class_spc), None)
        res['name'] = name_lat
        res['_uuid'] = uuid
        res['description'] = description
        res['table'] = (('Table', tab_name, None, '%s.tab' % tab_name, ic.getPrjName()),)
        res['db'] = self._get_db_psp(prj_res_ctrl)
        # Перечисления не меняются со временем, пэтому временная таблица не нужна
        res['is_tab_time'] = False

        # Для перечислений добавляем 1 уровень
        level_res = util.icSpcDefStruct(copy.deepcopy(spravlevel.ic_class_spc), None)
        level_res['name'] = 'lvl' + name_lat
        level_res['description'] = description
        level_len = self._get_enum_spravlevel_len()
        level_res['len'] = level_len
        res['child'].append(level_res)
        return res

    def _gen_enum_sprav(self, prj_res_ctrl=None):
        """
        Генерация ресурса справочника перечисления 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения перечислений 1С не взможна.')
            return False

        sprav_res = self._gen_enum_sprav_res(prj_res_ctrl,
                                             name=self.name,
                                             description=self.description,
                                             uuid=self.uid)

        res_name = DEFAULT_ENUM_RES
        # Загрузить ресурс
        res = prj_res_ctrl.loadRes(res_name, 'mtd')

        child_names = [child['name'] for child in res['child']]
        if sprav_res['name'] in child_names:
            del res['child'][child_names.index(sprav_res['name'])]
        res['child'].append(sprav_res)

        # Сохранить ресурс
        prj_res_ctrl.saveRes(res_name, 'mtd', res)
        return True
