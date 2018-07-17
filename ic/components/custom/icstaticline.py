#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.StaicLine. Генерирут объект линию по ресурсному описанию.

@type SPC_IC_LINE: C{Dictionary}
@var SPC_IC_LINE: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'StaticLine'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{size = (-1,-1)}: Размер картинки.
    - B{layout = 'horizontal'}: Стиль линии ('horizontal' | 'verical').
    
"""
import wx
from ic.utils.util import icSpcDefStruct
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_LINE = {'type': 'StaticLine',
               'name': 'DefaultName',

               'position': (-1, -1),
               'size': (-1, -1),
               'layout': 'horizontal',

               '__parent__': SPC_IC_WIDGET,
               }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icStaticLine'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_LINE
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtStaticLine'
ic_class_pic2 = '@common.imgEdtStaticLine'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icstaticline.icStaticLine-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 2)


class icStaticLine(icWidget, wx.StaticLine):
    """
    Класс реализует интерфейс к классу wx.StaticLine
    через ресурсное описание.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания линии icStaticLine.

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
        """
        icSpcDefStruct(SPC_IC_LINE, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        size = component['size']
        pos = component['position']
        layout = component['layout']

        if layout == 'vertical':
            style = wx.LI_VERTICAL
        else:
            style = wx.LI_HORIZONTAL

        wx.StaticLine.__init__(self, parent, id, pos, size, style, name=self.name)


def test(par=0):
    """
    Тестируем класс icStaticLine.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icStaticLine Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icStaticLine(win, -1, {'size': (500, 1),
                                    'position': (10, 10)})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
