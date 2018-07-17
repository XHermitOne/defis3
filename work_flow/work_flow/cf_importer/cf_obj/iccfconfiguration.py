#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента конфигурации.
"""

import os
import os.path

from . import iccfresource
from . import iccfobject
from . import iccfsprav
from . import iccfdocument
from . import iccfenum
from . import iccfaccreg
from . import iccfinforeg

from ic.log import log
from ic.utils import util1c
from ic.utils import ic_str


__version__ = (0, 0, 1, 1)

DEFAULT_ENCODING = 'utf-8'


class icCFConfiguration(iccfobject.icCFObject):
    """
    Класс элемента конфигурации.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)
        
        # Список справочников
        self.spravs = list()

        # Список документов
        self.documents = list()

        # Список перечислений
        self.enums = list()

        # Список регистров накопления
        self.acc_regs = list()

        # Список регистров сведений
        self.info_regs = list()

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'brightness.png')

    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_cfg_filename = os.path.join(os.path.abspath(self.cf_dir), 'metadata', self.uid)
        if not os.path.exists(cf_cfg_filename):
            cf_cfg_filename = os.path.join(os.path.abspath(self.cf_dir), self.uid)
        if not os.path.exists(cf_cfg_filename):
            log.warning(u'Не найден файл <%s>' % cf_cfg_filename)
            return

        cf_cfg_res = iccfresource.icCFResource(cf_cfg_filename)
        cf_cfg_res.loadData()

        if cf_cfg_res.data is None:
            log.warning(u'Ошибка загрузки данных дерева конфигурации')
            return
        
        self.name = ic_str.toUnicode(cf_cfg_res.data[3][1][1][1][1][2], DEFAULT_ENCODING)
        # После определения имени метаобъекта можно изменить прогресс бар
        iccfobject.icCFObject.build(self)

        log.info(u'CONFIGURATION RESOURCE: <%s>' % self.name)
        # util1c.print_idx_paths(cf_cfg_res.data)

        # idx = util1c.ValueIndexPath(cf_cfg_res.data, '4938909f-92f5-4cd8-992f-6c53996d1af9')

        # Справочники
        sprav_uid_lst = cf_cfg_res.data[4][1][1][16][2:]
        log.info(u'Количество справочников: <%d>' % len(sprav_uid_lst))
        self.spravs = [iccfsprav.icCFSprav(self, uid) for uid in sprav_uid_lst]
        for sprav in self.spravs:
            sprav.build()

        # Документы
        doc_uid_lst = cf_cfg_res.data[4][1][1][4][2:]
        log.info(u'Количество документов: <%d>' % len(doc_uid_lst))
        self.documents = [iccfdocument.icCFDocument(self, uid) for uid in doc_uid_lst]
        for doc in self.documents:
            doc.build()

        # Перечисления
        enum_uid_lst = cf_cfg_res.data[4][1][1][17][2:]
        log.info(u'Количество перечислений: <%d>' % len(enum_uid_lst))
        self.enums = [iccfenum.icCFEnum(self, uid) for uid in enum_uid_lst]
        for enum in self.enums:
            enum.build()

        # Регистры накопления
        acc_uid_lst = cf_cfg_res.data[4][1][1][13][2:]
        log.info(u'Количество регистров накопления: <%d>' % len(acc_uid_lst))
        self.acc_regs = [iccfaccreg.icCFAccRegistry(self, uid) for uid in acc_uid_lst]
        for acc_reg in self.acc_regs:
            acc_reg.build()

        # Регистры сведений
        info_uid_lst = cf_cfg_res.data[4][1][1][6][2:]
        log.info(u'Количество регистров сведений: <%d>' % len(info_uid_lst))
        self.info_regs = [iccfinforeg.icCFInfoRegistry(self, uid) for uid in acc_uid_lst]
        for info_reg in self.info_regs:
            info_reg.build()

        self.children = [iccfobject.icCFFolder(parent=self,
                                               name=u'Справочники', children=self.spravs,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'books-brown.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Документы', children=self.documents,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'documents-text.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Перечисления', children=self.enums,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'sort-alphabet.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Регистры накопления', children=self.acc_regs,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'table-money.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Регистры сведений', children=self.info_regs,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'table-join.png')),
                         ]
