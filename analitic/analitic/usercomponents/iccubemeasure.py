#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мера/Фактические данные OLAP Куба.
"""

from ic.log import log
from ic.bitmap import ic_bmp
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from analitic.olap import cube_measure_proto

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubeMeasure'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubeMeasure',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'field_name': None,  # Альтернативное название поля факта в таблице куба,
                                     # Если не определено, то используется имя объекта
                'label': None,  # Надпись, если не определена, то берется description

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'field_name', 'label'],
                                   },
                '__parent__': cube_measure_proto.SPC_IC_CUBEMEASURE,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('measure.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('measure.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icCubeMeasure(icwidget.icSimple,
                    cube_measure_proto.icCubeMeasureProto):
    """
    Мера/Фактические данные OLAP Куба.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        cube_measure_proto.icCubeMeasureProto.__init__(self)

    def getFieldName(self):
        """
        Имя поля факта в таблице куба.
        """
        field_name = self.getICAttr('field_name')
        if not field_name:
            field_name = self.getName()
        return field_name

    def getLabel(self):
        """
        Надпись, если не определена, то берется description.
        """
        label = self.getICAttr('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

