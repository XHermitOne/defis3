#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент уровня каталога.
"""

from ic.utils import util
from ic.bitmap import ic_bmp
from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.log import log
from ic.utils import coderror

from STD.cataloger import level_proto as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCatalogLevel'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'CatalogLevel',

                'get_folder_name': None,

                '__attr_types__': {0: ['name', 'type'],
                                   },

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'get_folder_name': u'Функция получеия имени папки',
                                 },
                }

ic_class_pic = ic_bmp.createLibraryBitmap('folder_brick.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('folder_brick.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 0, 0, 3)


class icCatalogLevel(icwidget.icSimple, parentModule.icCatalogLevelProto):
    """
    Компонент уровня каталога.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
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

        parentModule.icCatalogLevelProto.__init__(self)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        if self.isGetFolderNameFunc():
            self._get_folder_name_func = self.getFolderNameFunc
        else:
            log.warning(u'Не определена функция определения имени папки уровня каталога <%s>' % self.name)
            self._get_folder_name_func = None

    def isGetFolderNameFunc(self):
        """
        Определена функция получения имени папки расположения объекта?
        @return: True/False.
        """
        return self.isICAttrValue('get_folder_name')

    def getFolderNameFunc(self, obj):
        """
        Функция получения имени папки расположения объекта по
        самому объекту.
        @param obj: Каталогизируемый (размещаемый в каталоге) объект.
        @return: Строковое имя папки.
        """
        context = self.GetContext()
        context['OBJ'] = obj
        result = self.eval_attr('get_folder_name')
        if result[0] == coderror.IC_EVAL_OK:
            log.debug(u'Папка размещения <%s>' % result[1])
            return result[1]
        else:
            log.warning(u'Каталогизатор. Ошибка определения имени папки по уровню <%s>' % self.name)
        return self.name
