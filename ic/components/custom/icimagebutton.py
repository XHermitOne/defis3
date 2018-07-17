#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.ImageButton.
Содержит описание класса icImageButton, который по ресурсному описанию создает кнопку с картинкой.

@type SPC_IC_IMGBUTTON: C{dictionary}
@var SPC_IC_IMGBUTTON: Спецификация на ресурсное описание окна. Описание ключей SPC_IC_IMGBUTTON:

    - B{name = 'default'}: Имя окна.
    - B{type = 'ImageButton'}: Тип объекта.
    - B{image = None}: Объект картинки (wx.Bitmap), которая будет выводится на конпке либо
        полный путь до картинки.
    - B{position = (-1,-1)}: Расположение на родительском окне.
    - B{size = (-1,-1)}: Размер кнопки.
    - B{label = ''}: Текст кнопки.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=wx.SUNKEN_BORDER | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB}: Дополнительные (+стандартные стили wx.Window) стили:
        - C{wx.BU_LEFT}: Выравнивает по левому краю кнопки (Win32).
        - C{wx.BU_TOP}: Выравнивает по верхней границе кнопки (Win32).
        - C{wx.BU_RIGHT}: Выравнивает по правому краю кнопки (Win32).
        - C{wx.BU_BOTTOM}: Выравнивает по нижней границе кнопки (Win32).
        - C{wx.BU_AUTODRAW}: Если указан этот стиль, то кнопка будет рисоваться, используя только картинку,
            и 3D бордюр. Если этот стиль не определен, то кнопка будет рисоваться без бордюр (Win32).
   
    - B{keyCode=None}: Код клавиши, эмулирующей нажатие кнопки (mouseClick).
    - B{mouseClick=None}: Выражение, выполняемое после нажатия кнопки.
    - B{mouseDown=None}: Выражение, выполняемое после нажатия левой кнопки мыши.
    - B{mouseUp=None}: Выражение, выполняемое после отпускания левой кнопки мыши.
    - B{mouseContextDown=None}: Выражение, выполняемое после нажатия правой кнопки мыши.
    - B{shortHelpString=''}: Текст всплывающей подсказки.

@type ICImageButtonStyle: C{dictionary}
@var ICImageButtonStyle: Словарь специальных стилей компонента. Описание ключей ICImageButtonStyle:

    - C{wx.BU_LEFT}: Выравнивает текст подписи по левому краю кнопки (Win32).
    - C{wx.BU_TOP}: Выравнивает текст подписи по верхней границе кнопки (Win32).
    - C{wx.BU_RIGHT}: Выравнивает текст подписи по правому краю кнопки (Win32).
    - C{wx.BU_BOTTOM}: Выравнивает текст подписи по нижней границе кнопки (Win32).
    - C{wx.BU_AUTODRAW}: Если указан этот стиль, то кнопка будет рисоваться, используя только картинку,
        и 3D бордюр. Если этот стиль не определен, то кнопка будет рисоваться без бордюр (Win32).
