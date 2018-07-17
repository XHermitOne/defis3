#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента регистра сведений конфигурации 1с.
"""

import os
import os.path

from . import iccfresource
from . import iccfobject

from ic.log import log
from ic.utils import util1c


__version__ = (0, 0, 0, 2)


class icCFInfoRegDimension(iccfobject.icCFObject):
    """
    Класс элемента измерения регистра сведений.
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


class icCFInfoRegResource(iccfobject.icCFObject):
    """
    Класс элемента ресурса регистра сведений.
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


class icCFInfoRegRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита регистра сведений.
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

        self.name = res[0][1][1][1][2]
        try:
            self.description = unicode(res[0][1][1][1][3][2], 'utf-8')
        except:
            self.description = u''


class icCFInfoRegistry(iccfobject.icCFObject):
    """
    Класс элемента регистра сведений конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.description = ''
        
        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'table-join.png')

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
            dimension = icCFInfoRegDimension(self)
            dimension.init(res)
            self.dimensions.append(dimension)

        # Ресурсы
        for res in cf_doc_res.data[5][2:]:
            resource = icCFInfoRegResource(self)
            resource.init(res)
            self.resources.append(resource)

        # Реквизиты
        for res in cf_doc_res.data[6][2:]:
            requisite = icCFInfoRegRequisite(self)
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
