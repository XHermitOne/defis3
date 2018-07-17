#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.RadioBox.

@type SPC_IC_RADIOGROUP: C{dictionary}
@var SPC_IC_RADIOGROUP: Спецификация на ресурсное описание панели инструментов. Описание ключей SPC_IC_RADIOGROUP:

    - B{type='RadioGroup'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{style=0}: Стиль окна.
    - B{layout='vertical'}: Расположение ('vertical' | 'horizontal')
    - B{max=0}:  Количество возможных выборов.
    - B{items=[]}: Список выборов.
    - B{selected=0}: Текущий выбор.
    - B{font={}}: Шрифт.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры компонента.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{source=None}: Описание или ссылка на источник данных.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.components.icfont import *
import ic.utils.util as util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf


SPC_IC_RADIOGROUP = {'type': 'RadioGroup',
                     'name': 'default',

                     'label': '',
                     'style': 0,
                     'position': (-1, -1),
                     'size': (-1, -1),
                     'layout': 'vertical',
                     'max': 0,
                     'items': ['first', 'second'],
                     'selected': 0,
                     'font': {},
                     'onSelected': None,
                     'foregroundColor': (0, 0, 0),
                     'backgroundColor': (255, 255, 255),

                     '__events__': {'onSelected': ('wx.EVT_RADIOBOX', 'OnSelected', False),
                                    },
                     '__attr_types__': {icDefInf.EDT_NUMBER: ['selected', 'max'],
                                        icDefInf.EDT_TEXTLIST: ['items'],
                                        },
                     '__parent__': SPC_IC_WIDGET,
                     }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icRadioGroup'

#   Описание стилей компонента
ic_class_styles = {'RA_SPECIFY_ROWS': wx.RA_SPECIFY_ROWS,
                   'RA_SPECIFY_COLS': wx.RA_SPECIFY_COLS}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_RADIOGROUP
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtRadioButton'
ic_class_pic2 = '@common.imgEdtRadioButton'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icradiogroup.icRadioGroup-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icRadioGroup(icWidget, wx.RadioBox):
    """
    Класс icRadioGroup реализует обкладку для компонента wx.RadioBox.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания  icRadioGroup

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
        util.icSpcDefStruct(SPC_IC_RADIOGROUP, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        for key in lst_keys:
            setattr(self, key, component[key])
        
        layout = component['layout']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        max = component['max']
        label = component['label']
        items = component['items']
        size = component['size']
        pos = component['position']
        sel = component['selected']
        style = component['style']

        if layout == 'vertical' :
            style = style | wx.RA_SPECIFY_ROWS | wx.CLIP_SIBLINGS
        else:
            style = style | wx.RA_SPECIFY_COLS | wx.CLIP_SIBLINGS

        wx.RadioBox.__init__(self, parent, id, label, pos, size, items, max, style, name = self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_RADIOBOX, self.OnSelected)
        self.BindICEvt()

    def OnSelected(self, evt):
        self.eval_event('onSelected', evt, True)


def test(par=0):
    """
    Тестируем класс icRadioBox.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icRadioBox Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icRadioGroup(win, -1, {'items': ['1', '2', '3', '4'],
                                    'position': (10, 10)})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
