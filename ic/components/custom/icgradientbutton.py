#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.Button.
Содержит описание класса icButton, который по ресурсному описанию создает стандартную кнопку.

@type SPC_IC_GRBUTTON: C{dictionary}
@var SPC_IC_GRBUTTON: Спецификация на ресурсное описание окна.
Описание ключей SPC_IC_GRBUTTON:
    - B{name = 'default'}: Имя окна.
    - B{type = 'Button'}: Тип объекта.
    - B{label = 'button'}: Надпись на кнопке. При наличии '@' атрибут вычисляется.
    - B{position = (-1,-1)}: Расположение на родительском окне.
    - B{size = (-1,-1)}: Размер кнопки.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB}: Дополнительные (+стандартные стили wx.Window) стили:
        - C{wx.BU_LEFT}: Выравнивает текст подписи по левому краю кнопки (Win32).
        - C{wx.BU_TOP}: Выравнивает текст подписи по верхней границе кнопки (Win32).
        - C{wx.BU_RIGHT}: Выравнивает текст подписи по правому краю кнопки (Win32).
        - C{wx.BU_BOTTOM}: Выравнивает текст подписи по нижней границе кнопки (Win32).
        - C{wx.BU_EXACTFIT}: Создает кнопку с минимально возможными размерами.
    - B{font={}}: Шрифт надписи на кнопке.
    - B{keyCode=None}: Код клавиши, эмулирующей нажатие кнопки (mouseClick) (не используется).
    - B{mouseClick=None}: Выражение, выполняемое после нажатия кнопки.
    - B{mouseDown=None}: Выражение, выполняемое после нажатия левой кнопки мыши.
    - B{mouseUp=None}: Выражение, выполняемое после отпускания левой кнопки мыши.
    - B{mouseContextDown=None}: Выражение, выполняемое после нажатия правой кнопки мыши.
    - B{keyDown=None}: Выражение, выполняемое при получении сообщения от клавиатуры.
@type ICButtonStyle: C{dictionary}
@var ICButtonStyle: Словарь специальных стилей компонента.
Описание ключей ICButtonStyle:
    - C{wx.BU_LEFT}: Выравнивает текст подписи по левому краю кнопки (Win32).
    - C{wx.BU_TOP}: Выравнивает текст подписи по верхней границе кнопки (Win32).
    - C{wx.BU_RIGHT}: Выравнивает текст подписи по правому краю кнопки (Win32).
    - C{wx.BU_BOTTOM}: Выравнивает текст подписи по нижней границе кнопки (Win32).
    - C{wx.BU_EXACTFIT}: Создает кнопку с минимально возможными размерами.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.components.icfont import *
import ic.utils.util as util
from ic.components import icwidget
from ic.PropertyEditor.ExternalEditors import baseeditor
import ic.utils.coderror as coderror

import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import wx.lib.agw.gradientbutton as GB

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

ICGRButtonStyle = {'BU_LEFT': wx.BU_LEFT,
                   'BU_TOP': wx.BU_TOP,
                   'BU_RIGHT': wx.BU_RIGHT,
                   'BU_BOTTOM': wx.BU_BOTTOM,
                   'BU_EXACTFIT': wx.BU_EXACTFIT}

SPC_IC_GRBUTTON = {'type': 'GRButton',
                   'name': 'default',

                   'label': 'button',
                   'style': 0,
                   'position': (-1, -1),
                   'size': (-1, -1),
                   'font': {},
                   'foregroundColor': None,
                   'backgroundColor': None,

                   # gradient colors
                   'topStartColour': None,
                   'topEndColour': None,
                   'bottomStartColour': None,
                   'bottomEndColor': None,
                   'pressedTopColour': None,
                   'pressedBottomColour': None,
                
                   'keyDown': None,
                   'mouseClick': None,
                   'mouseDown': None,
                   'mouseUp': None,             # Выражение, выполняемое после отпускания левой кнопки мыши
                   'mouseContextDown': None,    # Выражение, выполняемое после нажатия правой кнопки мыши
                   'attach_focus': False,       # Привязать фокус автоматически при создании

                   '__events__': {'mouseClick': ('wx.EVT_BUTTON', 'OnMouseClick', False),
                                  'mouseContextDown': ('wx.EVT_RIGHT_DOWN', 'OnMouseContextDown', False),
                                  'mouseDown': ('wx.EVT_LEFT_DOWN', 'OnMouseDown', False),
                                  'mouseUp': ('wx.EVT_LEFT_UP', 'OnMouseUp', False),
                                  },
                   '__attr_types__': {icDefInf.EDT_CHECK_BOX: ['attach_focus'],
                                      icDefInf.EDT_COLOR: ['topStartColour', 'topEndColour',
                                                           'bottomStartColour', 'bottomEndColor',
                                                           'pressedTopColour', 'pressedBottomColour'],
                                      },
                   '__parent__': icwidget.SPC_IC_WIDGET,
                   '__attr_hlp__': {'mouseUp': u'Выражение, выполняемое после отпускания левой кнопки мыши',
                                    'mouseContextDown': u'Выражение, выполняемое после нажатия правой кнопки мыши',
                                    'attach_focus': u'Привязать фокус автоматически при создании',
                                    },
                   }
     

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icGRButton'