"""
                            
import wx
from wx.lib import buttons
from ic.dlg.msgbox import MsgBox
from ic.bitmap.icbitmap import icBitmapType
from ic.log.iclog import *
import ic.utils.util as util
from ic.components.icwidget import icWidget, icShortHelpString, SPC_IC_WIDGET
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

try:
    from ic.components import icImage
except:
    icImage = None
    
ICImageButtonStyle = {'BU_LEFT': wx.BU_LEFT,
                      'BU_TOP': wx.BU_TOP,
                      'BU_RIGHT': wx.BU_RIGHT,
                      'BU_BOTTOM': wx.BU_BOTTOM,
                      'BU_AUTODRAW': wx.BU_AUTODRAW}

SPC_IC_IMGBUTTON = {'type': 'ImageButton',
                    'name': 'default',

                    'style': 0,
                    'position': (-1, -1),
                    'size': (-1, -1),
                    'label': '',
                    'image': None,
                    'foregroundColor': (0, 0, 0),
                    'backgroundColor': None,
                    'mouseClick': None,
                    'mouseDown': None,
                    'mouseUp': None,
                    'mouseContextDown': None,
                    'shortHelpString': '',

                    '__events__': {'mouseClick': ('wx.EVT_BUTTON', 'OnMouseClick', False),
                                   'mouseContextDown': ('wx.EVT_RIGHT_DOWN', 'OnMouseContextDown', False),
                                   'mouseDown': ('wx.EVT_LEFT_DOWN', 'OnMouseDown', False),
                                   'mouseUp': ('wx.EVT_LEFT_UP', 'OnMouseUp', False),
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
ic_class_name = 'icImageButton'

#   Описание стилей компонента
ic_class_styles = ICImageButtonStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_IMGBUTTON
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImgButton'
ic_class_pic2 = '@common.imgEdtImgButton'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icimagebutton.icImageButton-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 5)


class icImgButtonPrototype(icWidget):
    """
    Прототип кнопки с картинкой.
    """
    def __init__(self, parent, id, component, logType = 0, evalSpace = {},
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

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
        util.icSpcDefStruct(SPC_IC_IMGBUTTON, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

    def OnMouseMove(self, evt):
        """
        """
        x, y = self.GetPosition()
        sx, sy = self.GetSize()

        px, py = p = evt.GetPosition()
        d = 5
        r = wx.Rect(d, d, sx-2*d, sy-2*d)

        #   Создаем окно подсказки
        if r.Inside(p) and self.shortHelpString not in ['', None, 'None']:
            if self._helpWin is None:
                self._helpWin = icShortHelpString(self.parent, self.shortHelpString,
                                                  (x + px, y+sy+10), 750)
            else:
                self._helpWin.bNextPeriod = True
        elif self._helpWin:
            self._helpWin.Show(False)
            self._helpWin.Destroy()
        else:
            self._helpWin = None
        
    def OnMouseClick(self, evt):
        """
        Обрабатываем нажатие на кнопку (сообщение C{EVT_BUTTON}).
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['self'] = self

        self.eval_attr('mouseClick')
        
        evt.Skip()

    def OnMouseDown(self, evt):
        """
        Обрабатываем нажатие левой кнопки мыши (сообщение C{EVT_LEFT_DOWN}).
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['self'] = self

        self.eval_attr('mouseDown')
        evt.Skip()

    def OnMouseUp(self, evt):
        """
        Обрабатываем отпускание левой кнопки мыши (сообщение C{EVT_LEFT_UP}).
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('mouseUp')
        
        evt.Skip()

    def OnMouseContextDown(self, evt):
        """
        Обрабатываем нажатие правой кнопки мыши (сообщение C{EVT_RIGHT_DOWN}).
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('mouseContextDown')

        evt.Skip()


class icImageButton(icImgButtonPrototype, buttons.GenBitmapTextButton):
    """
    Класс icImageButton реализует интерфейс для обработки рисованной кнопки.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icImageButton

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
        icImgButtonPrototype.__init__(self, parent, id, component, logType, evalSpace)

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        sz = component['size']
        pos = component['position']
        border = component['border']

        self.img = img = self.getICAttr('image', bExpectedExpr=True)
        if img and issubclass(img.__class__, wx.Bitmap):
            pass
        elif type(img) in (str, unicode) and img not in ['', 'None', u'', u'None']:
            bmptype = icBitmapType(img)
            img = wx.Image(img, bmptype).ConvertToBitmap()
        elif img in (None, 'None'):
            img = common.imgEdtImage
        elif not img:
            img = None

        x = sz[0]

        if x == -2:
            x = img.getWidth()

        y = sz[1]

        if y == -2:
            y = img.getHeight()

        #   Устанавливае реальные размеры для дальнейшего использования
        component['size'] = (x, y)
        sz = (x, y)

        style = component['style']
        self.mouse_click = component['mouseClick']
        self.mouse_down = component['mouseDown']
        self.mouse_up = component['mouseUp']
        self.mouse_contextdown = component['mouseContextDown']
        self.label = component['label']
        self.shortHelpString = component['shortHelpString']
        self._helpWin = None

        buttons.GenBitmapTextButton.__init__(self, parent, id, img, self.label, pos, sz,
                                             style=style, name=self.name)

        self.SetBezelWidth(1)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_BUTTON, self.OnMouseClick, id=id)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseContextDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.BindICEvt()
        

class icBitmapButton(icImgButtonPrototype, wx.BitmapButton):
    """
    Класс icBitmapButton реализует интерфейс для обработки рисованной кнопки.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icBitmapButton

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
        icImgButtonPrototype.__init__(self, parent, id, component, logType, evalSpace)

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        sz = component['size']
        pos = component['position']
        border = component['border']

        self.img = img = self.getICAttr('image', bExpectedExpr=True)
        if img and issubclass(img.__class__, wx.Bitmap):
            pass
        elif type(img) in (str, unicode) and img not in ['', 'None', u'', u'None']:
            bmptype = icBitmapType(img)
            img = wx.Image(img, bmptype).ConvertToBitmap()
        elif img in (None, 'None'):
            img = common.imgEdtImage
        elif not img:
            img = None
        
        x = sz[0]

        if x == -2:
            x = img.getWidth()

        y = sz[1]

        if y == -2:
            y = img.getHeight()

        #   Устанавливае реальные размеры для дальнейшего использования
        component['size'] = (x, y)
        sz = (x, y)

        style = component['style']
        self.mouse_click = component['mouseClick']
        self.mouse_down = component['mouseDown']
        self.mouse_up = component['mouseUp']
        self.mouse_contextdown = component['mouseContextDown']
        self.label = component['label']
        self.shortHelpString = component['shortHelpString']
        self._helpWin = None

        wx.BitmapButton.__init__(self, parent, id, img, pos, sz,
                                 style=style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_BUTTON, self.OnMouseClick, id=id)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseContextDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.BindICEvt()


def get_ext_btn(prnt, pos=(100, 5), size=(18, 16)):
    """
    """
    global icImage
    if not icImage:
        import ic.components.icImage as lib
        icImage = lib
    
    ctrl = icImageButton(prnt, -1, {'position': pos,
                                    'size': size,
                                    'backgroundColor': (225, 225, 220),
                                    'image': icImage.extEditor2,
                                    'shortHelpString': u'Внешний редактор/Помощь'})
    return ctrl


def test(par=0):
    """
    Тестируем класс icImageButton.
    """
    from ic.components.ictestapp import TestApp
    
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icImageButton Test')
    win = wx.Panel(frame, -1)
    s = '''
import ic.imglib.common as common
return common.imgEdtImage
    '''
    ctrl_1 = get_ext_btn(win)
    ctrl_2 = wx.Button(win, -1, 'wx.Button',  pos=(5, 5))
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
