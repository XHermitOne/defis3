#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.ImageButton.
Содержит описание класса icImageButton, который по ресурсному описанию создает кнопку с картинкой.

@type SPC_IC_TOGGLE_IMGBUTTON: C{dictionary}
@var SPC_IC_TOGGLE_IMGBUTTON: Спецификация на ресурсное описание окна. Описание ключей SPC_IC_IMGBUTTON:

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

@type ICToggleImageButtonStyle: C{dictionary}
@var ICToggleImageButtonStyle: Словарь специальных стилей компонента. Описание ключей:

    - C{wx.BU_LEFT}: Выравнивает текст подписи по левому краю кнопки (Win32).
    - C{wx.BU_TOP}: Выравнивает текст подписи по верхней границе кнопки (Win32).
    - C{wx.BU_RIGHT}: Выравнивает текст подписи по правому краю кнопки (Win32).
    - C{wx.BU_BOTTOM}: Выравнивает текст подписи по нижней границе кнопки (Win32).
    - C{wx.BU_AUTODRAW}: Если указан этот стиль, то кнопка будет рисоваться, используя только картинку,
        и 3D бордюр. Если этот стиль не определен, то кнопка будет рисоваться без бордюр (Win32).
"""
                            
import wx
from wx.lib import buttons
from ic.bitmap.icbitmap import icBitmapType
from ic.log.iclog import *
import ic.utils.util as util
import ic.PropertyEditor.icDefInf as icDefInf
from ic.components.icwidget import icWidget, icShortHelpString, SPC_IC_WIDGET
import ic.imglib.common as common

ICToggleImageButtonStyle = {'BU_LEFT': wx.BU_LEFT,
                            'BU_TOP': wx.BU_TOP,
                            'BU_RIGHT': wx.BU_RIGHT,
                            'BU_BOTTOM': wx.BU_BOTTOM,
                            'BU_AUTODRAW': wx.BU_AUTODRAW}

SPC_IC_TOGGLE_IMGBUTTON = {'type': 'ImageButton',
                           'name': 'default',

                           'style': 0,
                           'position': (-1, -1),
                           'size': (-1, -1),
                           'label': '',
                           'image': None,
                           'bFocusIndicator': False,
                           'foregroundColor': (0, 0, 0),
                           'backgroundColor': None,
                           'mouseClick': None,
                           'mouseDown': None,
                           'mouseUp': None,
                           'mouseContextDown': None,
                           'shortHelpString': '',

                           '__attr_types__': {icDefInf.EDT_CHECK_BOX: ['bFocusIndicator'],
                                              },
                           '__styles__': ICToggleImageButtonStyle,
                           '__parent__': SPC_IC_WIDGET,
                           }


class icToggleImageButton(icWidget, buttons.ThemedGenBitmapTextToggleButton):
    """
    Класс icImageButton реализует интерфейс для обработки рисованной кнопки
    как обкладку над компонентом wx.BitmapButton.

    События, обрабатываемые классом B{icImageButton}:
    - C{mouseClick}: Нажатие левой кнопки.
    - C{mouseDown}: Нажатие левой кнопки.
    - C{mouseUp}: Отпускание левой кнопки.
    - C{mouseContextDown}: Нажатие правой кнопки.

    Для того, чтобы обработка сообщения передалась в другую функцию необходимо определить
    в файле ресурсов поле с ключем (событие) указать нужную функцию.

    B{Пример:}
    C{'mouseClick':'OnPressButton(evt)'.} evt - объект описание сообщения.
    C{'mouseDown':'OnDown(evt)'}
    C{'mouseContextDown':'OnRightDown(evt)'}
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        util.icSpcDefStruct(SPC_IC_TOGGLE_IMGBUTTON, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        sz = component['size']
        pos = component['position']
        border = component['border']

        self.image = img = util.getICAttr(component['image'], evalSpace,
                                          'Error in getICAttr in icimagebutton. name=%s attribute <image>' % self.name)

        if type(img) in (str, unicode) and img not in ['', 'None', u'', u'None']:
            bmptype = icBitmapType(img)
            img = wx.Image(img, bmptype).ConvertToBitmap()
        elif not img:
            img = common.imgEdtImage

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
        self.bFocusIndicator = component['bFocusIndicator']
        self._helpWin = None

        buttons.ThemedGenBitmapTextToggleButton.__init__(self, parent, id, img, self.label, pos, sz,
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
                                                  (x + px, y + sy + 10), 750)
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
        self.eval_event('mouseClick', evt, True)

    def OnMouseDown(self, evt):
        """
        Обрабатываем нажатие левой кнопки мыши (сообщение C{EVT_LEFT_DOWN}).
        """
        self.eval_event('mouseDown', evt, True)

    def OnMouseUp(self, evt):
        """
        Обрабатываем отпускание левой кнопки мыши (сообщение C{EVT_LEFT_UP}).
        """
        self.eval_event('mouseUp', evt, True)

    def OnMouseContextDown(self, evt):
        """
        Обрабатываем нажатие правой кнопки мыши (сообщение C{EVT_RIGHT_DOWN}).
        """
        self.eval_event('mouseContextDown', evt, True)

    def DrawFocusIndicator(self, dc, w, h):
        if self.bFocusIndicator:
            super(icToggleImageButton, self).DrawFocusIndicator(dc, w, h)
    
    def DrawBezel(self, dc, x1, y1, x2, y2):
        rect = wx.Rect(x1, y1, x2, y2)
        if self.up:
            state = 0
        else:
            state = wx.CONTROL_PRESSED
            return
        if not self.IsEnabled():
            state = wx.CONTROL_DISABLED
            return
        pt = self.ScreenToClient(wx.GetMousePosition())
        if self.GetClientRect().Contains(pt):
            state = wx.CONTROL_CURRENT
        elif state == 0:
            return
        wx.RendererNative.Get().DrawPushButton(self, dc, rect, state)


def test(par=0):
    """
    Тестируем класс icImageButton.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icImageButton Test')
    win = wx.Panel(frame, -1)
    ctrl_12 = icToggleImageButton(win, -1, {'image': '',
                                            'position': (100, 5),
                                            'size': (60, 25),
                                            'label': 'Label',
                                            'shortHelpString': u'Пример всплывающей подсказки'})
    ctrl_2 = wx.Button(win, -1, 'wx.Button',  pos=(5, 5))
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
