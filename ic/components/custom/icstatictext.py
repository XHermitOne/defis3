#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.StaticText (Статический текст).

@type SPC_IC_STATICTEXT: C{dictionary}
@var SPC_IC_STATICTEXT: Спецификация на ресурсное описание компонента icStaticText.
Описание ключей SPC_IC_STATICTEXT:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'StaticText'}: Тип объекта.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{text=''}: Текст.
    - B{style=0}: Стиль компонента.
    - B{font={}}. Шрифт текста.
    - B{position=(-1,-1)'}: Расположение на родительском окне.
    - B{size=(70,-1)}: Размер поля.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{source=None}: Описание или ссылка на источник данных.

@type ICStaticTextStyle: C{dictionary}
@var ICStaticTextStyle: Словарь специальных стилей компонента. Описание ключей ICStaticTextStyle:

    - C{wx.ALIGN_LEFT}: Выравнивание по левому краю.
    - C{wx.ALIGN_RIGHT}: Выравнивание по правому краю.
    - C{wx.ALIGN_CENTRE}: Выравнивание по центру.
    - C{wx.ST_NO_AUTORESIZE}: Автоподбор размера.
"""

import wx
from ic.log.iclog import *
from ic.components.icfont import *
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
from ic.utils.util import ic_eval, icSpcDefStruct, getICAttr
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

ICStaticTextStyle = {'ALIGN_LEFT': wx.ALIGN_LEFT,
                     'ALIGN_RIGHT': wx.ALIGN_RIGHT,
                     'ALIGN_CENTRE': wx.ALIGN_CENTRE,
                     'ST_NO_AUTORESIZE': wx.ST_NO_AUTORESIZE}

SPC_IC_STATICTEXT = {'type': 'StaticText',
                     'name': 'default',
                     'activate': True,

                     'style': wx.ALIGN_LEFT,
                     'position': (-1, -1),
                     'size': (70, 18),
                     'text': 'StaticText',
                     'font': {},
                     'foregroundColor': (50, 50, 50),
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
ic_class_name = 'icStaticText'

#   Описание стилей компонента
ic_class_styles = ICStaticTextStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_STATICTEXT
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtStaticText'
ic_class_pic2 = '@common.imgEdtStaticText'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icstatictext.icStaticText-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icStaticText(icWidget, wx.StaticText):
    """
    Объект статического текста
    """
    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icStaticText

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
        icSpcDefStruct(SPC_IC_STATICTEXT, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        text = component['text']
        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        font = component['font']
        style = component['style']

        #   Вычисляем текст поля после создания объекта
        if text.find('@') == -1:
            val = getICAttr('@'+text, self.evalSpace, None)
        else:
            val = getICAttr('@'+text, self.evalSpace, 'Error in icstatictext.__init__()<text>. Name:' + self.name)

        if not val:
            val = text
            
        wx.StaticText.__init__(self, parent, id, val, pos, size=size, style=style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        obj = icFont(font)
        self.SetFont(obj)

    def setValue(self, Data_):
        """
        Установить данные в виджет.
        """
        return self.SetLabel(Data_)
    
    def getValue(self):
        """
        Получить данные из виджета.
        """
        return self.GetLabel()


def test(par=0):
    """
    Тестируем класс icStaicText.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icStaticText Test')
    win = wx.Panel(frame, -1)
    ctrl = icStaticText(win, -1, {'text': '@\'icStaticText\'+\'>>\'',
                                  'font': {'style': 'boldItalic', 'size': 14}})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
