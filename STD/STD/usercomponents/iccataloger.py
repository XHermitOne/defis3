#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент каталогизатора.
"""

import os
import os.path
from ic.utils import util
from ic.bitmap import bmpfunc
from ic.log import log
from ic.utils import coderror
from ic.PropertyEditor import icDefInf
from ic.components import icwidget
import ic.components.icResourceParser as prs

from STD.cataloger import cataloger_proto as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCataloger'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'Cataloger',
                'child': [],
                '_uuid': None,

                'folder': None,    # Папка размещения физического каталога
                'put_physic_func': None,
                'get_physic_func': None,
                'logic_catalogs': None,

                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_DIR: ['folder'],
                                   icDefInf.EDT_DICT: ['logic_catalogs'],
                                   },

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'folder': u'Папка размещения физического каталога',
                                 'put_physic_func': u'Функция размещения в физическом каталоге',
                                 'get_physic_func': u'Фукнция получения из физического каталога',
                                 'logic_catalogs': u'Логические каталоги',
                                 },
                }

ic_class_pic = bmpfunc.createLibraryBitmap('folders_explorer.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('folders_explorer.png')

#   Путь до файла документации
ic_class_doc = 'STD/doc/_build/html/STD.usercomponents.iccataloger.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['CatalogLevel']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icCataloger(icwidget.icSimple, parentModule.icCatalogerProto):
    """
    Компонент каталогизатора.

    :type component_spc: C{dictionary}
    :cvar component_spc: Specification.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icCatalogerProto.__init__(self)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        # Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        # Список уровней физического каталога
        self.physic_catalog = self.get_children_lst()

        if self.isPutPhysicFunc():
            self._put_physic_func = self.putPhysicFunc
        if self.isGetPhysicFunc():
            self._get_physic_func = self.getPhysicFunc

        # Определить физическую папку размещения каталога
        self.physic_catalog_folder = self.getFolder()

    def getFolder(self):
        """
        Путь к папке размещения документов.
        """
        folder = self.getICAttr('folder')

        # Если папки размещения не существует, то создать ее
        if folder and os.path.isabs(folder) and not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except OSError:
                log.fatal(u'Ошибка создания папки размещения документов каталогизатора <%s>' % self.name)
        return folder

    def isPutPhysicFunc(self):
        """
        Определена функция расположения в каталогизаторе?

        :return: True/False.
        """
        return self.isICAttrValue('put_physic_func')

    def isGetPhysicFunc(self):
        """
        Определена функция получения объекта из каталогизатора?

        :return: True/False.
        """
        return self.isICAttrValue('get_physic_func')

    def putPhysicFunc(self, obj, physic_path):
        """
        Функция помещения объекта в физический каталог.

        :param obj: Размещаемый в физическом каталоге объект.
        :param physic_path: Путь размещения объекта в физическом каталоге.
        :return: True/False.
        """
        context = self.GetContext()
        context['OBJ'] = obj
        context['PHYSIC_PATH'] = physic_path
        context['PATH'] = physic_path
        result = self.eval_attr('put_physic_func')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Каталогизатор <%s>. Ошибка помещения объекта в физический каталог. Путь <%s>' % (self.name,
                                                                                                           physic_path))
        return False

    def getPhysicFunc(self, physic_path):
        """
        Функция получения объекта из физического каталога.

        :param physic_path: Путь размещения объекта в физическом каталоге.
        :return: Объект/Имя файла, размещенного в физическом каталоге.
        """
        context = self.GetContext()
        context['PHYSIC_PATH'] = physic_path
        context['PATH'] = physic_path
        result = self.eval_attr('get_physic_func')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Каталогизатор <%s>. Ошибка получения объекта из физического каталога. Путь <%s>' % (self.name,
                                                                                                              physic_path))
        return None
