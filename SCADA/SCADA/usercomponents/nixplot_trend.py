#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Компонент реализован на утилите nixplot.

Тренд позволяет отображать данные только в пределах суток.
"""

import wx

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import bmpfunc

from SCADA.nixplot_trend_ctrl import nixplot_trend_proto
from SCADA.scada_proto import trend_proto

# --- Спецификация ---
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icNixplotTrend'

#   Описание стилей компонента
ic_class_styles = 0

DEFAULT_X_FORMATS = ('time', 'date', 'datetime')
DEFAULT_Y_FORMATS = ('numeric', )

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'NixplotTrend',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                'x_format': trend_proto.DEFAULT_X_FORMAT,  # Формат представления данных оси X
                'y_format': trend_proto.DEFAULT_Y_FORMAT,  # Формат представления данных оси Y
                'scene_min': ('00:00:00', 0.0),    # Минимальное значение видимой сцены тренда
                'scene_max': ('12:00:00', 0.0),    # Максимальное значение видимой сцены тренда
                'x_tunes': nixplot_trend_proto.DEFAULT_X_TUNES,     # Возможные настройки шкалы X
                'y_tunes': nixplot_trend_proto.DEFAULT_Y_TUNES,     # Возможные настройки шкалы Y
                'x_precision': nixplot_trend_proto.DEFAULT_X_PRECISION,  # Цена деления сетки тренда по шкале X
                'y_precision': nixplot_trend_proto.DEFAULT_Y_PRECISION,  # Цена деления сетки тренда по шкале Y

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'x_format': list(DEFAULT_X_FORMATS),
                              'y_format': list(DEFAULT_Y_FORMATS),
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            'x_precision', 'y_precision'],
                                   icDefInf.EDT_CHOICE: ['x_format', 'y_format'],
                                   icDefInf.EDT_TEXTLIST: ['x_tunes', 'y_tunes'],
                                   },
                '__parent__': nixplot_trend_proto.SPC_IC_NIXPLOT_TREND,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('diagramm.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('diagramm.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.nixplot_trend.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 2)


class icNixplotTrend(icwidget.icWidget,
                     nixplot_trend_proto.icNixplotTrendProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на утилите nixplot.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        nixplot_trend_proto.icNixplotTrendProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        # Инициализация внутренного состояния контрола:

        # Шкалы настройки
        self.setTunes(self.x_tunes, self.y_tunes)
        # Цена деления
        self.setPrecisions(self.x_precision, self.y_precision)
        # Формат шкал
        self.setFormats(self.x_format, self.y_format)

        # Текущая сцена тренда - Границы окна сцены в данных предметной области.
        # Представляется в виде кортежа (X1, Y1, X2, Y2)
        self.setScene(self.scene_min[0], self.scene_min[1], self.scene_max[0], self.scene_max[1])

        # отрисовать в соответствии с внутренним состоянием
        # self.draw()

    def setPens(self, pens):
        """
        Установить перья тренда.

        :param pens: Описания перьев.
        :return: True/False.
        """
        self.components['child'] = pens
        self.child = pens
        self.childCreator()

        self.adaptScene()

    def getPens(self):
        """
        Список перьев тренда.
        """
        pens = self.get_children_lst()
        if not pens:
            log.warning(u'Не определены перья тренда <%s>' % self.name)
        return pens

