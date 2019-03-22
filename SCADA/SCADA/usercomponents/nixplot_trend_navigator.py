#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель навигации тренда на базе утилиты nixplot.
"""

import wx

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import ic_bmp

from SCADA.nixplot_trend_ctrl import nixplot_trend_proto
from SCADA.nixplot_trend_ctrl import nixplot_trend_navigator_proto


# --- Спецификация ---
DEFAULT_FORMATS = (nixplot_trend_proto.DEFAULT_TIME_FMT,
                   nixplot_trend_proto.DEFAULT_DATETIME_FMT,
                   nixplot_trend_proto.DEFAULT_DATE_FMT)

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icNixplotTrendNavigator'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'NixplotTrendNavigator',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'time_axis_fmt': list(DEFAULT_FORMATS)},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            ],
                                   },
                '__parent__': nixplot_trend_navigator_proto.SPC_IC_NIXPLOT_TREND_NAVIGATOR,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('chart_curve_edit.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('chart_curve_edit.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icNixplotTrendNavigator(icwidget.icWidget,
                              nixplot_trend_navigator_proto.icNixplotTrendNavigatorProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на утилите nixplot.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        nixplot_trend_navigator_proto.icNixplotTrendNavigatorProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

        self.draw()

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getPens(self):
        """
        Список перьев тренда.
        """
        pens = self.get_children_lst()
        if not pens:
            log.warning(u'Не определены перья тренда <%s>' % self.name)
        return pens

