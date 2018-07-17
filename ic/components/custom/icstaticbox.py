#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.StaticBox.

@type SPC_IC_STATICBOX: C{dictionary}
@var SPC_IC_STATICBOX: Спецификация на ресурсное описание панели инструментов.
Описание ключей SPC_IC_STATICBOX:

    - B{type='StaticBox'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры поля.
    - B{label=''}: Подпись.
    - B{style=wx.CLIP_SIBLINGS}: Стиль компонента (все стили wx.Window/icWindow).
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
"""

import wx
from ic.log.iclog import *
from ic.utils.util import icSpcDefStruct
from ic.components.icfont import *
from ic.utils.util import ic_eval
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
from ic.components import icwindow
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_STATICBOX = {'type': 'StaticBox',
                    'name': 'default',

                    'label': '',
                    'style': wx.CLIP_SIBLINGS,
                    'position': (-1, -1),
                    'size': (-1, -1),
                    'foregroundColor': (0, 0, 0),
                    'backgroundColor': None,

                    '__parent__': SPC_IC_WIDGET,
                    }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icStaticBox'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_STATICBOX
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtStaticBox'
ic_class_pic2 = '@common.imgEdtStaticBox'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icstaticbox.icStaticBox-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 2)


class icStaticBox(icWidget, wx.StaticBox):
    """
    Класс icStaticBox реализует интерфейс для обработки элемента группировки
    как обкладку над компонентом wx.StaticBox.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icStaticBox

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        icSpcDefStruct(SPC_IC_STATICBOX, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        size = component['size']
        pos = component['position']
        label = component['label']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']

        wx.StaticBox.__init__(self, parent, id, label=label, pos=pos, size=size, style=style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))


def test(par=0):
    """
    Тестируем класс icStaticBox.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icStaticBox Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icStaticBox(win, -1, {'label': 'StaticBox Label',
                                   'size': (200, 200),
                                   'position': (10, 10)})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
