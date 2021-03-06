#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Измерение OLAP Куба.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from analitic.olap import cube_dimension_proto
from analitic.olap import cube_dimension_level_proto
from analitic.olap import cube_dimension_hierarchy_proto

import ic.components.icResourceParser as prs

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubeDimension'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubeDimension',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'field_name': None,  # Альтернативное название поля измерения в таблице куба,
                                     # Если не определено, то используется имя объекта
                'detail_tabname': None,  # Имя таблицы детализации, связанной с полем таблицы куба
                'detail_fldname': None,  # Имя поля таблицы детализации, по которому осуществляется связь
                'attributes': None,  # Список имен полей дополнительных атрибутов
                'label': None,  # Надпись измерения
                'mapping': None,  # Физичекое указание поля для отображения

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'field_name',
                                                            'detail_tabname', 'detail_fldname',
                                                            'label', 'mapping'],
                                   icDefInf.EDT_TEXTLIST: ['attributes'],
                                   },
                '__parent__': cube_dimension_proto.SPC_IC_CUBEDIMENSION,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('proportion.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('proportion.png')

#   Путь до файла документации
ic_class_doc = 'analitic/doc/_build/html/analitic.usercomponents.iccubedimension.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['CubeDimensionLevel', 'CubeDimensionHierarchy']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icCubeDimension(icwidget.icSimple,
                      cube_dimension_proto.icCubeDimensionProto):
    """
    Измерение OLAP Куба.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        cube_dimension_proto.icCubeDimensionProto.__init__(self)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

    def getFieldName(self):
        """
        Имя поля измерения в таблице куба.
        """
        field_name = self.getICAttr('field_name')
        if not field_name:
            field_name = self.getName()
        return field_name

    def getMapping(self):
        """
        Физичекое указание поля для отображения измерения.
        """
        return self.getICAttr('mapping')

    def getAttributes(self):
        """
        Список имен полей дополнительных атрибутов
        """
        attributes = self.getICAttr('attributes')
        return [attribute for attribute in attributes if attribute] if attributes else list()

    def getDetailTableName(self):
        """
        Имя таблицы детализации, связанной с полем таблицы куба.
        """
        detail_tabname = self.getICAttr('detail_tabname')
        return detail_tabname if detail_tabname else self.getName()

    def getDetailFieldName(self):
        """
        Имя поля таблицы детализации, по которому осуществляется связь.
        """
        return self.getICAttr('detail_fldname')

    def getLabel(self):
        """
        Надпись измерения.
        Если не определено, то берется description.
        Если и в этом случае не определено, то берем name.
        """
        label = self.getICAttr('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

    def getLevels(self):
        """
        Список объектов уровней измерения.
        """
        # Нужно отфильтровать дочерние объекты
        return [child for child in self.component_lst if isinstance(child, cube_dimension_level_proto.icCubeDimensionLevelProto)]

    def getHierarchies(self):
        """
        Список объектов иерархий уровней измерения.
        """
        # Нужно отфильтровать дочерние объекты
        return [child for child in self.component_lst if isinstance(child, cube_dimension_hierarchy_proto.icCubeDimensionHierarchyProto)]
