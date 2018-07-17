#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Индикатор состояний.
Класс пользовательского визуального компонента.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import wx.lib.buttons as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'StateIndicator'

#   Описание стилей компонента
ic_class_styles = {'BU_RIGHT': 256,
                   'BU_TOP': 128,
                   'BU_LEFT': 64,
                   'BU_BOTTOM': 512,
                   'BU_EXACTFIT': 1,
                   }

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'urIndicator',
                'name': 'Default',

                'position': (-1, -1),
                'size': (100, -1),
                'style': 0,
                'foregroundColor': None,
                'onButton': None,
                'image': None,
                'label': 'Label',
                'backgroundColor': None,
                'onLeftDown': 'True',
                'onLeftUp': None,

                '__styles__': ic_class_styles,
                '__events__': {'onLeftDown': ('wx.EVT_LEFT_DOWN', 'OnLeft_DWN', None),
                               'onLeftUp': ('wx.EVT_LEFT_UP', 'OnLeft_Up', None),
                               'onButton': ('wx.EVT_BUTTON', None, 1),
                               },
                '__attr_types__': {0: ['label'],
                                   8: ['foregroundColor', 'backgroundColor'],
                                   12: ['onButton', 'onLeftDown', 'onLeftUp'],
                                   },
                '__version__': (0, 0, 0, 1),
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImage'
ic_class_pic2 = '@common.imgEdtImage'

#   Путь до файла документации
ic_class_doc = None
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class StateIndicator(icwidget.icWidget, parentModule.GenBitmapTextButton):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{style=0}:
        - B{foregroundColor=None}:
        - B{name='Default'}:
        - B{onButton=None}:
        - B{image=None}:
        - B{label='Label'}:
        - B{backgroundColor=None}:
        - B{position=(-1, -1)}:
        - B{onLeftDown='True'}:
        - B{onLeftUp=None}:
        - B{type='urButton'}:
        - B{size=(100, -1)}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace={},
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        img = common.imgEdtImage
        parentModule.GenBitmapTextButton.__init__(self, parent, id, img, self.label, self.position, self.size, style = self.style, name = self.name)
        
        #   Регистрация обработчиков событий
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeft_DWN)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeft_Up)
        self.Bind(wx.EVT_BUTTON, self.On_onButton, id=id)
        self.BindICEvt()
        
        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий
    def OnLeft_DWN(self, evt):
        """
        Обработчик события wx.EVT_LEFT_DOWN, атрибут=onLeftDown
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = util.ic_eval(self.onLeftDown, 0, self.evalSpace,
                                'EVAL ATTRIBUTE ERROR: attr=onLeftDown')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnLeft_Up(self, evt):
        """
        Обработчик события wx.EVT_LEFT_UP, атрибут=onLeftUp
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = util.ic_eval(self.onLeftUp, 0, self.evalSpace,
                                'EVAL ATTRIBUTE ERROR: attr=onLeftUp')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def On_onButton(self, evt):
        """
        Обработчик события wx.EVT_BUTTON, атрибут=onButton
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = util.ic_eval(self.onButton, 0, self.evalSpace,
                                'EVAL ATTRIBUTE ERROR: attr=onButton')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    
    ctrl_1 = StateIndicator(win, -1, {'position': (100, 35),
                                      'size': (100, 30)})
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
