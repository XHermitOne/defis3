#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wxGauge.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.components.icfont import *
import ic.utils.util as util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_GAUGE = {'type': 'Gauge',
                'name': 'default',

                'position': (-1, -1),
                'size': (-1, -1),
                'layout': 'horizontal',
                'max': 10,
                'value': 0,
                'foregroundColor': (0, 0, 0),
                'backgroundColor': (255, 255, 255),

                '__attr_types__': {icDefInf.EDT_NUMBER: ['max', 'value'],
                                   },
                '__parent__': SPC_IC_WIDGET,
                }
                
#-------------------------------------------
#   Общий интерфэйс модуля
#-------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icGauge'

#   Описание стилей компонента
ic_class_styles = {'GA_HORIZONTAL': wx.GA_HORIZONTAL,
                   'GA_VERTICAL': wx.GA_VERTICAL,
                   'GA_SMOOTH': wx.GA_SMOOTH}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_GAUGE
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtGauge'
ic_class_pic2 = '@common.imgEdtGauge'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icgauge.icGauge-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icGauge(icWidget, wx.Gauge):
    """
    Класс icGuage реализует интерфейс для обработки индикатора относительного количества.
    """

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icGuage

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - диалоговое окно)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        self.parent = parent
        
        util.icSpcDefStruct(SPC_IC_GAUGE, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        size = component['size']
        pos = component['position']
        layout = component['layout']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        max = component['max']
        val = component['value']

        if layout == 'vertical':
            style = wx.GA_VERTICAL | wx.GA_SMOOTH
        else:
            style = wx.GA_HORIZONTAL | wx.GA_SMOOTH

        wx.Gauge.__init__(self, parent, id, max, pos, size,
                          style=style, name=self.name)
        self.SetValue(val)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.BindICEvt()


def test(par=0):
    """
    Тестируем класс icFrame.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icGauge Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icGauge(win, -1, {'value': 30, 'max': 100, 'size': (300, -1),
                               'position': (10, 10),
                               'keyDown': 'print \'keyDown in Gauge\''})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
