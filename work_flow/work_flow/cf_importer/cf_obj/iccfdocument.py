#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента документа конфигурации 1с.
"""

import copy
import os
import os.path

from . import iccfresource
from . import iccfobject
from . import iccfdocform

from ic.log import log
from ic.utils import util1c
from ic.utils import ic_str
from ic.utils import util
import ic


__version__ = (0, 0, 1, 1)


class icCFDocRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита документа.
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


class icCFDocTab(iccfobject.icCFObject):
    """
    Класс элемента табличной части документа.
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
            requisite = icCFDocTabRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)
            
        self.children = self.requisites        

    def _gen_tab_requisite_res(self):
        """
        Сгенерировать ресурс табличного реквизита.
        """
        from work_flow.usercomponents import requisite
        from work_flow.usercomponents import nsi_requisite
        from work_flow.usercomponents import tab_requisite

        # Преобразовать русское наименование из 1С в латинское
        name_lat = ic_str.rus2lat(self.name)
        res = util.icSpcDefStruct(copy.deepcopy(tab_requisite.ic_class_spc), None)
        res['name'] = name_lat
        res['_uuid'] = self.uid
        res['description'] = self.description
        res['label'] = self.description

        # Добавляем реквизиты
        for cf_requisite in self.requisites:
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


class icCFDocTabRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита табличной части документа.
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


class icCFDocument(iccfobject.icCFObject):
    """
    Класс элемента документа конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.description = ''
        
        # Список реквизитов документа
        self.requisites = []
        # Список табличных частей документа
        self.tabs = []
        # Список форм документа
        self.forms = []
        
        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', 'document-text.png')       
        
    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_doc_filename = os.path.join(os.path.abspath(self.cf_dir), 'metadata', self.uid)
        if not os.path.exists(cf_doc_filename):
            cf_doc_filename = os.path.join(os.path.abspath(self.cf_dir), self.uid)
        if not os.path.exists(cf_doc_filename):
            log.warning(u'Не найден файл <%s>' % cf_doc_filename)
            return

        cf_doc_res = iccfresource.icCFResource(cf_doc_filename)
        cf_doc_res.loadData()
        
        self.name = cf_doc_res.data[1][9][1][2]
        self.description = u''
        if len(cf_doc_res.data[1][9][1][3]) > 1:
            self.description = unicode(cf_doc_res.data[1][9][1][3][2], 'utf-8')
        
        # После определения имени метаобъекта можно изменить прогресс бар
        iccfobject.icCFObject.build(self)

        self.requisites = []
        for res in cf_doc_res.data[5][2:]:
            requisite = icCFDocRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)
        
        self.tabs = []
        for res in cf_doc_res.data[3][2:]:
            tab = icCFDocTab(self)
            tab.init(res)
            self.tabs.append(tab)

        frm_uid_lst = cf_doc_res.data[7][2:]
        self.forms = [iccfdocform.icCFDocForm(self, uid) for uid in frm_uid_lst]
        for frm in self.forms:
            frm.build()
            
        self.children = [iccfobject.icCFFolder(parent=self,
                                               name=u'Реквизиты', children=self.requisites,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'ui-buttons.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Табличные части', children=self.tabs,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'tables-stacks.png')),
                         iccfobject.icCFFolder(parent=self,
                                               name=u'Формы', children=self.forms,
                                               img_filename=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                                         'img', 'applications.png')),
                         ]

    # --- Функции изменения метаобъекта в конфигурации ---
    def createModule(self, txt=None):
        """
        Создать модуль.
        @param txt: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        module_dir = os.path.join(self.getCFDir(), self.uid+'.0')
        module_info = os.path.join(module_dir, 'info')
        module_txt = os.path.join(module_dir, 'text')
        
        if not os.path.isdir(module_dir):
            os.makedirs(module_dir)
        if not os.path.exists(module_info):
            file.createTxtFile(module_info, u'{3,1,0,"",0}')
        if not os.path.exists(module_txt):
            file.createTxtFile(module_txt, u' ')
        return True
        
    def addInModule(self, txt):
        """
        Добавить в модуль объекта текст.
        @param txt: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        txt = util1c.encodeText(txt)
        
        module_filename = os.path.join(self.getCFDir(), self.uid + '.0', 'text')
        if not os.path.exists(module_filename):
            return
        
        f = None
        try:
            f = open(module_filename, 'r')
            txt = f.read()
            f.close()
            f = None
            if txt not in txt:
                try:
                    f = open(module_filename, 'a')
                    f.write(txt)
                    f.close()
                except:
                    if f:
                        f.close()
                        f = None
                    raise
            return True
        except:
            if f:
                f.close()
                f = None
            raise
        return False

    def delInModule(self, txt):
        """
        Удалить из модуля объекта текст.
        @param txt: Удаляемый текст.
        @return: True - удаление прошло успешно, False - удаления не произошло.
        """
        txt = util1c.encodeText(txt)
        
        module_filename = os.path.join(self.getCFDir(), self.uid+'.0', 'text')
        
        f = None
        try:
            f = open(module_filename, 'w')
            txt = f.read()
            txt = txt.replace(txt, '')
            f.write(txt)
            f.close()
            return True
        except:
            if f:
                f.close()
                f = None
            raise
        return False
        
    def replaceInModule(self, srctxt, dsttxt):
        """
        Заменить текст в модуле объекта.
        @param srctxt: Заменяемый текст.
        @param dsttxt: Заменяющий текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        if self.delInModule(srctxt):
            return self.addInModule(dsttxt)
        return False

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
        self._gen_doc(prj_res_ctrl)

        return True

    def _gen_doc_res(self, prj_res_ctrl=None, name=None, description=u'',
                     uuid=iccfobject.NONE_UID):
        """
        Генерация ресурса дакумента 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @param name: Наименование объекта ресурса.
        @param description: Описание объекта ресурса.
        @param uuid: Уникальный идентификатор объекта ресурса.
        @return: Ресурс справочника перечисления 1С.
        """
        from work_flow.usercomponents import document
        from work_flow.usercomponents import requisite
        from work_flow.usercomponents import nsi_requisite

        # Преобразовать русское наименование из 1С в латинское
        name_lat = ic_str.rus2lat(name)
        res = util.icSpcDefStruct(copy.deepcopy(document.ic_class_spc), None)
        res['name'] = name_lat
        res['_uuid'] = uuid
        res['description'] = description
        res['db'] = self._get_db_psp(prj_res_ctrl)

        # Добавляем реквизиты
        for cf_requisite in self.requisites:
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

        # Добавляем табличные части
        for tab_requisite in self.tabs:
            requisite_res = tab_requisite._gen_tab_requisite_res()
            res['child'].append(requisite_res)

        return res

    def _gen_doc(self, prj_res_ctrl=None):
        """
        Генерация ресурса документа 1С.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return: True/False.
        """
        if prj_res_ctrl is None:
            log.warning(u'Не определен контроллер управления ресурсом проекта. Генерация ресурса 1С не взможна.')
            return False

        doc_res = self._gen_doc_res(prj_res_ctrl, name=self.name,
                                    description=self.description, uuid=self.uid)

        res_name = ic_str.rus2lat(self.name)

        if prj_res_ctrl.isRes(res_name, 'mtd'):
            prj_res_ctrl.delRes(res_name, 'mtd')

        # Сохранить ресурс
        prj_res_ctrl.saveRes(res_name, 'mtd', doc_res)
        return True

