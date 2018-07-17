#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента справочника конфигурации 1с.
"""

import copy
import os
import os.path

from . import iccfresource
from . import iccfobject

from ic.log import log
from ic.utils import util1c
from ic.utils import ic_str
from ic.utils import util
import ic


__version__ = (0, 0, 1, 1)


DEFAULT_SPRAV_RES = 'nsi_sprav_1c'

MAX_SPRAV_LEVEL_COUNT = 5
MAX_SPRAV_LEVEL_LEN = 5


class icCFSpravRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита справочника.
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
        # Тип реквизита
        self.type_value = None

    def init(self, res=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if res is None:
            return

        self.name = unicode(res[0][1][1][1][2], 'utf-8')
        try:
            self.description = unicode(res[0][1][1][1][3][2], 'utf-8')
        except:
            self.description = u''

        self.type_value = res[0][1][1][2][1]

    def _gen_field_type_res(self):
        """
        Генерация типа поля по типу значения 1С.
        @return:
        """
        if self.type_value is None:
            return 'T'

        if self.type_value[0] == 'B':
            return 'I'
        elif self.type_value[0] == 'S':
            return 'T'
        elif self.type_value[0] == 'D':
            return 'DateTime'
        elif self.type_value[0] == 'N' and self.type_value[2] == 0:
            return 'I'
        elif self.type_value[0] == 'N' and self.type_value[2] > 0:
            return 'F'

        return 'T'

    def _get_field_default_res(self):
        """
        Значение по умолчанию для поля.
        @return:
        """
        field_type = self._gen_field_type_res()
        if field_type == 'T':
            return ''
        elif field_type == 'I':
            return 0
        elif field_type == 'F':
            return 0.0
        return None


class icCFSpravTab(iccfobject.icCFObject):
    """
    Класс элемента табличной части справочника.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self, uid=iccfobject.ANY_UID, *args, **kwargs)

        self.requisites = []

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'table.png')
        self.description = u''

    def init(self, res=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if res is None:
            return

        self.name = unicode(res[0][1][5][1][2], 'utf-8')

        try:
            self.description = unicode(res[0][1][1][1][3][2], 'utf-8')
        except:
            self.description = u''

        self.requisites = []
        for res in res[2][2:]:
            requisite = icCFSpravTabRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)

        self.children = self.requisites


class icCFSpravTabRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита табличной части справочника.
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

        self.name = unicode(res[0][1][1][1][2], 'utf-8')

        try:
            self.description = unicode(res[0][1][1][1][3][2], 'utf-8')
        except:
            self.description = u''


