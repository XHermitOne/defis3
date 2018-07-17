#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Объект временного графика. Тренд.
ВНИМАНИЕ! 11.01.2016
Разработка компонента остановлена.
Начата разработка компонента icMPLTrend на базе библиотеки matplotlib.
"""

import wx
import wx.lib.plot as parentModule

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

import ic.utils.util as util
from ic.log import log
from ic.bitmap import ic_bmp

# --- Спецификация ---
TIME_AXIS_TIME_TYPE = 'time'
TIME_AXIS_DATE_TYPE = 'date'
TIME_AXIS_DATETIME_TYPE = 'datetime'
TIME_AXIS_TYPES = (TIME_AXIS_TIME_TYPE,
                   TIME_AXIS_DATE_TYPE,
                   TIME_AXIS_DATETIME_TYPE)

SPC_IC_TREND = {'title': u'Тренд',  # Заголовок
                'data_label': None,  # Надпись оси данных
                'time_label': None,  # Надпись оси времени
                'time_type': TIME_AXIS_TIME_TYPE,   # Тип данных оси времени
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'title': u'Заголовок',
                                 'data_label': u'Надпись оси данных',
                                 'time_label': u'Надпись оси времени',
                                 'time_type': u'Тип данных оси времени',
                                 },
                }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTrend'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'Trend',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'time_type': list(TIME_AXIS_TYPES),
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            'title',
                                                            'data_label', 'time_label'],
                                   icDefInf.EDT_CHOICE: ['time_type'],
                                   },
                '__parent__': SPC_IC_TREND,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('chart_line.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('chart_line.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)


class icTrendProto(parentModule.PlotCanvas):
    """
    Объект временного графика. Тренд.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        parentModule.PlotCanvas.__init__(self, *args, **kwargs)

        self.setDefaults()

    def setDefaults(self):
        """
        Установить параметры по умолчанию.
        """
        self.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.SetFontSizeAxis(10)
        self.SetFontSizeLegend(7)
        self.setLogScale((False, False))
        self.SetXSpec('auto')
        self.SetYSpec('auto')
        self.SetEnableGrid(True)

    def getTitle(self):
        """
        Заголовок тренда.
        """
        return u''

    def getDataLabel(self):
        """
        Надпись оси данных.
        """
        return u''

    def getTimeLabel(self):
        """
        Надпись оси времени.
        """
        return u''

    def getGraphics(self):
        """
        Получение объекта графиков из данных
        """
        pens = self.getPens()
        title = self.getTitle()
        data_label = self.getDataLabel()
        time_label = self.getTimeLabel()
        return parentModule.PlotGraphics(pens, title,
                                         data_label, time_label)

    def draw(self):
        """
        Отрисовка тренда.
        """
        return self.Draw(self.getGraphics())

    def getPens(self):
        """
        Получить список перьев тренда.
        """
        return list()


class icTrend(icwidget.icWidget, icTrendProto):
    """
    Объект временного графика. Тренд.

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
        icTrendProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

        self.draw()

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getTitle(self):
        """
        Заголовок тренда.
        """
        title = self.getICAttr('title')
        return u'' if title is None else title

    def getDataLabel(self):
        """
        Надпись оси данных.
        """
        label = self.getICAttr('data_label')
        return u'' if label is None else label

    def getTimeLabel(self):
        """
        Надпись оси времени.
        """
        label = self.getICAttr('time_label')
        return u'' if label is None else label

    def getPens(self):
        """
        Получить список перьев тренда.
        """
        return self.get_children_lst()


def test():
    """
    Функция тестирования.
    """
    from ic import config
    import copy
    from . import trendpen

    log.init(config)

    app = wx.PySimpleApp()
    # Внимание!
    # Это отключает ошибку
    # wx._core.PyAssertionError: C++ assertion "m_window" failed at ../src/gtk/dcclient.cpp(2043)
    # in DoGetSize(): GetSize() doesn't work without window
    app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)

    frame = wx.Frame(None, -1)

    res = copy.deepcopy(ic_class_spc)
    res['child'].append(copy.deepcopy(trendpen.ic_class_spc))
    trend = icTrend(frame, -1, component=res)
    trend.draw()

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
