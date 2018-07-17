#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxWindow. Генерирут объект по ресурсному описанию.
Содержит описание класса icWindow, который по ресурсному описанию создает простейшее окно.

@type SPC_IC_WINDOW: C{dictionary}
@var SPC_IC_WINDOW: Спецификация на ресурсное описание окна. Описание ключей SPC_IC_WINDOW:

    - B{name = 'default'}: Имя окна.
    - B{type = 'Window'}: Тип объекта.
    - B{title = 'default'}: Заголовок окна, там где это необходимо, например, в icNotebook.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=0}:Стиль окна. Используются все стили класса wxWindow.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на окне.
    - B{child=[]}:Cписок дочерних элементов.
        
@type ICWindowStyle: C{List}
@var ICWindowStyle: Словарь всех стилей окна.
"""

import wx
from ic.dlg.msgbox import MsgBox
import ic.utils.util as util
from .icwidget import icWidget, SPC_IC_WIDGET
from ic.kernel import io_prnt
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf


_ = wx.GetTranslation

ICWindowStyle = {'CAPTION': wx.CAPTION,
                 'MINIMIZE_BOX': wx.MINIMIZE_BOX,
                 'MAXIMIZE_BOX': wx.MAXIMIZE_BOX,
                 'THICK_FRAME': wx.THICK_FRAME,
                 'SIMPLE_BORDER': wx.SIMPLE_BORDER,
                 'DOUBLE_BORDER': wx.DOUBLE_BORDER,
                 'SUNKEN_BORDER': wx.SUNKEN_BORDER,
                 'RAISED_BORDER': wx.RAISED_BORDER,
                 'STATIC_BORDER': wx.STATIC_BORDER,
                 'TRANSPARENT_WINDOW': wx.TRANSPARENT_WINDOW,
                 'TAB_TRAVERSAL': wx.TAB_TRAVERSAL,
                 'WANTS_CHARS': wx.WANTS_CHARS,
                 'NO_FULL_REPAINT_ON_RESIZE': wx.NO_FULL_REPAINT_ON_RESIZE,
                 'VSCROLL': wx.VSCROLL,
                 'HSCROLL': wx.HSCROLL,
                 'CLIP_CHILDREN': wx.CLIP_CHILDREN
                 }

SPC_IC_WINDOW = {'type': 'Window',
                 'name': 'defaultWindow',
                 'child': [],

                 'title': 'default',
                 'position': (-1, -1),
                 'size': (-1, -1),
                 'foregroundColor': None,
                 'backgroundColor': None,
                 'style': 0,
                 'keyDown': None,

                 '__parent__': SPC_IC_WIDGET,
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icWindow'

#   Описание стилей компонента
ic_class_styles = ICWindowStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_WINDOW
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtWindow'
ic_class_pic2 = '@common.imgEdtWindow'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icwindow.icWindow-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icWindow(icWidget, wx.Window):
    """
    Класс icWindow реализует интерфейс для создания окна класса wxWindow
    через ресурсное описание.
    """
    component_spc = ic_class_spc
    
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
                 evalSpace=None, bCounter=False, progressDlg=None):
        """
        Конструктор для создания icWindow

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
        #   Атрибуты сайзера
        self.sizer = None
        self.bSizerAdd = False
        
        util.icSpcDefStruct(SPC_IC_WINDOW, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        self.keydown = component['keyDown']

        wx.Window.__init__(self, parent, id, pos, size, style=style, name=self.name)
        self.SetAutoLayout(True)
        
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))
            
        self.BindICEvt()
        
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
    Тестируем класс icWindow.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'wxWindow Test')
    win = icWindow(frame, -1, {'keyDown': 'print(\'KeyDown in Window\')'})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
