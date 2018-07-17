#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс описания ячейки сложной шапки.
Модуль содержит описания класса ячейки сложной шапки.

@type BGR_SOLID: C{int}
@var BGR_SOLID: Идентификатор сплошной одноцветной заливки.
@type BGR_GRAD_TOP: C{int}
@var BGR_GRAD_TOP: Идентификатор градиентной заливки в вертикальном направлении
    от светлого к темному.
@type BGR_GRAD_BOTTOM: C{int}
@var BGR_GRAD_BOTTOM: Идентификатор градиентной заливки в вертикальном направлении
    от темного к светлому.
@type BGR_GRAD_LEFT: C{int}
@var BGR_GRAD_LEFT: Идентификатор градиентной заливки в горизонтальном направлении
    от светлого к темному.
@type BGR_GRAD_RIGHT: C{int}
@var BGR_GRAD_RIGHT: Идентификатор градиентной заливки в горизотнальном направлении
    от темного к светлому.

@type SPC_IC_HEADCELL: C{Dictionary}
@var SPC_IC_HEADCELL: Спецификация на описание ячееки сложной шапки. Описание ключей:

    - B{name='CellHead'}: Имя объекта.
    - B{type='CellHead'}: Тип объекта.
    - B{position=(-1,-1)}: Позиция на окне если используется как самостоятельный компонент.
    - B{size=(-1,-1)}: Размер компонента.
    - B{pos=(-1,-1)}: Позиция в шапке.
    - B{span=(1,1)}: Размер области объедененных ячеек.
    - B{label=''}: Текст ячейки.
    - B{backgroundType=0}: Тип заливки фона (см. описание стат. переменных. BGR_GRAD_*).
    - B{backgroundColor=None}: Цвет подложки.
    - B{backgroundColor2=None}: Цвет2 подложки используется для градиентных заливок.
    - B{foregroundColor=None}: Цвет текста.
    - B{borderLeftColor=(250,250,250)}: Цвет левой границы.
    - B{borderTopColor=(250,250,250)}: Цвет верхней границы.
    - B{borderRightColor=(100,100,100)}: Цвет правой границы.
    - B{borderBottomColor=(100,100,100)}: Цвет нижней границы.
    - B{borderStep=0}: Отступ при прорисовки гарницы от краев ячейки.
    - B{borderStyle=None}: Стиль границы (wx.SOLID, wx.DOT, wx.LONG_DASH
        wx.SHORT_DASH, wx.DOT_DASH).
    - B{cursorColor=(100,100,100)}: Цвет подсветки компонента при наезде на него мышкой.
    - B{borderWidth=1}: Ширина границы.
    - B{isSort=False}: Признак сортировки.
    - B{font={}}: Шрифт (см. описание icFont).
    - B{bgrImage=None}: Изображение положки.
    - B{alignment=('centred','middle')}: Способ выравниввания текста ячейки ('centred','left', 'right', 'middle', 'top', 'bottom').
    - B{child=[]}: Список компонентов ячейки.
