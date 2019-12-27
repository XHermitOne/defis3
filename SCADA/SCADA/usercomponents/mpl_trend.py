#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Компонент реализован на библиотеке matplotlib.
"""

import wx
import datetime

import matplotlib
import matplotlib.dates
import matplotlib.figure
matplotlib.use('WXAgg')
import matplotlib.backends.backend_wxagg

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import bmpfunc

from SCADA.scada_proto import trend_proto

# --- Спецификация ---
SPC_IC_MPLTREND = {'time_axis_fmt': trend_proto.DEFAULT_TIME_FMT,   # Формат данных оси времени
                   'show_grid': True,   # Отображать сетку?
                   '__parent__': icwidget.SPC_IC_WIDGET,
                   '__attr_hlp__': {'time_axis_fmt': u'Формат данных оси времени',
                                    'show_grid': u'Отображать сетку?',
                                    },
                   }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMPLTrend'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MPLTrend',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'time_axis_fmt': list(trend_proto.DEFAULT_DT_FORMATS)},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            ],
                                   icDefInf.EDT_CHOICE: ['time_axis_fmt'],
                                   icDefInf.EDT_CHECK_BOX: ['show_grid'],
                                   },
                '__parent__': SPC_IC_MPLTREND,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart_line.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart_line.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.mpl_trend.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 2)


class icMPLTrendProto(wx.Panel, trend_proto.icTrendProto):
    """
    Базовый класс временного графика. Тренд.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Panel.__init__(self, *args, **kwargs)

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        trend_proto.icTrendProto.__init__(self, *args, **kwargs)

        self.setDefaults()

    def getTimeFormat(self):
        """
        Формат надписей временной оси.
        """
        return None

    def getShowGrid(self):
        """
        Отображать сетку?
        """
        return True

    def setDefaults(self):
        """
        Установить параметры по умолчанию.
        """
        # Отображение сетки
        is_show_grid = self.getShowGrid()
        if is_show_grid:
            self.axes.grid()

        # Установка формата временной шкалы
        time_format = self.getTimeFormat()
        if time_format:
            # Цена деления временной оси
            hours = matplotlib.dates.HourLocator()
            self.axes.xaxis.set_major_locator(hours)
            self.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(time_format))

        # Отображение подписи временнй шкалы в удобном виде
        self.figure.autofmt_xdate()

    def draw_empty(self):
        """
        Отрисовка пустого тренда.
        """
        time_data = [datetime.datetime.now()]
        time_float = matplotlib.dates.date2num(time_data)
        self.axes.plot(time_float, [1])
        self.figure.canvas.draw()

    def draw(self, redraw=True):
        """
        Основной метод отрисовки тренда.

        :param redraw: Принудительная прорисовка.
        """
        pens = self.getPens()

        if pens:
            self.axes.clear()
            self.setDefaults()

            # Признак не пустого тренда
            not_empty = False
            for pen in pens:
                if pen:
                    line_data = pen.getLineData()
                    if line_data:
                        time_data = [point[0] for point in line_data]
                        time_float = matplotlib.dates.date2num(time_data)
                        y_data = [point[1] for point in line_data]
                        rgb_str = pen.getColourStr()

                        self.axes.plot(time_float, y_data, color=rgb_str)
                        if redraw:
                            self.figure.canvas.draw()
                        not_empty = True
                    else:
                        log.warning(u'Пустые значения MPLTrend <%s>' % self.name)
                        not_empty = not_empty or False
                else:
                    log.warning(u'Не определено перо тренда <%s>' % self.name)
                    not_empty = False

            if not not_empty:
                # Если тренд пустой, то отрисовать пустой тренд
                self.draw_empty()
        else:
            # Если перья не определены то просто отобразить тренд
            self.draw_empty()


class icMPLTrend(icwidget.icWidget, icMPLTrendProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на библиотеке matplotlib.

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
        icMPLTrendProto.__init__(self, parent)

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

    def getTimeFormat(self):
        """
        Формат надписей временной оси.
        """
        return self.getICAttr('time_axis_fmt')

    def getShowGrid(self):
        """
        Отображать сетку?
        """
        return self.getICAttr('show_grid')


def test():
    """
    Тестовая функция.
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(None, title='My Data')
    panel = icMPLTrendProto(frame)
    panel.draw()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
