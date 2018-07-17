#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.Button.
Содержит описание класса icButton, который по ресурсному описанию создает стандартную кнопку.

@type SPC_IC_BUTTON: C{dictionary}
@var SPC_IC_BUTTON: Спецификация на ресурсное описание окна.
Описание ключей SPC_IC_BUTTON:

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
import copy
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.components.icfont import *
import ic.utils.util as util
from ic.components import icwidget
from ic.PropertyEditor.ExternalEditors import baseeditor
import ic.utils.coderror as coderror
from ic.interfaces import icedtresourcemanager
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

ICButtonStyle = {'BU_LEFT': wx.BU_LEFT,
                 'BU_TOP': wx.BU_TOP,
                 'BU_RIGHT': wx.BU_RIGHT,
                 'BU_BOTTOM': wx.BU_BOTTOM,
                 'BU_EXACTFIT': wx.BU_EXACTFIT}

SPC_IC_BUTTON = {'type': 'Button',
                 'name': 'default',

                 'label': 'button',
                 'style': 0,
                 'position': (-1, -1),
                 'size': (-1, -1),
                 'font': {},
                 'foregroundColor': None,
                 'backgroundColor': None,
                 'keyDown': None,
                 'userAttr': None,
                 'mouseClick': None,
                 'mouseDown': None,
                 'mouseUp': None,           # Выражение, выполняемое после отпускания левой кнопки мыши
                 'mouseContextDown': None,  # Выражение, выполняемое после нажатия правой кнопки мыши
                 'attach_focus': False,     # Привязать фокус автоматически при создании

                 '__events__': {'mouseClick': ('wx.EVT_BUTTON', 'OnMouseClick', False),
                                'mouseContextDown': ('wx.EVT_RIGHT_DOWN', 'OnMouseContextDown', False),
                                'mouseDown': ('wx.EVT_LEFT_DOWN', 'OnMouseDown', False),
                                'mouseUp': ('wx.EVT_LEFT_UP', 'OnMouseUp', False),
                                },
                 '__attr_types__': {icDefInf.EDT_CHECK_BOX: ['attach_focus'],
                                    icDefInf.EDT_USER_PROPERTY: ['userAttr'],
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
ic_class_name = 'icButton'

#   Описание стилей компонента
ic_class_styles = ICButtonStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_BUTTON
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
__version__ = (1, 0, 0, 6)

# EDITOR_FUNCS_BLOCK


# --- Функции редактирования
def get_property_editor_userAttr(attr, value, pos, size,
                                style, propEdt, *arg, **kwarg):
    """
    """
    parent = propEdt.GetPropertyGrid().GetView()

    lst = [u'один', u'два', u'три']
    dlg = baseeditor.ChoiceMenu(parent, lst)
    parent.PopupMenu(dlg, pos)

    #   Возвращаем выбранный элемент списка
    if lst and dlg.IsSelString():
        value = dlg.GetSelString()

    dlg.Destroy()
    return value


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    @type attr: C{string}
    @param attr: Имя текущего атрибута.
    @type value: C{string}
    @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
    @type pos: C{wx.Point}
    @param pos: Позиция окна.
    @type size: C{wx.Size}
    @param size: Размер диалогового окна.
    @type style: C{int}
    @param style: Стиль диалога.
    @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    @param propEdt: Указатель на редактор свойств.
    """
    if attr == 'userAttr':
        return get_property_editor_userAttr(attr, value, pos, size, style, propEdt, *arg, **kwarg)


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr == 'userAttr':
        if value == u'один':
            return coderror.IC_CTRL_FAILED
        return coderror.IC_CTRLKEY_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if text == u'два':
        return 2
    elif text == u'три':
        return 3

# END_EDITOR_FUNCS_BLOCK


class ERMButton(icedtresourcemanager.IEditorResourceManager):

    component_class = None

    @staticmethod
    def SetObjProperty(obj, attr, value, *arg, **kwarg):
        """
        Изменяет свойство объекта при редактировании в редакторе форм.
        """
        if attr == 'label':
            obj.SetLabel(value)
            return True
        return False


class icButton(icwidget.icWidget, wx.Button):
    """
    Класс icButton реализует обкладку над компонентом wx.Button.
    """

    @staticmethod
    def GetEditorResourceManager():
        """
        Указатель на класс управления ресурсом в редакторе ресурсов.
        """
        return ERMButton

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
        component = util.icSpcDefStruct(SPC_IC_BUTTON, component)
        component['font'] = util.icSpcDefStruct(SPC_IC_FONT, component['font'])

        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        self.label = self.getICAttr('label')

        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        font = component['font']
        _style = component['style'] | wx.WANTS_CHARS

        self.mouse_click = component['mouseClick']
        self.mouse_down = component['mouseDown']
        self.mouse_up = component['mouseUp']
        self.mouse_contextdown = component['mouseContextDown']

        wx.Button.__init__(self, parent, id, self.label, pos, size, style=_style, name=self.name)
        self.SetToolTipString(component['description'] or self.label)
        if component['description']:
            self.SetHelpText(component['description'])

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        obj = icFont(font)
        self.SetFont(obj)

        # Автоматически установить фокус
        attachFocus = component['attach_focus']
        if attachFocus:
            self.SetFocus()

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
        self.eval_event('mouseClick', evt, True)

    def OnMouseDown(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_LEFT_DOWN).
        """
        self.eval_event('mouseDown', evt, True)

    def OnMouseUp(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_LEFT_UP).
        """
        self.eval_event('mouseUp', evt, True)

    def OnMouseContextDown(self, evt):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_RIGHT_DOWN).
        """
        self.eval_event('mouseContextDown', evt, True)


def test(par=0):
    """
    Тестируем класс icButton.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, u'Тест кнопки')
    win = wx.Panel(frame, -1)
    ctrl_1 = icButton(win, -1, {'label': '@\'icButton\'', 'position': (100, 0),
                                'mouseContextDown': 'print \'mouseContextDown\'',
                                'mouseClick': 'print \'mouseClick\'',
                                'mouseDown': 'print \'mouseDown\'',
                                'description': u'Help для кнопки',
                                'mouseUp': 'print \'mouseUp\''})
    ctrl_2 = wx.Button(win, -1, 'wx.Button')
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
