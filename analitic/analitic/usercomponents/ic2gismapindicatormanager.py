#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления индикациеей на гео-картах на базе 2GIS.
Документация по API 2GIS https://api.2gis.ru/doc/maps/ru/quickstart/.

В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.

В качестве системы определения геолокации по адресу используется Yandex.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.components import icResourceParser as prs

from ..indicators import double_gis_map_indicator_manager

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'ic2GISMapIndicatorManager'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'DoubleGISMapIndicatorManager',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   },
                '__parent__': double_gis_map_indicator_manager.SPC_IC_2GISMAPINDICATORMANAGER,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('map-pin.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('map-pin.png')

#   Путь до файла документации
ic_class_doc = 'analitic/doc/_build/html/analitic.usercomponents.ic2gismapindicatormanager.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class ic2GISMapIndicatorManager(icwidget.icWidget,
                                double_gis_map_indicator_manager.ic2GISMapIndicatorManagerProto):
    """
    Менеджер управления индикациеей на гео-картах.
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
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        double_gis_map_indicator_manager.ic2GISMapIndicatorManagerProto.__init__(self)
