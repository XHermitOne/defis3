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

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            ],
                                   },
                '__parent__': gnuplot_trend_navigator_proto.SPC_IC_GNUPLOT_TREND_NAVIGATOR,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart_curve_edit.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart_curve_edit.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 1)


class icGnuplotTrendNavigator(icwidget.icWidget,
                              gnuplot_trend_navigator_proto.icGnuplotTrendNavigatorProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на утилите gnuplot.

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
        gnuplot_trend_navigator_proto.icGnuplotTrendNavigatorProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        # self.childCreator(bCounter, progressDlg)

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

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def setPens(self, pens):
        """
        Установить перья тренда.
        @param pens: Описания перьев.
        @return: True/False.
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
        @param is_update_size: Произвести обновление размера?
        """
        save_data = self.load_ext_data(self.name)
        default_sash_pos = self.trend_splitter.GetSashPosition() if self.show_legend else 1
        result = self.trend_splitter.SetSashPosition(save_data.get('sash_pos', default_sash_pos))
        if is_update_size:
            self.trend_splitter.UpdateSize()
        return result
