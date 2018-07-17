#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.ScrolledPanel. Генерирут окно с прокруткой.

@type SPC_IC_SCROLLED_WINDOW: C{Dictionary}
@var SPC_IC_SCROLLED_WINDOW: Спецификация на ресурсное описание окна. Описание ключей:

    - B{name = 'default'}: Имя окна.
    - B{type = 'ScrolledPanel'}: Тип объекта.
    - B{title = 'default'}: Заголовок окна, там где это необходимо, например, в icNotebook.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=0}:Стиль окна. Используются все стили класса icWindow +
        wx.RETAINED - использует bitmap для ускорения перерисовки.
    - B{scrollRate = (1,1)}: Сдвиг по оси x и y соответственно при скроллировании.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на окне.
    - В{child=[]}:Cписок дочерних элементов.
    
@type ICWindowStyle: C{dictionary}
@var ICWindowStyle: Словарь специальных стилей компонента:
    wx.RETAINED - использует bitmap для ускорения перерисовки.

"""

import wx
import wx.lib.scrolledpanel
import copy
from ic.log.iclog import *
import ic.utils.util as util
from .icwidget import icWidget, SPC_IC_WIDGET
from .icwindow import ICWindowStyle
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt
import ic.imglib.common as common

_ = wx.GetTranslation

ICScrolledPanelStyle = copy.deepcopy(ICWindowStyle)
ICScrolledPanelStyle['RETAINED'] = wx.RETAINED

SPC_IC_SCROLLED_PANEL = {'type': 'ScrolledPanel',
                         'name': 'defaultPanel',
                         'child': [],

                         'position': (-1, -1),
                         'title': 'default',
                         'size': (-1, -1),
                         'foregroundColor': None,
                         'backgroundColor': None,
                         'style': 0,
                         'scrollRate': [5, 5],
                         'keyDown': None,

                         '__styles__': ICScrolledPanelStyle,
                         '__attr_types__': {icDefInf.EDT_TEXTLIST: ['scrollRate'],
                                            },
                         '__parent__': SPC_IC_WIDGET,
                         }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icScrolledPanel'

#   Описание стилей компонента
ic_class_styles = ICScrolledPanelStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_SCROLLED_PANEL
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtScrolledPanel'
ic_class_pic2 = '@common.imgEdtScrolledPanel'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icscrolledpanel.icScrolledPanel-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 5)


class icScrolledPanel(icWidget, wx.lib.scrolledpanel.ScrolledPanel):
    """
    Класс icScrolledPanel реализует интерфейс для создания панели c прокруткой
    класса wxScrolledPanel через ресурсное описание.
    """
    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        import ic.components.icResourceParser as prs
        testObj = prs.CreateForm('Test', formRes=res,
                                 evalSpace=context, parent=parent, bIndicator=True)
        #   Для оконных компонентов надо вызвать метод Show
        try:
            testObj.context['_root_obj'].Show(True)
            testObj.context['_root_obj'].SetFocus()
        except: 
            io_prnt.outErr()
    
    def __init__(self, parent, id=-1, component={}, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор.
        @type parent: C{wxWindow}
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
        util.icSpcDefStruct(SPC_IC_SCROLLED_PANEL, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        self.keydown = component['keyDown']
        
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, id, self.position, self.size, 
                                                    style=style, name=self.name)
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        bx,by = (True, True)
        if component['scrollRate'][0] < 0:
            bx = False
            sx = 0
        else: sx = component['scrollRate'][0]
        
        if component['scrollRate'][1] < 0:
            by = False
            sy = 0
        else: sy = component['scrollRate'][1]
                
        self.enableScr = (bx, by)
        self.SetScrollRate(sx, sy)
        self.EnableScrolling(bx, by)
        self.BindICEvt()
        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)

    def DestroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except:
                    pass
        except:
            pass


def test(par=0):
    """
    Тестируем класс icScrolledPanel.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icScrolledPanel Test')
    win = icScrolledPanel(frame, -1, {'keyDown': 'print(\'keyDown in ScrolledPanel\')'})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
