#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxPanel.
Модуль содержит класс icwxPanel, который по ресурсному описанию создает окно (wxPanel).
@type SPC_IC_PANEL: C{dictionary}
@var SPC_IC_PANEL: Спецификация на ресурсное описание окна. Ключи SPC_IC_PANEL:

    - B{name = 'default'}: Имя окна.
    - B{type = 'Panel'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=wx.TAB_TRAVERSAL}:Стиль окна. Используются все стили класса wxWindow.
    - B{onClose = None}: Выражение, выполняемое при закрытии окна (обработка события EVT_CLOSE).
    - B{keyDown=None}: Выражение, выполняемое при нажатии кнопки <EVT_KEY_DOWN>.
    - B{child=[]}:Cписок дочерних элементов.

@type ICPanelStyle: C{dictionary}
@var ICPanelStyle: Словарь стилей компонента. Все стили wxWindow:
"""

import wx
from ic.utils.util import icSpcDefStruct
import ic.utils.util as util
from .icwidget import icWidget, SPC_IC_WIDGET
from . import icwindow
import ic.utils.graphicUtils as graphicUtils
from ic.kernel import io_prnt
from ic.log import log
from ic.engine import ic_user
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

SPC_IC_PANEL = {'type': 'Panel',
                'name': 'defaultWindow',
                'child': [],

                'position': (-1, -1),
                'size': (100, 100),
                'foregroundColor': None,
                'backgroundColor': None,
                'onRightMouseClick': None,
                'onLeftMouseClick': None,
                'style': wx.TAB_TRAVERSAL,
                'docstr': 'ic.components.icwxpanel-module.html',
                'onClose': None,
                'keyDown': None,

                '__default_page__': 1,
                '__events__': {'onClose': ('wx.EVT_CLOSE', 'ObjDestroy', False),
                               'onLeftMouseClick': ('wx.EVT_LEFT_DOWN', 'OnLeftDown', False),
                               'onRightMouseClick': ('wx.EVT_RIGHT_DOWN', 'OnRightDown', False),
                               },
                '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['onClose', 'keyDown'],
                                   icDefInf.EDT_TEXTFIELD: ['docstr'],
                                   },
                '__parent__': SPC_IC_WIDGET,
                }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icWXPanel'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_PANEL
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtPanel'
ic_class_pic2 = '@common.imgEdtPanel'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icwxpanel.icWXPanel-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 1, 1)

DESIGN_BORDER_CLR = (112, 146, 190)

DEFAULT_TEST_WIDTH = 800
DEFAULT_TEST_HEIGHT = 600


class icWXPanel(icWidget, wx.Panel):
    """
    Интерфейс для создания окна класса wxPanel через ресурсное описание.
    """
    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        import ic.components.icResourceParser as prs
        testObj = prs.CreateForm('Test', formRes=res,
                                 evalSpace=context, parent=parent, bIndicator=True)
        #   Для оконных компонентов надо вызвать метод Show
        try:
            if testObj:
                testObj.SetSize(wx.Size(DEFAULT_TEST_WIDTH, DEFAULT_TEST_HEIGHT))
                testObj.Show(True)
                testObj.SetFocus()
        except:
            io_prnt.outErr()
    
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icWXPanel.
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
        #   Размер до границы
        self.boundStep = 0
        icSpcDefStruct(SPC_IC_PANEL, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        # log.debug('Widget context kernel <%s> ' % self.context.kernel)

        self.components = {}
        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        self.on_close = component['onClose']
        self.keydown = component['keyDown']
        
        #   Признак режима редактирования
        self.is_editor_mode = False
        #   Признак скругленных границ формы
        self.is_round_border = False
        
        pre = wx.PrePanel()
        bCreate = pre.Create(parent, id, pos, size, style=style, name=self.name)

        if fgr is not None:
            pre.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
        if bgr is not None:
            pre.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))
        else:
            clr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
            pre.SetBackgroundColour(clr)
        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnPanelSize)
        self.BindICEvt()
        #   Задаем режим положки редактора
        if (self.context['__runtime_mode'] == util.IC_RUNTIME_MODE_EDITOR and
           ('_root_obj' in self.context and self.context['_root_obj'] is None)):
            self.SetEditorMode()
            
        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if '_root_obj' not in self.evalSpace or not self.evalSpace['_root_obj']:
                    self.evalSpace['_root_obj'] = self
            kernel = self.GetKernel()
            if kernel:
                kernel.parse_resource(self, self.child, None, context=self.evalSpace,
                                      bCounter=bCounter, progressDlg=progressDlg)
            else:
                log.warning('Not define kernel in widget <%s>' % self)

    def DestroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                #   Функционал перед закрытием
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except:
                    log.fatal(u'Ошибка разрушения объекта <%s>' % key)
        except:
            log.fatal(u'Ошибка закрытия панели')

    def Draw(self, dc):
        """
        Отрисовка панели.
        """
        dc.BeginDrawing()
        bgr, fgr = self.GetBackgroundColour(), self.GetForegroundColour()
        d = self.boundStep
        width, height = self.GetClientSize()
        bgr_prnt = self.GetParent().GetBackgroundColour()
        
        if d > 0 and (self.is_editor_mode or self.is_round_border):
            backBrush = wx.Brush(bgr_prnt, wx.SOLID)
        else:
            backBrush = wx.Brush(bgr, wx.SOLID)
            
        dc.SetBackground(backBrush)
        dc.SetBrush(wx.Brush(bgr, wx.SOLID))
        dc.Clear()

        if self.is_editor_mode:
            pen = wx.Pen(wx.Colour(*DESIGN_BORDER_CLR))
        else:
            pen = wx.Pen(fgr)
            
        dc.SetPen(pen)
        
        if d > 0 and not self.is_editor_mode and not self.is_round_border:
            dc.DrawLines([wx.Point(d, d),
                          wx.Point(width-1 - d, d),
                          wx.Point(width-1 - d, height-1-d),
                          wx.Point(d, height-1-d),
                          wx.Point(d, d)])
        elif d > 0:
            dc.DrawRectangle(d, d, width-2*d, height-2*d)
        else:
            dc.DrawLines([wx.Point(d, d),
                          wx.Point(width-1 - d, d),
                          wx.Point(width-1 - d, height-1-d),
                          wx.Point(d, height-1-d),
                          wx.Point(d, d)])
        # Для редактора форм
        if 0:
            step = 10
            pen = wx.Pen('GREY')
            dc.SetPen(pen)
            for y in xrange(int(height/step)-1):
                for x in xrange(int(width/step)-1):
                    dc.DrawPoint((x+1)*step, (y+1)*step)
        # Рисуем круглые углы
        if self.is_round_border:
            pen = wx.Pen(fgr)
            dc.SetPen(pen)
            graphicUtils.drawRoundCorners(dc, (width, height),
                                          fgr, bgr, bgr_prnt, d,
                                          (fgr, fgr, fgr, fgr))
                    
        dc.EndDrawing()
        
    def ObjDestroy(self):
        """
        Обрабатывает сообщение о закрытии окна.
        """
        if self.isICAttrValue('onClose'):
            self.evalSpace['self'] = self
            self.eval_attr('onClose')

    def OnLeftDown(self, evt):
        """
        wx.EVT_LEFT_DOWN
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('onLeftMouseClick')
        evt.Skip()

    def OnRightDown(self, evt):
        """
        wx.EVT_RIGHT_DOWN
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('onRightMouseClick')
        evt.Skip()

    def OnPaint(self, evt):
        """
        wx.EVT_PAINT.
        """
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def OnPanelSize(self, evt):
        """
        wx.EVT_SIZE
        """
        self.Refresh()
        evt.Skip()

    def SetRoundBoundMode(self, boundClr=None, step=0):
        """
        Устанавливает режим скругленных границ.
        @type boundClr: C{wx.Colour}
        @param boundClr: Цвет границы.
        @type step: C{int}
        @param step: Отступ границы от края окна.
        """
        self.boundStep = step
        if boundClr:
            if isinstance(boundClr, tuple):
                self.SetForegroundColour(wx.Colour(*boundClr))
            else:
                self.SetForegroundColour(boundClr)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.is_round_border = True

    def SetBorderMode(self, boundClr=None, step=0):
        """
        Устанавливает режим скругленных границ.
        @type boundClr: C{wx.Colour}
        @param boundClr: Цвет границы.
        @type step: C{int}
        @param step: Отступ границы от края окна.
        """
        self.boundStep = step
        if boundClr:
            if isinstance(boundClr, tuple):
                self.SetForegroundColour(wx.Colour(*boundClr))
            else:
                self.SetForegroundColour(boundClr)

        if not self.is_round_border:
            self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.is_round_border = False

    def SetEditorMode(self):
        """
        Устанавливает режим редактора.
        """
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.is_editor_mode = True


def test(par=0):
    """
    Тестируем класс icWXPanel.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icWXPanel Test')
    win = icWXPanel(frame, -1,  {'keyDown': 'print(\'keyDown in Panel\')',
                                 'foregroundColor': (0, 100, 100),
                                 })
    win.SetRoundBoundMode((200, 200, 200), 2)

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
