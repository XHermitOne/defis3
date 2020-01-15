#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель навигации тренда на базе утилиты gnuplot.
"""

import wx

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import bmpfunc

from SCADA.gnuplot_trend_ctrl import gnuplot_trend_navigator_proto
from SCADA.gnuplot_trend_ctrl import gnuplot_trend_proto
from SCADA.scada_proto import trend_proto


# --- Спецификация ---

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icGnuplotTrendNavigator'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'GnuplotTrendNavigator',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                'show_legend': True,

                'x_format': trend_proto.DEFAULT_X_FORMAT,  # Формат представления данных оси X
                'y_format': trend_proto.DEFAULT_Y_FORMAT,  # Формат представления данных оси Y
                'scene_min': ('00:00:00', 0.0),  # Минимальное значение видимой сцены тренда
                'scene_max': ('12:00:00', 100.0),  # Максимальное значение видимой сцены тренда
                'adapt_scene': False,  # Признак адаптации сцены по данным

                'x_precision': gnuplot_trend_proto.DEFAULT_X_PRECISION,  # Цена деления сетки тренда по шкале X
                'y_precision': gnuplot_trend_proto.DEFAULT_Y_PRECISION,  # Цена деления сетки тренда по шкале Y

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            ],
                                   },
                '__parent__': gnuplot_trend_navigator_proto.SPC_IC_GNUPLOT_TREND_NAVIGATOR,

                '__attr_hlp__': {'x_format': u'Формат представления данных оси X',
                                 'y_format': u'Формат представления данных оси Y',
                                 'x_precision': u'Цена деления сетки тренда по шкале X',
                                 'y_precision': u'Цена деления сетки тренда по шкале Y',
                                 'scene_min': u'Минимальное значение видимой сцены тренда',
                                 'scene_max': u'Максимальное значение видимой сцены тренда',
                                 'adapt_scene': u'Признак адаптации сцены по данным',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart_curve_edit.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart_curve_edit.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.gnuplot_trend_navigator.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 2)


class icGnuplotTrendNavigator(icwidget.icWidget,
                              gnuplot_trend_navigator_proto.icGnuplotTrendNavigatorProto):
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
        gnuplot_trend_navigator_proto.icGnuplotTrendNavigatorProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        # Передаем тренду основные атрибуты

        # Перья определенные в навигаторе передаем тренду
        self.setPens(self.child)

        # self.draw()

        # Установить переключатель легенды
        self.setIsShowLegend(self.show_legend)

        # self.loadTrendSplitterSashPos()

        # ВНИМАНИЕ! Если необходимо удалить/освободить
        # ресуры при удалении контрола, то необходимо воспользоваться
        # событием wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def onDestroy(self, event):
        """
        При удалении панели. Обработчик события.
        ВНИМАНИЕ! Если необходимо удалить/освободить
        ресуры при удалении контрола, то необходимо воспользоваться
        событием wx.EVT_WINDOW_DESTROY.
        """
        self.saveTrendSplitterSashPos()

    def setPens(self, pens):
        """
        Установить перья тренда.

        :param pens: Описания перьев.
        :return: True/False.
        """
        # Заполнить легенду
        self.setLegend(pens)
        return self.trend.setPens(pens)

    def getPens(self):
        """
        Список перьев тренда.
        """
        return self.trend.getPens()

    def saveTrendSplitterSashPos(self):
        """
        Сохранить позицию сплиттера разделения легенды и тренда.
        """
        return self.save_ext_data(self.name, sash_pos=self.trend_splitter.GetSashPosition())

    def loadTrendSplitterSashPos(self, is_update_size=True):
        """
        Загрузить позицию сплиттера разделения легенды и тренда.

        :param is_update_size: Произвести обновление размера?
        """
        save_data = self.load_ext_data(self.name)
        default_sash_pos = self.trend_splitter.GetSashPosition() if self.show_legend else 1
        result = self.trend_splitter.SetSashPosition(save_data.get('sash_pos', default_sash_pos))
        if is_update_size:
            self.trend_splitter.UpdateSize()
        return result

    def setXFormat(self, x_format=None):
        """
        Формат представления данных оси X. Установка в тренде.

        :param x_format: Формат представления данных оси X.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if x_format is None:
            x_format = self.getICAttr('x_format')
        trend = self.getTrend()
        return trend.setXFormat(x_format)

    def setYFormat(self, y_format=None):
        """
        Формат представления данных оси Y. Установка в тренде.

        :param y_format: Формат представления данных оси Y.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if y_format is None:
            y_format = self.getICAttr('y_format')
        trend = self.getTrend()
        return trend.setYFormat(y_format)

    def setSceneMin(self, scene_min=None):
        """
        Минимальные значения видимой сцены тренда. Установка в тренде.

        :param scene_min: Минимальные значения видимой сцены тренда.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if scene_min is None:
            scene_min = self.getICAttr('scene_min')
        trend = self.getTrend()
        return trend.setSceneMin(scene_min)

    def setSceneMax(self, scene_max=None):
        """
        Максимальные значение видимой сцены тренда. Установка в тренде.

        :param scene_max: Максимальные значение видимой сцены тренда.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if scene_max is None:
            scene_max = self.getICAttr('scene_max')
        trend = self.getTrend()
        return trend.setSceneMax(scene_max)

    def setAdaptScene(self, adapt_scene=None):
        """
        Признак адаптации сцены по данным. Установка в тренде.

        :param adapt_scene: Признак адаптации сцены по данным.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if adapt_scene is None:
            adapt_scene = self.getICAttr('adapt_scene')
        trend = self.getTrend()
        return trend.setAdaptScane(adapt_scene)

    def setXPrecision(self, x_precision=None):
        """
        Цена деления сетки тренда по шкале X. Установка в тренде.

        :param x_precision: Цена деления сетки тренда по шкале X.
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if x_precision is None:
            x_precision = self.getICAttr('x_precision')
        trend = self.getTrend()
        return trend.setXPrecision(x_precision)

    def setYPrecision(self, y_precision=None):
        """
        Цена деления сетки тренда по шкале Y. Установка в тренде.

        :param y_precision: Цена деления сетки тренда по шкале Y
            Если не определено, то берется из ресурсного описания объекта.
        :return:
        """
        if y_precision is None:
            y_precision = self.getICAttr('y_precision')
        trend = self.getTrend()
        return trend.setYPrecision(y_precision)
