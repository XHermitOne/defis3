#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Куб.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.components import icResourceParser as prs

from analitic.olap import cube_proto

from ..olap import cube_dimension_proto
from ..olap import cube_measure_proto
from ..olap import cube_aggregate_proto


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCube'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'Cube',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'table_name': None,  # Альтернативное название таблицы куба в БД,
                                     # Если не определено, то используется имя куба
                'label': None,  # Надпись, если не определена, то берется description

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'table_name', 'label'],
                                   },
                '__parent__': cube_proto.SPC_IC_CUBE,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('soil_layers.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('soil_layers.png')

#   Путь до файла документации
ic_class_doc = 'analitic/doc/_build/html/analitic.usercomponents.iccube.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['CubeDimension', 'CubeMeasure', 'CubeAggregate']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icCube(icwidget.icSimple, cube_proto.icCubeProto):
    """
    OLAP Куб.
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

        cube_proto.icCubeProto.__init__(self)
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getTableName(self):
        """
        Имя таблицы куба.
        """
        table_name = self.getICAttr('table_name')
        if not table_name:
            table_name = self.getName()
        return table_name

    def getDimensions(self):
        """
        Список объектов измерений
        """
        return [child for child in self.component_lst if isinstance(child, cube_dimension_proto.icCubeDimensionProto)]

    def getMeasures(self):
        """
        Список объектов мер/фактов.
        """
        return [child for child in self.component_lst if isinstance(child, cube_measure_proto.icCubeMeasureProto)]

    def getAggregates(self):
        """
        Список объектов функций аггрегаций.
        """
        return [child for child in self.component_lst if isinstance(child, cube_aggregate_proto.icCubeAggregateProto)]

    def getLabel(self):
        """
        Надпись, если не определена, то берется description.
        Если и в этом случае не определено, то берем name.
        """
        label = self.getICAttr('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

    def getChildren(self):
        """
        Список дочерних элементов.
        """
        return self.component_lst
