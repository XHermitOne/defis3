#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скроллируемая панель.
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
import ic.components.icwindow as icwindow

import wx.lib.scrolledpanel as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icScrolledPanel'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ScrolledPanel',
                'name': 'default',
                'child': [],

                'backgroundColor': None,
                'foregroundColor': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type'],
                                   8: ['backgroundColor', 'foregroundColor'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtScrolledWindow'
ic_class_pic2 = '@common.imgEdtScrolledWindow'

#   Путь до файла документации
ic_class_doc = 'public/icscrolledpanel.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icScrolledPanel(icwidget.icWidget, parentModule.ScrolledPanel):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{foregroundColor=''}:
        - B{name='default'}:
        - B{backgroundColor=(0, 0, 0)}:
        - B{child=[]}:
        - B{type='ScrolledPanel'}:
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.ScrolledPanel.__init__(self, parent, id, self.position, self.size,
                                            style=self.style, name=self.name)
        
        fgr = self.foregroundColor
        bgr = self.backgroundColor
        
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.BindICEvt()

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        self.SetAutoLayout(1)
        self.SetupScrolling()
                    
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)


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
    
    pnl = icScrolledPanel(win, -1, {'position': (10, 10),
                                    'size': (100, 100),
                                    'backgroundColor': (0, 0, 0)})
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
