#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxFrame. Генерирут объект по ресурсному описанию.
Содержит описание класса icFrame, который по ресурсному описанию создает фрэймовое окно.
@type SPC_IC_FRAME: C{dictionary}
@var SPC_IC_FRAME: Спецификация на ресурсное описание окна. Описание ключей SPC_IC_FRAME:
    - B{name = 'default'}: Имя окна.
    - B{type = 'Frame'}: Тип объекта.
    - B{title = 'Frame'}: Заголовок окна.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{onClose = None}: Выражение, выполняемое при закрытии окна (обработка события EVT_CLOSE).
        Если выражение вернет False, то окно не будет закрыто (не будет вызываться evt.Skip() ).
    - B{setFocus = None}: Выражение, выполняемое при установлении фокуса (обработка события EVT_SET_FOCUS).
    - B{killFocus = None}: Выражение, выполняемое при потере фокуса (обработка события EVT_KILL_FOCUS).
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на фрэйме.
    - B{style=0}: Стиль окна.
    - B{child=[]}: Cписок дочерних элементов.
        
@type ICFrameStyle: C{dictionary}
@var ICFrameStyle: Словарь специальных стилей компонента. Описание ключей ICFrameStyle:
    - C{DEFAULT_FRAME_STYLE} - определяется как wxMINIMIZE_BOX | wxMAXIMIZE_BOX | wxRESIZE_BORDER | wxSYSTEM_MENU | wxCAPTION.
    - C{ICONIZE} - выводит окно в свернутом виде.
    - C{MINIMIZE} - аналогично  wxICONIZE.
    - C{MAXIMIZE} - раскрывает окно на весь экран.
    - C{STAY_ON_TOP} - оставляет окно всегда верхним.
    - C{SYSTEM_MENU} - выводит системное меню.
    - C{RESIZE_BORDER} - позволяет изменять размеры окна.
    - C{CAPTION} - Поле для перетаскивания фрэйма.
    - C{MINIMIZE_BOX} - Выводит кнопку для минимизации.
    - C{MAXIMIZE_BOX} - Выводит кнопку для полного развертывания.
    - C{SIMPLE_BORDER} - Окно без бордюр. Только под GTK и Windows.
    - C{FRAME_NO_TASKBAR} -  Создается нормальное окно, которое не отражается в панели задач.
         Работает только под Windows.
    - C{FRAME_EX_CONTEXTHELP} -  Под Windows, контекстная подсказка.
    - C{FRAME_FLOAT_ON_PARENT} - окно всегда находится вверху родительского окна.
    - C{FRAME_TOOL_WINDOW} - создает маленькое окно, но на панель задач не помещает.