#   Описание стилей компонента
ic_class_styles = ICGRButtonStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_GRBUTTON
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtButton'
ic_class_pic2 = '@common.imgEdtButton'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icbutton.icButton-class.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 5)


class icGRButton(icwidget.icWidget, GB.GradientButton):
    """
    Класс icGRButton реализует обкладку над компонентом wx.Button.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icButton.

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
        self.parent = parent
    
        component = util.icSpcDefStruct(SPC_IC_GRBUTTON, component)
        component['font'] = util.icSpcDefStruct(SPC_IC_FONT, component['font'])
        
        for key in [x for x in component.keys() if not x.startswith('__') ]:
            setattr(self, key, component[key])
        
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        self.label = self.getICAttr('label')
        
        GB.GradientButton.__init__(self, parent, id, label=self.label, pos=self.position, size=self.size,
                                   style=wx.NO_BORDER | self.style, name=self.name)

        if self.backgroundColor is not None:
            self.SetBackgroundColour(wx.Colour(*self.backgroundColor))

        if self.foregroundColor is not None:
            self.SetForegroundColour(wx.Colour(*self.foregroundColor))
        
        if self.topStartColour is not None:
            self.SetTopStartColour(wx.Colour(*self.topStartColour))
        if self.topEndColour is not None:
            self.SetTopEndColour(wx.Colour(*self.topEndColour))
        if self.bottomStartColour is not None:
            self.SetBottomStartColour(wx.Colour(*self.bottomStartColour))
        if self.bottomEndColor is not None:
            self.SetBottomEndColour(wx.Colour(*self.bottomEndColor))
        if self.pressedTopColour is not None:
            self.SetPressedTopColour(wx.Colour(*self.pressedTopColour))
        if self.pressedBottomColour is not None:
            self.SetPressedBottomColour(wx.Colour(*self.pressedBottomColour))

        obj = icFont(self.font)
        self.SetFont(obj)
        
        #   Обработчики сообщений
        self.Bind(wx.EVT_BUTTON, self.OnMouseClick, id=id)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseContextDown)
        self.BindICEvt()
        
    def OnMouseClick(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_BUTTON).
        """
        if self.context['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.context['evt'] = evt
            self.eval_attr('mouseClick')
        evt.Skip()
    
    def OnMouseDown(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_LEFT_DOWN).
        """
        if self.context['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.context['evt'] = evt
            self.eval_attr('mouseDown')
        evt.Skip()

    def OnMouseUp(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_LEFT_UP).
        """
        if self.context['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.context['evt'] = evt
            self.eval_attr('mouseUp')
        evt.Skip()

    def OnMouseContextDown(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_RIGHT_DOWN).
        """
        if self.context['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.context['evt'] = evt
            self.eval_attr('mouseContextDown')
        evt.Skip()


def test(par=0):
    """
    Тестируем класс icButton.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, u'Тест кнопки')
    win = wx.Panel(frame, -1)
    ctrl_1 = icGRButton(win, -1, {'label': '@\'icButton\'', 'position': (100, 0),
                                  'mouseContextDown': 'print \'mouseContextDown\'',
                                  'mouseClick': 'print \'mouseClick\'',
                                  'mouseDown': 'print \'mouseDown\'',
                                  'mouseUp': 'print \'mouseUp\''})
    ctrl_2 = wx.Button(win, -1, 'wx.Button')
    frame.Show(True)
    app.MainLoop()
    

if __name__ == '__main__':
    test(0)