class icCFSprav(iccfobject.icCFObject):
    """
    Класс элемента справочника конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.description = u''
        
        # Список реквизитов
        self.requisites = list()

        # Список табличных частей
        self.tabs = list()

        # Признак иерархического справочника
        self.is_hierarchy = False
        # Признак ограничения количества уровней иерархии
        self.is_limit_hierarchy = False
        # Количество уровней иерархии
        self.hierarchy_level_count = 2

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'book-brown.png')
        
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
            log.warning(u'Ошибка загрузки данных справочника <%s>' % self.uid)
            return

        # util1c.print_idx_paths(cf_doc_res.data)
        # print '>>', util1c.ValueIndexPath(cf_doc_res.data, 'b5818d6c-2f83-4927-a320-bb81a4253603')
        # import sys
        # sys.exit(1)

        self.name = unicode(cf_doc_res.data[1][9][1][2], 'utf-8')
        # if unicode(self.name, 'utf-8') == u'Контрагенты':
        #     util1c.print_idx_paths(cf_doc_res.data)
        #     import sys
        #     sys.exit(1)

        self.description = u''
        if len(cf_doc_res.data[1][9][1][3]) > 1:
            self.description = cf_doc_res.data[1][9][1][3][2]

        self.is_hierarchy = bool(cf_doc_res.data[1][37])
        log.debug(u'Признак иерархии в справочнике <%s> - %s' % (self.name,
                                                                 u'[v]' if self.is_hierarchy else u'[ ]'))

        self.is_limit_hierarchy = bool(cf_doc_res.data[1][38])
        log.debug(u'Признак ограничения количества уровней иерархии в справочнике <%s> - %s' % (self.name,
                                                                                                u'[v]' if self.is_limit_hierarchy else u'[ ]'))

        self.hierarchy_level_count = int(cf_doc_res.data[1][10])
        log.debug(u'Количество уровней иерархии в справочнике <%s> - %s' % (self.name,
                                                                            self.hierarchy_level_count))

        for res in cf_doc_res.data[6][2:]:
            requisite = icCFSpravRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)

        self.tabs = []
        for res in cf_doc_res.data[5][2:]:
            tab = icCFSpravTab(self)
            tab.init(res)
            self.tabs.append(tab)

        self.children = [iccfobject.icCFFolder(parent=self,
                                               name=u'Реквизиты', children=self.requisites,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'ui-buttons.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Табличные части', children=self.tabs,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'tables-stacks.png')),
                         ]

    def gen_resource(self):
        """
        Генерация ресурса, соответстствующего объеку 1С.
        @return: True/False.
        """
        # Открыть проект
        prj_res_ctrl = ic.getKernel().getProjectResController()
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения справочника <%s> 1С не взможна.' % self.name)
            return False
        else:
            log.debug(u'Контроллер управления ресурсом проекта <%s>' % prj_res_ctrl)
        prj_res_ctrl.openPrj()

        # Создать необходимые ресурсные файлы
        self._gen_sprav_tab(prj_res_ctrl)
        self._gen_sprav_spravmanager(prj_res_ctrl)
        self._gen_sprav(prj_res_ctrl)

        return True

    def _get_sprav_tabname(self, prj_res_ctrl=None):
        """
        Имя таблицы хранения справочника 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        """
        name_lat = ic_str.rus2lat(self.name)
        return 'nsi_' + name_lat

    def _gen_sprav_field_res(self, field_name, field_type='T', field_len=0,
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

    def _gen_sprav_tab_res(self, prj_res_ctrl=None, table_name=None):
        """
        Создать ресурс таблицы хранения справочника 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        """
        from ic.components.user import ic_tab_wrp

        if table_name is None:
            table_name = self._get_sprav_tabname(prj_res_ctrl)

        tab_res = util.icSpcDefStruct(copy.deepcopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        tab_res['name'] = table_name
        tab_res['description'] = ic_str.str2unicode(self.description)
        tab_res['table'] = table_name.lower()
        tab_res['source'] = self._get_db_psp(prj_res_ctrl)

        tab_res['child'].append(self._gen_sprav_field_res(field_name='type', field_description=u'Тип справочника'))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='cod', field_description=u'Код справочника'))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='name', field_description=u'Наименование'))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='count', field_type='I', field_description=u'Cчетчик'))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='access', field_description=u'Доступ'))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='s1', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='s2', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='s3', field_type='T', field_default=u''))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='n1', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='n2', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='n3', field_type='I', field_default=0))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='f1', field_type='F', field_default=0.0))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='f2', field_type='F', field_default=0.0))
        tab_res['child'].append(self._gen_sprav_field_res(field_name='f3', field_type='F', field_default=0.0))
        # Добавить поле UID объекта из 1С. Его необходимо заполнять при заполнении данными
        # Через это поле будет контролироваться целосность данных при импорте данных из 1С
        tab_res['child'].append(self._gen_sprav_field_res(field_name='uid1c', field_type='T',
                                                          field_description=u'UID объекта из 1С'))
        # Генерация полей реквизитов
        for requisite in self.requisites:
            field_name = ic_str.rus2lat(requisite.name)
            field_type = requisite._gen_field_type_res()
            tab_res['child'].append(self._gen_sprav_field_res(field_name=field_name,
                                                              field_type=field_type,
                                                              field_description=requisite.description,
                                                              field_default=requisite._get_field_default_res()))

        return tab_res

    def _gen_sprav_tab(self, prj_res_ctrl=None):
        """
        Генерация ресурса таблицы хранения справочника 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения справочника 1С не взможна.')
            return False

        # Проверка на добавление нового ресурса
        table_name = self._get_sprav_tabname()
        # Если имя таблицы определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if table_name and not prj_res_ctrl.isRes(table_name, 'tab'):
            table_res = self._gen_sprav_tab_res(prj_res_ctrl, table_name=table_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(table_name, 'tab', table_res)
            return True

        return False

    def _gen_sprav_spravmanager_res(self, prj_res_ctrl=None, res_name=None):
        """
        Генерация ресурса менеджера справочников 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: Ресурс справочников перечислений 1С.
        """
        from NSI.usercomponents import spravmanager

        if res_name is None:
            res_name = DEFAULT_SPRAV_RES

        res = util.icSpcDefStruct(copy.deepcopy(spravmanager.ic_class_spc), None)
        res['name'] = res_name
        res['description'] = u'Менеджер справочников 1С'
        return res

    def _gen_sprav_spravmanager(self, prj_res_ctrl=None):
        """
        Генерация ресурса менеджера справочников 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса 1С не взможна.')
            return False

        # Проверка на добавление нового ресурса
        res_name = DEFAULT_SPRAV_RES
        if res_name and not prj_res_ctrl.isRes(res_name, 'mtd'):
            res = self._gen_sprav_spravmanager_res(prj_res_ctrl, res_name=res_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(res_name, 'mtd', res)
            return True
        return False

    def _get_sprav_spravlevel_len(self):
        """
        Длина кода уровня справочника.
        По умолчанию будем считать что длина уровня MAX_SPRAV_LEVEL_COUNT.
        """
        return MAX_SPRAV_LEVEL_LEN

    def _gen_sprav_res(self, prj_res_ctrl=None, name=None, description=u'',
                       uuid=iccfobject.NONE_UID):
        """
        Генерация ресурса справочника 1С.
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
        tab_name = self._get_sprav_tabname(prj_res_ctrl)
        res = util.icSpcDefStruct(copy.deepcopy(sprav.ic_class_spc), None)
        res['name'] = name_lat
        res['_uuid'] = uuid
        res['description'] = description
        res['table'] = (('Table', tab_name, None, '%s.tab' % tab_name, ic.getPrjName()),)
        res['db'] = self._get_db_psp(prj_res_ctrl)
        # Справочнки меняются со временем, поэтому временная таблица нужна
        res['is_tab_time'] = True

        # Добавляем уровни
        if not self.is_hierarchy:
            # Справочник не иерархичный то у нас только 1 уровень
            level_res = util.icSpcDefStruct(copy.deepcopy(spravlevel.ic_class_spc), None)
            level_res['name'] = 'lvl' + name_lat
            level_res['description'] = description
            level_len = self._get_sprav_spravlevel_len()
            level_res['len'] = level_len
            res['child'].append(level_res)
        else:
            level_count = self.hierarchy_level_count if self.is_limit_hierarchy else MAX_SPRAV_LEVEL_COUNT
            for i_level in range(level_count):
                level_res = util.icSpcDefStruct(copy.deepcopy(spravlevel.ic_class_spc), None)
                level_res['name'] = 'lvl%d' % (i_level + 1) + name_lat
                level_res['description'] = u''
                level_len = self._get_sprav_spravlevel_len()
                level_res['len'] = level_len
                res['child'].append(level_res)

        return res

    def _gen_sprav(self, prj_res_ctrl=None):
        """
        Генерация ресурса справочника 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса 1С не взможна.')
            return False

        sprav_res = self._gen_sprav_res(prj_res_ctrl, name=self.name,
                                        description=self.description, uuid=self.uid)

        res_name = DEFAULT_SPRAV_RES
        # Загрузить ресурс
        res = prj_res_ctrl.loadRes(res_name, 'mtd')

        child_names = [child['name'] for child in res['child']]
        if sprav_res['name'] in child_names:
            del res['child'][child_names.index(sprav_res['name'])]
        res['child'].append(sprav_res)

        # Сохранить ресурс
        prj_res_ctrl.saveRes(res_name, 'mtd', res)
        return True