"""
import wx
import ic.utils.util as util
from . import icwidget as icwidget
import ic.kernel.io_prnt as io_prnt
import ic.PropertyEditor.icDefInf as icDefInf

ICFrameStyle = {'DEFAULT_FRAME_STYLE': wx.DEFAULT_FRAME_STYLE,
                'ICONIZE': wx.ICONIZE,
                'CAPTION': wx.CAPTION,
                'MINIMIZE': wx.MINIMIZE,
                'MAXIMIZE': wx.MAXIMIZE,
                'MINIMIZE_BOX': wx.MINIMIZE_BOX,
                'MAXIMIZE_BOX': wx.MAXIMIZE_BOX,
                'STAY_ON_TOP': wx.STAY_ON_TOP,
                'SYSTEM_MENU': wx.SYSTEM_MENU,
                'RESIZE_BORDER': wx.RESIZE_BORDER,
                'SIMPLE_BORDER': wx.SIMPLE_BORDER,
                'FRAME_NO_TASKBAR': wx.FRAME_NO_TASKBAR,
                'FRAME_FLOAT_ON_PARENT': wx.FRAME_FLOAT_ON_PARENT,
                'FRAME_TOOL_WINDOW': wx.FRAME_TOOL_WINDOW}

SPC_IC_FRAME = {'name': 'defaultFrame',
                'type': 'Frame',
                'child': [],

                'title': 'Frame',
                'position': (-1, -1),
                'size': (500, 400),
                'foregroundColor': None,
                'backgroundColor': None,
                'style': wx.DEFAULT_FRAME_STYLE,
                'onClose': None,
                'setFocus': None,
                'keyDown': None,
                'killFocus': None,

                '__events__': {'onClose': ('wx.EVT_CLOSE', 'OnClose', False),
                               'setFocus': ('wx.EVT_SET_FOCUS', 'OnSetFocus', False),
                               'killFocus': ('wx.EVT_KILL_FOCUS', 'OnKillFocus', False)},
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icFrame'

#   Описание стилей компонента
ic_class_styles = ICFrameStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_FRAME
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtFrame'
ic_class_pic2 = '@common.imgEdtFrame'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icframe.icFrame-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 9)


# ---------- Классы --------------
class icFrame(icwidget.icWidget, wx.Frame):
    """
    Класс icFrame реализует интерфейс для создания окна класса wxFrame через
    ресурсное описание.
    """

    @staticmethod
    def GetDesigner():
        """
        Указатель на класс графического редактора компонента.
        """
        from ic.PropertyEditor.designers import icframedesigner
        return icframedesigner.icFrameDesigner
    
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

    def __init__(self, parent=None, id=-1, component=None, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icFrame
        @type parent: C{wxWindow}
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
        if component is None:
            component = {}
        #   Атрибуты сайзера
        self.sizer = None
        self.bSizerAdd = False
        util.icSpcDefStruct(SPC_IC_FRAME, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.title = component['title']
        pos = component['position']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        self.on_close = component['onClose']
        self.set_focus = component['setFocus']
        self.kill_focus = component['killFocus']

        #   Флаг, указывающий, что необходимо сохранять изменяющиеся
        #   параметры окна (позицию и размеры).
        self.saveChangeProperty = True

        #   Читаем расположение и размеры диалога из файла настроек пользователя
        _pos = self.LoadUserProperty('position')
        size = self.LoadUserProperty('size')

        if _pos:
            pos = _pos
        if size:
            self.size = size
    
        wx.Frame.__init__(self, parent, id, self.title, pos, self.size,
                          style=style, name=self.name)
        
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
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

    def OnSize(self, evt):
        self.Refresh()
        evt.Skip()
        
    def OnSetFocus(self, evt):
        """
        Обрабатывает событие установки фокуса (EVT_SET_FOCUS).
        """
        self.evalSpace['evt'] = evt
        self.eval_attr('setFocus')
        evt.Skip()
        
    def OnKillFocus(self, evt):
        """
        Обрабатывает событие установки фокуса (EVT_SET_FOCUS).
        """
        self.evalSpace['evt'] = evt
        self.eval_attr('killFocus')
        evt.Skip()

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
                    io_prnt.outWarning(u'Ошибка разрушения фрейма')
        except:
            io_prnt.outWarning(u'Ошибка разрушения фрейма')

    def OnCloseFrame(self, evt):
        """
        Обрабатывает сообщение о закрытии окна.
        """
        if self.isICAttrValue('onClose'):
            #   Запоминаем расположение и размеры диалога в файле настроек пользователя
            self.SaveUserProperty('position', self.GetPosition())
            self.SaveUserProperty('size', self.GetSize())
            self.evalSpace['__block_lock_rec'] = True
            self.evalSpace['evt'] = evt
            ret, val = self.eval_attr('onClose')
            #   Если выражение вернет False, то отменяем закрытие окна. None трактуем
            #   как True,  поскольку если выражение не определяет возвращаемое значение,
            #   то ic_eval вернет (True,  None)
            if ret and not val and val is not None:
                return

        #   Снимаем блокировки у классов данных
        for key in self.evalSpace['_sources']:
            self.evalSpace['_sources'][key].UnlockAll()

        # self.DestroyWin()
        if evt:
            evt.Skip()
        
    def Destroy(self):
        try:
            if self.parent:
                for key in self.parent.components:
                    if self.parent.components[key] == self:
                        self.parent.components.pop(key)
                        break
        except:
            io_prnt.outWarning(u'FRAME DESTROY: can\'t pop element from parent.components dctionary.')

        #   Удаляем форму
        wx.Window.Destroy(self)


def test(par=0):
    """
    Тестируем класс icFrame.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = icFrame(component={'title': 'wxFrame Test',
                               'keyDown': 'print(\'keyDown in icFrame\')'})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
