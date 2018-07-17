#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента регистра накопления конфигурации 1с.
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


class icCFAccRegDimension(iccfobject.icCFObject):
    """
    Класс элемента измерения регистра накопления.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self, uid=iccfobject.ANY_UID, *args, **kwargs)

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'ruler.png')
        self.description = u''
        # Тип реквизита
        self.type_value = None

    def init(self, res=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if res is None:
            return

        self.name = res[0][1][1][1][2]
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


class icCFAccRegResource(iccfobject.icCFObject):
    """
    Класс элемента ресурса регистра накопления.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self, uid=iccfobject.ANY_UID, *args, **kwargs)

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'puzzle.png')
        self.description = u''
        # Тип реквизита
        self.type_value = None

    def init(self, res=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if res is None:
            return

        self.name = res[0][1][1][1][2]
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


class icCFAccRegRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита регистра накопления.
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

        self.name = res[0][1][1][1][2]
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


class icCFAccRegistry(iccfobject.icCFObject):
    """
    Класс элемента регистра накопления конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.description = u''
        
        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'table-money.png')

        # Измерения
        self.dimensions = list()

        # Ресурсы
        self.resources = list()

        # Реквизиты
        self.requisites = list()

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

        self.name = cf_doc_res.data[1][13][1][2]
        # if unicode(self.name, 'utf-8') == u'СвободныеОстатки':
        #     util1c.print_idx_paths(cf_doc_res.data)
        #     import sys
        #     sys.exit(1)

        self.description = u''
        if len(cf_doc_res.data[1][13][1][3]) > 1:
            self.description = unicode(cf_doc_res.data[1][13][1][3][2], 'utf-8')

        # Измерения
        for res in cf_doc_res.data[7][2:]:
            dimension = icCFAccRegDimension(self)
            dimension.init(res)
            self.dimensions.append(dimension)

        # Ресурсы
        for res in cf_doc_res.data[5][2:]:
            resource = icCFAccRegResource(self)
            resource.init(res)
            self.resources.append(resource)

        # Реквизиты
        for res in cf_doc_res.data[6][2:]:
            requisite = icCFAccRegRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)

        self.children = [iccfobject.icCFFolder(parent=self,
                                               name=u'Измерения', children=self.dimensions,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'ruler-crop.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Ресурсы', children=self.resources,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'puzzle.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Реквизиты', children=self.requisites,
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
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса таблицы хранения справочника <%s> 1С не взможна.' % self.name)
            return False
        else:
            log.debug(u'Контроллер управления ресурсом проекта <%s>' % prj_res_ctrl)
        prj_res_ctrl.openPrj()

        # Создать необходимые ресурсные файлы
        self._gen_registry(prj_res_ctrl)

        return True

    def _gen_registry_res(self, prj_res_ctrl=None, name=None, description=u'',
                          uuid=iccfobject.NONE_UID):
        """
        Генерация ресурса регистра накопления 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @param name: Наименование объекта ресурса.
        @param description: Описание объекта ресурса.
        @param uuid: Уникальный идентификатор объекта ресурса.
        @return: Ресурс справочника перечисления 1С.
        """
        from work_flow.usercomponents import acc_registry
        from work_flow.usercomponents import requisite
        from work_flow.usercomponents import nsi_requisite

        # Преобразовать русское наименование из 1С в латинское
        name_lat = ic_str.rus2lat(name)
        res = util.icSpcDefStruct(copy.deepcopy(acc_registry.ic_class_spc), None)
        res['name'] = name_lat
        res['_uuid'] = uuid
        res['description'] = description
        res['db'] = self._get_db_psp(prj_res_ctrl)
        res['dimension_requisites'] = [ic_str.rus2lat(cf_requisite.name) for cf_requisite in self.dimensions]
        res['resource_requisites'] = [ic_str.rus2lat(cf_requisite.name) for cf_requisite in self.resources]
        res['operation_table'] = name_lat + '_operation_tab'
        res['result_table'] = name_lat + '_result_tab'

        # Добавляем реквизиты
        all_requisites = self.dimensions + self.resources + self.requisites
        for cf_requisite in all_requisites:
            if cf_requisite.type_value[0] == iccfobject.REF_SIGNATURE_1C:
                # Если это ссылка, то считаем что это ссылка на справочник
                requisite_res = util.icSpcDefStruct(copy.deepcopy(nsi_requisite.ic_class_spc), None)
            else:
                requisite_res = util.icSpcDefStruct(copy.deepcopy(requisite.ic_class_spc), None)
                requisite_res['type_val'] = cf_requisite._gen_field_type_res()
            requisite_res['name'] = ic_str.rus2lat(cf_requisite.name)
            requisite_res['_uuid'] = cf_requisite.uid
            requisite_res['description'] = cf_requisite.description
            requisite_res['label'] = cf_requisite.description
            res['child'].append(requisite_res)

        return res

    def _gen_registry(self, prj_res_ctrl=None):
        """
        Генерация ресурса регистра накопления 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса 1С не взможна.')
            return False

        reg_res = self._gen_registry_res(prj_res_ctrl, name=self.name,
                                         description=self.description, uuid=self.uid)

        res_name = ic_str.rus2lat(self.name)

        if prj_res_ctrl.isRes(res_name, 'mtd'):
            prj_res_ctrl.delRes(res_name, 'mtd')

        # Сохранить ресурс
        prj_res_ctrl.saveRes(res_name, 'mtd', reg_res)
        return True