"""

import wx
import wx.grid as  gridlib
import ic.components.icgrid as icgrid
import ic.components.icwidget as icwidget
from ic.utils.util import icSpcDefStruct, getICAttr
from ic.components.icfont import icFont
from ic.log.iclog import LogLastError
import ic.PropertyEditor.icDefInf as icDefInf
import ic.utils.graphicUtils as graphicUtils
import ic.utils.util as util
from ic.kernel import io_prnt

_ = wx.GetTranslation

SPC_IC_HEADCELL = {'type': 'HeadCell',
                   'name': 'HeadCell',
                   'child': [],

                   'position': (-1, -1),
                   'size': (50, -1),
                   'span': (1, 1),
                   'label': '',
                   'backgroundType': 0,
                   'backgroundColor': None,
                   'backgroundColor2': None,
                   'foregroundColor': None,
                   'borderLeftColor': (250, 250, 250),
                   'borderTopColor': (250, 250, 250),
                   'borderRightColor': (100, 100, 100),
                   'borderBottomColor': (100, 100, 100),
                   'borderStep': 0,
                   'borderStyle': None,
                   'borderWidth': 1,
                   'cursorColor': (100, 100, 100),
                   'roundConer': [0, 0, 0, 0],
                   'isSort': False,
                   'font': {},
                   'shortHelpString': '',
                   'bgrImage': None,
                   'alignment': ('centred', 'middle'),
                   'onLeftDown': None,

                   '__events__': {'onLeftDown': ('wx.EVT_BUTTON', 'OnLeftDown', False),
                                  },
                   '__attr_types__': {icDefInf.EDT_CHOICE: ['alignment'],
                                      icDefInf.EDT_COMBINE: ['flag'],
                                      icDefInf.EDT_TEXTLIST: ['roundConer'],
                                      icDefInf.EDT_NUMBER: ['backgroundType', 'borderStep',
                                                            'borderWidth', 'isSort'],
                                      icDefInf.EDT_COLOR: ['backgroundColor', 'borderLeftColor', 'borderTopColor',
                                                           'borderRightColor', 'borderBottomColor',
                                                           'cursorColor', 'backgroundColor2'],
                                      },
                   '__parent__': icwidget.SPC_IC_WIDGET,
                   }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icComboType

#   Имя пользовательского класса
ic_class_name = 'icHeadCell'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_HEADCELL
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtHeadCell'
ic_class_pic2 = '@common.imgEdtHeadCell'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icheadcell.icHeadCell-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'DatasetNavigator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 4)


# Кнопка сортировки по убыванию
SortMarkPointsDark = [(0, 0), (8, 0), (4, 4), (0, 0)]
SortMarkPointsLight = [(9, 0), (4, 5), (-1, 0), (0, 0), (9, 0)]

# Кнопка сортировки по возрастанию
SortMarkPointsDarkUp = [(0, 4), (8, 4), (4, 0), (0, 4)]
SortMarkPointsLightUp = [(-1, 4), (4, -1), (9, 4), (8, 4), (-1, 4)]

# Располоожение кнопки сортировки
mark_shith_x = 4
mark_shith_y = 5


class icHeadCell(icwidget.icWidget, wx.PyControl):
    """
    Стандартное представление ячейки шапки.
    """

    labelDelta = 1

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания объекта icBoxSizer.
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
        icSpcDefStruct(SPC_IC_HEADCELL, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        self.position = pos = component['position']
        self.size = size = component['size']
        self.span = component['span']
        label = self.getICAttr('label')
        if not label:
            label = ''

        self.add_style = wx.EXPAND | wx.GROW
        self._isSort = getICAttr('@'+str(component['isSort']), self.evalSpace,
                                 'Error in icheadgrid.__init__()<isSort>. Name:' + self.name)
        self.shortHelpString = component['shortHelpString']
        self._helpWin = None
        # -----------------------------------------------------------------------
        aln = component['alignment']
        if type(aln) in (str, unicode):
            try:
                aln = eval(aln)
            except:
                aln = ('centred', 'middle')

        horiz, vert = self.alignment = aln
        
        if horiz == 'centred':
            style = wx.ALIGN_CENTRE
        elif horiz == 'right':
            style = wx.ALIGN_RIGHT
        else:
            style = wx.ALIGN_LEFT
            
        style = style | wx.ST_NO_AUTORESIZE | wx.NO_BORDER
        
        # ----------------------------------------------------------------------
        wx.PyControl.__init__(self, parent, id, pos, size, style, name=self.name)
        # ----------------------------------------------------------------------
        self.SetLabel(label)
        self.SetPosition(pos)
        font = parent.GetFont()
        if not font.Ok():
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        wx.PyControl.SetFont(self, font)

        self.defBackClr = parent.GetBackgroundColour()
        if not self.defBackClr.Ok():
            self.defBackClr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
        self.SetBackgroundColour(self.defBackClr)

        clr = parent.GetForegroundColour()
        if not clr.Ok():
            clr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
        self.SetForegroundColour(clr)

        rw, rh = size
        bw, bh = self.GetBestSize()
        if rw == -1:
            rw = bw
        if rh == -1:
            rh = bh
        self.SetSize(wx.Size(rw, rh))
        # ----------------------------------------------------------------------

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.BindICEvt()

        #   Цвета текста и фона
        self.bgr = bgr = component['backgroundColor']
        if component['backgroundColor2']:
            self.bgr2 = bgr2 = wx.Colour(*component['backgroundColor2'])
        else:
            self.bgr2 = bgr2 = None

        if not bgr2:
            if bgr:
                self.bgr2 = graphicUtils.GetMidColor(wx.Colour(*bgr), wx.Colour(0, 0, 0), 0.25)
            else:
                self.bgr2 = graphicUtils.GetMidColor(parent.GetBackgroundColour(), wx.Colour(0, 0, 0), 0.25)

        self.fgr = fgr = component['foregroundColor']

        #   Цвета границы
        self.leftColor = component['borderLeftColor']
        self.topColor = component['borderTopColor']
        self.rightColor = component['borderRightColor']
        self.bottomColor = component['borderBottomColor']
        self.borderStep = component['borderStep']
        self.borderWidth = component['borderWidth']
        self.cursorColor = component['cursorColor']
           
        #   Стиль границы - соответствует стиль wx.Pen
        self.borderStyle = None
        ret, val = self.eval_attr('borderStyle')
        if ret:
            self.borderStyle = val
            
        if not self.borderStyle or not isinstance(self.borderStyle, wx.SOLID):
            self.borderStyle = wx.SOLID

        #   Тип штриховки фона
        self.backgroundType = component['backgroundType']
        
        #   Изображение подложки
        if component['bgrImage'] and issubclass(component['bgrImage'].__class__, wx.Bitmap):
            self.bgrImage = component['bgrImage']
        else:
            self.bgrImage = self.countAttr('bgrImage')
            
        #   Шрифт текста
        self.font = font = component['font']

        if bgr:
            self.SetBackgroundColour(bgr)

        if fgr:
            self.SetForegroundColour(fgr)

        if font:
            obj = icFont(font)
            self.SetFont(obj)

        # Направление сортировки.
        #  0 - сортировка не установлена
        #  1 - сортировка по возрастанию
        # -1 - сортировка по убыванию
        self.sortDirection = 0
        
        #
        self.bButton = False
        self._buttonPress = False
        self._buttonEnter = False

        # Описание наличия скругленных углов границы в виде (LT, RT, RB, LB)
        self.SetRoundCorners(((component.get('roundConer', None) or []) + [0]*4)[:4])

        #   Создаем дочерние компоненты
        self.child = component['child']
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)

    def SetButtonStyle(self, style=True):
        """
        Устанавоивает стиль кнопки.
        """
        self.bButton = style
        
    def CanSort(self):
        """
        Возвращает признак сортировки колонки.
        """
        return self._isSort

    def OnMove(self, evt):
        """
        Обработка сообщения <wx.EVT_MOTION>.
        """
        x, y = self.GetPosition()
        sx, sy = self.GetSize()
        px,py = p = evt.GetPosition()
        d = 5
        r = wx.Rect(d, d, sx-2*d, sy-2*d)

        #   Создаем окно подсказки
        if r.Inside(p) and self.shortHelpString not in ['', None, 'None']:
            if self._helpWin is None:
                self._helpWin = icwidget.icShortHelpString(self.parent, self.shortHelpString,
                                                           (x + px, y+sy+10), 750)
            else:
                self._helpWin.bNextPeriod = True
        elif self._helpWin:
            self._helpWin.Show(False)
            self._helpWin.Destroy()
        else:
            self._helpWin = None
        
        evt.Skip()
        
    def OnLeftDown(self, evt):
        if self.bButton:
            self._buttonPress = True
            self.Refresh()
        
        if self.CanSort():
            if self.sortDirection == 0:
                self.sortDirection = -1
            elif self.sortDirection == -1:
                self.sortDirection = 1
            else:
                self.sortDirection = -1

            if self.GetParent().grid:
                try:
                    col = self.position[1]
                    self.GetParent().grid.SortCol(col, self.sortDirection)
                except:
                    io_prnt.outLastErr(u'Error in icheadergrid')
              
            self.Refresh()

            # Убираем признак сортировки у других колонок
            for obj in self.GetParent().parAddList:
                if obj.CanSort() and obj != self:
                    obj.sortDirection = 0
                    obj.Refresh()
        
        # --- onLeftDown
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('onLeftDown')

    def OnLeftUp(self, evt):
        if self.bButton:
            self._buttonPress = False
            self.Refresh()

        evt.Skip()
        
    def OnLeave(self, evt):
        if self.bButton:
            self._buttonPress = False
            self.Refresh()
            
        evt.Skip()
        self._buttonEnter = False
        
    def OnEnter(self, evt):
        evt.Skip()
        self._buttonEnter = True
        self.Refresh()
        
    def OnSize(self, evt):
        self.Refresh()
        
    def SetLabel(self, label):
        """
        Sets the static text label and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.
        """
        label = label.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\r\n', '\n')
        # Заглушка!!!
        if isinstance(label, str):
            try:
                label = unicode(label, 'utf-8')
            except:
                io_prnt.outLog(_('WARRNING')+':' + 'icHeadCell, label is not in utf-8 encoding.')
                label = unicode(label, 'cp1251')
        # Заглушка!!!
        if label.strip().startswith('_('):
            label = label.replace('_(', '').replace(')', '').replace('\'', '').replace('"', '')
            label = _(label.encode('utf-8').strip())
            
        wx.PyControl.SetLabel(self, label)
        style = self.GetWindowStyleFlag()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()
        
    def SetFont(self, font):
        """
        Sets the static text font and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.
        """
        wx.PyControl.SetFont(self, font)
        style = self.GetWindowStyleFlag()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()
        
    def SetRoundCorners(self, corners):
        """
        Устанавливает скругленные углы.
        @type corners: C{tuple}
        @param corners: Картеж, описывает наличие скругленных углов границы
            в виде (LT, RT, RB, LB). Пример: (1,0,0,1)
        """
        if corners:
            self._corners = corners
        
    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the
        button based on the label size.
        """
        if True:
            return self.GetSize()

        label = self.GetLabel()
        maxWidth = totalHeight = 0
        for line in label.split('\n'):
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)
            totalHeight += h
            maxWidth = max(maxWidth, w)
        return wx.Size(maxWidth, totalHeight)
        
    def AcceptsFocus(self):
        """
        Overridden base class virtual.
        """
        return False

    def _drawSquareEdge(self, dc, idEdgeMode=0):
        """
        Рисует границы компонента.
        """
        #   Рисуем правую и нижнюю грань
        width, height = self.GetClientSize()
        st = self.borderStep
        brg, fgr = self.GetBackgroundColour(), self.GetForegroundColour()
        
        if self._buttonPress:
            clrL, clrT, clrB, clrR = self.rightColor, self.bottomColor, self.topColor, self.leftColor
        else:
            clrR, clrB, clrT, clrL = self.rightColor, self.bottomColor, self.topColor, self.leftColor
        
        if clrR:
            pen = wx.Pen(clrR, self.borderWidth, self.borderStyle)
            dc.SetPen(pen)
            dc.DrawLine(width-1-st, 0+st, width-1-st, height-st)

        if clrB:
            pen = wx.Pen(clrB, self.borderWidth, self.borderStyle)
            dc.SetPen(pen)
            dc.DrawLine(0+st, height-1-st, width-1-st, height-1-st)

        #   Рисуем лувую и верхнюю грань
        if height > 1:
            if clrT:
                pen = wx.Pen(clrT, self.borderWidth, self.borderStyle)
                dc.SetPen(pen)
                dc.DrawLine(0+st, 0+st, width-st, 0+st)

            if clrL:
                pen = wx.Pen(clrL, self.borderWidth, self.borderStyle)
                dc.SetPen(pen)
                dc.DrawLine(0+st, 0+st, 0+st, height-st)

    def _drawBackground(self, dc):
        """
        Рисуем подложку компонента.
        """
        clr = self.GetBackgroundColour()
        clr2 = self.bgr2
        width, height = self.GetClientSize()
        if self.bgrImage:
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bgrImage)
            for n in range(int(width/self.bgrImage.GetWidth())+1):
                dc.Blit(n*self.bgrImage.GetWidth(), 0, self.bgrImage.GetWidth(),
                        height, memDC, 0, 0, wx.COPY, True)
        elif self.backgroundType in [graphicUtils.BGR_GRAD_TOP,
                                     graphicUtils.BGR_GRAD_BOTTOM, graphicUtils.BGR_GRAD_LEFT,
                                     graphicUtils.BGR_GRAD_RIGHT]:
            if self._buttonPress and self.backgroundType == graphicUtils.BGR_GRAD_TOP:
                graphicUtils.DrawLineGradient(dc, 0, 0, width, height, clr, clr2, gradType=graphicUtils.BGR_GRAD_BOTTOM)
            elif self._buttonPress and self.backgroundType == graphicUtils.BGR_GRAD_BOTTOM:
                graphicUtils.DrawLineGradient(dc, 0, 0, width, height, clr, clr2, gradType=graphicUtils.BGR_GRAD_TOP)
            elif self._buttonPress and self.backgroundType == graphicUtils.BGR_GRAD_LEFT:
                graphicUtils.DrawLineGradient(dc, 0, 0, width, height, clr, clr2, gradType=graphicUtils.BGR_GRAD_RIGHT)   
            elif self._buttonPress and self.backgroundType == graphicUtils.BGR_GRAD_RIGHT:
                graphicUtils.DrawLineGradient(dc, 0, 0, width, height, clr, clr2, gradType=graphicUtils.BGR_GRAD_LEFT)
            else:
                graphicUtils.DrawLineGradient(dc, 0, 0, width, height, clr, clr2, gradType=self.backgroundType)
        else:
            dc.Clear()
        
    def _drawCorners(self, dc, mode=0):
        """
        Рисует скругленные углы (радиус=4).
        """
        #   Рисуем правую и нижнюю грань
        bgr = self.GetBackgroundColour()
        return graphicUtils.drawRoundCorners(dc, self.GetClientSize(),
                                             self.GetForegroundColour(), bgr,
                                             self.GetParent().GetBackgroundColour(), self.borderStep,
                                             (self.topColor or bgr, self.rightColor or bgr,
                                              self.bottomColor or bgr, self.leftColor or bgr),
                                             self._corners, self.backgroundType)
        
    def Draw(self, dc):
        """
        Функция рисует ячейку.
        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        """
        dc.BeginDrawing()
        clr = self.GetBackgroundColour()
        clr2 = self.bgr2
        
        # Для градиентых типов цвет подложки берем промежуточный между clr, clr2
        if self.backgroundType:
            bgr_clr = graphicUtils.GetMidColor(clr2, clr)
        else:
            bgr_clr = clr
            
        backBrush = wx.Brush(bgr_clr, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.SetTextForeground(self.GetForegroundColour())
        width, height = self.GetClientSize()

        # Рисуем подложку
        self._drawBackground(dc)
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(self.fgr)
        label = self.GetLabel()
        style = self.GetWindowStyleFlag()

        #   Выводим текст
        x = 1
        y = 0
        labelLine = label.split('\n')
        w, h = self.GetTextExtent('W')
        horz, vert = self.alignment

        if vert == 'middle' and h*len(labelLine) < height:
            y = (height - h*len(labelLine))/2

        if vert == 'bottom':
            y = height - h*len(labelLine)

        for line in labelLine:
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)

            if horz == 'right':
                x = width - w - 1
            if horz == 'centred':
                x = (width - w)/2

            if self.CanSort() and x <= mark_shith_x + 11:
                x = mark_shith_x + 12

            dc.DrawText(line, x, y)
            y += h
            
        st = self.borderStep
        
        #   Рисуем признак сортируемой ячейки
        if self.CanSort():
            penBound = wx.Pen((150, 150, 150))
            # Колока не сортирована
            if self.sortDirection == 0:
                brush = wx.Brush(clr, wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDark, mark_shith_x+st, mark_shith_y+st)
                dc.SetPen(penBound)
                dc.DrawLines(SortMarkPointsLight, mark_shith_x+st, mark_shith_y+st)
            # Колонка отсортирована по убыванию
            elif self.sortDirection < 0:
                brush = wx.Brush((100, 100, 100), wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDark, mark_shith_x+st, mark_shith_y+st)
                dc.SetPen(penBound)
                dc.DrawLines(SortMarkPointsLight, mark_shith_x+st, mark_shith_y+st)
            # Колонка отсортирована по возрастанию
            else:
                brush = wx.Brush((100, 100, 100), wx.SOLID)
                dc.SetBrush(brush)
                dc.DrawPolygon(SortMarkPointsDarkUp, mark_shith_x+st, mark_shith_y+st)
                dc.SetPen(penBound)
                dc.DrawLines(SortMarkPointsLightUp, mark_shith_x+st, mark_shith_y+st)
        # Рисуем границы
        self._drawSquareEdge(dc)
        
        # Рисуем скругленные углы по необходимости
        if self._corners and self._corners != (0, 0, 0, 0) and self._corners != [0, 0, 0, 0]:
            self._drawCorners(dc)
        
        #   Рисуем курсор компонента
        if self.bButton and self._buttonEnter:
            dz = 2
            clr = self.cursorColor
            pen = wx.Pen(clr, 1, wx.SOLID)
            dc.SetPen(pen)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle(0+st+dz, 0+st+dz, width-2*st-2*dz-1, height-2*st-2*dz-1)

        dc.EndDrawing()
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        width, height = self.GetClientSize()
        if not width or not height:
            return

        self.Draw(dc)
        
    def OnEraseBackground(self, event):
        pass


def test(par=0):
    """
    Тестируем класс icHeadCell.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, u'icHeadCell Test')
    win = wx.Panel(frame, -1)

    clr1 = graphicUtils.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), -50)
    clr2 = graphicUtils.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), 50)
    
    cell = icHeadCell(win, -1, {'size': (100, 30),
                                'backgroundType': 1,
                                'position': (10, 10),
                                'foregroundColor': (25, 25, 25),
                                'backgroundColor': clr1,
                                'backgroundColor2': clr2,
                                'label': 'Label',
                                'roundConer': [20, 0, 0, '12'],
                                'shortHelpString': u'Пример подсказки'})

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
