#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Компонент реализован на утилите gnuplot.

Тренд позволяет отображать данные только в пределах суток.
"""

import datetime
import wx

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import bmpfunc

from SCADA.gnuplot_trend_ctrl import gnuplot_trend_proto
from SCADA.scada_proto import trend_proto


# --- Спецификация ---

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icGnuplotTrend'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'GnuplotTrend',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                'x_format': trend_proto.DEFAULT_X_FORMAT,  # Формат представления данных оси X
                'y_format': trend_proto.DEFAULT_Y_FORMAT,  # Формат представления данных оси Y
                'scene_min': ('00:00:00', 0.0),    # Минимальное значение видимой сцены тренда
                'scene_max': ('23:59:59', 100.0),    # Максимальное значение видимой сцены тренда
                'adapt_scene': False,  # Признак адаптации сцены по данным

                'x_precision': gnuplot_trend_proto.DEFAULT_X_PRECISION,  # Цена деления сетки тренда по шкале X
                'y_precision': gnuplot_trend_proto.DEFAULT_Y_PRECISION,  # Цена деления сетки тренда по шкале Y

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'x_format': list(trend_proto.DEFAULT_X_FORMATS),
                              'y_format': list(trend_proto.DEFAULT_Y_FORMATS),
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            'x_precision', 'y_precision'],
                                   icDefInf.EDT_CHOICE: ['x_format', 'y_format'],
                                   icDefInf.EDT_CHECK_BOX: ['adapt_scane'],
                                   icDefInf.EDT_PY_SCRIPT: ['scene_min', 'scene_max'],
                                   },
                '__parent__': gnuplot_trend_proto.SPC_IC_GNUPLOT_TREND,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('action_log.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('action_log.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.gnuplot_trend.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 3, 1)


class icGnuplotTrend(icwidget.icWidget,
                     gnuplot_trend_proto.icGnuplotTrendProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на утилите gnuplot.

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
        gnuplot_trend_proto.icGnuplotTrendProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        # Инициализация внутренного состояния контрола:
        self.setAdaptScene()
        self.setSceneMin()
        self.setSceneMax()

        self.setXFormat()
        self.setYFormat()

        self.setXPrecision()
        self.setYPrecision()

        # Шкалы настройки
        # self.setTunes(self.x_tunes, self.y_tunes)
        # Цена деления
        # self.setPrecisions(self.x_precision, self.y_precision)
        # Формат шкал
        # self.setFormats(self.x_format, self.y_format)

        # Текущая сцена тренда - Границы окна сцены в данных предметной области.
        # Представляется в виде кортежа (X1, Y1, X2, Y2)
        # self.setScene(self.scene_min[0], self.scene_min[1], self.scene_max[0], self.scene_max[1])

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
        self.createChildren(children=pens)

        if self.isAdaptScene():
            self.adaptScene()
        else:
            dt_min, y_min = self.getSceneMin()
            dt_max, y_max = self.getSceneMax()
            self.setScene(min_x=dt_min, min_y=y_min, max_x=dt_max, max_y=y_max)

        # Установить цвет линий перьев
        self._set_pens_colour()

    def _set_pens_colour(self, pens=None, manager=None):
        """
        Установить цвет линий перьев.

        :param pens: Список объектов перьев.
        :param manager: Менеджер управления утилитой gnuplot.
        :return: True/False.
        """
        if pens is None:
            pens = self.get_children_lst()
        if manager is None:
            manager = self._getManager()
        for i, pen in enumerate(pens):
            self._set_pen_colour(n_pen=i + 1, pen=pen, manager=manager)

    def _set_pen_colour(self, n_pen, pen, manager=None):
        """
        Установить цвет линии пера.

        :param n_pen: Номер пера.
        :param pen: Объект пера.
        :param manager: Менеджер управления утилитой gnuplot.
        :return: True/False.
        """
        if manager is None:
            manager = self._getManager()
        try:
            str_colour = pen.getColourStr()
            log.debug(u'Цвет пера [%d] <%s>' % (n_pen, str_colour))
            if str_colour:
                manager.setLineStyle(n_line=n_pen, line_color=str_colour)
        except:
            log.fatal(u'Ошибка установки цвета пера тренда <%d>' % n_pen)

    def getPens(self):
        """
        Список перьев тренда.
        """
        pens = self.get_children_lst()
        if not pens:
            log.warning(u'Не определены перья тренда <%s>' % self.name)
        return pens

    def isAdaptScene(self):
        """
        Произвести адаптацию сцены тренда по данным?
        """
        if self.adapt_scene is None:
            self.adapt_scene = self.getICAttr('adapt_scene')
        return self.adapt_scene

    def getSceneMin(self):
        """
        Минимальные значения сцены.
        """
        if self.scene_min:
            scene_min = self.scene_min
        else:
            scene_min = self.getICAttr('scene_min')
        if scene_min and isinstance(scene_min, str):
            try:
                scene_min = eval(scene_min)
            except:
                log.fatal(u'Ошибка формата минимальных значений сцены')
                log.warning(u'Минимальные значения должны задаваться кортежем. Например (\'00:00:00\', 0.0)')
                scene_min = ('00:00:00', 0.0)
        dt_min = self._str2dt(scene_min[0], self.x_format) if isinstance(scene_min[0], str) else scene_min[0]
        y_min = float(scene_min[1])
        self.scene_min = (dt_min, y_min)
        return dt_min, y_min

    def getSceneTimeMin(self):
        """
        Минимальное значение сцены по временной оси.
        """
        scene_min = self.getSceneMin()
        return scene_min[0]

    def getSceneYMin(self):
        """
        Минимальное значение сцены по оси значений.
        """
        scene_min = self.getSceneMin()
        return scene_min[1]

    def getSceneMax(self):
        """
        Максимальные значения сцены.
        """
        if self.scene_max:
            scene_max = self.scene_max
        else:
            scene_max = self.getICAttr('scene_max')
        if scene_max and isinstance(scene_max, str):
            try:
                scene_max = eval(scene_max)
            except:
                log.fatal(u'Ошибка формата максимальных значений сцены')
                log.warning(u'Максимальные значения должны задаваться кортежем. Например (\'00:00:00\', 0.0)')
                scene_max = ('23:59:59', 100.0)
        dt_max = self._str2dt(scene_max[0], self.x_format) if isinstance(scene_max[0], str) else scene_max[0]
        y_max = float(scene_max[1])
        self.scene_max = (dt_max, y_max)
        return dt_max, y_max

    def getSceneTimeMax(self):
        """
        Максимальное значение сцены по временной оси.
        """
        scene_max = self.getSceneMax()
        return scene_max[0]

    def getSceneYMax(self):
        """
        Максимальное значение сцены по оси значений.
        """
        scene_max = self.getSceneMax()
        return scene_max[1]

    def setXFormat(self, x_format=None):
        """
        Формат представления данных оси X. Установка

        :param x_format: Формат представления данных оси X.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if x_format is None:
            x_format = self.getICAttr('x_format')
        self.x_format = x_format
        # Формат шкал
        return self.setFormats(self.x_format, self.y_format)

    def setYFormat(self, y_format=None):
        """
        Формат представления данных оси Y. Установка.

        :param y_format: Формат представления данных оси Y.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if y_format is None:
            y_format = self.getICAttr('y_format')
        self.y_format = y_format
        # Формат шкал
        return self.setFormats(self.x_format, self.y_format)

    def setSceneMin(self, scene_min=None):
        """
        Минимальные значения видимой сцены тренда. Установка.

        :param scene_min: Минимальные значения видимой сцены тренда.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if scene_min is None:
            scene_min = self.getICAttr('scene_min')
        self.scene_min = scene_min

    def setSceneMax(self, scene_max=None):
        """
        Максимальные значение видимой сцены тренда. Установка.

        :param scene_max: Максимальные значение видимой сцены тренда.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if scene_max is None:
            scene_max = self.getICAttr('scene_max')
        self.scene_max = scene_max

    def setAdaptScene(self, adapt_scene=None):
        """
        Признак адаптации сцены по данным. Установка.

        :param adapt_scene: Признак адаптации сцены по данным.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if adapt_scene is None:
            adapt_scene = self.getICAttr('adapt_scene')
        self.adapt_scene = adapt_scene

    def setXPrecision(self, x_precision=None):
        """
        Цена деления сетки тренда по шкале X. Установка.

        :param x_precision: Цена деления сетки тренда по шкале X.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if x_precision is None:
            x_precision = self.getICAttr('x_precision')
        self.x_precision = x_precision
        # Цена деления
        return self.setPrecisions(self.x_precision, self.y_precision)

    def setYPrecision(self, y_precision=None):
        """
        Цена деления сетки тренда по шкале Y. Установка.

        :param y_precision: Цена деления сетки тренда по шкале Y
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if y_precision is None:
            y_precision = self.getICAttr('y_precision')
        self.y_precision = y_precision
        # Цена деления
        return self.setPrecisions(self.x_precision, self.y_precision)
